import streamlit as st
import pandas as pd
from model import prepare_model, predict_aqi

# Page configuration
st.set_page_config(
    page_title="Air Quality Index Predictor",
    page_icon="🌬️",
    layout="centered"
)

# Main title
st.title("Air Quality Index Prediction System")
st.markdown("""
This system predicts Air Quality Index (AQI) based on key air pollutants. 
Enter values for the following major pollutants:
""")

# Load the model
@st.cache_resource
def load_model():
    model, scaler = prepare_model()
    return model, scaler

model, scaler = load_model()

# Create input form
with st.form("prediction_form"):
    st.subheader("Enter Pollutant Values")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        pm25 = st.number_input("PM2.5 (μg/m³)", 
                              help="Particulate matter less than 2.5 micrometers in diameter",
                              min_value=0.0, max_value=500.0, value=0.0)
        no2 = st.number_input("NO₂ (μg/m³)", 
                             help="Nitrogen Dioxide",
                             min_value=0.0, max_value=500.0, value=0.0)
        so2 = st.number_input("SO₂ (μg/m³)", 
                             help="Sulfur Dioxide",
                             min_value=0.0, max_value=500.0, value=0.0)
    
    with col2:
        pm10 = st.number_input("PM10 (μg/m³)", 
                              help="Particulate matter less than 10 micrometers in diameter",
                              min_value=0.0, max_value=500.0, value=0.0)
        co = st.number_input("CO (mg/m³)", 
                            help="Carbon Monoxide",
                            min_value=0.0, max_value=100.0, value=0.0)
    
    submit_button = st.form_submit_button("Predict AQI")

# Make prediction when form is submitted
if submit_button:
    # Prepare input data
    input_data = pd.DataFrame([[pm25, pm10, no2, co, so2]], 
                             columns=['PM2.5', 'PM10', 'NO', 'NO2', 'NOx'])
    
    # Get prediction
    prediction = predict_aqi(model, scaler, input_data)
    
    # Display prediction with color coding and interpretation
    st.subheader("Prediction Results")
    
    # Create columns for prediction display
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Predicted AQI", f"{prediction:.2f}")
    
    with col2:
        if prediction <= 50:
            st.success("Air Quality: Good ✅")
            interpretation = "Air quality is satisfactory, and air pollution poses little or no risk."
        elif prediction <= 100:
            st.info("Air Quality: Moderate 💫")
            interpretation = "Air quality is acceptable; however, some pollutants may be of concern for very sensitive individuals."
        elif prediction <= 150:
            st.warning("Air Quality: Unhealthy for Sensitive Groups ⚠️")
            interpretation = "Members of sensitive groups may experience health effects, but the general public is less likely to be affected."
        elif prediction <= 200:
            st.error("Air Quality: Unhealthy 🚫")
            interpretation = "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
        elif prediction <= 300:
            st.error("Air Quality: Very Unhealthy ❌")
            interpretation = "Health alert: everyone may experience more serious health effects."
        else:
            st.error("Air Quality: Hazardous ☠️")
            interpretation = "Health warnings of emergency conditions. The entire population is more likely to be affected."
    
    st.info(f"**Interpretation**: {interpretation}")
    
    # Display recommended actions
    st.subheader("Recommended Actions")
    if prediction <= 50:
        st.success("- Ideal conditions for outdoor activities\n- No special precautions needed")
    elif prediction <= 100:
        st.info("- Unusually sensitive people should consider reducing prolonged outdoor exertion\n- Open windows to ventilate indoor spaces")
    elif prediction <= 150:
        st.warning("- People with respiratory or heart conditions should limit outdoor exertion\n- Close windows to avoid outdoor air pollution")
    elif prediction <= 200:
        st.error("- Everyone should reduce outdoor activities\n- Wear masks when outdoors\n- Use air purifiers indoors")
    elif prediction <= 300:
        st.error("- Avoid outdoor activities\n- Wear N95 masks if outdoors\n- Keep all windows closed\n- Use air purifiers")
    else:
        st.error("- Stay indoors\n- Keep all windows and doors closed\n- Use air purifiers\n- Seek medical help if experiencing adverse symptoms")