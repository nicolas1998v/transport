import requests

primary_key = 'b1efe66db0f748c3a9a248ca9ed03c9b'
secondary_key = '2e21963ed6f645da8fa40ef78065949d'
station_id = '940GZZLUKSX'
# Make the request
url = f'https://api.tfl.gov.uk/StopPoint/{station_id}/Arrivals'  
params = {
    'app_key': primary_key,
    'app_id': secondary_key
}

response = requests.get(url, params=params)

if response.status_code == 200:
    journey_data = response.text
    print(journey_data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)