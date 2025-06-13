import streamlit as st
import pandas as pd
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
                    return pd.read_json(cached_result)
            except Exception as e:
                st.warning(f"Redis error: {str(e)}")
        
        # If Redis fails or no cache hit, execute query
        st.warning(f"Cache MISS at {datetime.now().strftime('%H:%M:%S')} - executing query")
        result = client.query(query).to_dataframe()
        
        # Try to cache in Redis for next time
        if redis_client is not None:
            try:
                # Cache for 1 hour
                redis_client.setex(cache_key, 3600, result.to_json())
                st.info("Cached result in Redis")
            except Exception as e:
                st.warning(f"Failed to cache: {str(e)}")
        
        return result
        
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        raise

st.title("Redis Cache Test Dashboard")

# Simple count query
count_query = """
SELECT COUNT(*) as total_count 
FROM `nico-playground-384514.transport_predictions.any_errors`
"""

# Simple accuracy query
accuracy_query = """
SELECT 
    line,
    COUNT(*) as total_predictions,
    ROUND(COUNTIF(ABS(error_seconds) <= 30) / COUNT(*) * 100, 1) as accuracy_percentage
FROM `nico-playground-384514.transport_predictions.any_errors`
GROUP BY line
ORDER BY total_predictions DESC
LIMIT 5
"""

# Display total count
st.subheader("Total Predictions")
count_df = get_cached_query(count_query)
st.metric("Total Predictions", f"{count_df['total_count'].iloc[0]:,}")

# Display accuracy by line
st.subheader("Accuracy by Line (Top 5)")
accuracy_df = get_cached_query(accuracy_query)
st.dataframe(accuracy_df)

# Add a refresh button
if st.button("Refresh Data"):
    st.experimental_rerun() 