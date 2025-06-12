import logging
from google.cloud import storage
import pandas as pd
import tempfile
import os
import json
from datetime import datetime, time as dt_time, timedelta
from concurrent.futures import ThreadPoolExecutor
import time
import io
import requests
import argparse
import subprocess
import pytz
from dotenv import load_dotenv
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BUCKET_NAME = "london-transport-data"
RESULTS_DIR = "results"
LONDON_TZ = pytz.timezone('Europe/London')

# Get the project root directory (3 levels up from this file)
project_root = Path(__file__).resolve().parent.parent.parent
env_path = project_root / '.env'

# Load environment variables from .env file
if not env_path.exists():
    raise ValueError(f".env file not found at {env_path}")
load_dotenv(env_path)

# Get API keys from environment variables
TFL_API_KEYS = os.getenv('TFL_API_KEYS', '').split(',')
TFL_APP_ID = os.getenv('TFL_APP_ID')

if not TFL_API_KEYS or not TFL_APP_ID:
    raise ValueError("TFL_API_KEYS and TFL_APP_ID environment variables must be set")

# Initialize key rotation
current_key_index = 0

def get_next_api_key():
    """Rotate through API keys"""
    global current_key_index
    key = TFL_API_KEYS[current_key_index]
    current_key_index = (current_key_index + 1) % len(TFL_API_KEYS)
    return key

START_POSTCODE = "SW1A 2JR"  # Houses of Parliament

