import requests
from typing import Dict, List
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
TFL_API_KEY = os.getenv('TFL_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SKIDDLE_API_KEY = os.getenv('SKIDDLE_API_KEY')

if not all([TFL_API_KEY, GOOGLE_API_KEY, SKIDDLE_API_KEY]):
    raise ValueError("All API keys must be set in environment variables")

def get_station_info(station_id: str, 
                    tfl_api_key: str,
                    google_api_key: str,
                    radius: int = 500,
                    place_type: str = 'restaurant',
                    event_type: str = None):
    """Get station facilities, nearby places, and events"""
    facilities = get_station_facilities(station_id, tfl_api_key)
    
    if facilities and 'lat' in facilities and 'lon' in facilities:
        station_coords = {
            'lat': facilities['lat'],
            'lon': facilities['lon']
        }
        
        # Get places using Google Places API
        restaurants = get_places_near_station(
            station_coords=station_coords,
            api_key=google_api_key,
            radius=radius,
            place_type=place_type
        )
        
        attractions = get_places_near_station(
            station_coords=station_coords,
            api_key=google_api_key,
            radius=radius,
            place_type='tourist_attraction'
        )
        
        
        return {
            'facilities': facilities,
            'nearby_restaurants': restaurants,
            'nearby_attractions': attractions,
            'place_type': place_type
        }
    return None

def get_station_facilities(station_id: str, app_key: str = None):
    """Get facilities information for a TfL station"""
    base_url = f"https://api.tfl.gov.uk/StopPoint/{station_id}"
    params = {'app_key': app_key} if app_key else {}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        facilities = {
            'station_name': data.get('commonName'),
            'facilities': [],
            'lines': [],
            'zones': data.get('zones', []),
            'wifi': False,
            'toilets': False,
            'lifts': False,
            'parking': False,
            'lat': data.get('lat'),
            'lon': data.get('lon')
        }
        
        for prop in data.get('additionalProperties', []):
            category = prop.get('category')
            key = prop.get('key')
            value = prop.get('value')
            
            if category == 'Facility':
                facilities['facilities'].append(key)
            
            if 'wifi' in key.lower():
                facilities['wifi'] = value.lower() == 'yes'
            elif 'toilet' in key.lower():
                facilities['toilets'] = value.lower() == 'yes'
            elif 'lift' in key.lower() or 'elevator' in key.lower():
                facilities['lifts'] = value.lower() == 'yes'
            elif 'parking' in key.lower():
                facilities['parking'] = value.lower() == 'yes'
        
        for line in data.get('lines', []):
            facilities['lines'].append(line.get('name'))
        
        return facilities
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching station facilities: {e}")
        return None

def get_places_near_station(station_coords: Dict[str, float], 
                          api_key: str, 
                          radius: int = 500,
                          place_type: str = 'restaurant') -> List[Dict]:
    """
    Get places near a station using Google Places API
    Valid place_types include: restaurant, cafe, bar, tourist_attraction, 
    museum, park, art_gallery, night_club, shopping_mall
    """
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    print(f"Searching for {place_type}s near: {station_coords['lat']}, {station_coords['lon']}")
    
    params = {
        'location': f"{station_coords['lat']},{station_coords['lon']}",
        'radius': radius,
        'type': place_type,
        'key': api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        results = response.json().get('results', [])
        
        places = []
        for place in results:
            places.append({
                'name': place.get('name'),
                'address': place.get('vicinity'),
                'rating': place.get('rating'),
                'types': place.get('types'),
                'price_level': place.get('price_level'),
                'open_now': place.get('opening_hours', {}).get('open_now')
            })
        
        return places
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching places: {e}")
        return []

def get_events_near_station(station_coords: Dict[str, float], 
                          api_key: str,
                          radius: int = 500,
                          event_type: str = None):
    """
    Get events near a station using Skiddle API
    event_type options: FEST (Festivals), LIVE (Live Music), 
    CLUB (Clubbing/Dance), ARTS (Arts/Theatre), SPORT, COMEDY
    """
    base_url = "https://www.skiddle.com/api/v1/events/search/"
    
    radius_km = radius / 1000
    
    params = {
        'api_key': api_key,
        'latitude': station_coords['lat'],
        'longitude': station_coords['lon'],
        'radius': radius_km,
        'limit': 20,
        'order': 'date',
        'description': 1
    }
    
    # Add event type filter if specified
    if event_type:
        params['eventcode'] = event_type
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        events = []
        for event in data.get('results', []):
            events.append({
                'name': event.get('eventname', 'Unnamed Event'),
                'description': event.get('description', '')[:100] + '...' if event.get('description') else '',
                'venue': event.get('venue', {}).get('name', ''),
                'start_time': event.get('startdate', ''),
                'end_time': event.get('enddate', ''),
                'min_price': event.get('minPrice', ''),
                'max_price': event.get('maxPrice', ''),
                'url': event.get('link', ''),
                'type': event.get('eventtype', ''),
                'venue_address': event.get('venue', {}).get('address', '')
            })
        
        return events
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}")
        return []

def format_station_info(info: Dict) -> str:
    """Format all station information into a readable string"""
    if not info:
        return "No information available."
    
    output = []
    
    # Format facilities
    facilities = info['facilities']
    output.append(f"Station: {facilities['station_name']}")
    output.append(f"Zones: {', '.join(map(str, facilities['zones']))}")
    output.append(f"Lines: {', '.join(facilities['lines'])}")
    output.append("\nStation Amenities:")
    output.append(f"- WiFi Available: {'Yes' if facilities['wifi'] else 'No'}")
    output.append(f"- Toilets Available: {'Yes' if facilities['toilets'] else 'No'}")
    output.append(f"- Step-free Access/Lifts: {'Yes' if facilities['lifts'] else 'No'}")
    output.append(f"- Parking Available: {'Yes' if facilities['parking'] else 'No'}")
    
    if facilities['facilities']:
        output.append("\nOther Facilities:")
        for facility in facilities['facilities']:
            output.append(f"- {facility}")
    
    # Format nearby places (with generic filtering)
    place_type = info.get('place_type', 'restaurant').replace('_', ' ').title()
    output.append(f"\nNearby {place_type}s:")
    output.append("-" * 30)
    
    # First, group places by their base address
    address_groups = {}
    for place in info['nearby_restaurants']:
        # Get the base address (first part before comma)
        base_address = place['address'].split(',')[0].strip()
        
        if base_address not in address_groups:
            address_groups[base_address] = []
        address_groups[base_address].append(place)
    
    # Then, select the main place from each address group
    filtered_places = []
    for places in address_groups.values():
        if len(places) == 1:
            # If only one place at this address, add it
            filtered_places.append(places[0])
        else:
            # If multiple places, take the one with shortest name
            # (usually the main venue rather than a specific shop/unit)
            shortest_name_place = min(places, key=lambda x: len(x['name']))
            filtered_places.append(shortest_name_place)
    
    # Format filtered places
    for i, place in enumerate(filtered_places, 1):
        place_info = [f"{i}. {place['name']}"]
        if place.get('rating'):
            place_info.append(f"Rating: {place['rating']}/5")
        if place.get('price_level'):
            price = '£' * place['price_level']
            place_info.append(f"Price: {price}")
        if place.get('open_now') is not None:
            status = "Open" if place['open_now'] else "Closed"
            place_info.append(f"Status: {status}")
        place_info.append(f"Address: {place['address']}")
        output.append(" | ".join(place_info))
    
    # Format events (with generic filtering)
    output.append("\nUpcoming Events:")
    output.append("-" * 30)
    
    # Group events by venue first
    venue_groups = {}
    for event in info['upcoming_events']:
        venue = event.get('venue', '')
        if venue not in venue_groups:
            venue_groups[venue] = []
        venue_groups[venue].append(event)
    
    # Then handle similar events at each venue
    event_groups = {}
    for venue_events in venue_groups.values():
        for event in venue_events:
            name = event['name']
            venue = event.get('venue', '')
            start_time = datetime.fromisoformat(event['start_time'].replace('Z', '+00:00'))
            
            # Create key based on venue and simplified name
            key = f"{venue}_{name}"
            
            if key not in event_groups:
                event_groups[key] = {
                    'name': name,
                    'venue': venue,
                    'earliest_date': start_time,
                    'latest_date': start_time,
                    'url': event.get('url', '')
                }
            else:
                # Update date range for same event
                if start_time < event_groups[key]['earliest_date']:
                    event_groups[key]['earliest_date'] = start_time
                if start_time > event_groups[key]['latest_date']:
                    event_groups[key]['latest_date'] = start_time
    
    # Format grouped events
    for i, event in enumerate(event_groups.values(), 1):
        event_info = [f"{i}. {event['name']}"]
        
        if event['venue']:
            event_info.append(f"Where: {event['venue']}")
        
        # Format date range
        start = event['earliest_date'].strftime('%B %d, %Y at %I:%M %p')
        end = event['latest_date'].strftime('%B %d, %Y at %I:%M %p')
        
        if start != end:
            event_info.append(f"Running from {start} to {end}")
        else:
            event_info.append(f"When: {start}")
        
        if event['url']:
            event_info.append(f"Book at: {event['url']}")
        
        output.append(" | ".join(event_info))
    
    return "\n".join(output)


if __name__ == "__main__":
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    
    # OAuth 2.0 scopes for Google Calendar API
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    # Set up Google Calendar API credentials
    flow = InstalledAppFlow.from_client_secrets_file(
        '/Users/nicolas/credentials.json', SCOPES)
    google_credentials = flow.run_local_server(port=0)
    
    # Available options for user input
    PLACE_TYPES = ['restaurant', 'cafe', 'bar', 'museum', 
                   'park', 'art_gallery', 'night_club', 'shopping_mall']
    EVENT_TYPES = {
        'SPORTS': 'Sports',
        'FEST': 'Festivals',
        'LIVE': 'Live Music',
        'CLUB': 'Clubbing/Dance',
        'ARTS': 'Arts/Theatre',
        'COMEDY': 'Comedy'
    }
    
    # Get user input
    print("\nAvailable place types:", ", ".join(PLACE_TYPES))
    place_type = input("Enter place type (default: restaurant): ").lower() or 'restaurant'
    if place_type not in PLACE_TYPES:
        print(f"Invalid place type. Using 'restaurant' instead.")
        place_type = 'restaurant'
    
    print("\nAvailable event types:", ", ".join(EVENT_TYPES.values()))
    event_type_input = input("Enter event type (press Enter for all events): ")
    
    # Convert input to match EVENT_TYPES keys
    event_type = None
    if event_type_input:
        event_type_input = event_type_input.upper()
        # Find matching event type key
        for key, value in EVENT_TYPES.items():
            if value.upper() == event_type_input or key == event_type_input:
                event_type = key
                break
        if event_type is None:
            print(f"Invalid event type. Showing all events.")

    # API Keys
    STATION_ID = "9400ZZLUGGN"  # Borough Underground Station
    
    # Get station information with filters
    station_info = get_station_info(
        station_id=STATION_ID,
        tfl_api_key=TFL_API_KEY,
        google_api_key=GOOGLE_API_KEY,
        skiddle_api_key=SKIDDLE_API_KEY,
        place_type=place_type,
        event_type=event_type
    )
    
    # Print formatted results
    print("\nStation Information:")
    print("=" * 50)
    print(format_station_info(station_info))  
    
