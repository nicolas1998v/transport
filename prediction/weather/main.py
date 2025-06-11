import functions_framework
from weather_collector import main as weather_collector_main

@functions_framework.http
def fetch_weather(request):
    """Cloud Function to fetch weather data."""
    try:
        weather_collector_main()
        return ('Weather data collected successfully', 200)
    except Exception as e:
        return (f'Error collecting weather data: {str(e)}', 500) 