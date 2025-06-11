import requests
from datetime import datetime

def parse_journey(journey):
    """Parse a single journey and return formatted information"""
    total_duration = journey.get('duration', 0)
    start_time = journey.get('startDateTime', '').split('T')[1][:5]
    end_time = journey.get('arrivalDateTime', '').split('T')[1][:5]
    
    # Process each leg of the journey
    steps = []
    modes = set()
    
    for leg in journey.get('legs', []):
        mode = leg.get('mode', {}).get('name', '').capitalize()
        modes.add(mode)
        
        instruction = leg.get('instruction', {})
        summary = instruction.get('summary', '')
        duration = leg.get('duration', 0)
        
        if mode and summary:
            steps.append({
                'mode': mode,
                'instruction': summary,
                'duration': duration
            })
    
    return {
        'duration': total_duration,
        'start_time': start_time,
        'end_time': end_time,
        'steps': steps,
        'modes': sorted(list(modes))
    }

def format_duration(minutes):
    """Format minutes into hours and minutes string"""
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"

def format_journey_summary(journey_data):
    """Format journey information into a readable summary"""
    formatted = []
    formatted.append(f"Journey Option ({journey_data['start_time']} - {journey_data['end_time']})")
    formatted.append(f"Total Duration: {format_duration(journey_data['duration'])}")
    formatted.append(f"Travel Modes: {', '.join(journey_data['modes'])}")
    formatted.append("\nStep by Step:")
    
    for i, step in enumerate(journey_data['steps'], 1):
        formatted.append(f"{i}. [{step['mode']}] {step['instruction']} ({format_duration(step['duration'])})")
    
    return '\n'.join(formatted)

def process_journeys(data):
    """Process all journeys in the data"""
    print("Processing journeys...")
    print(f"Type of data: {type(data)}")
    
    if isinstance(data, dict):
        print("Keys in data:", list(data.keys()))
        if 'journeys' in data:
            journeys = data['journeys']
            print(f"Number of journeys: {len(journeys)}")
            
            parsed_journeys = []
            for journey in journeys:
                parsed_journey = parse_journey(journey)
                parsed_journeys.append(parsed_journey)
                
            # Print formatted summaries
            for i, journey in enumerate(parsed_journeys, 1):
                print(f"\nRoute Option {i}:")
                print("-" * 50)
                print(format_journey_summary(journey))
                print("-" * 50)
        else:
            print("No 'journeys' key found in data")
    else:
        print("Data is not a dictionary")

def get_journey_options(start_postcode, end_postcode, api_key=None):
    """Get journey options from TFL API using postcodes"""
    # Clean up postcodes: remove spaces and convert to uppercase
    start_postcode = start_postcode.replace(" ", "").upper()
    end_postcode = end_postcode.replace(" ", "").upper()
    
    # Format the URL with the postcodes in the path
    base_url = f"https://api.tfl.gov.uk/journey/journeyresults/{start_postcode}/to/{end_postcode}"
    
    params = {
        'app_key': api_key,
        'mode': 'tube,bus,walking',
        'time': datetime.now().strftime("%H%M"),
        'timeIs': 'Departing',
        'journeyPreference': 'LeastTime'
    }
    
    try:
        response = requests.get(base_url, params=params)
        print(f"Requesting URL: {response.url}")  # Debug line to see the full URL
        
        if response.status_code == 404:
            print("Error: Could not find a valid journey between these postcodes.")
            print("Make sure the postcodes are valid and within London's transport network.")
            return None
            
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching journey data: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    # Replace the sample data with real API call
    start = input("Enter start postcode: ")
    end = input("Enter end postcode: ")
    
    # Optional: Add your TFL API key here
    api_key = "b1efe66db0f748c3a9a248ca9ed03c9b"  # Replace with your API key if you have one
    
    journey_data = get_journey_options(start, end, api_key)
    if journey_data:
        process_journeys(journey_data)
    else:
        print("Failed to get journey data")