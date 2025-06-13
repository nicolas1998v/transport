import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery
import redis
import json
from datetime import datetime
import hashlib
import io

# Set page config first
st.set_page_config(page_title="Redis Cache Test", layout="wide")

client = bigquery.Client()

# Initialize Redis connection
redis_client = None
try:
    host = "redis-16505.c335.europe-west2-1.gce.redns.redis-cloud.com"
    port = 16505
    password = "TK0d2LZXE1umqarhMIM1tJsWD7LVHNdg"
    
    st.info(f"Connecting to Redis at {host}:{port}")
    
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
        st.success("Successfully connected to Redis without SSL")
    else:
        st.error("Failed to connect to Redis without SSL")
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

def get_cache_key(query):
    """Generate a consistent cache key for a query."""
    return f"query:{hashlib.md5(query.encode()).hexdigest()}"

def get_cached_query(query):
    """Try Redis first, fall back to direct query if Redis fails."""
    try:
        cache_key = get_cache_key(query)
        
        # Try Redis first
        if redis_client is not None:
            try:
                cached_result = redis_client.get(cache_key)
                if cached_result is not None:
                    st.success(f"Cache HIT at {datetime.now().strftime('%H:%M:%S')}")
                    # Parse the JSON string back to DataFrame
                    df = pd.read_json(cached_result)
                    # Ensure numeric columns are numeric
                    numeric_columns = ['accuracy_percentage', 'accuracy_percentage_60s', 'avg_error', 'avg_abs_error', 'total_predictions']
                    for col in numeric_columns:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    return df
            except Exception as e:
                st.warning(f"Redis error: {str(e)}")
        
        # If Redis fails or no cache hit, execute query
        st.warning(f"Cache MISS at {datetime.now().strftime('%H:%M:%S')} - executing query")
        result = client.query(query).to_dataframe()
        
        # Try to cache in Redis for next time
        if redis_client is not None:
            try:
                # Cache for 1 hour
                json_str = result.to_json(orient='records', date_format='iso')
                redis_client.setex(cache_key, 3600, json_str)
                st.info("Cached result in Redis")
            except Exception as e:
                st.warning(f"Failed to cache: {str(e)}")
        
        return result
        
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        raise

st.title("Redis Cache Test Dashboard")

# Test the day_line_query
st.subheader("Testing Day Line Query")
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
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Lines", len(day_line_df['line'].unique()))
    with col2:
        st.metric("Total Predictions", f"{day_line_df['total_predictions'].sum():,}")
    with col3:
        st.metric("Avg Accuracy", f"{day_line_df['accuracy_percentage'].mean():.1f}%")
    
    # Create a mapping of day numbers to names (1-7)
    day_names = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday'
    }
    
    # Map day numbers to names
    day_line_df['day_name'] = day_line_df['day_of_week'].map(day_names)
    
    # First aggregate any duplicate entries - use first() for error metrics
    agg_df = day_line_df.groupby(['line', 'day_name']).agg({
        'accuracy_percentage': 'mean',
        'accuracy_percentage_60s': 'mean',
        'avg_error': 'first',
        'avg_abs_error': 'first'
    }).reset_index()
    
    # Create pivot tables
    pivot_df = agg_df.pivot(index='line', columns='day_name', values='accuracy_percentage')
    error_df = agg_df.pivot(index='line', columns='day_name', values='avg_error')
    abs_error_df = agg_df.pivot(index='line', columns='day_name', values='avg_abs_error')
    
    # Reorder columns to match days of week
    all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_df = pivot_df.reindex(columns=all_days)
    error_df = error_df.reindex(columns=all_days)
    abs_error_df = abs_error_df.reindex(columns=all_days)
    
    # Display pivot tables with better formatting
    st.subheader("Accuracy by Line and Day (%)")
    st.dataframe(pivot_df.style.format("{:.1f}").background_gradient(cmap='RdYlGn', vmin=0, vmax=100))
    
    st.subheader("Average Error by Line and Day (seconds)")
    st.dataframe(error_df.style.format("{:.1f}").background_gradient(cmap='RdYlGn_r'))
    
    st.subheader("Average Absolute Error by Line and Day (seconds)")
    st.dataframe(abs_error_df.style.format("{:.1f}").background_gradient(cmap='RdYlGn_r'))
    
    # Create visualizations
    st.subheader("Accuracy Heatmap")
    fig = px.imshow(pivot_df,
                    labels=dict(x="Day of Week", y="Line", color="Accuracy (%)"),
                    color_continuous_scale='RdYlGn',
                    aspect="auto")
    st.plotly_chart(fig, use_container_width=True)
    
    # Show raw data in expandable section
    with st.expander("Show Raw Data"):
        st.dataframe(day_line_df)

# Add a refresh button
if st.button("Refresh Data"):
    st.experimental_rerun() 