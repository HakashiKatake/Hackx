"""
Tabbed Body Measurements Predictor with Enhanced Shirt Predictions
Created by: RohanVashisht1234
Created on: 2025-02-22 21:11:59 UTC
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

class ShirtPredictor:
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.scaler = StandardScaler()
        # Shirt-relevant measurements
        self.categorical_columns = ['Size', 'Fit']
        self.numerical_columns = [
            'ChestWidth', 'ShoulderWidth', 'ArmLength',
            'ShoulderToWaist', 'Belly', 'Waist'
        ]
        self.accuracies = {}
        self.units = {
            'ChestWidth': 'cm',
            'ShoulderWidth': 'cm',
            'ArmLength': 'cm',
            'ShoulderToWaist': 'cm',
            'Belly': 'cm',
            'Waist': 'cm',
            'Weight': 'kg',
            'TotalHeight': 'cm'
        }
        
    def train(self):
        logger.info("Loading and preparing data...")
        df = pd.read_csv(CSV_PATH)
        
        # Prepare input features
        base_features = ['TotalHeight']
        X = df[base_features].values
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        
        # Train models for categorical columns
        for col in self.categorical_columns:
            self.encoders[col] = LabelEncoder()
            encoded_values = self.encoders[col].fit_transform(df[col])
            self.models[col] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models[col].fit(X_scaled, encoded_values)
            
            predictions = self.models[col].predict(X_scaled)
            self.accuracies[col] = round(accuracy_score(encoded_values, predictions), 4)
        
        # Train models for numerical columns
        for col in self.numerical_columns:
            self.models[col] = RandomForestRegressor(n_estimators=100, random_state=42)
            self.models[col].fit(X_scaled, df[col])
            
            predictions = self.models[col].predict(X_scaled)
            self.accuracies[col] = round(r2_score(df[col], predictions), 4)
        
        logger.info("Training completed successfully")
    
    def predict(self, height, weight=None, body_type=None):
        # Prepare input features
        features = np.array([[height]])
        features_scaled = self.scaler.transform(features)
        
        predictions = {
            "input": {
                "height": float(height),
                "unit": "cm",
                "timestamp_utc": "2025-02-22 21:11:59",
                "user": "RohanVashisht1234"
            },
            "shirt_predictions": {},
            "model_accuracies": {}
        }
        
        # Add optional inputs if provided
        if weight is not None:
            predictions["input"]["weight"] = float(weight)
            predictions["input"]["weight_unit"] = "kg"
        if body_type is not None:
            predictions["input"]["body_type"] = body_type
        
        # Predict categorical values
        for col in self.categorical_columns:
            pred = self.encoders[col].inverse_transform(
                self.models[col].predict(features_scaled)
            )[0]
            predictions["shirt_predictions"][col] = {
                "value": str(pred)
            }
            predictions["model_accuracies"][col] = self.accuracies[col]
        
        # Predict numerical values
        for col in self.numerical_columns:
            pred = self.models[col].predict(features_scaled)[0]
            predictions["shirt_predictions"][col] = {
                "value": round(float(pred), 2),
                "unit": self.units.get(col, "")
            }
            predictions["model_accuracies"][col] = self.accuracies[col]
        
        return predictions

# Initialize and train the predictor
predictor = ShirtPredictor()
predictor.train()

def predict_shirt_measurements(height, weight=None, body_type=None):
    """Gradio interface function for shirt predictions"""
    try:
        predictions = predictor.predict(height, weight, body_type)
        return json.dumps(predictions, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "timestamp_utc": "2025-02-22 21:11:59",
            "user": "RohanVashisht1234"
        }, indent=2)

# Create Gradio interface with tabs
with gr.Blocks(title="Body Measurements Predictor") as demo:
    gr.Markdown("""
    # Body Measurements Predictor
    Created by: RohanVashisht1234
    Last Updated: 2025-02-22 21:11:59 UTC
    """)
    
    with gr.Tab("Shirt Measurements"):
        with gr.Row():
            with gr.Column():
                height_input = gr.Number(
                    label="Height (cm) *",
                    minimum=50,
                    maximum=250,
                    step=1,
                    value=170
                )
                weight_input = gr.Number(
                    label="Weight (kg) (optional)",
                    minimum=30,
                    maximum=200,
                    step=0.1
                )
                body_type_input = gr.Dropdown(
                    label="Body Type (optional)",
                    choices=["Slim", "Regular", "Athletic", "Large"],
                    value=None
                )
                predict_button = gr.Button("Predict Shirt Measurements")
            
            with gr.Column():
                output_json = gr.JSON(label="Shirt Measurements Predictions")
        
        predict_button.click(
            fn=predict_shirt_measurements,
            inputs=[height_input, weight_input, body_type_input],
            outputs=output_json
        )
        
        gr.Markdown("""
        ### Instructions:
        1. Enter your height (required)
        2. Optionally enter your weight and select your body type
        3. Click "Predict Shirt Measurements" to get detailed predictions
        
        The predictions include:
        - Size and Fit recommendations
        - Detailed measurements (chest, shoulders, arms, etc.)
        - Model accuracy scores
        """)

if __name__ == "__main__":
    logger.info("Starting Gradio interface...")
    demo.launch()