def get_journey_time(start_postcode, end_postcode):
    """Get journey time between two postcodes using TfL API"""
    try:
        url = f"https://api.tfl.gov.uk/Journey/JourneyResults/{start_postcode}/to/{end_postcode}"
        params = {
            'app_key': get_next_api_key(),  # Use rotating keys
            'app_id': TFL_APP_ID,
            'mode': 'tube,bus,dlr,elizabeth-line,overground',
            'time': '1000',
            'timeIs': 'Departing',
            'walkingSpeed': 'average',
            'cyclePreference': 'none',
            'accessibilityPreference': 'noRequirements'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'journeys' in data and len(data['journeys']) > 0:
            fastest_journey = min(data['journeys'], key=lambda x: x['duration'])
            return {
                'success': True,
                'duration': fastest_journey['duration'],
                'destination': end_postcode
            }
        else:
            return {
                'success': False,
                'reason': 'No journeys found',
                'destination': end_postcode
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'reason': str(e),
            'destination': end_postcode
        }

def process_postcode(postcode):
    """Process a single postcode"""
    try:
        result = get_journey_time(START_POSTCODE, postcode)
        if result['success']:
            logger.info(f"✓ {postcode}: {result['duration']} mins")
        else:
            logger.warning(f"✗ {postcode}: {result.get('reason', 'Unknown error')}")
        return result
    except Exception as e:
        logger.error(f"Error processing {postcode}: {str(e)}")
        return {
            'success': False,
            'reason': str(e),
            'destination': postcode
        }

def main(batch):
    """Main function to process postcodes"""
    logger.info("=== Starting Journey Time Collection ===")
    
    try:
        # Validate batch parameter
        try:
            batch = int(batch)
            if batch not in [1, 2]:
                logger.error(f"Invalid batch number: {batch}")
                return False
        except ValueError:
            logger.error(f"Invalid batch format: {batch}")
            return False
            
        logger.info(f"Processing Batch {batch} of 2")
        
        # Initialize GCP clients
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket('london-transport-data')
            logger.info("Successfully initialized GCP clients")
        except Exception as e:
            error_msg = f"Failed to initialize GCP clients: {str(e)}"
            logger.error(error_msg)
            return False
        
        # Get current time and add 1 hour for BST
        now = datetime.now() + timedelta(hours=1)
        timestamp = now.strftime('%Y%m%d_%H')
        
        # Load and validate postcodes
        try:
            logger.info("Loading postcodes from GCS...")
            blob = bucket.blob('london_postcodes_filtered.csv')
            
            if not blob.exists():
                error_msg = 'london_postcodes_filtered.csv not found in bucket'
                logger.error(error_msg)
                return False
            
            # Download to temp file
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                blob.download_to_file(temp_file)
                temp_file.flush()
                temp_file_path = temp_file.name
            
            postcodes_df = pd.read_csv(temp_file_path)
            os.unlink(temp_file_path)  # Clean up
            
            if len(postcodes_df) == 0:
                error_msg = 'Postcode file is empty'
                logger.error(error_msg)
                return False
                
            # Sample postcodes
            seed = int(timestamp[-2:]) + (batch - 1)
            sampled_postcodes = postcodes_df['Postcode'].sample(n=15000, random_state=seed).tolist()
            logger.info(f"Successfully sampled {len(sampled_postcodes)} postcodes for batch {batch}")
            
        except Exception as e:
            error_msg = f'Error processing postcodes: {str(e)}'
            logger.error(error_msg)
            return False
        
        # Process postcodes
        all_results = []
        failed_postcodes = []
        start_time = time.time()
        
        try:
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(process_postcode, postcode): postcode 
                          for postcode in sampled_postcodes}
                
                completed = 0
                for future in futures:
                    try:
                        result = future.result(timeout=2.0)
                        postcode = futures[future]
                        
                        if result['success']:
                            all_results.append({
                                'postcode': result['destination'],
                                'duration': result['duration']
                            })
                        else:
                            failed_postcodes.append(postcode)
                            logger.warning(f"Failed to process postcode {postcode}: {result.get('reason')}")
                        
                        completed += 1
                        if completed % 100 == 0:
                            elapsed_minutes = (time.time() - start_time) / 60
                            rate = completed / elapsed_minutes if elapsed_minutes > 0 else 0
                            remaining = len(sampled_postcodes) - completed
                            eta_minutes = remaining / rate if rate > 0 else 0
                            logger.info(f"Progress: {completed}/{len(sampled_postcodes)} | Rate: {rate:.0f}/min | ETA: {eta_minutes:.1f}min")
                            
                    except Exception as e:
                        postcode = futures[future]
                        failed_postcodes.append(postcode)
                        logger.error(f"Error processing {postcode}: {str(e)}")
                        continue
                        
        except Exception as e:
            error_msg = f'Error in postcode processing: {str(e)}'
            logger.error(error_msg)
            return False
        
        # Save results
        try:
            logger.info("Saving results...")
            final_results = {
                'timestamp': timestamp,
                'batch': batch,
                'data': all_results,
                'total_processed': len(all_results),
                'total_postcodes': len(sampled_postcodes),
                'failed_postcodes': failed_postcodes,
                'processing_time_minutes': (time.time() - start_time) / 60
            }
            
            results_blob = bucket.blob(f'results/journey_times_{timestamp}_batch{batch}.json')
            results_blob.upload_from_string(
                json.dumps(final_results),
                content_type='application/json'
            )
            
            logger.info(f"Successfully saved results to GCS: journey_times_{timestamp}_batch{batch}.json")
            return True
            
        except Exception as e:
            error_msg = f'Error saving results: {str(e)}'
            logger.error(error_msg)
            return False
            
    except Exception as e:
        error_msg = f'Unexpected error: {str(e)}'
        logger.error(error_msg)
        return False

def run_forever():
    logger.info("Starting heatmap collection service")
    
    while True:
        try:
            # Get current time and add 1 hour for BST
            now = datetime.now() + timedelta(hours=1)
            
            # Calculate time until next run (either XX:00 or XX:30)
            if now.minute >= 30:
                # Next run is at XX:00
                wait_until = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
                batch = 1
            else:
                # Next run is at XX:30
                wait_until = now.replace(minute=30, second=0, microsecond=0)
                batch = 2
            
            wait_seconds = (wait_until - now).total_seconds()
            logger.info(f"Waiting {wait_seconds:.0f} seconds until next run at {wait_until.strftime('%H:%M')} (batch {batch})")
            time.sleep(wait_seconds)
            
            # Run the batch
            logger.info(f"Running batch {batch}")
            main(batch)
            
        except Exception as e:
            logger.error(f"Error in run_forever: {str(e)}")
            time.sleep(60)  # Wait a minute before retrying

if __name__ == "__main__":
    logger.info("Starting heatmap collection service")
    run_forever() 