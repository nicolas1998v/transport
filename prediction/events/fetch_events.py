import os
import requests
import time
from datetime import datetime, timedelta
from google.cloud import bigquery
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ticketmaster API configuration
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')

# BigQuery configuration
client = bigquery.Client()
table_id = "nico-playground-384514.transport_predictions.events"

# List of major venues with their Ticketmaster IDs
MAJOR_VENUES = {
    'Wembley Stadium': 'KovZ9177ML0',
    'Twickenham Stadium': 'rZ7SnyZadM6',
    'Tottenham Hotspur Stadium': 'KovZ9177OxV',
    'London Stadium': 'KovZ9177EX0',
    'Emirates Stadium': 'KovZ9177-U7',
    'Stamford Bridge': 'KovZ9177F9V',
    "Lord's Cricket Ground": 'KovZpZAn6dlA',
    'The Oval': 'KovZ9177Oy0',
    'The O2': 'KovZ9177PFf',
    'Hyde Park': 'KovZ9177gxV'
}

# Music genre IDs for Ticketmaster
MUSIC_GENRES = {
    'KZazBEonSMnZfZ7v6JA': 'Music',  # General Music
    'KnvZfZ7vAvv': 'Rock',           # Rock
    'KnvZfZ7vAvd': 'Pop',            # Pop
    'KnvZfZ7vAeJ': 'Hip-Hop/Rap',    # Hip-Hop/Rap
    'KnvZfZ7vAvF': 'R&B',            # R&B
    'KnvZfZ7vAvE': 'Country',        # Country
    'KnvZfZ7vAv6': 'Jazz',           # Jazz
    'KnvZfZ7vAvA': 'Classical',      # Classical
    'KnvZfZ7vAvt': 'Electronic',     # Electronic
    'KnvZfZ7vAvk': 'Folk'            # Folk
}

def fetch_venue_events(venue_id, venue_name):
    """Fetch events for a specific venue."""
    headers = {
        'Accept': 'application/json'
    }
    
    # Calculate date range (next 30 days)
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)
    
    # Format dates as YYYY-MM-DDTHH:mm:ssZ
    start_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    url = f'https://app.ticketmaster.com/discovery/v2/events'
    params = {
        'apikey': TICKETMASTER_API_KEY,
        'venueId': venue_id,
        'startDateTime': start_str,
        'endDateTime': end_str,
        'locale': '*',
        'size': 100,
        'segmentId': 'KZFzniwnSyZfZ7v7nE',  # Sports segment
        'sort': 'date,asc'  # Sort by date ascending
    }
    
    print(f"Searching for sports events from {start_str} to {end_str}")
    
    events = []
    page = 0
    
    while True:
        try:
            params['page'] = page
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 429:  # Rate limit hit
                print(f"Rate limit hit for {venue_name}, waiting 1 second...")
                time.sleep(1)
                continue
                
            if response.status_code != 200:
                print(f"Error fetching events for {venue_name}: {response.status_code}")
                print(f"Response: {response.text}")
                break
                
            data = response.json()
            
            if '_embedded' not in data or 'events' not in data['_embedded']:
                break
                
            events.extend(data['_embedded']['events'])
            
            if page >= data.get('page', {}).get('totalPages', 0) - 1:
                break
                
            page += 1
            time.sleep(0.5)  # Increased rate limiting
            
        except Exception as e:
            print(f"Error fetching events for {venue_name}: {str(e)}")
            break
    
    # Now fetch music events
    params['segmentId'] = 'KZFzniwnSyZfZ7v7nJ'  # Music segment
    page = 0  # Reset page counter for music events
    print(f"Searching for music events from {start_str} to {end_str}")
    
    while True:
        try:
            params['page'] = page
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 429:  # Rate limit hit
                print(f"Rate limit hit for {venue_name}, waiting 1 second...")
                time.sleep(1)
                continue
            
            if response.status_code != 200:
                print(f"Error fetching events for {venue_name}: {response.status_code}")
                print(f"Response: {response.text}")
                break
                
            data = response.json()
            
            if '_embedded' not in data or 'events' not in data['_embedded']:
                break
                
            events.extend(data['_embedded']['events'])
            
            if page >= data.get('page', {}).get('totalPages', 0) - 1:
                break
                
            page += 1
            time.sleep(0.5)  # Increased rate limiting
            
        except Exception as e:
            print(f"Error fetching events for {venue_name}: {str(e)}")
            break
    
    return events

