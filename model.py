import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

def clean_data(df):
    df = df.replace('NA ', np.nan)
    
    for col in df.columns:
        if col != 'Timestamp':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna()
    return df

def prepare_model():
    # Load and clean data
    data = pd.read_csv('Data.csv')
    data = clean_data(data)
    
    # Select only the most important features
    key_features = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx']
    
    # Prepare features and target
    X = data[key_features]
    y = data['AQI']
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Initialize and train model with optimized parameters
    model = RandomForestRegressor(
        n_estimators=500,
        max_depth=20,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features='sqrt',
        bootstrap=True,
        random_state=42,
        n_jobs=-1
    )
    
    # Train the model
    model.fit(X_scaled, y)
    
    return model, scaler

def predict_aqi(model, scaler, input_data):
    # Scale the input data
    input_scaled = scaler.transform(input_data)
    # Make prediction
    prediction = model.predict(input_scaled)
    return prediction[0]