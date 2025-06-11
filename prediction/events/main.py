import functions_framework
from fetch_events import main as fetch_events_main

@functions_framework.http
def fetch_events(request):
    """Cloud Function to fetch events data."""
    try:
        fetch_events_main()
        return ('Events fetched successfully', 200)
    except Exception as e:
        return (f'Error fetching events: {str(e)}', 500) 