def process_events(events, venue_name):
    """Process events and extract relevant information."""
    processed_events = []
    
    # Sort events by date to handle duplicates
    events.sort(key=lambda x: x['dates']['start']['dateTime'])
    
    last_event_time = None
    last_event_venue = None
    
    for event in events:
        try:
            # Get event details
            event_date = datetime.strptime(event['dates']['start']['dateTime'], '%Y-%m-%dT%H:%M:%SZ')
            
            # Skip if this event is too close to the previous one at the same venue
            if (last_event_time and last_event_venue == venue_name and 
                (event_date - last_event_time).total_seconds() < 7200):  # 7200 seconds = 2 hours
                print(f"Skipping duplicate event at {venue_name}: {event['name']} (too close to previous event)")
                continue
            
            # Get venue information
            venue = event.get('_embedded', {}).get('venues', [{}])[0]
            
            # Get genre/segment information
            genres = []
            event_type = 'Other'
            if 'classifications' in event:
                for classification in event['classifications']:
                    segment = classification.get('segment', {})
                    if segment.get('name') == 'Music':
                        event_type = 'Music'
                        genres.append(classification.get('genre', {}).get('name', ''))
                    elif segment.get('name') == 'Sports':
                        event_type = 'Sports'
                        genres.append(classification.get('genre', {}).get('name', ''))
            
            # Get attendance information
            expected_attendance = None
            if 'priceRanges' in event:
                for price_range in event['priceRanges']:
                    if 'max' in price_range:
                        expected_attendance = max(expected_attendance or 0, price_range['max'])
            
            # Add event to processed events (moved outside the priceRanges check)
            processed_events.append({
                'event_id': event['id'],
                'event_name': event['name'],
                'event_date': event_date,
                'expected_attendance': expected_attendance,
                'venue_name': venue_name,
                'venue_address': venue.get('address', {}).get('line1', ''),
                'event_url': event['url'],
                'event_type': event_type,
                'genres': ','.join(genres),
                'last_updated': datetime.now()
            })
            
            # Update last event time and venue
            last_event_time = event_date
            last_event_venue = venue_name
            
        except Exception as e:
            print(f"Error processing event {event.get('id', 'unknown')}: {str(e)}")
            continue
    
    return processed_events

def update_bigquery(events):
    """Update BigQuery table with new event data."""
    if not events:
        print("No events found matching criteria")
        return
        
    # Convert to DataFrame
    df = pd.DataFrame(events)
    
    # Define schema
    schema = [
        bigquery.SchemaField("event_id", "STRING"),
        bigquery.SchemaField("event_name", "STRING"),
        bigquery.SchemaField("event_date", "TIMESTAMP"),
        bigquery.SchemaField("expected_attendance", "INTEGER"),
        bigquery.SchemaField("venue_name", "STRING"),
        bigquery.SchemaField("venue_address", "STRING"),
        bigquery.SchemaField("event_url", "STRING"),
        bigquery.SchemaField("event_type", "STRING"),
        bigquery.SchemaField("genres", "STRING"),
        bigquery.SchemaField("last_updated", "TIMESTAMP")
    ]
    
    try:
        # Try the DataFrame method first (requires pyarrow)
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )
        
        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )
        job.result()  # Wait for the job to complete
        
        print(f"Loaded {len(df)} events into {table_id}")
        
    except Exception as e:
        print(f"DataFrame method failed: {str(e)}")
        print("Falling back to JSON method...")
        
        # Fallback: Convert to JSON and use insert_rows method
        # First, get existing event IDs to avoid duplicates
        existing_events_query = f"SELECT event_id FROM `{table_id}`"
        try:
            existing_events_df = client.query(existing_events_query).to_dataframe()
            existing_event_ids = set(existing_events_df['event_id'].astype(str))
            print(f"Found {len(existing_event_ids)} existing events")
        except Exception as e:
            print(f"Could not check existing events: {str(e)}")
            existing_event_ids = set()
        
        rows_to_insert = []
        new_events_count = 0
        for _, row in df.iterrows():
            event_id = str(row['event_id'])
            if event_id not in existing_event_ids:
                rows_to_insert.append({
                    'event_id': event_id,
                    'event_name': str(row['event_name']),
                    'event_date': row['event_date'].isoformat(),
                    'expected_attendance': row['expected_attendance'] if pd.notna(row['expected_attendance']) else None,
                    'venue_name': str(row['venue_name']),
                    'venue_address': str(row['venue_address']),
                    'event_url': str(row['event_url']),
                    'event_type': str(row['event_type']),
                    'genres': str(row['genres']),
                    'last_updated': row['last_updated'].isoformat()
                })
                new_events_count += 1
            else:
                print(f"Skipping duplicate event: {event_id}")
        
        print(f"Adding {new_events_count} new events (skipped {len(df) - new_events_count} duplicates)")
        
        # Create table with schema (don't delete existing data)
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        
        # Insert rows
        errors = client.insert_rows_json(table, rows_to_insert)
        if errors:
            print(f"Errors inserting rows: {errors}")
        else:
            print(f"Successfully loaded {len(rows_to_insert)} events into {table_id}")

def main():
    """Main function to fetch and update event data."""
    print(f"Starting event fetch at {datetime.now()}")
    
    if not TICKETMASTER_API_KEY:
        print("Error: TICKETMASTER_API_KEY environment variable not set")
        return
        
    all_events = []
    
    # Fetch events for each venue
    for venue_name, venue_id in MAJOR_VENUES.items():
        try:
            print(f"\nFetching events for {venue_name}...")
            events = fetch_venue_events(venue_id, venue_name)
            print(f"Found {len(events)} raw events")
            
            print(f"Processing events for {venue_name}...")
            processed_events = process_events(events, venue_name)
            all_events.extend(processed_events)
        
            print(f"Processed {len(processed_events)} events for {venue_name}")
            time.sleep(1)  # Add delay between venues
        except Exception as e:
            print(f"Error processing venue {venue_name}: {str(e)}")
            continue
    
    print(f"\nTotal events found: {len(all_events)}")
    
    if all_events:
        print("Updating BigQuery...")
        try:
            update_bigquery(all_events)
            print("Successfully updated BigQuery!")
        except Exception as e:
            print(f"Error updating BigQuery: {str(e)}")
    else:
        print("No events found - skipping BigQuery update")
    
    print(f"Event fetch completed at {datetime.now()}")
    print("Done!")

if __name__ == "__main__":
    main()