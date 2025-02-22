"""
Comprehensive Height-Based Prediction Model with Gradio Interface
Created by: RohanVashisht1234
Created on: 2025-02-22 21:01:00 UTC
"""

import gradio as gr
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, accuracy_score
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CSV_PATH = '/Users/rohanvashisht/Hackx/datasetPrepairation/processedDatasets/bdm.csv'

class ComprehensivePredictor:
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.scaler = StandardScaler()
        self.categorical_columns = ['Gender', 'Size', 'Fit']
        self.numerical_columns = [
            'Age', 'HeadCircumference', 'ShoulderWidth', 'ChestWidth',
            'Belly', 'Waist', 'Hips', 'ArmLength', 'ShoulderToWaist',
            'WaistToKnee', 'LegLength', 'Weight'
        ]
        self.accuracies = {}
        
    def train(self):
        logger.info("Loading and preparing data...")
        df = pd.read_csv(CSV_PATH)
        
        # Prepare input feature (Height)
        X = df[['TotalHeight']].values
        X = self.scaler.fit_transform(X)
        
        # Train models for categorical columns
        for col in self.categorical_columns:
            self.encoders[col] = LabelEncoder()
            encoded_values = self.encoders[col].fit_transform(df[col])
            self.models[col] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models[col].fit(X, encoded_values)
            
            # Calculate accuracy
            predictions = self.models[col].predict(X)
            self.accuracies[col] = round(accuracy_score(encoded_values, predictions) * 100, 2)
        
        # Train models for numerical columns
        for col in self.numerical_columns:
            self.models[col] = RandomForestRegressor(n_estimators=100, random_state=42)
            self.models[col].fit(X, df[col])
            
            # Calculate R² score
            predictions = self.models[col].predict(X)
            self.accuracies[col] = round(r2_score(df[col], predictions) * 100, 2)
        
        logger.info("Training completed successfully")
    
    def predict(self, height):
        height_scaled = self.scaler.transform([[float(height)]])
        
        predictions = {
            "input": {
                "height": float(height),
                "timestamp_utc": "2025-02-22 21:01:00",
                "user": "RohanVashisht1234"
            },
            "predictions": {},
            "model_accuracies": {}
        }
        
        # Predict categorical values
        for col in self.categorical_columns:
            pred = self.encoders[col].inverse_transform(
                self.models[col].predict(height_scaled)
            )[0]
            predictions["predictions"][col] = str(pred)
            predictions["model_accuracies"][col] = f"{self.accuracies[col]}%"
        
        # Predict numerical values
        for col in self.numerical_columns:
            pred = self.models[col].predict(height_scaled)[0]
            predictions["predictions"][col] = round(float(pred), 2)
            predictions["model_accuracies"][col] = f"{self.accuracies[col]}%"
        
        return predictions

# Initialize and train the predictor
predictor = ComprehensivePredictor()
predictor.train()

def predict_from_height(height):
    """Gradio interface function"""
    try:
        predictions = predictor.predict(height)
        return json.dumps(predictions, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "timestamp_utc": "2025-02-22 21:01:00",
            "user": "RohanVashisht1234"
        }, indent=2)

# Create Gradio interface
demo = gr.Interface(
    fn=predict_from_height,
    inputs=gr.Number(
        label="Enter Height (cm)",
        minimum=50,
        maximum=250,
        step=1
    ),
    outputs=gr.JSON(label="Comprehensive Predictions with Accuracies"),
    title="Comprehensive Body Measurements Predictor",
    description="Enter height in centimeters to predict all body measurements and characteristics.",
    theme=gr.themes.Soft(),
    examples=[[165], [175], [185]],
)

if __name__ == "__main__":
    logger.info("Starting Gradio interface...")
    demo.launch()