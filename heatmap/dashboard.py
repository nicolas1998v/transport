import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from google.cloud import storage
from google.oauth2 import service_account
import json
from datetime import datetime, timedelta
import branca.colormap as cm
import numpy as np
from sklearn.neighbors import NearestNeighbors
import redis
import zlib
import base64
from io import StringIO
import io
import time

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

def get_cache_key(timestamp):
    """Generate a cache key for the current hour's data."""
    return f"heatmap:{timestamp}"

def get_cached_data(timestamp):
    """Try to get data from Redis cache."""
    if redis_client is None:
        return None
        
    try:
        cache_key = get_cache_key(timestamp)
        cached_result = redis_client.get(cache_key)
        if cached_result is not None:
            return decompress_data(cached_result)
    except Exception as e:
        st.warning(f"Redis error: {str(e)}")
    return None

def cache_data(data, timestamp):
    """Cache data in Redis."""
    if redis_client is None:
        return
        
    try:
        cache_key = get_cache_key(timestamp)
        compressed_data = compress_data(data)
        
        # Calculate seconds until next hour
        current_time = datetime.now() + timedelta(hours=1)  # Add 1 hour to match VM time
        next_hour = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        seconds_until_next_hour = int((next_hour - current_time).total_seconds())
        
        # Cache until next hour
        redis_client.setex(cache_key, seconds_until_next_hour, compressed_data)
    except Exception as e:
        st.warning(f"Redis error: {str(e)}")

# Initialize GCP client with credentials from Streamlit secrets
try:
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket('london-transport-data')
except Exception as e:
    st.error("""
    ⚠️ Error initializing Google Cloud client. Please check your credentials in Streamlit Cloud secrets.
    Make sure you've added the credentials in the correct TOML format.
    """)
    st.error(str(e))
    st.stop()

def create_map(data):
    """Create a map with color-coded points"""
    map_start = time.time()
    
    # Create base map
    m = folium.Map(
        location=[51.4995, -0.1248],
        zoom_start=11,
        tiles='cartodbpositron'
    )
    
    # Create color map
    colormap = cm.LinearColormap(
        colors=['green', 'yellow', 'orange', 'red'],
        vmin=data['duration'].min(),
        vmax=min(160, data['duration'].max()),
        caption='Journey Times (minutes)'
    )
    
    # Add source marker
    folium.Marker(
        [51.4995, -0.1248],
        popup='Houses of Parliament (SW1A 2JR)',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Optimize: Sample data if too many points
    if len(data) > 10000:
        # Sample data while preserving distribution
        data = data.sample(n=10000, random_state=42)
        st.info(f"📊 Note: Map shows 10,000 sampled points for better performance")
    
    # Optimize: Batch points using FeatureGroup
    points_start = time.time()
    fg = folium.FeatureGroup(name='Journey Times')
    
    # Prepare data for batch processing
    locations = data[['Latitude', 'Longitude']].values
    durations = data['duration'].values
    postcodes = data['postcode'].values
    
    # Create markers in batches
    for lat, lon, duration, postcode in zip(locations[:, 0], locations[:, 1], durations, postcodes):
        duration_capped = min(float(duration), 160)
        folium.CircleMarker(
            location=[lat, lon],
            radius=3,  # Slightly smaller radius
            color=colormap(duration_capped),
            fill=True,
            popup=f"{postcode}: {duration:.0f}min",  # Simplified popup
            weight=1  # Thinner border
        ).add_to(fg)
    
    fg.add_to(m)
    points_time = time.time() - points_start
    
    # Add color scale
    colormap.add_to(m)
    
    total_time = time.time() - map_start
    st.info(f"🗺️ Map creation metrics:\n"
           f"- Adding {len(data):,} points: {points_time:.2f} seconds\n"
           f"- Total map creation time: {total_time:.2f} seconds")
    
    return m

def filter_anomalies(df, threshold=0.3, min_neighbors=12):
    """Filter out points where journey time differs significantly from neighbors"""
    X = df[['Latitude', 'Longitude']].values
    n_neighbors = min_neighbors + 1
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)
    
    valid_points = []
    
    for i in range(len(df)):
        point = df.iloc[i]
        point_duration = point['duration']
        neighbors = df.iloc[indices[i][1:]]
        neighbor_durations = sorted(neighbors['duration'])
        
        diffs = np.diff(neighbor_durations)
        max_jump = max(diffs) if len(diffs) > 0 else 0
        
        closest_6_avg = np.mean(neighbor_durations[:6])
        furthest_6_avg = np.mean(neighbor_durations[-6:])
        overall_avg = np.mean(neighbor_durations)
        
        ratio_to_closest = point_duration / closest_6_avg if closest_6_avg > 0 else float('inf')
        ratio_to_overall = point_duration / overall_avg if overall_avg > 0 else float('inf')
        half_ratio = furthest_6_avg / closest_6_avg if closest_6_avg > 0 else float('inf')
        
        is_valid = (
            max_jump <= 15 and
            ratio_to_closest <= (1 + threshold) and 
            ratio_to_closest >= (1 - threshold) and
            ratio_to_overall <= (1 + threshold) and
            ratio_to_overall >= (1 - threshold) and
            half_ratio <= 1.5
        )
        
        if is_valid:
            valid_points.append(True)
        else:
            valid_points.append(False)
    
    return df[valid_points].copy()

