import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google.cloud import bigquery
from google.oauth2 import service_account
import redis
import hashlib
from io import StringIO
import zlib
import base64

st.set_page_config(layout="wide")

# Initialize GCP client with credentials from Streamlit secrets
try:
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    project_id = credentials.project_id
    client = bigquery.Client(credentials=credentials, project=project_id)
except Exception as e:
    st.error("""
    ⚠️ Error initializing Google Cloud client. Please check your credentials in Streamlit Cloud secrets.
    Make sure you've added the credentials in the correct TOML format.
    """)
    st.error(str(e))
    st.stop()

# Initialize Redis connection
redis_client = None
try:
    host = st.secrets["redis"]["host"]
    port = int(st.secrets["redis"]["port"])
    password = st.secrets["redis"]["password"]
        
    # Try connecting without SSL first
    redis_client = redis.Redis(
        host=host,
        port=port,
        password=password,
        ssl=False,  # Try without SSL first
        decode_responses=True,  # This will decode bytes to strings automatically
        socket_timeout=5,
        socket_connect_timeout=5
    )
    
    if redis_client.ping():
        print("Successfully connected to Redis without SSL")
    else:
        print("Failed to connect to Redis without SSL")
        redis_client = None
except Exception as e:
    st.error(f"Error connecting to Redis without SSL: {str(e)}")
    try:
        # If that fails, try with SSL
        redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True,  # This will decode bytes to strings automatically
            socket_timeout=5,
            socket_connect_timeout=5
        )
        
        if redis_client.ping():
            st.success("Successfully connected to Redis with SSL")
        else:
            st.error("Failed to connect to Redis with SSL")
            redis_client = None
    except Exception as e:
        st.error(f"Error connecting to Redis with SSL: {str(e)}")
        redis_client = None

def normalize_query(query):
    """Normalize query for consistent caching"""
    # Remove extra whitespace and convert to lowercase
    return ' '.join(query.lower().split())

def get_cache_key(query):
    """Generate a consistent cache key for a query."""
    normalized_query = normalize_query(query)
    key = f"query:{hashlib.md5(normalized_query.encode()).hexdigest()}"
    return key

def compress_data(data):
    """Compress data before storing in Redis."""
    json_str = data.to_json(orient='records', date_format='iso')
    compressed = zlib.compress(json_str.encode())
    return base64.b64encode(compressed).decode()

def decompress_data(compressed_data):
    """Decompress data retrieved from Redis."""
    decoded = base64.b64decode(compressed_data)
    decompressed = zlib.decompress(decoded)
    return pd.read_json(StringIO(decompressed.decode()))

def get_cached_query(query):
    """Try Redis first, fall back to direct query if Redis fails."""
    try:
        cache_key = get_cache_key(query)
        
        # Try Redis first
        if redis_client is not None:
            try:
                cached_result = redis_client.get(cache_key)
                if cached_result is not None:
                    return decompress_data(cached_result)
            except Exception as e:
                st.warning(f"Redis error: {str(e)}")
        
        # If Redis fails or no cache hit, execute query
        result = client.query(query).to_dataframe()
        
        # Try to cache in Redis for next time
        if redis_client is not None:
            try:
                compressed_data = compress_data(result)   
                redis_client.setex(cache_key, 43200, compressed_data)  # 12 hours
            except Exception as e:
                st.warning(f"Redis error: {str(e)}")
        
        return result
        
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        raise

# Get counts from both tables
count_query = """
SELECT 
    (SELECT COUNT(*) FROM `nico-playground-384514.transport_predictions.initial_errors`) +
    (SELECT COUNT(*) FROM `nico-playground-384514.transport_predictions.any_errors`) as total_count
"""
count_df = get_cached_query(count_query)
total_count = count_df['total_count'].iloc[0]

st.info(f"Data is cached and updates every 12 hours | Total observations: {total_count:,}")
st.title("Kings Cross Tube Prediction Analysis")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs([
    "Prediction Analysis", 
    "Initial Prediction Analysis", 
    "Line & Time Analysis", 
    "Prediction Precision Analysis", 
    "Location Analysis",
    "Direction Analysis",
    "Peak Time Analysis",
    "Error Pattern Analysis",
    "Prediction Drift Analysis",
    "Anomaly Detection",
    "Line Interaction Analysis",
    "Weather Impact Analysis", 
    "Event Impact Analysis",
])

# Add station order mappings at the top of the file after imports
STATION_ORDERS = {
    'victoria': {
        '1': [
            'Brixton Area', 'Between Brixton and Stockwell', 'Approaching Stockwell', 'At Stockwell',
            'Departing Stockwell', 'Between Stockwell and Vauxhall', 'Approaching Vauxhall', 'At Vauxhall',
            'Departing Vauxhall', 'Between Vauxhall and Pimlico', 'Approaching Pimlico', 'At Pimlico',
            'Departing Pimlico', 'Between Pimlico and Victoria', 'Approaching Victoria', 'Victoria Siding',
            'At Victoria', 'Departed Victoria', 'Between Victoria and Green Park', 'Approaching Green Park',
            'At Green Park', 'Departed Green Park', 'Between Green Park and Oxford Circus',
            'Approaching Oxford Circus', 'At Oxford Circus', 'Departed Oxford Circus',
            'Between Oxford Circus and Warren Street', 'Approaching Warren Street', 'At Warren Street',
            'Between Warren Street and Euston', 'Approaching Euston', 'At Euston',
            'Between Euston and Kings Cross St. P', 'Approaching Kings Cross St. Pancras'
        ],
        '2': [
            'Between Highbury & Islington and Kings Cross St. P',
            'Departed Highbury & Islington', 'At Highbury & Islington', 'Approaching Highbury & Islington',
            'Between Finsbury Park and Highbury & Islington', 'Departed Finsbury Park', 'At Finsbury Park',
            'Approaching Finsbury Park', 'Between Seven Sisters and Finsbury Park', 'Departed Seven Sisters',
            'At Seven Sisters Platform 5', 'Approaching Seven Sisters', 'Between Tottenham Hale and Seven Sisters',
            'Departed Tottenham Hale', 'At Tottenham Hale', 'Approaching Tottenham Hale', 'At Tottenham Hale',
            'Between Blackhorse Road and Tottenham Hale', 'Left Blackhorse Road', 'At Blackhorse Road',
            'Approaching Blackhorse Road', 'Between Walthamstow Central and Blackhorse Road'
        ]
    },
    'metropolitan': {
        '1': [
            'Between Wembley Park and Neasden', 'Approaching Neasden Platform 4', 'Approaching Neasden',
            'Left Neasden', 'At Neasden', 'Between Neasden and Willesden Green',
            'Approaching Willesden Green Platform 4', 'At Willesden Green', 'Left Willesden Green',
            'Between Willesden Green and Finchley Road', 'Approaching Finchley Road Platform 4',
            'At Finchley Road Platform 4', 'Left Finchley Road', 'Between Finchley Road and Baker Street',
            'Approaching Baker Street Platform 3', 'Approaching Baker Street', 'At Baker Street Platform 3',
            'Left Baker Street', 'Between Baker Street and Great Portland Street',
            'Approaching Great Portland Street Platform 2', 'At Great Portland Street Platform 2',
            'Left Great Portland Street', 'Between Great Portland Street and Euston Square',
            'Approaching Euston Square Platform 2', 'At Euston Square Platform 2', 'Left Euston Square',
            'Between Euston Square and Kings Cross St. Pancras', 'Approaching Kings Cross St. Pancras Platform 2'
        ],
        '2': [
            'Approaching Kings Cross St. Pancras Platform 1',
            'Between Farringdon and Kings Cross St. Pancras', 'Left Farringdon', 'At Farringdon Platform 2',
            'Approaching Farringdon Platform 2', 'Between Barbican and Farringdon', 'Left Barbican',
            'At Barbican Platform 2', 'Approaching Barbican Platform 2', 'Between Moorgate and Barbican',
            'Left Moorgate', 'At Moorgate Platform 2', 'Approaching Moorgate Platform 2',
            'Between Liverpool Street and Moorgate', 'Left Liverpool Street', 'At Liverpool Street Platform 2',
            'Approaching Liverpool Street Platform 2', 'Between Aldgate and Liverpool Street',
            'Left Aldgate', 'At Aldgate Platform 3', 'At Aldgate Platform 2'
        ]
    },
    'piccadilly': {
        '1': [
            'Between Acton Town and Turnham Green', 'Approaching Turnham Green', 'At Turnham Green Platform 3',
            'Left Turnham Green', 'Between Turnham Green and Ravenscourt Park', 'At Ravenscourt Park Platform 3',
            'Between Ravenscourt Park and Hammersmith', 'Approaching Hammersmith', 'Hammersmith area',
            'Left Hammersmith', 'Between Hammersmith and Barons Court', 'Approaching Barons Court',
            'At Barons Court Platform 3', 'Left Barons Court', 'Between Barons Court and Earl\'s Court',
            'Approaching Earl\'s Court', 'At Earl\'s Court Platform 5', 'Between Earl\'s Court and Gloucester Road',
            'Approaching Gloucester Road', 'At Gloucester Road Platform 5', 'Left Gloucester Road',
            'Approaching South Kensington', 'At South Kensington Platform 4', 'Left South Kensington',
            'Between South Kensington and Knightsbridge', 'Approaching Knightsbridge', 'At Knightsbridge Platform 1',
            'Left Knightsbridge', 'Between Knightsbridge and Hyde Park Corner', 'Approaching Hyde Park Corner',
            'At Hyde Park Corner Platform 1', 'Between Hyde Park Corner and Green Park', 'Approaching Green Park',
            'At Green Park Platform 2', 'Between Green Park and Piccadilly Circus', 'At Piccadilly Circus Platform 3',
            'Between Piccadilly Circus and Leicester Square', 'At Leicester Square Platform 2',
            'Between Leicester Square and Covent Garden', 'At Covent Garden Platform 2',
            'Between Covent Garden and Holborn', 'At Holborn Platform 4', 'Between Holborn and Russell Square',
            'At Russell Square Platform 1', 'Between Russell Square and King\'s Cross'
        ],
        '2': [
            'Between Caledonian Road and King\'s Cross',
            'At Caledonian Road Platform 2', 'Between Holloway Road and Caledonian Road',
            'At Holloway Road Platform 1', 'Between Arsenal and Holloway Road',
            'At Arsenal Platform 2', 'Between Finsbury Park and Arsenal',
            'At Finsbury Park Platform 3', 'Between Manor House and Finsbury Park',
            'At Manor House Platform 1', 'Between Turnpike Lane and Manor House',
            'Approaching Turnpike Lane', 'At Turnpike Lane Platform 2', 'Left Turnpike Lane',
            'Between Wood Green and Turnpike Lane', 'Approaching Wood Green',
            'At Wood Green Platform 2', 'Left Wood Green',
            'Between Bounds Green and Wood Green', 'Approaching Bounds Green',
            'At Bounds Green Platform 1', 'Left Bounds Green',
            'Between Arnos Grove and Bounds Green', 'Approaching Arnos Grove',
            'At Arnos Grove Platform 4', 'Left Arnos Grove',
            'Between Southgate and Arnos Grove', 'Approaching Southgate',
            'At Southgate Platform 2', 'Left Southgate',
            'Between Oakwood and Southgate', 'Approaching Oakwood',
            'At Oakwood Platform 1', 'Left Oakwood',
            'Between Cockfosters and Oakwood'
        ]
    },
    'hammersmith-city': {
        '1': [
            'On P9 crossover outside Hammersmith', 'Between Hammersmith and Goldhawk Road',
            'Approaching Goldhawk Road Platform 1', 'At Goldhawk Road Platform 1', 'Left Goldhawk Road',
            'Between Goldhawk Road and Shepherds Bush Market', 'At Shepherds Bush Market Platform 1',
            'Between Shepherds Bush Market and Wood Lane', 'Approaching Wood Lane Platform 1',
            'At Wood Lane Platform 1', 'Left Wood Lane', 'Between Wood Lane and Latimer Road',
            'Approaching Latimer Road Platform 1', 'At Latimer Road Platform 1', 'Left Latimer Road',
            'Between Latimer Road and Ladbroke Grove', 'Approaching Ladbroke Grove',
            'At Ladbroke Grove Platform 1', 'Left Ladbroke Grove', 'Between Ladbroke Grove and Westbourne Park',
            'Approaching Westbourne Park', 'At Westbourne Park Platform 2', 'Left Westbourne Park',
            'Between Westbourne Park and Royal Oak', 'Approaching Royal Oak', 'At Royal Oak Platform 2',
            'Left Royal Oak', 'Between Royal Oak and Paddington (Suburban)', 'Approaching Paddington (Suburban)',
            'At Paddington (Suburban) Platform 16', 'Left Paddington', 'Between Paddington and Edgware Road',
            'Approaching Edgware Road', 'At Edgware Road Platform 1', 'Left Edgware Road',
            'Between Edgware Road and Baker Street', 'Approaching Baker Street Platform 5',
            'At Baker Street Platform 5', 'Left Baker Street', 'Between Baker Street and Great Portland Street',
            'Approaching Great Portland Street Platform 2', 'At Great Portland Street Platform 2',
            'Left Great Portland Street', 'Between Great Portland Street and Euston Square',
            'Approaching Euston Square Platform 2', 'At Euston Square Platform 2', 'Left Euston Square',
            'Between Euston Square and Kings Cross St. Pancras', 'Approaching Kings Cross St. Pancras Platform 2'
        ],
        '2': [
            'Approaching Kings Cross St. Pancras Platform 1',
            'Between Farringdon and Kings Cross St. Pancras', 'Left Farringdon', 'At Farringdon Platform 2',
            'Approaching Farringdon Platform 2', 'Between Barbican and Farringdon', 'Left Barbican',
            'At Barbican Platform 2', 'Approaching Barbican Platform 2', 'Between Moorgate and Barbican',
            'Left Moorgate', 'At Moorgate Platform 2', 'Approaching Moorgate Platform 2',
            'Between Liverpool Street and Moorgate', 'Left Liverpool Street', 'At Liverpool Street Platform 2',
            'Approaching Liverpool Street Platform 2', 'Between Aldgate East and Liverpool Street',
            'Left Aldgate East', 'At Aldgate East Platform 1', 'Approaching Aldgate East Platform 1',
            'Between Whitechapel and Aldgate East', 'Left Whitechapel', 'At Whitechapel Platform 2',
            'Approaching Whitechapel Platform 2', 'Between Stepney Green and Whitechapel',
            'Left Stepney Green', 'At Stepney Green Platform 1', 'Approaching Stepney Green Platform 1',
            'Between Mile End and Stepney Green', 'Left Mile End', 'At Mile End Platform 2',
            'Approaching Mile End Platform 2', 'Between Bow Road and Mile End',
            'Left Bow Road', 'At Bow Road Platform 1', 'Approaching Bow Road Platform 1',
            'Between Bromley-by-Bow and Bow Road', 'Left Bromley-by-Bow', 'At Bromley-by-Bow Platform 1',
            'Approaching Bromley-by-Bow Platform 1', 'Between West Ham and Bromley-by-Bow',
            'Left West Ham', 'At West Ham Platform 1', 'Approaching West Ham Platform 1',
            'Between Plaistow and West Ham', 'Left Plaistow', 'At Plaistow Platform 1',
            'Approaching Plaistow Platform 1'
        ]
    },
    'northern': {
        '1': {
            'branch_1': ['Departed Edgware', 'Between Edgware and Burnt Oak', 'Approaching Burnt Oak', 'At Burnt Oak Platform 2',
                'Departed Burnt Oak', 'Between Burnt Oak and Colindale', 'Approaching Colindale', 'At Colindale Platform 2',
                'Departed Colindale', 'Between Colindale and Hendon Central', 'Approaching Hendon Central', 'At Hendon Central Platform 2',
                'Departed Hendon Central', 'Between Hendon Central and Brent Cross', 'Approaching Brent Cross', 'At Brent Cross Platform 2',
                'Departed Brent Cross', 'Between Brent Cross and Golders Green', 'Approaching Golders Green', 'At Golders Green Platform 5',
                'Departed Golders Green', 'Between Golders Green and Hampstead', 'Approaching Hampstead', 'At Hampstead Platform 2',
                'Between Hampstead and Belsize Park', 'Approaching Belsize Park', 'At Belsize Park Platform 2',
                'Between Belsize Park and Chalk Farm', 'Approaching Chalk Farm', 'At Chalk Farm Platform 2',
                'Between Chalk Farm and Camden Town', 'Approaching Camden Town', 'At Camden Town', 'Left Camden Town',
                'Between Camden Town and Mornington Crescent', 'On P23 crossover, between Camden and Euston',
                'Between Camden Town and Euston', 'Approaching Euston', 'At Euston', 'Between Euston and Kings Cross', 'Left Euston'
            ], 
            'branch_2': ['Between High Barnet and Totteridge & Whetstone', 'At Totteridge & Whetstone', 'Left Totteridge & Whetstone',
                'Between Totteridge & Whetstone and Woodside Park', 'Approaching Woodside Park', 'At Woodside Park', 
                'Between Woodside Park and West Finchley', 'Approaching West Finchley', 'At West Finchley Platform 2', 'Left West Finchley Platform 2',
                'Between West Finchley and Finchley Central', 'Approaching Finchley Central', 'Finchley Central Platform 3', 'Leaving Finchley Central',
                'Between Finchley Central and East Finchley', 'Approaching East Finchley',  'Left East Finchley',
                'Between East Finchley and Highgate', 'Approaching Highgate Platform 2', 'At Highgate Platform 2', 'Left Highgate Platform 2',
                'Between Highgate and Archway', 'Approaching Archway', 'At Archway Platform 2', 'Between Archway and Tufnell Park',
                'Approaching Tufnell Park', 'At Tufnell Park Platform 2', 'Between Tufnell Park and Kentish Town',
                'At Kentish Town Platform 2', 'Between Kentish Town and Camden Town',
                'Approaching Camden Town Platform 4', 'At Camden Town', 'Left Camden Town',
                'Between Camden Town and Mornington Crescent', 'On P23 crossover, between Camden and Euston',
                'Between Camden Town and Euston', 'Approaching Euston', 'At Euston', 'Between Euston and Kings Cross', 'Left Euston'
            ]
        },
        '2': [
            'Between Angel and Kings Cross',
            'Between Angel and Kings Cross', 'Left Angel, heading towards Kings Cross',
            'Between Old Street and Angel', 'At Old Street Platform 1', 'Departed Old Street',
            'Between Moorgate and Old Street', 'At Moorgate Platform 7', 'Departed Moorgate',
            'Between Bank and Moorgate', 'At Bank Platform 4', 'Between London Bridge and Bank',
            'At London Bridge Plaform 1', 'Between Borough and London Bridge',
            'Approaching Borough Platform 1', 'Approaching Borough Platform 1', 'At Borough Platform 1', 'Departed Borough',
            'Between Elephant and Castle and Borough', 'At Elephant and Castle Platform 1', 'Departed Elephant and Castle',
            'Between Kennington and Elephant and Castle', 'At Kennington Platform 3', 'In Kennington Sidings',
            'Between Oval and Kennington', 'At Oval Platform 1', 'Departed Oval',
            'Between Stockwell and Oval', 'At Stockwell Platform 2', 'Departed Stockwell',
            'Between Clapham North and Stockwell', 'At Clapham North Platform 1', 'Departed Clapham North',
            'Between Clapham Common and Clapham North', 'Approaching Clapham North', 'At Clapham North Platform 1',
            'Between Clapham South and Clapham Common', 'Approaching Clapham Common', 'At Clapham Common Platform 1', 'Departed Clapham Common',
            'Between Balham and Clapham South', 'Approaching Clapham South', 'At Clapham South Platform 1', 'Departed Clapham South',
            'Between Tooting Bec and Balham', 'Approaching Balham', 'At Balham Platform 1', 'Departed Balham'
        ]
    }
}

