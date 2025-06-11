import pandas as pd
from key_journey_information import get_journey_options
from tqdm import tqdm
import time
import concurrent.futures
import requests
from collections import deque
from threading import Lock
import time
import itertools
from collections import defaultdict
import os

# Create reliability_testing directory if it doesn't exist
os.makedirs('reliability_testing', exist_ok=True)

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

# Fast rate limit (about 3000 requests/minute)
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
            'reason': f'Response type: {type(journey_data)}, Value: {str(journey_data)[:100]}'
        }
            
    except Exception as e:
        return {
            'success': False,
            'destination': end_postcode,
            'reason': str(e)[:100]
        }

def run_test_pass(postcodes, pass_num, postcode_type):
    journey_results = []
    failed_postcodes = []
    
    print(f"\nStarting Pass {pass_num} for {postcode_type} with {len(postcodes)} postcodes...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
        futures = {executor.submit(process_postcode, postcode): postcode 
                  for postcode in postcodes}
        
        completed = 0
        total = len(futures)
        
        try:
            for future in tqdm(concurrent.futures.as_completed(futures), total=total):
                completed += 1
                remaining = total - completed
                
                try:
                    # Super aggressive timeout near the end
                    if remaining <= 10:
                        print(f"\nNear end, postcode: {futures[future]}")
                        result = future.result(timeout=0.1)  # 100ms timeout for last 10
                    else:
                        result = future.result(timeout=0.5)  # 500ms normal timeout
                    
                    if result['success']:
                        journey_results.append(result['destination'])
                    else:
                        failed_postcodes.append(result['destination'])
                        
                except Exception as e:
                    postcode = futures[future]
                    failed_postcodes.append(postcode)
                    if remaining <= 10:
                        print(f"\nSkipping stuck postcode near end: {postcode}")
                
                # Emergency escape if we're stuck at the end
                if remaining <= 5:
                    for f in list(futures.keys()):
                        if not f.done():
                            f.cancel()
                            failed_postcodes.append(futures[f])
                            print(f"\nForce cancelled: {futures[f]}")
                    break
                    
        except Exception as e:
            print(f"\nEmergency exit triggered: {str(e)}")
            # Force cancel all remaining futures
            for f in list(futures.keys()):
                if not f.done():
                    f.cancel()
                    failed_postcodes.append(futures[f])
    
    # Save results immediately
    pd.DataFrame(journey_results, columns=['destination']).to_csv(
        f'reliability_testing/{postcode_type}_pass_{pass_num}_successful.csv', index=False)
    pd.DataFrame(failed_postcodes, columns=['postcode']).to_csv(
        f'reliability_testing/{postcode_type}_pass_{pass_num}_failed.csv', index=False)
    
    print(f"\nCompleted {postcode_type} Pass {pass_num}: {len(journey_results)} successful, {len(failed_postcodes)} failed")
    return set(failed_postcodes)

# Read both sets of postcodes
none_type_df = pd.read_csv('journey_results_nonetype_final.csv')
filtered_df = pd.read_csv('london_postcodes_filtered.csv')
sample_size = 2000

# Create samples
sample_a = none_type_df['destination'].sample(n=sample_size, random_state=42).tolist()
sample_b = filtered_df['Postcode'].sample(n=sample_size, random_state=43).tolist()

print(f"\nTesting postcodes:")
print(f"None-type sample size: {len(sample_a)}")
print(f"Filtered London sample size: {len(sample_b)}")

# Save samples
pd.DataFrame(sample_a, columns=['postcode']).to_csv('reliability_testing/none_type_sample.csv', index=False)
pd.DataFrame(sample_b, columns=['postcode']).to_csv('reliability_testing/filtered_london_sample.csv', index=False)

START_POSTCODE = "SW1A 2JR"
NUM_PASSES = 5

failure_counts = defaultdict(int)
pass_results = defaultdict(list)

print("\n=== Starting None-type Tests ===")
none_type_results = []
for i in range(NUM_PASSES):
    failed = run_test_pass(sample_a, i+1, "none_type")
    none_type_results.append(failed)
    for postcode in failed:
        failure_counts[f"none_type_{postcode}"] = failure_counts.get(f"none_type_{postcode}", 0) + 1

print("\n=== Starting Filtered London Tests ===")
filtered_results = []
for i in range(NUM_PASSES):
    failed = run_test_pass(sample_b, i+1, "filtered_london")
    filtered_results.append(failed)
    for postcode in failed:
        failure_counts[f"filtered_{postcode}"] = failure_counts.get(f"filtered_{postcode}", 0) + 1

# Analysis
print("\nResults Analysis:")
print(f"None-type postcodes tested: {len(sample_a)}")
print(f"Filtered London postcodes tested: {len(sample_b)}")

for i in range(NUM_PASSES):
    print(f"\nPass {i+1}:")
    print(f"  None-type failures: {len(none_type_results[i])} ({len(none_type_results[i])/len(sample_a)*100:.1f}%)")
    print(f"  Filtered failures: {len(filtered_results[i])} ({len(filtered_results[i])/len(sample_b)*100:.1f}%)")

# Save final analysis
none_type_failures = {k[10:]: v for k, v in failure_counts.items() if k.startswith('none_type_')}
filtered_failures = {k[9:]: v for k, v in failure_counts.items() if k.startswith('filtered_')}

results_df = pd.DataFrame({
    'postcode': list(none_type_failures.keys()) + list(filtered_failures.keys()),
    'type': ['none_type'] * len(none_type_failures) + ['filtered'] * len(filtered_failures),
    'failure_count': list(none_type_failures.values()) + list(filtered_failures.values())
})
results_df.to_csv('reliability_testing/reliability_test_results.csv', index=False)

# Generate summary of multiple failures
failure_summary = ["\nPostcodes that failed multiple times:"]
for failures in range(NUM_PASSES, 0, -1):
    none_type_count = sum(1 for v in none_type_failures.values() if v == failures)
    filtered_count = sum(1 for v in filtered_failures.values() if v == failures)
    failure_summary.extend([
        f"Failed {failures}/{NUM_PASSES} times:",
        f"  None-type: {none_type_count} postcodes",
        f"  Filtered London: {filtered_count} postcodes"
    ])

# Save analysis to text file
with open('reliability_testing/analysis_summary.txt', 'w') as f:
    f.write('\n'.join(failure_summary))

print('\n'.join(failure_summary))
print("\nAll results saved in the 'reliability_testing' folder") 