import pandas as pd
from key_journey_information import get_journey_options
from tqdm import tqdm
import time
import concurrent.futures
import requests
from collections import deque, defaultdict
from threading import Lock
import itertools
import os
from datetime import datetime, timedelta
import json

# Create directory for this test
TEST_DIR = 'time_reliability_testing'
os.makedirs(TEST_DIR, exist_ok=True)

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
        self.lock = Lock()

    def acquire(self):
        with self.lock:
            now = time.time()
            while self.requests and self.requests[0] <= now - self.time_window:
                self.requests.popleft()
            if len(self.requests) >= self.max_requests:
                sleep_time = self.requests[0] - (now - self.time_window)
                time.sleep(max(0, sleep_time))
            self.requests.append(now)

rate_limiter = RateLimiter(max_requests=2940, time_window=60)

API_KEYS = [
    "b1efe66db0f748c3a9a248ca9ed03c9b",
    "2e21963ed6f645da8fa40ef78065949d",
    "515eb7d072db442097bf7cf91468f5b5",
    "c4aa169998d84f74a764cee3b527156f",
    "916255a1230148c498bb1293de159d9d",
    "61add53bd04c49e3917032fb7327d871"
]
key_cycle = itertools.cycle(API_KEYS)

def process_postcode(end_postcode):
    rate_limiter.acquire()
    api_key = next(key_cycle)
    
    try:
        journey_data = get_journey_options(START_POSTCODE, end_postcode, api_key)
        
        if journey_data and 'journeys' in journey_data and isinstance(journey_data['journeys'], list):
            valid_journeys = [j for j in journey_data['journeys'] if j.get('duration')]
            
            if valid_journeys:
                fastest_journey = min(valid_journeys, 
                                   key=lambda x: x.get('duration', float('inf')))
                return {
                    'success': True,
                    'destination': end_postcode,
                    'duration': fastest_journey.get('duration', None)
                }
        
        return {
            'success': False,
            'destination': end_postcode,
            'reason': f'No valid journeys found'
        }
            
    except Exception as e:
        return {
            'success': False,
            'destination': end_postcode,
            'reason': str(e)[:100]
        }

def process_batch(postcodes, batch_num, timestamp):
    journey_results = []
    failed_postcodes = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(process_postcode, postcode): postcode for postcode in postcodes}
        
        try:
            done, not_done = concurrent.futures.wait(
                futures.keys(),
                timeout=30,
                return_when=concurrent.futures.ALL_COMPLETED
            )
            
            for future in futures:
                try:
                    result = future.result(timeout=0.5)
                    if result['success']:
                        journey_results.append(result['destination'])
                    else:
                        failed_postcodes.append(result['destination'])
                except Exception:
                    failed_postcodes.append(futures[future])
                    
        except concurrent.futures.TimeoutError:
            print(f"\nBatch {batch_num} timed out, marking remaining as failed")
            for future in futures:
                if not future.done():
                    future.cancel()
                    failed_postcodes.append(futures[future])
    
    return journey_results, failed_postcodes

def run_test_pass(postcodes, timestamp):
    all_successful = []
    all_failed = []
    BATCH_SIZE = 100
    
    for i in range(0, len(postcodes), BATCH_SIZE):
        batch = postcodes[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        print(f"\nProcessing Batch {batch_num} at {timestamp}")
        
        successful, failed = process_batch(batch, batch_num, timestamp)
        all_successful.extend(successful)
        all_failed.extend(failed)
    
    # Save results for this timestamp
    results = {
        'timestamp': timestamp,
        'successful': all_successful,
        'failed': all_failed
    }
    
    with open(f'{TEST_DIR}/run_{timestamp.replace(":", "-")}.json', 'w') as f:
        json.dump(results, f)
    
    return set(all_successful), set(all_failed)

def analyze_results():
    # Load all results
    all_runs = []
    for filename in os.listdir(TEST_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(TEST_DIR, filename), 'r') as f:
                all_runs.append(json.load(f))
    
    # Get all unique postcodes
    all_postcodes = set()
    for run in all_runs:
        all_postcodes.update(run['successful'])
        all_postcodes.update(run['failed'])
    
    # Analyze each postcode
    always_works = set()
    never_works = set()
    sometimes_works = set()
    
    for postcode in all_postcodes:
        successes = sum(1 for run in all_runs if postcode in run['successful'])
        
        if successes == len(all_runs):
            always_works.add(postcode)
        elif successes == 0:
            never_works.add(postcode)
        else:
            sometimes_works.add(postcode)
    
    # Save results
    pd.DataFrame(list(always_works), columns=['postcode']).to_csv(f'{TEST_DIR}/always_works.csv', index=False)
    pd.DataFrame(list(never_works), columns=['postcode']).to_csv(f'{TEST_DIR}/never_works.csv', index=False)
    pd.DataFrame(list(sometimes_works), columns=['postcode']).to_csv(f'{TEST_DIR}/sometimes_works.csv', index=False)
    
    # Save summary
    summary = {
        'total_runs': len(all_runs),
        'total_postcodes': len(all_postcodes),
        'always_works': len(always_works),
        'never_works': len(never_works),
        'sometimes_works': len(sometimes_works)
    }
    
    with open(f'{TEST_DIR}/summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

START_POSTCODE = "SW1A 2JR"

# Read postcodes
none_type_df = pd.read_csv('none_type_postcodes.csv')
all_postcodes = none_type_df['Postcode'].tolist()

print(f"Starting 24-hour test with {len(all_postcodes)} postcodes")

# Run for 24 hours
start_time = datetime.now()
end_time = start_time + timedelta(hours=24)

while datetime.now() < end_time:
    current_time = datetime.now()
    timestamp = current_time.strftime('%Y%m%d_%H%M')
    
    print(f"\n=== Starting run at {timestamp} ===")
    successful, failed = run_test_pass(all_postcodes, timestamp)
    print(f"Run completed: {len(successful)} successful, {len(failed)} failed")
    
    # Wait until next 30-minute mark
    next_run = current_time + timedelta(minutes=30)
    next_run = next_run.replace(minute=next_run.minute // 30 * 30, second=0, microsecond=0)
    sleep_time = (next_run - datetime.now()).total_seconds()
    if sleep_time > 0:
        print(f"Sleeping for {sleep_time/60:.1f} minutes until next run")
        time.sleep(sleep_time)

# Analyze all results
print("\nAnalyzing results...")
analyze_results()
print("\nAnalysis complete! Check the time_reliability_testing folder for results.") 