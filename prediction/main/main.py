from google.cloud import bigquery
import requests
from datetime import datetime, timezone, timedelta
import functions_framework
import pandas as pd
import json
import os
import time
import pytz
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory (3 levels up from this file)
project_root = Path(__file__).resolve().parent.parent.parent
env_path = project_root / '.env'

# Load environment variables from .env file
if not env_path.exists():
    raise ValueError(f".env file not found at {env_path}")
load_dotenv(env_path)

# Get API key from environment variable
API_KEY = os.getenv('TFL_API_KEY')
if not API_KEY:
    raise ValueError("TFL_API_KEY environment variable is not set")

# Constants
STATION_ID = '940GZZLUKSX'  # King's Cross St. Pancras

def process_line_predictions(predictions, current_time, client):
    """Process predictions for a single line"""
    rows = []
        

    for prediction in predictions:
        try:
            # Extract basic info
            base_train_id = prediction.get('vehicleId', '')
            line_name = prediction.get('lineId', '')
            current_location = prediction.get('currentLocation', '')
            direction = prediction.get('direction', '')


            # Fix line name for Circle line trains mislabeled as H&C
            circle_stations = ['Westminster', 'St James', 'Victoria', 'Sloane Square', 
                             'South Kensington', 'Gloucester Road', 'High Street Kensington', 'Notting Hill Gate', 'Bayswater',
                             "St. James's Park", 'Embankment', 'Temple', 'Blackfriars', 'Mansion House', 'Cannon Street', 'Monument', 'Tower Hill']
            
            if (line_name == 'hammersmith-city' or line_name == 'metropolitan') and any(station in current_location for station in circle_stations):
                continue

            unwanted_metropolitan = ['Edgware Road', 'Paddington']
            if line_name == 'metropolitan' and any(station in current_location for station in unwanted_metropolitan):
                continue

            metropolitan_inbound = ['Left Kings Cross St. Pancras','Approaching Kings Cross St. Pancras Platform 1','Farringdon', 'Barbican', 'Moorgate', 'Liverpool Street', 'Aldgate']
            metropolitan_outbound = ['Approaching Kings Cross St. Pancras Platform 2', 'Euston', 'Great Portland', 'Baker Street', 'Wembley Park', 'Finchley', 'Harrow']

            if line_name == 'metropolitan' and any(station in current_location for station in metropolitan_inbound):
                direction = 'inbound'

            if line_name == 'metropolitan' and any(station in current_location for station in metropolitan_outbound):
                direction = 'outbound'
            
            if line_name == 'hammersmith-city' and direction == '':
                continue
            
            if line_name == 'metropolitan' and 'At Kings Cross St. Pancras' in current_location:
                if time_to_station < 100:
                    direction = 'outbound'
                if time_to_station > 100:
                    direction = 'inbound'
            
            train_id = f"{line_name}_{base_train_id}"
            time_to_station = prediction.get('timeToStation', 0)
            expected_arrival_timestamp = current_time + timedelta(seconds=time_to_station)

            # Skip Circle line trains at Hammersmith platforms
            if line_name == 'circle' or 'hammersmith-city' and current_location.startswith('At Hammersmith'):
                continue

            if line_name == 'northern' and (current_location.startswith('Around Mill Hill East') or current_location.startswith('At Golders Green Platform 3')):
                continue

            if line_name == 'piccadilly' and (current_location.startswith('At Wood Green Sidings')):
                continue

            # Normal prediction processing for all cases
            any_prediction_timestamp = expected_arrival_timestamp
            arrival_timestamp = None
            
            if time_to_station < 60 and ('At King' in current_location or 'At Platform' in current_location):
                arrival_timestamp = current_time
                any_prediction_timestamp = None

            # Now get the most recent previous observation
            prev_obs_query = f"""
                SELECT time_to_station, arrival_timestamp, initial_prediction_timestamp, timestamp
                FROM `nico-playground-384514.transport_predictions.prediction_history`
                WHERE train_id = '{train_id}'
                ORDER BY timestamp DESC
                LIMIT 1
                """
            prev_obs_results = list(client.query(prev_obs_query))
                
            if prev_obs_results:
                prev_time = prev_obs_results[0].time_to_station
                prev_arrival = prev_obs_results[0].arrival_timestamp
                prev_initial_prediction_timestamp = prev_obs_results[0].initial_prediction_timestamp
                prev_timestamp = prev_obs_results[0].timestamp
                # Check for abnormal jumps in time_to_station
                time_diff = time_to_station - prev_time

                # remove 2 arrivals in a row for the same train_id
                if prev_arrival is not None and arrival_timestamp is not None:
                    continue

                if (current_time - prev_timestamp).total_seconds() < 600:
                    # Normal case - keep previous initial prediction
                    initial_prediction_timestamp = prev_initial_prediction_timestamp

                # If previous observation had an arrival, reset predictions
                if prev_arrival is not None and arrival_timestamp is None:
                    print(f"Previous observation had arrival, resetting predictions for {train_id}")
                    initial_prediction_timestamp = expected_arrival_timestamp
                    any_prediction_timestamp = None
                    
                # If previous time_to_station was low (<100s) and there's any jump (>=5s) --> missed arrival
                if prev_time < 150 and prev_arrival is None and time_diff >= 10 :
                    if time_to_station > 200:
                        print(f"Missed arrival detected for train {train_id}: {prev_time} -> {time_to_station} seconds")
                        initial_prediction_timestamp = expected_arrival_timestamp
                        any_prediction_timestamp = None
                    else:
                        continue
                    
                # If previous train randomly got unrecorded and its a new journey all together with a few predictions 
                if  (current_time - prev_timestamp).total_seconds() > 600 and time_to_station > 200:
                    initial_prediction_timestamp = expected_arrival_timestamp
                    any_prediction_timestamp = None
                    
                # If previous train randomly got unrecorded and its a new journey all together with basically no predictions 
                if  (current_time - prev_timestamp).total_seconds() > 600 and time_to_station < 200:
                    continue

                # If previous time_to_station was high (>200s) and there's a significant jump (>=60s) --> Glitch 
                if prev_time > 200 and time_diff >= 40:
                    print(f"Glitch detected for train {train_id}: {prev_time} -> {time_to_station} seconds, skipping observation")
                    continue
                
            else:
                # If no previous observation, treat this as a new prediction
                initial_prediction_timestamp = expected_arrival_timestamp
                any_prediction_timestamp = None

            
            # Create the row now that we know we want to keep it
            row = {
                'train_id': train_id,
                'line': line_name,
                'timestamp': current_time.isoformat(),
                'time_to_station': time_to_station,
                'current_location': current_location,
                'any_prediction_timestamp': any_prediction_timestamp.isoformat() if any_prediction_timestamp else None,
                'initial_prediction_timestamp': initial_prediction_timestamp.isoformat() if initial_prediction_timestamp else None,
                'arrival_timestamp': arrival_timestamp.isoformat() if arrival_timestamp else None,
                'direction': direction
            }
            
            # Check if we already have a row with this timestamp
            existing_row = next((r for r in rows if r['timestamp'] == row['timestamp'] and r['train_id'] == row['train_id']), None)
            if existing_row:
                print(f"\nFound duplicate timestamp for train {train_id}:")
                
                # Only compare time_to_station if locations match
                if existing_row['current_location'] == row['current_location']:
                    # If new row has smaller time_to_station, replace the existing one
                    if row['time_to_station'] < existing_row['time_to_station']:
                        print(f"Replacing existing row because new time_to_station ({row['time_to_station']}) < existing ({existing_row['time_to_station']})")
                        rows.remove(existing_row)
                        rows.append(row)
                    else:
                        print(f"Keeping existing row because new time_to_station ({row['time_to_station']}) >= existing ({existing_row['time_to_station']})")
                else:
                    print(f"Skipping both rows because locations differ: {existing_row['current_location']} vs {row['current_location']}")
                    rows.remove(existing_row)
            else:
                print(f"\nNo duplicate found for train {train_id} at {row['timestamp']}, adding new row")
                rows.append(row)
            
        except Exception as e:
            continue
            
    return rows
    

