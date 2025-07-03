from datetime import datetime, timedelta
import requests
from google.cloud import bigquery
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize BigQuery client
client = bigquery.Client(project='nico-playground-384514')

# Weather API configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')  # Must be set in Cloud Function
LONDON_LAT = 51.5074
LONDON_LON = -0.1278

def create_weather_table():
    """Create the weather data table if it doesn't exist."""
    schema = [
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("temperature", "FLOAT64"),
        bigquery.SchemaField("humidity", "FLOAT64"),
        bigquery.SchemaField("wind_speed", "FLOAT64"),
        bigquery.SchemaField("weather_condition", "STRING"),
        bigquery.SchemaField("precipitation", "FLOAT64"),
        bigquery.SchemaField("cloud_coverage", "FLOAT64")
    ]
    
    table_id = "nico-playground-384514.transport_predictions.weather_data"
    
    try:
        # First check if table exists
        try:
            client.get_table(table_id)
            return
        except Exception:
            pass
        
        # Create table with time-based partitioning and clustering
        table = bigquery.Table(table_id, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.HOUR,
            field="timestamp"
        )
        table.clustering_fields = ["weather_condition"]
        
        table = client.create_table(table)
        
    except Exception as e:
        print(f"Error creating table: {e}")
        raise

def get_weather_data():
    """Fetch weather data from OpenWeatherMap API."""
    if not WEATHER_API_KEY:
        raise ValueError("WEATHER_API_KEY environment variable is not set")
        
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'lat': LONDON_LAT,
        'lon': LONDON_LON,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant weather data and round to nearest hour
        current_time = datetime.now()
        rounded_time = current_time.replace(minute=0, second=0, microsecond=0)
        
        weather_data = {
            'timestamp': rounded_time,
            'temperature': round(data['main']['temp'], 1),
            'humidity': round(data['main']['humidity'], 1),
            'wind_speed': round(data['wind']['speed'], 1),
            'weather_condition': data['weather'][0]['main'].lower(),
            'precipitation': round(data.get('rain', {}).get('1h', 0), 1),
            'cloud_coverage': round(data['clouds']['all'], 1)
        }
        
        return weather_data
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def store_weather_data(weather_data):
    """Store weather data in BigQuery."""
    if not weather_data:
        return
    
    table_id = "nico-playground-384514.transport_predictions.weather_data"
    
    try:
        # Insert directly - BigQuery will handle duplicates if any
        insert_query = f"""
        INSERT INTO `{table_id}` (
            timestamp, temperature, humidity, wind_speed, 
            weather_condition, precipitation, cloud_coverage
        ) VALUES (
            TIMESTAMP('{weather_data['timestamp'].isoformat()}'),
            {weather_data['temperature']},
            {weather_data['humidity']},
            {weather_data['wind_speed']},
            '{weather_data['weather_condition']}',
            {weather_data['precipitation']},
            {weather_data['cloud_coverage']}
        )
        """
        
        client.query(insert_query).result()
        print(f"Weather data inserted for {weather_data['timestamp']}")
            
    except Exception as e:
        print(f"Error storing weather data: {e}")
        raise

def main():
    """Main function to collect weather data."""
    # Create table if it doesn't exist
    create_weather_table()
    
    # Get and store weather data
    weather_data = get_weather_data()
    if weather_data:
        store_weather_data(weather_data)
        print("Weather data collected successfully")
    else:
        print("No weather data collected") 