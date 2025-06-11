import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from google.cloud import storage
import json
from datetime import datetime, timedelta
import branca.colormap as cm
import io
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Initialize GCP client
storage_client = storage.Client()
bucket = storage_client.bucket('london-transport-data')

def create_map(data):
    """Create a map with color-coded points"""
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
    
    # Add points
    for idx, row in data.iterrows():
        duration_capped = min(float(row['duration']), 160)
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=4,
            color=colormap(duration_capped),
            fill=True,
            popup=f"Postcode: {row['postcode']}<br>Travel time: {row['duration']} mins"
        ).add_to(m)
    
    # Add color scale
    colormap.add_to(m)
    
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
    try:
        with st.spinner('Loading journey time data...'):
            # List all result files
            blobs = list(bucket.list_blobs(prefix='results/journey_times_'))
            if not blobs:
                return None
            
            # Sort blobs by name (which includes timestamp) and get the latest hour's files
            sorted_blobs = sorted(blobs, key=lambda x: x.name, reverse=True)
            latest_hour = sorted_blobs[0].name.split('journey_times_')[1].split('_batch')[0]
            latest_blobs = [b for b in sorted_blobs if latest_hour in b.name][:2]
            
            # Load and combine both batches
            all_data = []
            total_processed = 0
            
            for blob in latest_blobs:
                data = json.loads(blob.download_as_string())
                all_data.extend(data['data'])
                total_processed += data['total_processed']
            
            # Load postcode coordinates
            postcode_blob = bucket.blob('london_postcodes_filtered.csv')
            postcodes_df = pd.read_csv(io.BytesIO(postcode_blob.download_as_string()))
            
            # Merge journey times with postcode coordinates
            results_df = pd.DataFrame(all_data)
            merged_df = pd.merge(results_df, postcodes_df, 
                               left_on='postcode', 
                               right_on='Postcode', 
                               how='inner')
            
            return {
                'data': merged_df,
                'timestamp': latest_hour,
                'total_processed': total_processed
            }
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

st.title('London Journey Times from Houses of Parliament')
st.caption('Journey times from SW1A 2JR to all London postcodes')

# Update the timestamp display
results = load_latest_results()
if results:
    current_time = datetime.now()
    last_update = datetime.now() 
    next_update = current_time.replace(minute=0) + pd.Timedelta(hours=1)
    minutes_until_update = int((next_update - current_time).total_seconds() / 60)
    
    st.write(f"🕒 Last updated: {last_update.strftime('%Y-%m-%d %H:00')} | "
             f"Next update: {next_update.strftime('%H:00')} "
             f"({minutes_until_update} mins)")

# Display the current map
if results is not None:
    data = pd.DataFrame(results['data'])
    filtered_df = filter_anomalies(data)
    
    m = create_map(filtered_df)
    
    st.subheader('Journey Time Heatmap')
    st.caption(f"Showing 10,000 points out of {len(filtered_df):,} total valid postcodes")
    folium_static(m)
    
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