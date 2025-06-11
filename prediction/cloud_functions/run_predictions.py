import time
import requests
import logging
import subprocess
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def start_server():
    logger.info("Starting Functions Framework server")
    # Start the server in the background using python -m
    subprocess.Popen([
        "/home/nicolas/transport/prediction/cloud_functions/venv/bin/python",
        "-m",
        "functions_framework",
        "--target=collect_predictions",
        "--port=8080"
    ])
    logger.info("Server started")

def make_request():
    try:
        response = requests.post('http://localhost:8080')
        if response.status_code == 200:
            logger.info("Request successful")
        else:
            logger.error(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error making request: {str(e)}")

def run_forever():
    logger.info("Starting prediction collection service")
    start_server()  # Start the server first
     
    while True: 
        try: 
            cycle_start = datetime.now() 
            make_request() 
             
            # Calculate how long to sleep 
            cycle_duration = (datetime.now() - cycle_start).total_seconds() 
            sleep_time = max(0, 33 - cycle_duration)  # Run every 33 seconds 
             
            logger.info(f"Cycle took {cycle_duration:.1f}s, sleeping for {sleep_time:.1f}s") 
            time.sleep(sleep_time)
    
        except Exception as e:
            logger.error(f"Error in run_forever: {e}")
            time.sleep(30)  # Sleep for 30 seconds on error

if __name__ == "__main__":
    run_forever() 