def fetch_predictions(current_time, client):
    """Collect predictions from TfL API"""
    rows_to_insert = []
    
    try:
        print(f"Fetching predictions for station {STATION_ID}...")
        
        url = f'https://api.tfl.gov.uk/StopPoint/{STATION_ID}/Arrivals'
        params = {
            'app_key': API_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
        predictions = response.json()
        print(f"Successfully fetched {len(predictions)} predictions")
        
        # Process predictions
        rows_to_insert.extend(process_line_predictions(predictions, current_time, client))
        
    except Exception as e:
        print(f"Error fetching predictions: {str(e)}")
        return None
        
    return rows_to_insert

@functions_framework.http
def collect_predictions(request):
    """Cloud Function to collect predictions and store them in BigQuery."""
    # Initialize time first
    current_time = datetime.now(pytz.timezone('Europe/London'))
    if current_time.dst() != timedelta(0):  # Check if we're in BST
        current_time = current_time + timedelta(hours=1)  # Add hour for BST

    # Initialize BigQuery client with explicit project ID
    client = bigquery.Client(project='nico-playground-384514')

    try:

        # Collect predictions
        rows_to_insert = fetch_predictions(current_time, client)
        

        
        if rows_to_insert:
            try:
                # Use fully qualified table ID
                table_id = "nico-playground-384514.transport_predictions.prediction_history"
                errors = client.insert_rows_json(table_id, rows_to_insert)
                
                if errors:
                    print(f"Encountered errors while inserting rows: {errors}")
                    print(f"First row that failed: {rows_to_insert[0]}")
                else:
                    print(f"Successfully inserted {len(rows_to_insert)} rows")
                    
                    # Process initial errors after successful insert
                if any(row.get('arrival_timestamp') for row in rows_to_insert):
                    one_min_ago = current_time - timedelta(minutes=1)
                    one_min_ago_str = one_min_ago.isoformat()

                    initial_errors_query = f"""
                        INSERT INTO `nico-playground-384514.transport_predictions.initial_errors`
                        WITH initial_predictions AS (
                            SELECT 
                                train_id,
                                line,
                                initial_prediction_timestamp,
                                arrival_timestamp,
                                ROW_NUMBER() OVER (PARTITION BY train_id, initial_prediction_timestamp ORDER BY arrival_timestamp DESC) as rn
                            FROM `nico-playground-384514.transport_predictions.prediction_history`
                            WHERE arrival_timestamp IS NOT NULL
                            AND arrival_timestamp >= TIMESTAMP('{one_min_ago_str}')
                        ),
                        initial_locations AS (
                            SELECT 
                                train_id,
                                initial_prediction_timestamp,
                                current_location,
                                direction,
                                ROW_NUMBER() OVER (PARTITION BY train_id, initial_prediction_timestamp ORDER BY timestamp ASC) as rn
                            FROM `nico-playground-384514.transport_predictions.prediction_history`
                            WHERE initial_prediction_timestamp IS NOT NULL
                        ),
                        max_times AS (
                            SELECT 
                                train_id,
                                initial_prediction_timestamp,
                                MAX(time_to_station) as max_time_to_station
                            FROM `nico-playground-384514.transport_predictions.prediction_history`
                            GROUP BY train_id, initial_prediction_timestamp
                        )
                        SELECT DISTINCT
                            ip.train_id,
                            ip.line,
                            ip.initial_prediction_timestamp,
                            ip.arrival_timestamp,
                            TIMESTAMP_DIFF(ip.initial_prediction_timestamp, ip.arrival_timestamp, SECOND) as error_seconds,
                            mt.max_time_to_station as time_to_station,
                            EXTRACT(HOUR FROM ip.arrival_timestamp) as hour,
                            EXTRACT(DAYOFWEEK FROM ip.arrival_timestamp) - 1 as day_of_week,
                            il.current_location,
                            il.direction
                        FROM initial_predictions ip
                        LEFT JOIN initial_locations il 
                            ON ip.train_id = il.train_id 
                            AND ip.initial_prediction_timestamp = il.initial_prediction_timestamp
                            AND il.rn = 1
                        LEFT JOIN max_times mt
                            ON ip.train_id = mt.train_id
                            AND ip.initial_prediction_timestamp = mt.initial_prediction_timestamp
                        WHERE ip.rn = 1
                        AND NOT EXISTS (
                            SELECT 1 
                            FROM `nico-playground-384514.transport_predictions.initial_errors` ie
                            WHERE ie.train_id = ip.train_id
                            AND ie.initial_prediction_timestamp = ip.initial_prediction_timestamp
                            AND ie.arrival_timestamp = ip.arrival_timestamp
                        )
                        """
                    client.query(initial_errors_query)
                    print("Processed initial errors")

                    # Process any_errors for each row with arrival_timestamp
                    any_errors_rows = []
                    for row in rows_to_insert:
                        if row.get('arrival_timestamp'):
                            try:
                                # Define arrival_ts first since we use it in both initial and any errors
                                arrival_ts = datetime.fromisoformat(row['arrival_timestamp'])
                                hour = arrival_ts.hour - 1
                                day_of_week = arrival_ts.weekday() + 1

                                print(f"Processing any errors for train: {row['train_id']}, arrival: {arrival_ts}")  # Debug log
                                        
                                # Then handle any_errors table
                                print(f"Getting any predictions for train: {row['train_id']}")  # Debug log
                                        
                                # Get predictions between initial prediction and arrival
                                predictions_query = f"""
                                        SELECT 
                                            train_id,
                                            line,
                                            timestamp,
                                            time_to_station,
                                            any_prediction_timestamp,
                                            arrival_timestamp,
                                            current_location,
                                            direction
                                        FROM `nico-playground-384514.transport_predictions.prediction_history`
                                        WHERE train_id = '{row['train_id']}'
                                        AND timestamp >= (
                                            SELECT timestamp 
                                            FROM `nico-playground-384514.transport_predictions.prediction_history`
                                            WHERE train_id = '{row['train_id']}'
                                            AND any_prediction_timestamp IS NULL
                                            AND arrival_timestamp IS NULL
                                            ORDER BY TIMESTAMP DESC
                                            LIMIT 1
                                        )
                                        AND any_prediction_timestamp IS NOT NULL
                                        ORDER BY timestamp ASC
                                        """
                                        
                                results = list(client.query(predictions_query))
                                print(f"Found {len(results)} any predictions for {row['train_id']}")
                                        
                                # Process ALL predictions, not just middle ones
                                for pred in results:
                                    if pred.any_prediction_timestamp:
                                        # Calculate error in seconds for this prediction
                                        prediction_ts = pred.any_prediction_timestamp
                                        error_seconds = int((prediction_ts - arrival_ts).total_seconds())
                                            
                                        print(f"Adding any error - Train: {pred.train_id}, Time: {pred.time_to_station}, Error: {error_seconds}")
                                            
                                        # Add to batch
                                        any_errors_rows.append({
                                            'train_id': pred.train_id,
                                            'line': pred.line,
                                            'timestamp': pred.timestamp.isoformat(),
                                            'any_prediction_timestamp': pred.any_prediction_timestamp.isoformat(),
                                            'arrival_timestamp': arrival_ts.isoformat(),
                                            'error_seconds': error_seconds,
                                            'hour': hour,
                                            'day_of_week': day_of_week,
                                            'time_to_station': pred.time_to_station,
                                            'current_location': pred.current_location,
                                            'direction': pred.direction
                                        })

                            except Exception as e:
                                print(f"Error processing any error for train {row['train_id']}: {e}")  # Debug log
                                continue

                    # Do batch insert if we have any rows
                    if any_errors_rows:
                        try:
                            errors = client.insert_rows_json(
                                "nico-playground-384514.transport_predictions.any_errors",
                                any_errors_rows
                            )
                            if errors:
                                print(f"Encountered errors while inserting any_errors rows: {errors}")
                            else:
                                print(f"Successfully inserted {len(any_errors_rows)} any_errors rows")
                        except Exception as e:
                            print(f"Error during any_errors batch insert: {str(e)}")

            except Exception as e:
                print(f"Error during batch insert: {str(e)}")
                print(f"First row that would be inserted: {rows_to_insert[0]}")
                raise
        
        return 'OK'
        
    except Exception as e:
        print(f"Major error in function: {str(e)}")
        raise








