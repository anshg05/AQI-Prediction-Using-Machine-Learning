import streamlit as st

st.set_page_config(
    page_title="Air Quality Analysis Portal",
    page_icon="🌍",
    layout="wide"
)

# Title and Description
st.title("🌍 Air Quality Analysis Portal")
st.markdown("""
### Welcome to the Air Quality Analysis Portal
Choose one of the following options to get started:
""")

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    st.info("### AQI Predictor")
    st.write("Predict Air Quality Index using key pollutant measurements.")
    if st.button("📊 Go to AQI Predictor", use_container_width=True):
        st.switch_page("pages/app.py")

with col2:
    st.info("### Data Analysis")
    st.write("Analyze and visualize your air quality datasets.")
    if st.button("📈 Go to Data Analysis", use_container_width=True):
        st.switch_page("pages/stream.py")

# Additional Information
st.markdown("""
---
### About the Portal

This portal offers two main functionalities:

1. **AQI Predictor**: 
   - Input key pollutant values
   - Get instant AQI predictions
   - Receive health recommendations

2. **Data Analysis**:
   - Upload your air quality datasets
   - Explore data through interactive visualizations
   - Perform detailed statistical analysis
""")