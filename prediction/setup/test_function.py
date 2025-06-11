import requests
import time

def test_function():
    url = "https://europe-west2-nico-playground-384514.cloudfunctions.net/collect_predictions"
    
    print("Testing cloud function directly...")
    try:
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Wait a few seconds and check if data was inserted
        print("\nWaiting 5 seconds to check data...")
        time.sleep(5)
        
        # Import here to avoid conflicts with the request above
        from google.cloud import bigquery
        client = bigquery.Client()
        
        query = """
        SELECT COUNT(*) as count
        FROM `nico-playground-384514.transport_predictions.prediction_history`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 MINUTE)
        """
        
        result = client.query(query).result().to_dataframe()
        print(f"\nRecords inserted in the last minute: {result['count'].iloc[0]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_function() 