import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Test different import combinations
st.title("Trendline Dependency Test")

try:
    import statsmodels
    st.success(f"✅ statsmodels imported successfully: {statsmodels.__version__}")
except ImportError as e:
    st.error(f"❌ statsmodels import failed: {e}")

try:
    import plotly
    st.success(f"✅ plotly imported successfully: {plotly.__version__}")
except ImportError as e:
    st.error(f"❌ plotly import failed: {e}")

# Create sample data
np.random.seed(42)
x = np.random.randn(100)
y = 2 * x + np.random.randn(100) * 0.5
df = pd.DataFrame({'x': x, 'y': y})

st.write("Sample data:")
st.dataframe(df.head())

# Test trendline functionality
st.subheader("Testing Trendline Functionality")

try:
    fig = px.scatter(df, x='x', y='y', title="Test Scatter with Trendline", trendline="ols")
    st.plotly_chart(fig)
    st.success("✅ Trendline works!")
except Exception as e:
    st.error(f"❌ Trendline failed: {e}")
    st.info("This means we need to try different package versions")

# Test manual trendline as fallback
st.subheader("Manual Trendline Fallback")
try:
    # Calculate trendline manually
    z = np.polyfit(df['x'], df['y'], 1)
    p = np.poly1d(z)
    df['trendline'] = p(df['x'])
    
    fig_manual = px.scatter(df, x='x', y='y', title="Manual Trendline")
    fig_manual.add_scatter(x=df['x'], y=df['trendline'], mode='lines', name='Trendline', line=dict(color='red'))
    st.plotly_chart(fig_manual)
    st.success("✅ Manual trendline works!")
except Exception as e:
    st.error(f"❌ Manual trendline failed: {e}")

st.info("""
**Next steps:**
1. If trendline fails, we'll need to try different package versions
2. If manual trendline works, we can use that as a fallback
3. We can test specific version combinations here before updating requirements.txt
""") 