# Station name mappings for renaming
STATION_RENAMES = {
    '0': 'Brixton Area',
    'Victoria Siding': 'At Victoria',
    'At Aldgate Platform 2': 'At Aldgate',
    'At Aldgate Platform 3': 'At Aldgate',
    'At Aldgate Platform 4': 'At Aldgate',
    'At Aldgate East Platform 1': 'At Aldgate East',
    'Between Russell Square and King\'s Cross': 'Between Russell Square and Kings Cross',
    'Between Russell Square and Kings Cross St. Pancras': 'Between Russell Square and Kings Cross'
}

def get_station_order(line, direction, station):
    """Get the order of a station in the sequence"""
    if line.lower() in STATION_ORDERS:
        if direction in ['1', '2']:  # Check for '1' or '2' instead of 'outbound'/'inbound'
            try:
                return STATION_ORDERS[line.lower()][direction].index(station)
            except ValueError:
                return float('inf')  # Put unknown stations at the end
    return float('inf')

def rename_station(station):
    """Rename station according to mapping"""
    return STATION_RENAMES.get(station, station)

with tab1:
    st.markdown("""      
        Welcome to my dashboard! Let's imagine you are on the platform at King's Cross and you're wondering when your train is coming, so you check the arrival screens.  
        Now imagine you have a bigger screen which shows the same predictions, but for every tube line disserving King's Cross, and for trains as far as 20 minutes away.
                    
        And you're wondering, but just how accurate are these predictions? What variables affect the accuracy? What variables make the errors go up? 
        This dashboard is my attempt to answer these two questions. 
        
        For this first tab, we will ask ourselves the following questions:
        The further away the train is, do the prediction errors increase?  
        And if they do, do these predictions then follow a trend? Are they optimistic and tend to underestimate the length of the journey ahead? Or are they pessimistic and tend to overestimate it?
        
        In this tab, you can isolate the data by clicking on the line you want to see, and zoom in on the scatter plot by dragging the mouse to see more details. You can also select a single train and isolate a few runs to better understand how Transport for London makes its predictions. Tube lines divided by direction, inbound to KC and outbound to KC.
        """)
    # Add metric for predictions within 30 seconds and 1 minute
    accuracy_query = """
    SELECT 
        CAST(COUNT(*) AS FLOAT64) as total_predictions,
        CAST(COUNTIF(ABS(error_seconds) <= 30) AS FLOAT64) as accurate_predictions_30s,
        CAST(COUNTIF(ABS(error_seconds) <= 60) AS FLOAT64) as accurate_predictions_60s,
        CAST(ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) AS FLOAT64) as accuracy_percentage_30s,
        CAST(ROUND(COUNTIF(ABS(error_seconds) <= 60) / COUNT(*) * 100, 1) AS FLOAT64) as accuracy_percentage_60s
    FROM `nico-playground-384514.transport_predictions.any_errors`
    """

    accuracy_results = get_cached_query(accuracy_query)

    if not accuracy_results.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
            "Predictions Within ±30 Seconds",
                f"{accuracy_results.iloc[0]['accuracy_percentage_30s']:.1f}%",
                help=f"Based on {accuracy_results.iloc[0]['total_predictions']:.0f} predictions"
            )
        with col2:
            st.metric(
                "Predictions Within ±1 Minute",
                f"{accuracy_results.iloc[0]['accuracy_percentage_60s']:.1f}%",
            help=f"Based on {accuracy_results.iloc[0]['total_predictions']:.0f} predictions"
        )

    # Query for any predictions by direction
    any_prediction_query = """
    SELECT 
        train_id,
        direction,
        CAST(error_seconds AS FLOAT64) as error_seconds,
        CAST(time_to_station AS FLOAT64) as time_to_station,
        line,
        current_location,
        FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', any_prediction_timestamp) as any_prediction_timestamp,
        FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', arrival_timestamp) as arrival_timestamp
    FROM `nico-playground-384514.transport_predictions.any_errors`
    ORDER BY direction, line
    """


    # Query for scatter plot with run information
    run_query = """
    WITH time_gaps AS (
    SELECT 
            train_id,
            timestamp,
            FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', any_prediction_timestamp) as any_prediction_timestamp,
            FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', arrival_timestamp) as arrival_timestamp,
            LAG(timestamp) OVER (PARTITION BY train_id ORDER BY timestamp) as prev_timestamp,
            CASE 
                WHEN LAG(timestamp) OVER (PARTITION BY train_id ORDER BY timestamp) IS NULL 
                OR TIMESTAMP_DIFF(timestamp, 
                                LAG(timestamp) OVER (PARTITION BY train_id ORDER BY timestamp), 
                                MINUTE) > 20
                THEN 1
                ELSE 0
            END as new_run
    FROM `nico-playground-384514.transport_predictions.any_errors`
    WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 10 HOUR)
    ),
    run_numbers AS (
        SELECT 
            train_id,
            timestamp,
            any_prediction_timestamp,
            arrival_timestamp,
            SUM(new_run) OVER (PARTITION BY train_id ORDER BY timestamp) as run_number
        FROM time_gaps
    )
    SELECT 
        CAST(e.error_seconds AS FLOAT64) as error_seconds,
        CAST(e.time_to_station AS FLOAT64) as time_to_station,
        e.line,
        e.train_id,
        e.current_location,
        r.run_number,
        r.any_prediction_timestamp,
        r.arrival_timestamp,
        MIN(e.timestamp) OVER (PARTITION BY e.train_id, r.run_number) as run_start_time,
        MAX(e.timestamp) OVER (PARTITION BY e.train_id, r.run_number) as run_end_time,
        e.direction
    FROM `nico-playground-384514.transport_predictions.any_errors` e
    JOIN run_numbers r
    ON e.train_id = r.train_id AND e.timestamp = r.timestamp
    WHERE e.timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 10 HOUR)
    ORDER BY e.timestamp
    """

    df = get_cached_query(run_query)
    df_any_prediction = get_cached_query(any_prediction_query)

    if not df.empty:
        # Add train_id filter
        train_ids = sorted(df['train_id'].unique())
        selected_train_id_2 = st.selectbox(
            "Select Train ID to Highlight - Runs dating the last 10 hours",
            options=['All'] + list(train_ids),
            index=0,
            key='train_id_selectbox'
        )        
        # Filter data based on selected train_id
        if selected_train_id_2 != 'All':
            # Get the line of the selected train
            selected_line = df[df['train_id'] == selected_train_id_2]['line'].iloc[0]
            
            # Get all data for the selected line
            line_df = df[df['line'] == selected_line]
        
            # Get data for the selected train
            train_df = line_df[line_df['train_id'] == selected_train_id_2]
            
            # Get unique runs for the selected train
            runs = sorted(train_df['run_number'].unique())
            
            # Add run selection with time window information
            st.write("Select Runs to Display (showing time window) - Maximum 3 runs")
            run_options = []
            for r in runs:
                run_data = train_df[train_df['run_number'] == r]
                start_time = run_data['run_start_time'].iloc[0]
                end_time = run_data['run_end_time'].iloc[0]
                duration = (end_time - start_time).total_seconds() / 60  # duration in minutes
                run_options.append(f"Run {r} ({duration:.0f} min)")
            
            selected_runs = st.multiselect(
                "Runs",
                options=run_options,
                default=run_options[:3] if len(run_options) > 3 else run_options,
                max_selections=3
            )
            
            # Extract run numbers from selected options
            selected_run_numbers = [int(r.split()[1]) for r in selected_runs]
            
            # Filter by selected runs
            filtered_df = train_df[train_df['run_number'].isin(selected_run_numbers)]
            
            # Create scatter plot with trend line
            fig = px.scatter(
                line_df[line_df['train_id'] != selected_train_id_2],  # Show all other trains from the line
                x='error_seconds',
                y='time_to_station',
                color_discrete_sequence=['lightgray'],  # Use a single color for all other trains
                trendline="ols",
                title=f"Prediction Error vs Time to Station - {selected_line.title()} Line",
                labels={
                    'error_seconds': 'Prediction Error (seconds)',
                    'time_to_station': 'Time to Station (seconds)',
                    'train_id': 'Train ID',
                    'run_number': 'Run Number',
                    'any_prediction_timestamp': 'Prediction Timestamp',
                    'arrival_timestamp': 'Arrival Timestamp',
                    'current_location': 'Location'
                },
                hover_data=['train_id', 'run_number', 'any_prediction_timestamp','arrival_timestamp', 'current_location']
            )
            
            # Update marker size and opacity for background points
            fig.update_traces(
                marker=dict(size=4),  # Even smaller size for background points
                opacity=0.30,  # Much lower opacity for background points
                selector=dict(mode='markers'),
                hovertemplate="<extra></extra>"  # Remove hover template for background points
            )
            
            # Define bright colors for runs
            run_colors = ['#FF0000', '#00FF00', '#0000FF']  # Pure red, green, blue
            
            # Add highlighted points for each selected run with different colors
            for i, run_num in enumerate(selected_run_numbers):
                run_data = filtered_df[filtered_df['run_number'] == run_num].copy()
            
                fig.add_trace(
                go.Scatter(
                    x=run_data['error_seconds'],
                    y=run_data['time_to_station'],
                    mode='markers',
                    name=f"Run {run_num}",
                    marker=dict(
                        size=10,
                        color=run_colors[i],
                        line=dict(width=2, color='white')
                    ),
                    opacity=1.0,
                    showlegend=True,
                    hovertemplate=(
                        "Train ID: " + selected_train_id_2 + "<br>" +
                        "Run: " + str(run_num) + "<br>" +
                        "Prediction Timestamp: %{text}<br>" +
                        "Arrival Timestamp: %{customdata[0]}<br>" +
                        "Time to Station: %{y:.0f} seconds<br>" +
                        "Error: %{x:.0f} seconds<br>" +
                        "Location: %{customdata[1]}<br>" +
                        "<extra></extra>"
                    ),
                    text=run_data['any_prediction_timestamp'],
                    customdata=run_data[['arrival_timestamp', 'current_location']].values
                ))
        
                # Update layout for better visibility
                fig.update_layout(
                    showlegend=True,  # Show legend
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    ),
                height=600,
                hovermode='closest'        )
        
        else:
            inbound_data = df_any_prediction[df_any_prediction['direction'] == 'inbound'].copy()
        
            if not inbound_data.empty:
            # Create scatter plot with trend line
                fig_inbound = px.scatter(
                inbound_data,
            x='error_seconds',
            y='time_to_station',
            color='line',
            trendline="ols",
                title="Prediction Error vs Time to Station (Inbound)",
            labels={
                'arrival_timestamp': 'Arrival Time',
                'error_seconds': 'Prediction Error (seconds)',
                'time_to_station': 'Time to Station (seconds)',
                'line': 'Tube Line',
                'any_prediction_timestamp': 'Prediction Timestamp',
                'train_id': 'Train ID',
                'current_location': 'Train location'},
                hover_data=['train_id','current_location','any_prediction_timestamp','arrival_timestamp'],
                category_orders={
                    'line': ['metropolitan', 'hammersmith-city', 'northern', 'piccadilly', 'victoria']
                },
                opacity=0.50
            )
            
            # Update layout and legend labels
            fig_inbound.update_layout(
            height=600,
            showlegend=True,
            hovermode='closest'
        )
        
            # Update legend labels for inbound
            legend_labels = {
                'metropolitan': 'Metropolitan (East to KC)',
                'hammersmith-city': 'Hammersmith & City (East to KC)',
                'northern': 'Northern (North to KC)',
                'piccadilly': 'Piccadilly (North East to KC)',
                'victoria': 'Victoria (North to KC)'
            }
            fig_inbound.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))

            outbound_data = df_any_prediction[df_any_prediction['direction'] == 'outbound'].copy()
        
            if not outbound_data.empty:
            # Create scatter plot with trend line
                fig_outbound = px.scatter(
                outbound_data,
                x='error_seconds',
                y='time_to_station',
                color='line',
                trendline="ols",
                title="Prediction Error vs Time to Station (Outbound)",
                labels={
                'arrival_timestamp': 'Arrival Time',
                'error_seconds': 'Prediction Error (seconds)',
                'time_to_station': 'Time to Station (seconds)',
                'line': 'Tube Line',
                    'any_prediction_timestamp': 'Prediction Timestamp',
                    'train_id': 'Train ID',
                    'current_location': 'Train location'

                },
                hover_data=['train_id', 'current_location','any_prediction_timestamp','arrival_timestamp'],
                category_orders={
                    'line': ['metropolitan', 'hammersmith-city', 'northern', 'piccadilly', 'victoria']
                },
                opacity=0.50
            )
            
            # Update layout and legend labels
            fig_outbound.update_layout(
                height=600,
                showlegend=True,
                hovermode='closest'
            )
            
            # Update legend labels for outbound
            legend_labels = {
                'metropolitan': 'Metropolitan (West to KC)',
                'hammersmith-city': 'Hammersmith & City (West to KC)',
                'northern': 'Northern (South to KC)',
                'piccadilly': 'Piccadilly (South West to KC)',
                'victoria': 'Victoria (South to KC)'
            }
            fig_outbound.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))
        

    if selected_train_id_2 == 'All':
        st.subheader("Inbound Predictions")
        st.plotly_chart(fig_inbound, use_container_width=True)
        st.info(""" ⚠️ A negative error means that the train is late with respect to the prediction.        
        If positive error means that the train is early with respect to the prediction.         
        """)
        st.markdown("---")  # Add a separator between inbound  sections

                    # Line-specific correlation analysis
        line_correlations = []
        line_correlations_abs = []
        for line in inbound_data['line'].unique():
            line_data = inbound_data[inbound_data['line'] == line]
            
            # Regular correlation (with sign)
            correlation = line_data['error_seconds'].corr(line_data['time_to_station'])
            avg_error = line_data['error_seconds'].mean()
            avg_time = line_data['time_to_station'].mean()
            slope = correlation * (line_data['error_seconds'].std() / line_data['time_to_station'].std())
            error_rate_per_minute = slope * 60
            
            # Absolute correlation (magnitude only)
            correlation_abs = line_data['error_seconds'].abs().corr(line_data['time_to_station'])
            avg_error_abs = line_data['error_seconds'].abs().mean()
            slope_abs = correlation_abs * (line_data['error_seconds'].abs().std() / line_data['time_to_station'].std())
            error_rate_per_minute_abs = slope_abs * 60
            
            line_correlations.append({
                'line': line,
                'correlation': correlation,
                'avg_error': avg_error,
                'avg_time': avg_time,
                'error_rate_per_minute': error_rate_per_minute
            })
            
            line_correlations_abs.append({
                'line': line,
                'correlation_abs': correlation_abs,
                'avg_error_abs': avg_error_abs,
                'avg_time': avg_time,
                'error_rate_per_minute_abs': error_rate_per_minute_abs
            })

            # Sort both lists by absolute correlation
            line_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            line_correlations_abs.sort(key=lambda x: abs(x['correlation_abs']), reverse=True)

    # Display line-specific insights
        
        st.subheader("Correlation Analysis - Absolute Error")
        st.info ("""⚠️ A positive correlation here means that the further away you predict, the more prediction errors increase in magnitude.""")
        for line_data_abs in line_correlations_abs:
            correlation_abs = line_data_abs['correlation_abs']
            line = line_data_abs['line']
            avg_time = line_data_abs['avg_time']
            avg_error_abs = line_data_abs['avg_error_abs']
            error_rate_abs = line_data_abs['error_rate_per_minute_abs']
            
            if abs(correlation_abs) > 0.5:
                strength_abs = "strong" if abs(correlation_abs) > 0.7 else "moderate"
                direction_abs = "positive" if correlation_abs > 0 else "negative"
                st.write(f"•  {line.title()} line shows a {strength_abs} {direction_abs} correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
            elif abs(correlation_abs) > 0.3:
                st.write(f"• {line.title()} line shows a weak correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
            else:
                st.write(f"• {line.title()} line shows minimal correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
        st.write("All metrics like these 3 below are from here onwards based on 3000 observations per line.")
        sampled_data_inbound = inbound_data.groupby('line').apply(lambda x: x.sample(n=min(3000, len(x)), random_state=42)).reset_index(drop=True)
        col1, col2, col3 = st.columns(3)
        with col1:
                st.metric("Average Error (abs)", f"{sampled_data_inbound['error_seconds'].abs().mean():.0f} seconds")
        with col2:
                st.metric("Average Time to Station", f"{sampled_data_inbound['time_to_station'].mean():.0f} seconds")
        with col3:
                st.metric("Overall Correlation (abs)", f"{sampled_data_inbound['error_seconds'].abs().corr(sampled_data_inbound['time_to_station']):.2f}")


        st.subheader("Correlation Analysis - Error")
        st.info ("""⚠️  A negative correlation here means that the further away the train is, predictions tend to be optimistic and underestimate the journey, and trains mostly arrive later than what they first predicted.   
        A positive correlation here means that the further away the train is, predictions tend to be pessimistic and overestimate the journey, and trains mostly arrive earlier than what they first predicted.    
        A negative average error here means that the tube line is late by x amount on average and vice versa for a positive average error.""")

        for line_data in line_correlations:
            correlation = line_data['correlation']
            line = line_data['line']
            avg_error = line_data['avg_error']
            avg_time = line_data['avg_time']
            error_rate = line_data['error_rate_per_minute']
        
            if abs(correlation) > 0.5:
                strength = "strong" if abs(correlation) > 0.7 else "moderate"
                direction = "positive" if correlation > 0 else "negative"
                st.write(f"• {line.title()} line shows a {strength} {direction} correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival is later than its prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            elif abs(correlation) > 0.3:
                st.write(f"• {line.title()} line shows a weak correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival is later than its prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            else:
                st.write(f"• {line.title()} line shows minimal correlation of {correlation:.2f}. For every minute increase in time to station, {'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival timestamp is later than the prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            
                col1, col2, col3 = st.columns(3)
        with col1:
                st.metric("Average Error - 3000 obsv per line", f"{sampled_data_inbound['error_seconds'].mean():.0f} seconds")
        with col3:
                st.metric("Overall Correlation", f"{sampled_data_inbound['error_seconds'].corr(sampled_data_inbound['time_to_station']):.2f}")


        st.markdown("---")  # Add a separator between inbound and outbound sections
            # Outbound predictions
        st.subheader("Outbound Predictions")
            
        st.plotly_chart(fig_outbound, use_container_width=True)

        st.markdown("---")  # Add a separator between  outbound sections

                    # Line-specific correlation analysis
        line_correlations = []
        line_correlations_abs = []
        for line in outbound_data['line'].unique():
            line_data = outbound_data[outbound_data['line'] == line]
            
            # Regular correlation (with sign)
            correlation = line_data['error_seconds'].corr(line_data['time_to_station'])
            avg_error = line_data['error_seconds'].mean()
            avg_time = line_data['time_to_station'].mean()
            slope = correlation * (line_data['error_seconds'].std() / line_data['time_to_station'].std())
            error_rate_per_minute = slope * 60
            
            # Absolute correlation (magnitude only)
            correlation_abs = line_data['error_seconds'].abs().corr(line_data['time_to_station'])
            avg_error_abs = line_data['error_seconds'].abs().mean()
            slope_abs = correlation_abs * (line_data['error_seconds'].abs().std() / line_data['time_to_station'].std())
            error_rate_per_minute_abs = slope_abs * 60
            
            line_correlations.append({
                'line': line,
                'correlation': correlation,
                'avg_error': avg_error,
                'avg_time': avg_time,
                'error_rate_per_minute': error_rate_per_minute
            })
            
            line_correlations_abs.append({
                'line': line,
                'correlation_abs': correlation_abs,
                'avg_error_abs': avg_error_abs,
                'avg_time': avg_time,
                'error_rate_per_minute_abs': error_rate_per_minute_abs
            })

            # Sort both lists by absolute correlation
            line_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            line_correlations_abs.sort(key=lambda x: abs(x['correlation_abs']), reverse=True)

         # Display line-specific insights
        
        st.subheader("Correlation Analysis - Absolute Error")
        st.info ("""⚠️ A positive correlation here means that the further away you predict, the more prediction errors increase in magnitude.""")
        for line_data_abs in line_correlations_abs:
            correlation_abs = line_data_abs['correlation_abs']
            line = line_data_abs['line']
            avg_time = line_data_abs['avg_time']
            avg_error_abs = line_data_abs['avg_error_abs']
            error_rate_abs = line_data_abs['error_rate_per_minute_abs']
            
            if abs(correlation_abs) > 0.5:
                strength_abs = "strong" if abs(correlation_abs) > 0.7 else "moderate"
                direction_abs = "positive" if correlation_abs > 0 else "negative"
                st.write(f"•  {line.title()} line shows a {strength_abs} {direction_abs} correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
            elif abs(correlation_abs) > 0.3:
                st.write(f"• {line.title()} line shows a weak correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
            else:
                st.write(f"• {line.title()} line shows minimal correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")

        sampled_data_outbound = outbound_data.groupby('line').apply(lambda x: x.sample(n=min(3000, len(x)), random_state=42)).reset_index(drop=True)
        col1, col2, col3 = st.columns(3)
        with col1:
                st.metric("Average Error (abs) - 3000 obsv per line", f"{sampled_data_outbound['error_seconds'].abs().mean():.0f} seconds")
        with col2:
                st.metric("Average Time to Station", f"{sampled_data_outbound['time_to_station'].mean():.0f} seconds")
        with col3:
                st.metric("Overall Correlation (abs)", f"{sampled_data_outbound['error_seconds'].abs().corr(sampled_data_outbound['time_to_station']):.2f}")


        st.subheader("Correlation Analysis - Error")
        st.info ("""⚠️  A negative correlation here means that the further away the train is, predictions tend to be optimistic and underestimate the journey, and trains mostly arrive later than what they first predicted.   
        A positive correlation here means that the further away the train is, predictions tend to be pessimistic and overestimate the journey, and trains mostly arrive earlier than what they first predicted.   
        A negative average error here means that the tube line is late by x amount on average and vice versa for a positive average error.""")

        for line_data in line_correlations:
            correlation = line_data['correlation']
            line = line_data['line']
            avg_error = line_data['avg_error']
            avg_time = line_data['avg_time']
            error_rate = line_data['error_rate_per_minute']
        
            if abs(correlation) > 0.5:
                strength = "strong" if abs(correlation) > 0.7 else "moderate"
                direction = "positive" if correlation > 0 else "negative"
                st.write(f"• {line.title()} line shows a {strength} {direction} correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival is later than its prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            elif abs(correlation) > 0.3:
                st.write(f"• {line.title()} line shows a weak correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival is later than its prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            else:
                st.write(f"• {line.title()} line shows minimal correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival timestamp is later than the prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            
                col1, col2, col3 = st.columns(3)
        with col1:
                st.metric("Average Error - 3000 obsv per line", f"{sampled_data_outbound['error_seconds'].mean():.0f} seconds")
        with col3:
                st.metric("Overall Correlation", f"{sampled_data_outbound['error_seconds'].corr(sampled_data_outbound['time_to_station']):.2f}")
    else:
        st.plotly_chart(fig, use_container_width=True)
            

with tab2:
    st.markdown("""
    This second tab introduces a new variable: the initial prediction. 
    The initial prediction is the first prediction of a train when first arriving in the dataset, at least 20 minutes after that said train was last seen (as trains eventually come back into the radar).  
    As such, the predictions in the last tab where all of those after these ones.
                
    Just like in the last tab, when taking the intial predictions of all of these runs, do errors go up in magnitude with respect to the time to station?
    Do we find the same patterns in overestimation and underestimation as with all the predictions, or do we find different patterns?                               
    """)
    
    # Add metrics for predictions within 30 seconds and 1 minute
    accuracy_query = """
    SELECT 
        CAST(COUNT(*) AS FLOAT64) as total_predictions,
        CAST(COUNTIF(ABS(error_seconds) <= 30) AS FLOAT64) as accurate_predictions_30s,
        CAST(COUNTIF(ABS(error_seconds) <= 60) AS FLOAT64) as accurate_predictions_60s,
        CAST(ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) AS FLOAT64) as accuracy_percentage_30s,
        CAST(ROUND(COUNTIF(ABS(error_seconds) <= 60) / COUNT(*) * 100, 1) AS FLOAT64) as accuracy_percentage_60s
    FROM `nico-playground-384514.transport_predictions.initial_errors`
    """
    
    accuracy_results = get_cached_query(accuracy_query)
    
    if not accuracy_results.empty:
        col1, col2 = st.columns(2)
        with col1:   
            st.metric(
            "Initial Predictions Within ±30 Seconds",
                f"{accuracy_results.iloc[0]['accuracy_percentage_30s']:.1f}%",
                help=f"Based on {accuracy_results.iloc[0]['total_predictions']:.0f} predictions"
            )
        with col2:
            st.metric(
                "Initial Predictions Within ±1 Minute",
                f"{accuracy_results.iloc[0]['accuracy_percentage_60s']:.1f}%",
            help=f"Based on {accuracy_results.iloc[0]['total_predictions']:.0f} predictions"
        )
        
    # Query for initial predictions by direction
    initial_direction_query = """
    SELECT 
        train_id,
        direction,
        CAST(error_seconds AS FLOAT64) as error_seconds,
        CAST(time_to_station AS FLOAT64) as time_to_station,
        line,
        current_location,
        FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', initial_prediction_timestamp) as initial_prediction_timestamp,
        FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', arrival_timestamp) as arrival_timestamp
    FROM `nico-playground-384514.transport_predictions.initial_errors`
    ORDER BY direction, line
    """
    
    initial_direction_results = get_cached_query(initial_direction_query)
    
    if initial_direction_results.empty:
        st.warning("No data available for analysis")
    else:
        # Inbound predictions
        st.subheader("Inbound Predictions")
        inbound_data = initial_direction_results[initial_direction_results['direction'] == 'inbound'].copy()
        
        if not inbound_data.empty:
        # Create scatter plot with trend line
            fig_inbound = px.scatter(
                inbound_data,
            x='error_seconds',
            y='time_to_station',
            color='line',
            trendline="ols",
                title="Initial Prediction Error vs Time to Station (Inbound)",
            labels={
                'error_seconds': 'Prediction Error (seconds)',
                'time_to_station': 'Time to Station (seconds)',
                    'line': 'Tube Line',
                    'arrival_timestamp': 'Arrival Time',
                    'initial_prediction_timestamp': 'Initial Prediction Time',
                    'train_id': 'Train ID',
                    'current_location': 'Train location'
                },
                hover_data=['current_location','initial_prediction_timestamp','arrival_timestamp','train_id'],
                category_orders={
                    'line': ['metropolitan', 'hammersmith-city', 'northern', 'piccadilly', 'victoria']
                }
            )
            
            # Update layout and legend labels
            fig_inbound.update_layout(
            height=600,
            showlegend=True,
            hovermode='closest'
        )
        
            # Update legend labels for inbound
            legend_labels = {
                'metropolitan': 'Metropolitan (East to KC)',
                'hammersmith-city': 'Hammersmith & City (East to KC)',
                'northern': 'Northern (North to KC)',
                'piccadilly': 'Piccadilly (North East to KC)',
                'victoria': 'Victoria (North to KC)'
            }
            fig_inbound.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))
            
            st.plotly_chart(fig_inbound, use_container_width=True)
        
        st.info(""" ⚠️ A negative error means that the train is late with respect to the prediction.        
        If positive error means that the train is early with respect to the prediction.         
        """)
        
        st.markdown("---")  # Add a separator between inbound  sections
                    # Line-specific correlation analysis
        line_correlations = []
        line_correlations_abs = []
        for line in inbound_data['line'].unique():
            line_data = inbound_data[inbound_data['line'] == line]
            
            # Regular correlation (with sign)
            correlation = line_data['error_seconds'].corr(line_data['time_to_station'])
            avg_error = line_data['error_seconds'].mean()
            avg_time = line_data['time_to_station'].mean()
            slope = correlation * (line_data['error_seconds'].std() / line_data['time_to_station'].std())
            error_rate_per_minute = slope * 60
            
            # Absolute correlation (magnitude only)
            correlation_abs = line_data['error_seconds'].abs().corr(line_data['time_to_station'])
            avg_error_abs = line_data['error_seconds'].abs().mean()
            slope_abs = correlation_abs * (line_data['error_seconds'].abs().std() / line_data['time_to_station'].std())
            error_rate_per_minute_abs = slope_abs * 60
            
            line_correlations.append({
                'line': line,
                'correlation': correlation,
                'avg_error': avg_error,
                'avg_time': avg_time,
                'error_rate_per_minute': error_rate_per_minute
            })
            
            line_correlations_abs.append({
                'line': line,
                'correlation_abs': correlation_abs,
                'avg_error_abs': avg_error_abs,
                'avg_time': avg_time,
                'error_rate_per_minute_abs': error_rate_per_minute_abs
            })

            # Sort both lists by absolute correlation
            line_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            line_correlations_abs.sort(key=lambda x: abs(x['correlation_abs']), reverse=True)

        # Display line-specific insights
        
        st.subheader("Correlation Analysis - Absolute Error")
        st.info ("""⚠️ A positive correlation here means that the further away you predict, the more prediction errors increase in magnitude.""")
        for line_data_abs in line_correlations_abs:
            correlation_abs = line_data_abs['correlation_abs']
            line = line_data_abs['line']
            avg_time = line_data_abs['avg_time']
            avg_error_abs = line_data_abs['avg_error_abs']
            error_rate_abs = line_data_abs['error_rate_per_minute_abs']
            
            if abs(correlation_abs) > 0.5:
                strength_abs = "strong" if abs(correlation_abs) > 0.7 else "moderate"
                direction_abs = "positive" if correlation_abs > 0 else "negative"
                st.write(f"•  {line.title()} line shows a {strength_abs} {direction_abs} correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
            elif abs(correlation_abs) > 0.3:
                st.write(f"• {line.title()} line shows a weak correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
            else:
                st.write(f"• {line.title()} line shows minimal correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
        
        st.info ("""⚠️ Insight ! The correlations are lower than those in the last tab and some even negative! The furthest the initial predictions are, the more accurate they are with respect to the rest of the predictions.""")
        
        st.write("All metrics like these 3 below are from here onwards based on 3000 observations per line.")
        
        sampled_data_inbound = inbound_data.groupby('line').apply(lambda x: x.sample(n=min(3000, len(x)), random_state=42)).reset_index(drop=True)
        col1, col2, col3 = st.columns(3)
        with col1:
                st.metric("Average Error (abs)", f"{sampled_data_inbound['error_seconds'].abs().mean():.0f} seconds")
        with col2:
                st.metric("Average Time to Station", f"{sampled_data_inbound['time_to_station'].mean():.0f} seconds")
        with col3:
                st.metric("Overall Correlation (abs)", f"{sampled_data_inbound['error_seconds'].abs().corr(sampled_data_inbound['time_to_station']):.2f}")

        st.subheader("Correlation Analysis - Error")
        st.info ("""⚠️  A negative correlation here means that the further away the train is, predictions tend to be optimistic and underestimate the journey, and trains mostly arrive later than what they first predicted.   
        A positive correlation here means that the further away the train is, predictions tend to be pessimistic and overestimate the journey, and trains mostly arrive earlier than what they first predicted.     
        A negative average error here means that the tube line is late by x amount on average and vice versa for a positive average error.""")

        for line_data in line_correlations:
            correlation = line_data['correlation']
            line = line_data['line']
            avg_error = line_data['avg_error']
            avg_time = line_data['avg_time']
            error_rate = line_data['error_rate_per_minute']
        
            if abs(correlation) > 0.5:
                strength = "strong" if abs(correlation) > 0.7 else "moderate"
                direction = "positive" if correlation > 0 else "negative"
                st.write(f"• {line.title()} line shows a {strength} {direction} correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival is later than its prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            elif abs(correlation) > 0.3:
                st.write(f"• {line.title()} line shows a weak correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival is later than its prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            else:
                st.write(f"• {line.title()} line shows minimal correlation of {correlation:.2f}. For every minute increase in time to station, {'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival timestamp is later than the prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
        
        st.info ("""⚠️ Insight ! Many correlations have switched signs with respect to the last tab! This means that predictions are pessimistic when they are the furthest away and then they become increasingly optimistic the further they go along the rail network.""")
        col1, col2, col3 = st.columns(3)
        with col1:
                st.metric("Average Error - 3000 obsv per line", f"{sampled_data_inbound['error_seconds'].mean():.0f} seconds")
        with col3:
                st.metric("Overall Correlation", f"{sampled_data_inbound['error_seconds'].corr(sampled_data_inbound['time_to_station']):.2f}")
         
                
        st.markdown("---")  # Add a separator between inbound and outbound sections
        
            # Outbound predictions
        st.subheader("Outbound Predictions")
        outbound_data = initial_direction_results[initial_direction_results['direction'] == 'outbound'].copy()
            
        if not outbound_data.empty:
            # Create scatter plot with trend line
            fig_outbound = px.scatter(
                outbound_data,
                x='error_seconds',
                y='time_to_station',
                color='line',
                trendline="ols",
                title="Initial Prediction Error vs Time to Station (Outbound)",
                labels={
                    'error_seconds': 'Prediction Error (seconds)',
                    'time_to_station': 'Time to Station (seconds)',
                    'line': 'Tube Line',
                    'arrival_timestamp': 'Arrival Time',
                    'initial_prediction_timestamp': 'Initial Prediction Time',
                    'train_id': 'Train ID',
                    'current_location': 'Train location'
                },
                hover_data=['current_location','initial_prediction_timestamp','arrival_timestamp','train_id'],
                category_orders={
                    'line': ['metropolitan', 'hammersmith-city', 'northern', 'piccadilly', 'victoria']
                }
            )
            
                # Update layout and legend labels
            fig_outbound.update_layout(
                height=600,
                showlegend=True,
                hovermode='closest'
                )
            
            # Update legend labels for outbound
            legend_labels = {
                'metropolitan': 'Metropolitan (West to KC)',
                'hammersmith-city': 'Hammersmith & City (West to KC)',
                'northern': 'Northern (South to KC)',
                'piccadilly': 'Piccadilly (South West to KC)',
                'victoria': 'Victoria (South to KC)'
            }
            fig_outbound.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))
            
            st.plotly_chart(fig_outbound, use_container_width=True)
        
        st.markdown("---")  # Add a separator between  outbound sections

                    # Line-specific correlation analysis
        line_correlations = []
        line_correlations_abs = []
        for line in outbound_data['line'].unique():
            line_data = outbound_data[outbound_data['line'] == line]
            
            # Regular correlation (with sign)
            correlation = line_data['error_seconds'].corr(line_data['time_to_station'])
            avg_error = line_data['error_seconds'].mean()
            avg_time = line_data['time_to_station'].mean()
            slope = correlation * (line_data['error_seconds'].std() / line_data['time_to_station'].std())
            error_rate_per_minute = slope * 60
            
            # Absolute correlation (magnitude only)
            correlation_abs = line_data['error_seconds'].abs().corr(line_data['time_to_station'])
            avg_error_abs = line_data['error_seconds'].abs().mean()
            slope_abs = correlation_abs * (line_data['error_seconds'].abs().std() / line_data['time_to_station'].std())
            error_rate_per_minute_abs = slope_abs * 60
            
            line_correlations.append({
                'line': line,
                'correlation': correlation,
                'avg_error': avg_error,
                'avg_time': avg_time,
                'error_rate_per_minute': error_rate_per_minute
            })
            
            line_correlations_abs.append({
                'line': line,
                'correlation_abs': correlation_abs,
                'avg_error_abs': avg_error_abs,
                'avg_time': avg_time,
                'error_rate_per_minute_abs': error_rate_per_minute_abs
            })

            # Sort both lists by absolute correlation
            line_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            line_correlations_abs.sort(key=lambda x: abs(x['correlation_abs']), reverse=True)

    # Display line-specific insights
        
        st.subheader("Correlation Analysis - Absolute Error")
        for line_data_abs in line_correlations_abs:
            correlation_abs = line_data_abs['correlation_abs']
            line = line_data_abs['line']
            avg_time = line_data_abs['avg_time']
            avg_error_abs = line_data_abs['avg_error_abs']
            error_rate_abs = line_data_abs['error_rate_per_minute_abs']
            
            if abs(correlation_abs) > 0.5:
                strength_abs = "strong" if abs(correlation_abs) > 0.7 else "moderate"
                direction_abs = "positive" if correlation_abs > 0 else "negative"
                st.write(f"•  {line.title()} line shows a {strength_abs} {direction_abs} correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
            elif abs(correlation_abs) > 0.3:
                st.write(f"• {line.title()} line shows a weak correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
            else:
                st.write(f"• {line.title()} line shows minimal correlation of {correlation_abs:.2f}. For every minute increase in time to station, absolute prediction errors {'increase' if correlation_abs > 0 else 'decrease'} by {abs(error_rate_abs):.1f} seconds. Absolute average error: {avg_error_abs:.0f}s. Average time to station: {avg_time:.0f}s.")
        st.info ("""⚠️ Insight ! Once again, correlations are lower than those in the last tab and some even negative! Seemingly, the furthest initial predictions are pretty accurate compared to the rest of the predictions.""")
        sampled_data_outbound = outbound_data.groupby('line').apply(lambda x: x.sample(n=min(3000, len(x)), random_state=42)).reset_index(drop=True)
        col1, col2, col3 = st.columns(3)
        with col1:
                st.metric("Average Error (abs) - 3000 obsv per line", f"{sampled_data_outbound['error_seconds'].abs().mean():.0f} seconds")
        with col2:
                st.metric("Average Time to Station", f"{sampled_data_outbound['time_to_station'].mean():.0f} seconds")
        with col3:
                st.metric("Overall Correlation (abs)", f"{sampled_data_outbound['error_seconds'].abs().corr(sampled_data_outbound['time_to_station']):.2f}")


        st.subheader("Correlation Analysis - Error")
        st.info ("""⚠️  A negative correlation here means that the further away the train is, predictions tend to be optimistic and underestimate the journey, and trains mostly arrive later than what they first predicted.   
        A positive correlation here means that the further away the train is, predictions tend to be pessimistic and overestimate the journey, and trains mostly arrive earlier than what they first predicted.  
        In this case however, when looking at the graph for Hammersmith and City, the predictions are just less late when they are furthest away, but they arent pessimistic at all.   
        A negative average error here means that the tube line is late by x amount on average and vice versa for a positive average error.""")

        for line_data in line_correlations:
            correlation = line_data['correlation']
            line = line_data['line']
            avg_error = line_data['avg_error']
            avg_time = line_data['avg_time']
            error_rate = line_data['error_rate_per_minute']
        
            if abs(correlation) > 0.5:
                strength = "strong" if abs(correlation) > 0.7 else "moderate"
                direction = "positive" if correlation > 0 else "negative"
                st.write(f"• {line.title()} line shows a {strength} {direction} correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival is later than its prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            elif abs(correlation) > 0.3:
                st.write(f"• {line.title()} line shows a weak correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival is later than its prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
            else:
                st.write(f"• {line.title()} line shows minimal correlation of {correlation:.2f}. For every minute increase in time to station,{'the arrival is earlier than its prediction by' if correlation > 0 else 'the arrival timestamp is later than the prediction by'} {abs(error_rate):.1f} seconds. Average error: {avg_error:.0f}s.")
        
        st.info ("""⚠️ Insight ! The outbound initial predictions seem more in line with their respective counterparts. Except for the Hammersmith and City line, whose initial predictions start somewhat accurately and then turn optimistic the further along it goes through the rail.""")
        
        col1, col2, col3 = st.columns(3)
        with col1:
                st.metric("Average Error - 3000 obsv per line", f"{sampled_data_outbound['error_seconds'].mean():.0f} seconds")
        with col3:
                st.metric("Overall Correlation", f"{sampled_data_outbound['error_seconds'].corr(sampled_data_outbound['time_to_station']):.2f}")

with tab3:
    st.header("Line & Time Analysis")

    st.markdown("""   
    If we establish accuracy as being the percentage of predictions that are within the arrival time and a window of +-/30s or +-/60s (specified in the charts), then how does accuracy vary by line, hour and day of the week with respect to initial predictions and all the other predictions?
    """)

    
    # Create two columns for side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        
        # Line performance analysis
        line_query = """
        SELECT 
            line,
            COUNT(*) as total_predictions,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage
        FROM `nico-playground-384514.transport_predictions.initial_errors`
        GROUP BY line
        ORDER BY accuracy_percentage DESC
        """
        
        line_df = get_cached_query(line_query)
        
        if not line_df.empty:
            # Line performance bar chart
            fig = px.bar(
                line_df,
                x='line',
                y='accuracy_percentage',
                title="Initial Prediction Accuracy by Line",
                labels={
                    'line': 'Tube Line',
                    'accuracy_percentage': 'Accuracy % (±30s)',
                    'avg_error': 'Average Error (seconds)',
                    'avg_abs_error': 'Average Absolute Error (seconds)'
                },
                hover_data=['avg_error','avg_abs_error']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Time of day analysis
            time_query = """
            SELECT 
                EXTRACT(HOUR FROM arrival_timestamp) as hour,
                COUNT(*) as total_predictions,
                ROUND(AVG(error_seconds), 1) as avg_error,
                ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error,
                ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage
            FROM `nico-playground-384514.transport_predictions.initial_errors`
            WHERE hour >= 5 OR hour < 1  
            GROUP BY hour
            ORDER BY hour
            """
            
            time_df = get_cached_query(time_query)
            
            if not time_df.empty:
                fig = px.line(
                    time_df,
                    x='hour',
                    y='accuracy_percentage',
                    title="Initial Prediction Accuracy by Hour",
                    range_x=[4.5, 24],
                    labels={
                        'hour': 'Hour of Day',
                        'accuracy_percentage': 'Accuracy % (±30s)',
                        'avg_error': 'Average Error (seconds)',
                        'avg_abs_error': 'Average Absolute Error (seconds)'
                    },
                    hover_data=['avg_error','avg_abs_error']
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        
        # Line performance analysis
        line_query = """
        SELECT 
            line,
            COUNT(*) as total_predictions,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage
        FROM `nico-playground-384514.transport_predictions.any_errors`
        GROUP BY line
        ORDER BY accuracy_percentage DESC
        """
        
        line_df = get_cached_query(line_query)
        
        if not line_df.empty:
            # Line performance bar chart
            fig = px.bar(
                line_df,
                x='line',
                y='accuracy_percentage',
                title="Prediction Accuracy by Line",
                labels={
                    'line': 'Tube Line',
                    'accuracy_percentage': 'Accuracy % (±30s)',
                    'avg_error': 'Average Error (seconds)',
                    'avg_abs_error': 'Average Absolute Error (seconds)'
                },
                hover_data=['avg_error','avg_abs_error']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Time of day analysis
            time_query = """
            SELECT 
                 hour,
                COUNT(*) as total_predictions,
                ROUND(AVG(error_seconds), 1) as avg_error,
                ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error,
                ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage
            FROM `nico-playground-384514.transport_predictions.any_errors`
            GROUP BY hour
            ORDER BY hour
            """
            
            time_df = get_cached_query(time_query)
            
            if not time_df.empty:
                fig = px.line(
                    time_df,
                    x='hour',
                    y='accuracy_percentage',
                    title="Prediction Accuracy by Hour",
                     range_x=[4.5, 24],
                    labels={
                        'hour': 'Hour of Day',
                        'accuracy_percentage': 'Accuracy % (±30s)',
                        'avg_error': 'Average Error (seconds)',
                        'avg_abs_error': 'Average Absolute Error (seconds)'
                    },
                    hover_data=['avg_error','avg_abs_error']
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Day of week analysis (full width)
    col1, col2 = st.columns(2)
    
    with col1:
        day_query = """
        SELECT 
            day_of_week,
            COUNT(*) as total_predictions,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage
        FROM `nico-playground-384514.transport_predictions.initial_errors`
        GROUP BY day_of_week
        ORDER BY day_of_week
        """
        
        day_df = get_cached_query(day_query)
        
        if not day_df.empty:
            # Create a mapping of day numbers to names
            day_names = {
                1: 'Monday',
                2: 'Tuesday',
                3: 'Wednesday',
                4: 'Thursday',
                5: 'Friday',
                6: 'Saturday',
                0: 'Sunday'
            }
            # Map only the days we have data for
            day_df['day_name'] = day_df['day_of_week'].map(day_names)
            fig = px.bar(
                day_df,
                x='day_name',
                y='accuracy_percentage',
                title="Initial Prediction Accuracy by Day",
                labels={
                    'day_name': 'Day of Week',
                    'accuracy_percentage': 'Accuracy % (±30s)',
                    'avg_error': 'Average Error (seconds)',
                    'avg_abs_error': 'Average Absolute Error (seconds)'
                },
                hover_data=['avg_error','avg_abs_error']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        day_query = """
        SELECT 
            day_of_week,
            COUNT(*) as total_predictions,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage
        FROM `nico-playground-384514.transport_predictions.any_errors`
        GROUP BY day_of_week
        ORDER BY day_of_week
        """
        
        day_df = get_cached_query(day_query)
        
        if not day_df.empty:
            # Create a mapping of day numbers to names
            day_names = {
                1: 'Monday',
                2: 'Tuesday',
                3: 'Wednesday',
                4: 'Thursday',
                5: 'Friday',
                6: 'Saturday',
                0: 'Sunday'
            }
            # Map only the days we have data for
            day_df['day_name'] = day_df['day_of_week'].map(day_names)
            fig = px.bar(
                day_df,
                x='day_name',
                y='accuracy_percentage',
                title="Prediction Accuracy by Day",
                labels={
                    'day_name': 'Day of Week',
                    'accuracy_percentage': 'Accuracy % (±30s)',
                    'avg_error': 'Average Error (seconds)',
                    'avg_abs_error': 'Average Absolute Error (seconds)'
                },
                hover_data=['avg_error','avg_abs_error']
            )
            st.plotly_chart(fig, use_container_width=True)

     # Add new visualization for accuracy per line by day of week
    st.subheader("Accuracy by Line and Day of Week")
            
    day_line_query = """
            SELECT 
                line,
                day_of_week,
                COUNT(*) as total_predictions,
                ROUND(AVG(error_seconds), 1) as avg_error,
                ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error,
                ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage,
                ROUND(COUNTIF(ABS(error_seconds) <= 60) / COUNT(*) * 100, 1) as accuracy_percentage_60s
            FROM `nico-playground-384514.transport_predictions.any_errors`
            GROUP BY line, day_of_week
            ORDER BY line, day_of_week
            """

    day_line_df = get_cached_query(day_line_query)
    
    if not day_line_df.empty:
        
        # Create a mapping of day numbers to names (1-7)
        day_names = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            0: 'Sunday'
        }

        if not day_line_df.empty:
        # Convert numeric columns to float
            numeric_columns = ['accuracy_percentage', 'accuracy_percentage_60s', 'avg_error', 'avg_abs_error']
        for col in numeric_columns:
            day_line_df[col] = pd.to_numeric(day_line_df[col], errors='coerce')
        
        # Map day numbers to names
        day_line_df['day_name'] = day_line_df['day_of_week'].map(day_names)
        
        # Create complete index and columns for all combinations
        all_lines = sorted(day_line_df['line'].unique())
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # First aggregate any duplicate entries - use first() for error metrics
        agg_df = day_line_df.groupby(['line', 'day_name']).agg({
            'accuracy_percentage': 'mean',
            'accuracy_percentage_60s': 'mean',
            'avg_error': 'first',
            'avg_abs_error': 'first'
        }).reset_index()
        
        
        # Create pivot tables from aggregated data
        pivot_df = agg_df.pivot(index='line', columns='day_name', values='accuracy_percentage')
        error_df = agg_df.pivot(index='line', columns='day_name', values='avg_error')
        abs_error_df = agg_df.pivot(index='line', columns='day_name', values='avg_abs_error')
        
        # Reorder columns to match all_days
        pivot_df = pivot_df.reindex(columns=all_days)
        error_df = error_df.reindex(columns=all_days)
        abs_error_df = abs_error_df.reindex(columns=all_days)
        
        # Create hover text with all metrics
        hover_text = []
        for i in range(len(pivot_df.index)):
            row = []
            for j in range(len(pivot_df.columns)):
                text = f"Line: {pivot_df.index[i]}<br>"
                text += f"Day: {pivot_df.columns[j]}<br>"
                text += f"Accuracy: {pivot_df.iloc[i,j]:.1f}%<br>"
                text += f"Avg Error: {error_df.iloc[i,j]:.1f}s<br>"
                text += f"Avg Abs Error: {abs_error_df.iloc[i,j]:.1f}s"
                row.append(text)
            hover_text.append(row)
        
        # Create the heatmap with fixed color scale for 30s
        fig = px.imshow(
            pivot_df,
            labels=dict(x="Day of Week", y="Line", color="Accuracy % (±30s)"),
            title="Prediction Accuracy by Line and Day of Week (±30s)",
            color_continuous_scale='RdYlGn',
            aspect='auto',
            zmin=0,
            zmax=100
        )
        
        # Update layout and add hover text
        fig.update_layout(
            height=600,
            xaxis={'categoryorder': 'array', 'categoryarray': all_days}
        )
        fig.update_traces(hovertemplate="%{customdata}<extra></extra>", customdata=hover_text)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create a heatmap showing accuracy by line and day (±60s)
        pivot_df_60s = agg_df.pivot(index='line', columns='day_name', values='accuracy_percentage_60s')
        pivot_df_60s = pivot_df_60s.reindex(columns=all_days)
        
        # Create hover text with all metrics for 60s
        hover_text_60s = []
        for i in range(len(pivot_df_60s.index)):
            row = []
            for j in range(len(pivot_df_60s.columns)):
                text = f"Line: {pivot_df_60s.index[i]}<br>"
                text += f"Day: {pivot_df_60s.columns[j]}<br>"
                text += f"Accuracy: {pivot_df_60s.iloc[i,j]:.1f}%<br>"
                text += f"Avg Error: {error_df.iloc[i,j]:.1f}s<br>"
                text += f"Avg Abs Error: {abs_error_df.iloc[i,j]:.1f}s"
                row.append(text)
            hover_text_60s.append(row)
        
        fig_60s = px.imshow(
            pivot_df_60s,
            labels=dict(x="Day of Week", y="Line", color="Accuracy % (±60s)"),
            title="Prediction Accuracy by Line and Day of Week (±60s)",
            color_continuous_scale='RdYlGn',
            aspect='auto',
            zmin=0,
            zmax=100
        )
        
        # Update layout and add hover text
        fig_60s.update_layout(
            height=600,
            xaxis={'categoryorder': 'array', 'categoryarray': all_days}
        )
        fig_60s.update_traces(hovertemplate="%{customdata}<extra></extra>", customdata=hover_text_60s)
        
        st.plotly_chart(fig_60s, use_container_width=True)

with tab4:
    st.header("Prediction Precision Analysis")

    st.markdown(""" How does accuracy vary per line and time to station?
    """)

    
    # Query to get binned time to station data
    precision_query = """
    WITH binned_data AS (
        SELECT 
            line,
            CASE 
                WHEN time_to_station <= 60 THEN '0-1 min'
                WHEN time_to_station <= 120 THEN '1-2 min'
                WHEN time_to_station <= 180 THEN '2-3 min'
                WHEN time_to_station <= 240 THEN '3-4 min'
                WHEN time_to_station <= 300 THEN '4-5 min'
                WHEN time_to_station <= 600 THEN '5-10 min'
                WHEN time_to_station <= 900 THEN '10-15 min'
                ELSE '15+ min'
            END as time_bin,
            COUNT(*) as total_predictions,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage_30s,
            ROUND(COUNTIF(ABS(error_seconds) <= 60) / COUNT(*) * 100, 1) as accuracy_percentage_60s,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error
        FROM `nico-playground-384514.transport_predictions.any_errors`
        GROUP BY line, time_bin
    )
    SELECT *
    FROM binned_data
    ORDER BY 
        CASE time_bin
            WHEN '0-1 min' THEN 1
            WHEN '1-2 min' THEN 2
            WHEN '2-3 min' THEN 3
            WHEN '3-4 min' THEN 4
            WHEN '4-5 min' THEN 5
            WHEN '5-10 min' THEN 6
            WHEN '10-15 min' THEN 7
            ELSE 8
        END,
        line
    """
    
    precision_df = get_cached_query(precision_query)
    
    if not precision_df.empty:
        # Create a line chart showing accuracy by time bin (±30s)
        fig = px.line(
            precision_df,
            x='time_bin',
            y='accuracy_percentage_30s',
            color='line',
            markers=True,
            title="Prediction Accuracy by Time to Station (±30s)",
            labels={
                'time_bin': 'Time to Station',
                'accuracy_percentage_30s': 'Accuracy % (±30s)',
                'line': 'Tube Line',
                'avg_error': 'Average Error (seconds)',
                'avg_abs_error': 'Average Absolute Error (seconds)'
            },
            hover_data=['avg_error','avg_abs_error']
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            showlegend=True,
            hovermode='closest',
            xaxis={'categoryorder': 'array', 'categoryarray': ['15+ min', '10-15 min', '5-10 min', '4-5 min', '3-4 min', '2-3 min', '1-2 min', '0-1 min']}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create a line chart showing accuracy by time bin (±60s)
        fig = px.line(
            precision_df,
            x='time_bin',
            y='accuracy_percentage_60s',
            color='line',
            markers=True,
            title="Prediction Accuracy by Time to Station (±60s)",
            labels={
                'time_bin': 'Time to Station',
                'accuracy_percentage_60s': 'Accuracy % (±60s)',
                'line': 'Tube Line',
                'avg_error': 'Average Error (seconds)',
                'avg_abs_error': 'Average Absolute Error (seconds)'
            },
            hover_data=['avg_error','avg_abs_error']
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            showlegend=True,
            hovermode='closest',
            xaxis={'categoryorder': 'array', 'categoryarray': ['15+ min', '10-15 min', '5-10 min', '4-5 min', '3-4 min', '2-3 min', '1-2 min', '0-1 min']}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add summary statistics
        st.subheader("Summary Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Most accurate time bin (±30s)
            best_bin_30s = precision_df.loc[precision_df['accuracy_percentage_30s'].idxmax()]
            st.metric(
                "Most Accurate Time Window (±30s)",
                f"{best_bin_30s['time_bin']} ({best_bin_30s['accuracy_percentage_30s']:.1f}%)",
                f"Line: {best_bin_30s['line']}"
            )
        
        with col2:
            # Most accurate time bin (±60s)
            best_bin_60s = precision_df.loc[precision_df['accuracy_percentage_60s'].idxmax()]
            st.metric(
                "Most Accurate Time Window (±60s)",
                f"{best_bin_60s['time_bin']} ({best_bin_60s['accuracy_percentage_60s']:.1f}%)",
                f"Line: {best_bin_60s['line']}"
            )
        
        with col3:
            # Least accurate time bin (using ±30s)
            worst_bin = precision_df.loc[precision_df['accuracy_percentage_30s'].idxmin()]
            st.metric(
                "Least Accurate Time Window (±30s)",
                f"{worst_bin['time_bin']} ({worst_bin['accuracy_percentage_30s']:.1f}%)",
                f"Line: {worst_bin['line']}"
            )
        
        # Calculate biggest changes for each line
        st.subheader("Biggest Accuracy Changes by Line")
        
        # Function to calculate biggest change for a line
        def get_biggest_change(line_data, accuracy_col):
            # Sort by time bin to ensure correct order
            line_data = line_data.sort_values('time_bin', key=lambda x: pd.Categorical(x, 
                categories=['0-1 min', '1-2 min', '2-3 min', '3-4 min', '4-5 min', '5-10 min', '10-15 min', '15+ min'],
                ordered=True))
            
            # Calculate percentage changes between consecutive time bins
            changes = []
            for i in range(len(line_data) - 1):
                current = line_data.iloc[i]
                next_bin = line_data.iloc[i + 1]
                change = next_bin[accuracy_col] - current[accuracy_col]
                changes.append({
                    'from_bin': current['time_bin'],
                    'to_bin': next_bin['time_bin'],
                    'change': change
                })
            
            # Find biggest change (absolute value)
            if changes:
                biggest_change = max(changes, key=lambda x: abs(x['change']))
                return biggest_change
            return None
        
        # Calculate changes for each line
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Biggest Changes (±30s)")
            for line in precision_df['line'].unique():
                line_data = precision_df[precision_df['line'] == line]
                change = get_biggest_change(line_data, 'accuracy_percentage_30s')
                if change:
                    direction = "decrease" if change['change'] > 0 else "increase"
                    st.write(f"• {line.title()}: {abs(change['change']):.1f}% {direction} from {change['to_bin']} to {change['from_bin']}")
        
        with col2:
            st.write("Biggest Changes (±60s)")
            for line in precision_df['line'].unique():
                line_data = precision_df[precision_df['line'] == line]
                change = get_biggest_change(line_data, 'accuracy_percentage_60s')
                if change:
                    direction = "decrease" if change['change'] > 0 else "increase"
                    st.write(f"• {line.title()}: {abs(change['change']):.1f}% {direction} from {change['to_bin']} to {change['from_bin']}")

with tab5:
    st.header("Location Analysis")

    st.markdown("""
    How does accuracy vary by location where the prediction is made?  
    The Red Marker is the location of King's Cross. 
    """)
    
    # Query to get location-based statistics with direction
    location_query = """
    WITH location_stats AS (
        SELECT 
            line,
            current_location,
            COUNT(*) as total_predictions,
            ROUND(AVG(error_seconds),1) as avg_error, 
            ROUND(AVG(ABS(error_seconds)),1) as avg_abs_error,
            STDDEV(error_seconds) as std_error,
            ROUND(LEAST(COUNT(CASE WHEN ABS(error_seconds) <= 30 THEN 1 END) * 100.0 / COUNT(*), 100),2) as accuracy_30s,
            LEAST(COUNT(CASE WHEN ABS(error_seconds) <= 60 THEN 1 END) * 100.0 / COUNT(*), 100) as accuracy_60s
        FROM `nico-playground-384514.transport_predictions.any_errors`
        WHERE current_location IS NOT NULL
        GROUP BY line, current_location
    )
    SELECT * FROM location_stats
    ORDER BY line, total_predictions DESC
    """
    
    location_df = get_cached_query(location_query)
    
    if not location_df.empty:
        # Create a line selector
        selected_line = st.selectbox(
            "Select Line",
            options=sorted(location_df['line'].unique()),
            key="any_location_line"
        )
        
        # Filter data for selected line
        line_data = location_df[location_df['line'] == selected_line]
        
        # Get stations in exact order from the lists
        if selected_line.lower() in STATION_ORDERS:
            if selected_line.lower() == 'northern':
                # For Northern line, show both branches
                st.subheader("Edgware Branch")
                branch1_stations = STATION_ORDERS[selected_line.lower()]['1']['branch_1']
                branch2_stations = STATION_ORDERS[selected_line.lower()]['1']['branch_2']
                list2_stations = STATION_ORDERS[selected_line.lower()]['2']
                
                # Create DataFrames for each branch
                branch1_data = pd.DataFrame({'current_location': branch1_stations})
                branch2_data = pd.DataFrame({'current_location': branch2_stations})
                list2_data = pd.DataFrame({'current_location': list2_stations})
                
                # Merge with actual data
                branch1_data = branch1_data.merge(line_data, on='current_location', how='left')
                branch2_data = branch2_data.merge(line_data, on='current_location', how='left')
                list2_data = list2_data.merge(line_data, on='current_location', how='left')
                
                # Fill NaN values with 0
                branch1_data = branch1_data.fillna(0)
                branch2_data = branch2_data.fillna(0)
                list2_data = list2_data.fillna(0)
                
                # Create charts for each branch
                fig1 = px.bar(
                    branch1_data,
                    x='current_location',
                    y='accuracy_30s',
                    title=f"Prediction Accuracy by Location - {selected_line} (Southbound - Edgware Branch)",
                    labels={
                        'current_location': 'Location',
                        'accuracy_30s': 'Accuracy % (±30s)',
                        'avg_error': 'Average Error (seconds)',
                        'avg_abs_error': 'Average Absolute Error (seconds)'
                    },
                    hover_data=['avg_error','avg_abs_error']
                )
                
                fig2 = px.bar(
                    branch2_data,
                    x='current_location',
                    y='accuracy_30s',
                    title=f"Prediction Accuracy by Location - {selected_line} (Southbound - High Barnet Branch)",
                    labels={
                        'current_location': 'Location',
                        'accuracy_30s': 'Accuracy % (±30s)',
                        'avg_error': 'Average Error (seconds)',
                        'avg_abs_error': 'Average Absolute Error (seconds)'
                    },
                    hover_data=['avg_error','avg_abs_error']
                )   
                
                fig3 = px.bar(
                    list2_data,
                    x='current_location',
                    y='accuracy_30s',
                    title=f"Prediction Accuracy by Location - {selected_line} (Northbound)",
                    labels={
                        'current_location': 'Location',
                        'accuracy_30s': 'Accuracy % (±30s)',
                        'avg_error': 'Average Error (seconds)',
                        'avg_abs_error': 'Average Absolute Error (seconds)'
                    },
                    hover_data=['avg_error','avg_abs_error']
                )
                
                # Update layouts
                for fig in [fig1, fig2, fig3]:
                    fig.update_layout(
                        height=800,
                        width=1200,
                        xaxis=dict(
                            tickangle=45,
                            tickfont=dict(size=10),
                            tickmode='array',
                            ticktext=fig.data[0].x,
                            tickvals=fig.data[0].x,
                            side='bottom'
                        ),
                        margin=dict(b=150),
                        bargap=0.1,
                        bargroupgap=0.1,
                        showlegend=False
                    )
                    fig.update_traces(
                        width=0.8,
                        marker=dict(line=dict(width=0))
                    )
                
                st.plotly_chart(fig1, use_container_width=True)
                st.plotly_chart(fig2, use_container_width=True)
                st.plotly_chart(fig3, use_container_width=True)
                
            else:
                # For other lines, show single graph
                all_stations = STATION_ORDERS[selected_line.lower()]['1'] + STATION_ORDERS[selected_line.lower()]['2']
                ordered_data = pd.DataFrame({'current_location': all_stations})
                line_data = ordered_data.merge(line_data, on='current_location', how='left')
                line_data = line_data.fillna(0)
                
                fig = px.bar(
                    line_data,
                    x='current_location',
                    y='accuracy_30s',
                    title=f"Prediction Accuracy by Location - {selected_line}",
                    labels={
                        'current_location': 'Location',
                        'accuracy_30s': 'Accuracy % (±30s)',
                        'avg_error': 'Average Error (seconds)',
                        'avg_abs_error': 'Average Absolute Error (seconds)'
                    },
                    hover_data=['avg_error','avg_abs_error']
                )
                
                fig.update_layout(
                    height=800,
                    width=1200,
                    xaxis=dict(
                        tickangle=45,
                        tickfont=dict(size=10),
                        tickmode='array',
                        ticktext=line_data['current_location'],
                        tickvals=line_data['current_location'],
                        side='bottom'
                    ),
                    margin=dict(b=150),
                    bargap=0.1,
                    bargroupgap=0.1,
                    showlegend=False
                )
                
                fig.update_traces(
                    width=0.8,
                    marker=dict(line=dict(width=0))
                )
                
                # Add red marker between list 1 and list 2
                list1_count = len(STATION_ORDERS[selected_line.lower()]['1'])
                if list1_count > 0:
                    marker_idx = list1_count - 0.5
                    fig.add_vline(
                        x=marker_idx,
                        line_dash="solid",
                        line_color="red",
                        opacity=1
                    )
                
                st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.header("Direction Analysis")
    
    st.markdown(""" How does accuracy vary by direction per line?
    """)
    
    # Query to get direction-based statistics
    direction_query = """
    SELECT 
        line,
        direction,
        COUNT(*) as total_predictions,
        ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_30s,
        ROUND(AVG(error_seconds), 1) as avg_error,
        ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error
    FROM `nico-playground-384514.transport_predictions.any_errors`
    WHERE direction in ('outbound', 'inbound')
    GROUP BY line, direction
    ORDER BY line, direction
    """
    
    direction_df = get_cached_query(direction_query)
    
    if not direction_df.empty:
        # Create a line selector
        selected_line = st.selectbox(
            "Select Line",
            options=sorted(direction_df['line'].unique()),
            key="direction_line"
        )
        
        # Filter data for selected line
        line_data = direction_df[direction_df['line'] == selected_line]
        
        # Define direction labels based on line
        if selected_line in ['hammersmith-city', 'metropolitan']:
            line_data['direction'] = line_data['direction'].map({
                'outbound': 'West to KC',
                'inbound': 'East to KC'
            })
        elif selected_line in ['victoria', 'northern']:
            line_data['direction'] = line_data['direction'].map({
                'outbound': 'South to KC',
                'inbound': 'North to KC'
            })
        elif selected_line == 'piccadilly':
            line_data['direction'] = line_data['direction'].map({
                'outbound': 'South West to KC',
                'inbound': 'North East to KC'
            })
        
        # Create bar plot
        fig = px.bar(
            line_data,
            x='direction',
            y='accuracy_30s',
            title=f"Prediction Accuracy by Direction - {selected_line.title()}",
            labels={
                'direction': 'Direction',
                'accuracy_30s': 'Accuracy % (±30s)',
                'avg_error': 'Average Error (seconds)',
                'avg_abs_error': 'Average Absolute Error (seconds)'
            },
            hover_data=['avg_error','avg_abs_error']
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            showlegend=False,
            bargap=0.3,
            yaxis=dict(
                range=[0, 100],
                title='Accuracy %'
            )
        )
        
        # Add value labels on top of bars
        fig.update_traces(
            texttemplate='%{y:.1f}%',
            textposition='outside'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show total predictions for each direction
        st.subheader("Total Predictions by Direction")
        for _, row in line_data.iterrows():
            st.write(f"{row['direction']}: {row['total_predictions']:,.0f} predictions")

with tab7:
    st.header("Peak vs Off-Peak Analysis")

    st.markdown(""" How does peak times and off peak times compare in terms of accuracy and error?
    """)
    
    # Query to get peak time analysis
    peak_query = """
    WITH time_periods AS (
        SELECT 
            line,
            CASE 
                WHEN (EXTRACT(HOUR FROM arrival_timestamp) = 7 AND EXTRACT(MINUTE FROM arrival_timestamp) >= 0)
                    OR (EXTRACT(HOUR FROM arrival_timestamp) = 8)
                    OR (EXTRACT(HOUR FROM arrival_timestamp) = 9 AND EXTRACT(MINUTE FROM arrival_timestamp) < 30)
                THEN 'Morning Peak (7:00-9:30)'
                WHEN (EXTRACT(HOUR FROM arrival_timestamp) = 16 AND EXTRACT(MINUTE FROM arrival_timestamp) >= 30)
                    OR (EXTRACT(HOUR FROM arrival_timestamp) = 17)
                    OR (EXTRACT(HOUR FROM arrival_timestamp) = 18)
                    OR (EXTRACT(HOUR FROM arrival_timestamp) = 19 AND EXTRACT(MINUTE FROM arrival_timestamp) = 0)
                THEN 'Evening Peak (16:30-19:00)'
                ELSE 'Off-Peak'
            END as time_period,
            COUNT(*) as total_predictions,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error
        FROM `nico-playground-384514.transport_predictions.any_errors`
        GROUP BY line, time_period
    )
    SELECT *
    FROM time_periods
    ORDER BY 
        CASE time_period
            WHEN 'Morning Peak (7:00-9:30)' THEN 1
            WHEN 'Evening Peak (16:30-19:00)' THEN 2
            ELSE 3
        END,
        line
    """
    
    peak_df = get_cached_query(peak_query)
    
    if not peak_df.empty:
        # Create a grouped bar chart showing accuracy by time period and line
        fig = px.bar(
            peak_df,
            x='line',
            y='accuracy_percentage',
            color='time_period',
            barmode='group',
            title="Prediction Accuracy by Time Period and Line",
            labels={
                'line': 'Tube Line',
                'accuracy_percentage': 'Accuracy % (±30s)',
                'time_period': 'Time Period',
                'avg_error': 'Average Error (seconds)',
                'avg_abs_error': 'Average Absolute Error (seconds)'
            },
            hover_data=['avg_error','avg_abs_error']
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            showlegend=True,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add summary statistics
        st.subheader("Summary Statistics by Time Period")
        
        # Calculate overall statistics for each time period
        period_stats = peak_df.groupby('time_period').agg({
            'total_predictions': 'sum',
            'accuracy_percentage': 'mean',
            'avg_error': lambda x: (x * peak_df.loc[x.index, 'total_predictions']).sum() / peak_df.loc[x.index, 'total_predictions'].sum()
        }).reset_index()
        
        # Display metrics in three columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            morning_peak = period_stats[period_stats['time_period'] == 'Morning Peak (7:00-9:30)']
            if not morning_peak.empty:
                st.metric(
                    "Morning Peak (7:00-9:30)",
                    f"{morning_peak['accuracy_percentage'].iloc[0]:.1f}%",
                    f"Avg Error: {morning_peak['avg_error'].iloc[0]:.1f}s"
                )
            else:
                st.metric("Morning Peak (7:00-9:30)", "No data")
        
        with col2:
            evening_peak = period_stats[period_stats['time_period'] == 'Evening Peak (16:30-19:00)']
            if not evening_peak.empty:
                st.metric(
                    "Evening Peak (16:30-19:00)",
                    f"{evening_peak['accuracy_percentage'].iloc[0]:.1f}%",
                    f"Avg Error: {evening_peak['avg_error'].iloc[0]:.1f}s"
                )
            else:
                st.metric("Evening Peak (16:30-19:00)", "No data")
        
        with col3:
            off_peak = period_stats[period_stats['time_period'] == 'Off-Peak']
            if not off_peak.empty:
                st.metric(
                    "Off-Peak",
                    f"{off_peak['accuracy_percentage'].iloc[0]:.1f}%",
                    f"Avg Error: {off_peak['avg_error'].iloc[0]:.1f}s"
                )
            else:
                st.metric("Off-Peak", "No data")
        
with tab8:
    st.header("Error Pattern Analysis")

    st.markdown(""" Which lines has the most observations? Which lines have the most early arrivals? Which lines have the most late arrivals?
    """)
    
    # Query to analyze error patterns
    error_pattern_query = """
    WITH error_analysis AS (
        SELECT 
            line,
            CASE 
                WHEN error_seconds > 30 THEN 'Early Arrival'
                WHEN error_seconds < -30 THEN 'Late Arrival'
                ELSE 'Accurate'
            END as error_type,
            COUNT(*) as count,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY line), 1) as percentage
        FROM `nico-playground-384514.transport_predictions.any_errors`
        GROUP BY line, error_type
    )
    SELECT *
    FROM error_analysis
    ORDER BY line, error_type
    """
    
    error_df = get_cached_query(error_pattern_query)
    
    if not error_df.empty:
        # Create stacked bar chart for error types by line
        fig = px.bar(
            error_df,
            x='line',
            y='count',
            color='error_type',
            title="Prediction Error Types by Line",
            labels={
                'line': 'Tube Line',
                'count': 'Number of Predictions',
                'error_type': 'Error Type',
                'avg_error': 'Average Error (seconds)',
                'avg_abs_error': 'Average Absolute Error (seconds)'
            },
            hover_data=['avg_error','avg_abs_error']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add summary statistics
        st.subheader("Error Pattern Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            # Most overestimated line
            overestimate = error_df[error_df['error_type'] == 'Early Arrival'].sort_values('percentage', ascending=False)
            if not overestimate.empty:
                st.metric(
                    "Earliest Line",
                    f"{overestimate.iloc[0]['line']} ({overestimate.iloc[0]['percentage']:.1f}%)",
                    f"Avg Error: {overestimate.iloc[0]['avg_error']:.1f}s"
                )
        
        with col2:
            # Most underestimated line
            underestimate = error_df[error_df['error_type'] == 'Late Arrival'].sort_values('percentage', ascending=False)
            if not underestimate.empty:
                st.metric(
                    "Latest Line",
                    f"{underestimate.iloc[0]['line']} ({underestimate.iloc[0]['percentage']:.1f}%)",
                    f"Avg Error: {underestimate.iloc[0]['avg_error']:.1f}s"
                )

with tab9:
    st.header("Prediction Drift Analysis")
    
    st.markdown(""" How did the accuracy vary throughout the last 14 days?
    """)
    
    # Query to analyze prediction drift over time
    drift_query = """
    WITH daily_stats AS (
        SELECT 
            DATE(arrival_timestamp) as date,
            line,
            COUNT(*) as total_predictions,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error
        FROM `nico-playground-384514.transport_predictions.any_errors`
        WHERE DATE(arrival_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
        GROUP BY date, line
    )
    SELECT *
    FROM daily_stats
    ORDER BY date, line
    """
    
    drift_df = get_cached_query(drift_query)
    
    if not drift_df.empty:
        # Create line chart for accuracy over time
        fig = px.line(
            drift_df,
            x='date',
            y='accuracy_percentage',
            color='line',
            title="Prediction Accuracy Over Time (Last few days)",
            labels={
                'date': 'Date',
                'accuracy_percentage': 'Accuracy % (±30s)',
                'line': 'Tube Line',
                'avg_error': 'Average Error (seconds)',
                'avg_abs_error': 'Average Absolute Error (seconds)'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add trend analysis
        st.subheader("Trend Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            # Calculate overall trend
            overall_trend = drift_df.groupby('date')['accuracy_percentage'].mean().reset_index()
            if len(overall_trend) > 1:
                # Sort by date to ensure correct order
                overall_trend = overall_trend.sort_values('date')
                # Get the last 14 days
                last_14_days = overall_trend.tail(14)
                if len(last_14_days) >= 14:
                    # Split into two weeks
                    last_week = last_14_days.tail(7)['accuracy_percentage'].mean()
                    previous_week = last_14_days.head(7)['accuracy_percentage'].mean()
                    trend = last_week - previous_week
                st.metric(
                    "Overall Accuracy Trend",
                    f"{trend:+.1f}%",
                    "Change in last 7 days vs previous 7 days"
                )
        
        with col2:
            # Most improved line
            line_trends = drift_df.groupby('line').apply(
                lambda x: x.sort_values('date').tail(14).tail(7)['accuracy_percentage'].mean() - 
                         x.sort_values('date').tail(14).head(7)['accuracy_percentage'].mean()
            ).sort_values(ascending=False)
            if not line_trends.empty:
                st.metric(
                    "Most Improved Line",
                    f"{line_trends.index[0]} ({line_trends.iloc[0]:+.1f}%)",
                    "Change in last 7 days vs previous 7 days"
                )

with tab10:
    st.header("Anomaly Detection")
    
    st.markdown("""
    What is an anomaly? Which lines have the most anomalies? Which lines has the worst anomalies?
    
    In this analysis, an anomaly is defined as an hour where the prediction accuracy is significantly lower than normal. Specifically:
    
    - We calculate the average accuracy and its standard deviation across all hours
    - An hour is considered anomalous if its accuracy is more than 1.5 standard deviations below the mean
    - The size of each dot represents the average absolute error in seconds for that period
    - The y-axis shows accuracy percentage (0-25% range to focus on anomalies)
    
    This helps identify periods where the prediction system is performing significantly worse than usual.
    """)
    
    # Query to detect anomalies with less strict thresholds
    anomaly_query = """
    WITH daily_stats AS (
        SELECT 
            TIMESTAMP_TRUNC(arrival_timestamp, HOUR) as date,
            line,
            COUNT(*) as total_predictions,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage,
            ROUND(ABS(AVG(error_seconds)), 1) as avg_error,
            ROUND(STDDEV(ABS(error_seconds)), 1) as error_stddev
        FROM `nico-playground-384514.transport_predictions.any_errors`
        GROUP BY date, line
    ),
    thresholds AS (
        SELECT 
            AVG(accuracy_percentage) as avg_accuracy,
            STDDEV(accuracy_percentage) as accuracy_stddev,
            AVG(avg_error) as avg_error,
            STDDEV(avg_error) as error_stddev
        FROM daily_stats
    ),
    anomalies AS (
        SELECT 
            d.*,
            CASE 
                WHEN d.accuracy_percentage < (t.avg_accuracy - 1.5 * t.accuracy_stddev) THEN 'Low Accuracy'
                ELSE 'Normal'
            END as anomaly_type
        FROM daily_stats d
        CROSS JOIN thresholds t
    )
    SELECT *
    FROM anomalies
    WHERE anomaly_type != 'Normal'
    ORDER BY date, line
    """
    
    # First, let's see the overall statistics
    stats_query = """
    SELECT 
        TIMESTAMP_TRUNC(arrival_timestamp, HOUR) as date,
        COUNT(*) as total_predictions,
        ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage,
        ROUND(AVG(error_seconds), 1) as avg_error
    FROM `nico-playground-384514.transport_predictions.any_errors`
    GROUP BY date
    ORDER BY date
    """
    
    stats_df = get_cached_query(stats_query)
    anomaly_df = get_cached_query(anomaly_query)
    
    if not anomaly_df.empty:
        # Create scatter plot for anomalies
        fig = px.scatter(
            anomaly_df,
            x='date',
            y='accuracy_percentage',
            size='avg_error',  # Make dot size proportional to average error
            color='line',
            hover_data=['total_predictions'],  # Add total predictions to hover data
            title="Anomaly Detection by Hour and Line",
            labels={
                'date': 'Hour',
                'accuracy_percentage': 'Accuracy % (±30s)',
                'line': 'Tube Line',
                'avg_error': 'Average Absolute Error (seconds)',
                'total_predictions': 'Number of Predictions'
            }
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            yaxis=dict(
                range=[0, 25],
                title='Accuracy %'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add anomaly analysis
        st.subheader("Anomaly Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            # Biggest anomaly by average error
            biggest_anomaly = anomaly_df.sort_values('avg_error', ascending=False).iloc[0]
            st.metric(
                "Biggest Anomaly",
                f"{biggest_anomaly['line']} ({biggest_anomaly['avg_error']:.1f}s)",
                )
        
        with col2:
            # Most affected line
            most_affected = anomaly_df.groupby('line').size().sort_values(ascending=False)
            if not most_affected.empty:
                st.metric(
                    "Most Affected Line",
                    f"{most_affected.index[0]} ({most_affected.iloc[0]} periods)",
                )
        
        # Add summary statistics
        st.subheader("Summary Statistics by Line")
        
        # Calculate statistics per line
        line_stats = anomaly_df.groupby('line').agg({
            'avg_error': ['count', 'mean'],
            'accuracy_percentage': 'mean',
            'total_predictions': 'sum'
        }).reset_index()
        
        # Rename columns for clarity
        line_stats.columns = ['Line', 'Number of Anomalies', 'Average Error (s)', 'Average Accuracy (%)', 'Total Predictions']
        
        # Sort by total predictions
        line_stats = line_stats.sort_values('Number of Anomalies', ascending=False)
        
        # Display as a table
        st.dataframe(
            line_stats.style.format({
                'Average Error (s)': '{:.1f}',
                'Average Accuracy (%)': '{:.1f}',
                'Total Predictions': '{:,.0f}'
            }),
            use_container_width=True
        )

with tab11:
    st.header("Line Interaction Analysis")
    
    st.markdown("""
     What is line interaction analysis? 
     What is the best and worst line sequence?
    
    The visualization shows:
    - A heatmap where each cell represents a combination of two lines
    - Those that have just arrived are on the y axis, and those that arrived previous to these on the x axis.
    - The color intensity shows the average prediction accuracy for that line combination (for some reason, it says sum of accuracy, but it's actually the average)
    - Darker colors indicate higher accuracy
    """)
    
    # Query to analyze line interactions
    interaction_query = """
    WITH time_windows AS (
        SELECT 
            arrival_timestamp,
            line,
            error_seconds,
            LAG(line) OVER (ORDER BY arrival_timestamp) as prev_line,
            LAG(error_seconds) OVER (ORDER BY arrival_timestamp) as prev_error
        FROM `nico-playground-384514.transport_predictions.any_errors`
    ),
    interactions AS (
        SELECT 
            line,
            prev_line,
            COUNT(*) as interaction_count,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage
        FROM time_windows
        WHERE prev_line IS NOT NULL
        GROUP BY line, prev_line
    )
    SELECT *
    FROM interactions
    ORDER BY interaction_count DESC
    """
    
    interaction_df = get_cached_query(interaction_query)
    
    if not interaction_df.empty:
        # Create heatmap for line interactions
        fig = px.density_heatmap(
            interaction_df,
            x='prev_line',
            y='line',
            z='accuracy_percentage',
            title="Prediction Accuracy by Line Sequence",
            labels={
                'prev_line': 'Previous Line',
                'line': 'Current Line',
                'accuracy_percentage': 'Accuracy % (±30s)',
                'avg_error': 'Average Error (seconds)',
                'avg_abs_error': 'Average Absolute Error (seconds)'
            },
            hover_data=['avg_error','avg_abs_error']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add interaction summary
        st.subheader("Line Interaction Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            # Best line sequence
            best_sequence = interaction_df.loc[interaction_df['accuracy_percentage'].idxmax()]
            st.metric(
                "Best Line Sequence",
                f"{best_sequence['prev_line']} → {best_sequence['line']}",
                f"{best_sequence['accuracy_percentage']:.1f}% accuracy"
            )
        
        with col2:
            # Worst line sequence
            worst_sequence = interaction_df.loc[interaction_df['accuracy_percentage'].idxmin()]
            st.metric(
                "Worst Line Sequence",
                f"{worst_sequence['prev_line']} → {worst_sequence['line']}",
                f"{worst_sequence['accuracy_percentage']:.1f}% accuracy"
            )

with tab12:
    st.header("Weather Impact Analysis")

    st.markdown("""
    How do weather conditions, temperature, wind speed, precipitation and cloud coverage affect accuracy and errors?
    Data from OpenWeatherMap API, fetched every hour.
    """)
    
    # Get weather data
    weather_query = """
    WITH weather_data AS (
        SELECT 
            timestamp,
            temperature,
            humidity,
            wind_speed,
            weather_condition,
            precipitation,
            cloud_coverage
        FROM `nico-playground-384514.transport_predictions.weather_data`
    ),
    prediction_data AS (
        SELECT 
            TIMESTAMP_TRUNC(arrival_timestamp, HOUR) as hour,
            line,
            COUNT(*) as total_predictions,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage,
            ROUND(AVG(error_seconds), 2) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 2) as avg_abs_error
        FROM `nico-playground-384514.transport_predictions.any_errors`
        GROUP BY 1, 2
    )
    SELECT 
        w.timestamp,
        w.temperature,
        w.humidity,
        w.wind_speed,
        w.weather_condition,
        w.precipitation,
        w.cloud_coverage,
        p.line,
        p.total_predictions,
        p.accuracy_percentage,
        p.avg_error,
        p.avg_abs_error
    FROM weather_data w
    LEFT JOIN prediction_data p
    ON w.timestamp = p.hour
    ORDER BY w.timestamp DESC
    """
    
    weather_df = get_cached_query(weather_query)
    
    if not weather_df.empty:
        # First row: Bar plots for weather condition and temperature bins
        col1, col2 = st.columns(2)
        
        with col1:
            # Weather Condition vs Accuracy
            weather_accuracy = weather_df.groupby('weather_condition').agg({
                'accuracy_percentage': 'mean',
                'total_predictions': 'sum',
                'avg_error': lambda x: round((x * weather_df.loc[x.index, 'total_predictions']).sum() / weather_df.loc[x.index, 'total_predictions'].sum(), 1),
                'avg_abs_error': lambda x: round((x * weather_df.loc[x.index, 'total_predictions']).sum() / weather_df.loc[x.index, 'total_predictions'].sum(), 1)
            }).reset_index()
            fig = px.bar(weather_accuracy, 
                        x='weather_condition', 
                        y='accuracy_percentage',
                        title='Prediction Accuracy by Weather Condition',
                        labels={'weather_condition': 'Weather Condition',
                               'accuracy_percentage': 'Accuracy % (±30s)',
                               'avg_error': 'Average Error (seconds)',
                               'avg_abs_error': 'Average Absolute Error (seconds)'},
                               hover_data=['avg_error','avg_abs_error'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Temperature Bins Analysis
            temp_bins = [-float('inf'), 5, 10, 15, 20, float('inf')]
            temp_labels = ['below_5', '5_to_10', '10_to_15', '15_to_20', 'above_20']
            display_labels = {
                'below_5': '<5°C',
                '5_to_10': '5-10°C',
                '10_to_15': '10-15°C',
                '15_to_20': '15-20°C',
                'above_20': '>20°C'
            }
            
            weather_df['temp_bin'] = pd.cut(weather_df['temperature'], 
                                          bins=temp_bins,
                                          labels=temp_labels)
            
            temp_bin_stats = weather_df.groupby('temp_bin').agg({
                'accuracy_percentage': 'mean',
                'total_predictions': 'sum',
                'avg_error': lambda x: round(x.mean(), 1),
                'avg_abs_error': lambda x: round(x.mean(), 1)
            }).reset_index()
            
            temp_bin_stats['display_bin'] = temp_bin_stats['temp_bin'].map(display_labels)
            
            fig = px.bar(temp_bin_stats, 
                        x='display_bin', 
                        y='accuracy_percentage',
                        title='Average Accuracy by Temperature Range',
                        labels={'display_bin': 'Temperature Range',
                               'accuracy_percentage': 'Accuracy % (±30s)',
                               'avg_error': 'Average Error (seconds)',
                               'avg_abs_error': 'Average Absolute Error (seconds)'
                               },
                               hover_data=['avg_error','avg_abs_error'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Second row: Wind speed and precipitation bar plots
        col1, col2 = st.columns(2)
        
        with col1:
            # Wind speed bins
            wind_bins = pd.cut(
                weather_df['wind_speed'],
                bins=[-float('inf'), 5, 10, 15, 20, float('inf')],
                labels=['0-5 mph', '5-10 mph', '10-15 mph', '15-20 mph', '20+ mph']
            )
            wind_group = weather_df.groupby(wind_bins).agg({
                'accuracy_percentage': lambda x: round(x.mean(), 1),
                'total_predictions': 'sum',
                'avg_error': lambda x: round(x.mean(), 1),
                'avg_abs_error': lambda x: round(x.mean(), 1)
            }).reset_index()
            
            fig = px.bar(
                wind_group,
                x='wind_speed',
                y='accuracy_percentage',
                title="Prediction Accuracy by Wind Speed",
                labels={'wind_speed': 'Wind Speed', 'accuracy_percentage': 'Accuracy % (±30s)', 'avg_error': 'Average Error (seconds)', 'avg_abs_error': 'Average Absolute Error (seconds)'},
                hover_data=['avg_error','avg_abs_error'])
            fig.update_layout(height=400, showlegend=False, yaxis=dict(range=[0, 100], title='Accuracy %'))
            fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Precipitation bins
            precip_bins = pd.cut(
                weather_df['precipitation'],
                bins=[-float('inf'), 0, 0.5, 2, 4, float('inf')],
                labels=['No Rain', 'Light Rain (<0.5mm)', 'Moderate Rain (0.5-2mm)', 'Heavy Rain (2-4mm)', 'Very Heavy Rain (>4mm)']
            )
            precip_group = weather_df.groupby(precip_bins).agg({
                'accuracy_percentage': lambda x: round(x.mean(), 1),
                'total_predictions': 'sum',
                'avg_error': lambda x: round(x.mean(), 1),
                'avg_abs_error': lambda x: round(x.mean(), 1)
            }).reset_index()
            
            fig = px.bar(
                precip_group,
                x='precipitation',
                y='accuracy_percentage',
                title="Prediction Accuracy by Precipitation",
                labels={'precipitation': 'Precipitation', 'accuracy_percentage': 'Accuracy % (±30s)', 'avg_error': 'Average Error (seconds)', 'avg_abs_error': 'Average Absolute Error (seconds)'},
                hover_data=['avg_error','avg_abs_error'])
            fig.update_layout(height=400, showlegend=False, yaxis=dict(range=[0, 100], title='Accuracy %'))
            fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        # Third row: Scatter plots for temperature and humidity
        col1, col2 = st.columns(2)
        
        with col1:
            # Temperature vs Prediction Accuracy
            fig = px.scatter(weather_df, 
                           x='temperature', 
                           y='accuracy_percentage',
                           color='line',
                           title='Temperature vs Prediction Accuracy',
                           labels={'temperature': 'Temperature (°C)',
                                 'accuracy_percentage': 'Accuracy % (±30s)'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Humidity vs Accuracy
            fig = px.scatter(weather_df, 
                           x='humidity', 
                           y='accuracy_percentage',
                           color='line',
                           title='Humidity vs Prediction Accuracy',
                           labels={'humidity': 'Humidity (%)',
                                 'accuracy_percentage': 'Accuracy % (±30s)'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Fourth row: Correlation matrix
        # Calculate correlation between weather variables and accuracy for each line
        correlations = []
        for line in weather_df['line'].unique():
            line_data = weather_df[weather_df['line'] == line]
            if len(line_data) > 1:  # Need at least 2 points for correlation
                temp_corr = line_data['temperature'].corr(line_data['accuracy_percentage'])
                humidity_corr = line_data['humidity'].corr(line_data['accuracy_percentage'])
                wind_corr = line_data['wind_speed'].corr(line_data['accuracy_percentage'])
                precip_corr = line_data['precipitation'].corr(line_data['accuracy_percentage'])
                correlations.append({
                    'line': line,
                    'temperature_correlation': round(temp_corr, 2),
                    'humidity_correlation': round(humidity_corr, 2),
                    'wind_correlation': round(wind_corr, 2),
                    'precipitation_correlation': round(precip_corr, 2)
                })
        
        # Create correlation heatmap
        corr_df = pd.DataFrame(correlations)
        if not corr_df.empty:
            fig = px.bar(corr_df, 
                        x='line', 
                        y=['temperature_correlation', 'humidity_correlation', 'wind_correlation', 'precipitation_correlation'],
                        title='Correlation between Weather Variables and Prediction Accuracy',
                        labels={'value': 'Correlation Coefficient',
                               'variable': 'Weather Variable'})
            st.plotly_chart(fig, use_container_width=True)
        
        
        # Temperature and Weather Condition Analysis
        st.subheader("Temperature and Weather Condition Analysis")
        
        # Filter out rows with NaN weather conditions
        weather_df = weather_df.dropna(subset=['weather_condition'])
        
        # Create a pivot table of average accuracy by temperature and weather condition
        pivot_data = weather_df.pivot_table(
            values='accuracy_percentage',
            index='weather_condition',
            columns='temp_bin',
            aggfunc='mean'
        ).round(2)
        
        # Ensure all temperature bins exist in the pivot table
        for label in temp_labels:
            if label not in pivot_data.columns:
                pivot_data[label] = None
        
        # Reorder columns to match the expected order
        pivot_data = pivot_data.reindex(columns=temp_labels)
        
        # Rename columns for display
        pivot_data.columns = [display_labels[col] for col in pivot_data.columns]
        
        pivot_data.index.name = 'Weather Condition'
        
        st.write("Average Accuracy by Temperature and Weather Condition")
        st.dataframe(
            pivot_data,
            use_container_width=True,
            height=200,  # Make the table taller
            hide_index=False  # Show the index (weather conditions)
        )

with tab13:
    st.header("Event Impact Analysis")
    st.markdown("""
        How do days with events vs. non event days impact accuracy and errors?   
        Are there many anomalies in the hour leading up to an event, and after these events?   
        If I wanted to make this more accurate, would use PredictHQ API, but it's not free.
        Data from Ticketmaster API, fetched every month.
        Will add Premier League data soon.
    """)

    
    # Query to analyze event impact
    event_query = """
    WITH event_stats AS (
        SELECT 
            DATE(arrival_timestamp) as date,
            EXTRACT(HOUR FROM arrival_timestamp) as hour,
            line,
            COUNT(*) as total_predictions,
            ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage,
            ROUND(AVG(error_seconds), 1) as avg_error,
            ROUND(AVG(ABS(error_seconds)), 1) as avg_abs_error
        FROM `nico-playground-384514.transport_predictions.any_errors`
        GROUP BY date, hour, line
    ),
    event_data AS (
        SELECT 
            DATE(event_date) as date,
            EXTRACT(HOUR FROM event_date) as event_hour,
            event_name,
            venue_name,
            COUNT(*) OVER (PARTITION BY DATE(event_date)) as events_per_day
        FROM `nico-playground-384514.transport_predictions.events`
    ),
    event_windows AS (
        SELECT 
            e.date,
            e.hour,
            e.line,
            e.total_predictions,
            e.accuracy_percentage,
            e.avg_error,
            e.avg_abs_error,
            d.event_name,
            d.venue_name,
            d.event_hour,
            d.events_per_day,
            CASE 
                WHEN d.date IS NOT NULL 
                AND (
                    -- Handle before window (2 hours before)
                    (d.event_hour >= 2 AND e.hour BETWEEN d.event_hour - 2 AND d.event_hour)
                    OR (d.event_hour < 2 AND e.hour BETWEEN 0 AND d.event_hour)
                    -- Handle after window (2-4 hours after)
                    OR (d.event_hour <= 20 AND e.hour BETWEEN d.event_hour + 2 AND d.event_hour + 4)
                    OR (d.event_hour > 20 AND e.hour BETWEEN d.event_hour + 2 AND 23)
                )
                THEN 'Event Window'
                WHEN d.date IS NOT NULL THEN 'Event Day (Outside Window)'
                ELSE 'Non-Event Day'
            END as time_window
        FROM event_stats e
        LEFT JOIN event_data d
        ON e.date = d.date
    ),
    anomaly_stats AS (
        SELECT 
            AVG(accuracy_percentage) as mean_accuracy,
            STDDEV(accuracy_percentage) as std_accuracy
        FROM event_windows
    ),
    final_data AS (
        SELECT 
            w.*,
            CASE 
                WHEN w.accuracy_percentage < (a.mean_accuracy - 1.5 * a.std_accuracy)
                AND w.total_predictions > 10 THEN 'Anomaly'
                ELSE 'Normal'
            END as anomaly_status
        FROM event_windows w
        CROSS JOIN anomaly_stats a
    ),
    anomaly_counts AS (
        SELECT 
            COUNTIF(anomaly_status = 'Anomaly') as total_anomalies,
            COUNTIF(anomaly_status = 'Anomaly' AND time_window = 'Event Window') as event_window_anomalies,
            COUNTIF(anomaly_status = 'Anomaly' AND (time_window = 'Event Day (Outside Window)' OR time_window = 'Non-Event Day')) as outside_window_anomalies
        FROM final_data
    )
    SELECT 
        f.*,
        a.event_window_anomalies,
        a.outside_window_anomalies,
        a.total_anomalies
    FROM final_data f
    CROSS JOIN anomaly_counts a
    ORDER BY date, hour, line
    """
    event_df = get_cached_query(event_query)
    
    if not event_df.empty:
        # Check if we have any event days
        has_events = event_df['time_window'].notna().any()
        
        if has_events:
            # Create event day categories
            event_df['event_category'] = event_df.apply(
                lambda x: f'Event Day ({int(x["events_per_day"])} events)' 
                if pd.notna(x['events_per_day']) 
                else 'Non-Event Day', 
                axis=1
            )
            
            # Calculate average metrics by event category
            category_stats = event_df.groupby(['event_category', 'line']).agg({
                'accuracy_percentage': 'mean',
                'avg_abs_error': 'mean',
                'total_predictions': 'sum'
            }).round(1).reset_index()
            
            # Create accuracy bar plot
            fig_accuracy = px.bar(
                category_stats,
                x='event_category',
                y='accuracy_percentage',
                color='line',
                title='Average Prediction Accuracy by Event Category',
                labels={
                    'event_category': 'Day Category',
                    'accuracy_percentage': 'Average Accuracy % (±30s)',
                    'line': 'Tube Line'
                },
                barmode='group'
            )
            st.plotly_chart(fig_accuracy, use_container_width=True)
            
            # Create error bar plot
            fig_error = px.bar(
                category_stats,
                x='event_category',
                    y='avg_abs_error',
                color='line',
                title='Average Prediction Error by Event Category',
                labels={
                    'event_category': 'Day Category',
                    'avg_abs_error': 'Average Absolute Error (seconds)',
                    'line': 'Tube Line'
                },
                barmode='group'
            )
            st.plotly_chart(fig_error, use_container_width=True)
            
            # Show venue statistics during event windows
            st.subheader("Venue Performance During Event Windows (2 hours before and 4 hours after start)")
            venue_stats = event_df[event_df['time_window'] == 'Event Window'].groupby('venue_name').agg({
                'total_predictions': 'sum',
                'accuracy_percentage': 'mean',
                'avg_abs_error': 'mean'
            }).round(1).reset_index()
            venue_stats = venue_stats.sort_values('accuracy_percentage', ascending=False)
            # Rename columns for better display
            venue_stats = venue_stats.rename(columns={
                'venue_name': 'Venue Name',
                'total_predictions': 'Total Predictions',
                'accuracy_percentage': 'Accuracy % (±30s)',
                'avg_abs_error': 'Average Absolute Error (seconds)'
            })
            
            st.dataframe(venue_stats)
            
            # Show anomalies during event windows
            st.subheader("Anomalies During Event Windows (min 10 predictions)")
            anomalies = event_df[
                (event_df['anomaly_status'] == 'Anomaly') & 
                (event_df['time_window'] == 'Event Window')
            ]
            if not anomalies.empty:
                # Create a mapping of old to new column names
                column_mapping = {
                    'date': 'Date',
                    'hour': 'Hour',
                    'line': 'Line',
                    'avg_abs_error': 'Average Absolute Error (seconds)',
                    'total_predictions': 'Total Predictions',
                    'accuracy_percentage': 'Accuracy % (±30s)',
                    'event_name': 'Event Name',
                    'venue_name': 'Venue Name',
                    'event_hour': 'Event Hour',
                    'events_per_day': 'Events per Day',
                    'event_category': 'Event Category'
                }
                
                # Rename columns first
                anomalies = anomalies.rename(columns=column_mapping)
                
                # Then remove unwanted columns
                display_columns = [col for col in anomalies.columns if col not in ['time_window', 'avg_error', 'anomaly_status', 'event_window_anomalies', 'outside_window_anomalies', 'total_anomalies']]
                
                st.dataframe(anomalies[display_columns])
    else:
                st.write("No anomalies detected during event windows")


            # Add anomaly comparison metrics
    st.subheader("Anomaly Distribution")
    if event_df['total_anomalies'].iloc[0] > 0:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Anomalies in Event Windows",
                        f"{event_df['event_window_anomalies'].iloc[0]}",
                        f"{round(event_df['event_window_anomalies'].iloc[0] / event_df['total_anomalies'].iloc[0] * 100, 1)}% of total"
                    )
                with col2:
                    st.metric(
                        "Anomalies Outside Event Windows",
                        f"{event_df['outside_window_anomalies'].iloc[0]}",
                        f"{round(event_df['outside_window_anomalies'].iloc[0] / event_df['total_anomalies'].iloc[0] * 100, 1)}% of total"
                    )
    else:
            st.info("No event data available for analysis. Showing general accuracy trends instead.")
            
            # Show general accuracy trends over time
            st.subheader("Prediction Accuracy Trends")