@st.cache_data(ttl=3600)
def load_latest_results():
    """Load the most recent journey times results from both batches"""
    start_time = time.time()
    try:
        # Get current time and subtract 1 hour
        current_time = datetime.now() + timedelta(hours=1)
        target_hour = (current_time - timedelta(hours=1)).strftime('%Y%m%d_%H')
        
        # Try to get data from Redis cache first
        cache_start = time.time()
        cached_data = get_cached_data(target_hour)
        cache_time = time.time() - cache_start
        
        if cached_data is not None:
            st.info(f"✅ Data loaded from cache in {cache_time:.2f} seconds")
            return {
                'data': cached_data,
                'timestamp': target_hour,
                'total_processed': len(cached_data),
                'batches': [1, 2]  # Assume both batches are available when cached
            }
        
        with st.spinner('Loading journey time data...'):
            # List all result files
            gcs_start = time.time()
            blobs = list(bucket.list_blobs(prefix='results/journey_times_'))
            if not blobs:
                return None
            
            # Sort blobs by name (which includes timestamp)
            sorted_blobs = sorted(blobs, key=lambda x: x.name, reverse=True)
            
            # Get both batch files for the target hour
            batch1_blob = next((b for b in sorted_blobs if f'journey_times_{target_hour}_batch1' in b.name), None)
            batch2_blob = next((b for b in sorted_blobs if f'journey_times_{target_hour}_batch2' in b.name), None)
                        
            # Load and combine available batches
            all_data = []
            total_processed = 0
            available_batches = []
            
            if batch1_blob:
                data = json.loads(batch1_blob.download_as_string())
                all_data.extend(data['data'])
                total_processed += data['total_processed']
                available_batches.append(1)
            
            if batch2_blob:
                data = json.loads(batch2_blob.download_as_string())
                all_data.extend(data['data'])
                total_processed += data['total_processed']
                available_batches.append(2)
            
            if not all_data:
                st.warning(f"Dashboard closed for today ! Come back tomorrow ! 😎")
                return None
                
            # Load postcode coordinates
            postcode_blob = bucket.blob('london_postcodes_filtered.csv')
            postcodes_df = pd.read_csv(io.BytesIO(postcode_blob.download_as_string()))
            
            # Merge journey times with postcode coordinates
            results_df = pd.DataFrame(all_data)
            merged_df = pd.merge(results_df, postcodes_df, 
                               left_on='postcode', 
                               right_on='Postcode', 
                               how='inner')
            
            gcs_time = time.time() - gcs_start
            
            # Cache the merged data
            cache_start = time.time()
            cache_data(merged_df, target_hour)
            cache_time = time.time() - cache_start
            
            total_time = time.time() - start_time
            st.info(f"⏱️ Performance metrics:\n"
                   f"- GCS data loading: {gcs_time:.2f} seconds\n"
                   f"- Caching data: {cache_time:.2f} seconds\n"
                   f"- Total loading time: {total_time:.2f} seconds")
            
            return {
                'data': merged_df,
                'timestamp': target_hour,
                'total_processed': total_processed,
                'batches': available_batches
            }
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

st.title('London Journey Times from Houses of Parliament')
st.caption('Fastest journey times from SW1A 2JR to all London postcodes, via tube, bus and walking')

# Update the timestamp display
results = load_latest_results()
if results:
    current_time = datetime.now()
    # Add 1 hour to match VM time
    current_time = current_time + timedelta(hours=1)
    last_update = current_time.replace(minute=0)
    next_update = current_time.replace(minute=0) + timedelta(hours=1)
    minutes_until_update = int((next_update - current_time).total_seconds() / 60)
    
    st.write(f"🕒 Last updated: {last_update.strftime('%Y-%m-%d %H:00')} | "
             f"Next update: {next_update.strftime('%H:00')} "
             f"({minutes_until_update} mins)")

# Display the current map
if results is not None:
    data = pd.DataFrame(results['data'])
    filtered_df = filter_anomalies(data)
    
    map_start = time.time()
    m = create_map(filtered_df)
    map_time = time.time() - map_start
    
    st.subheader('Journey Time Heatmap')
    st.caption(f"Showing {len(filtered_df):,} points out of {len(data):,} total valid postcodes")
    
    display_start = time.time()
    folium_static(m)
    display_time = time.time() - display_start
    
    st.info(f"📊 Display metrics:\n"
           f"- Map rendering time: {display_time:.2f} seconds\n"
           f"- Total visualization time: {map_time + display_time:.2f} seconds")
    
    # Show filtering stats
    total_points = len(data)
    valid_points = len(filtered_df)
    st.write(
        f"Filtered {total_points - valid_points:,} anomalous points "
        f"({((total_points - valid_points)/total_points)*100:.1f}%) "
    )
    
    # Show statistics
    st.subheader('Journey Time Statistics')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average Time", f"{filtered_df['duration'].mean():.0f} mins")
    with col2:
        st.metric("Median Time", f"{filtered_df['duration'].median():.0f} mins")
    with col3:
        st.metric("95th Percentile", f"{filtered_df['duration'].quantile(0.95):.0f} mins")
    with col4:
        st.metric("Valid Postcodes", f"{len(filtered_df):,}")