"""
Comprehensive Body Measurements Predictor with Brand Comparisons
Created by: RohanVashisht1234
Created on: 2025-02-22 21:26:00 UTC

This application provides:
1. Body measurements predictions based on height
2. Brand-specific size recommendations
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

# Constants
CURRENT_TIME = "2025-02-22 21:26:00"
CURRENT_USER = "RohanVashisht1234"
CSV_PATH = '/Users/rohanvashisht/Hackx/datasetPrepairation/processedDatasets/bdm.csv'
SIZE_CHARTS_PATH = 'size_charts.json'

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



class ShirtPredictor:
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.scaler = StandardScaler()
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
        features = np.array([[height]])
        features_scaled = self.scaler.transform(features)
        
        predictions = {
            "input": {
                "height": float(height),
                "unit": "cm",
                "timestamp_utc": CURRENT_TIME,
                "user": CURRENT_USER
            },
            "shirt_predictions": {},
            "model_accuracies": {}
        }
        
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
    


class BrandSizePredictor:
    def __init__(self):
        with open(SIZE_CHARTS_PATH, 'r') as f:
            self.brand_charts = json.load(f)
    
    def find_matching_sizes(self, measurements):
        results = {
            "input_measurements": {
                "chest": measurements["chest"],
                "waist": measurements["waist"],
                "shoulder": measurements["shoulder"],
                "unit": "cm"
            },
            "brand_recommendations": [],
            "timestamp_utc": CURRENT_TIME,
            "user": CURRENT_USER
        }
        
        for brand in self.brand_charts:
            brand_result = {
                "brand": brand["brand"],
                "matching_sizes": []
            }
            
            for size in brand["sizes"]:
                if (size["chest"][0] <= measurements["chest"] <= size["chest"][1] and
                    size["waist"][0] <= measurements["waist"] <= size["waist"][1] and
                    size["shoulder"][0] <= measurements["shoulder"] <= size["shoulder"][1]):
                    
                    brand_result["matching_sizes"].append({
                        "size": size["label"],
                        "fit_details": {
                            "chest_range": size["chest"],
                            "waist_range": size["waist"],
                            "shoulder_range": size["shoulder"]
                        }
                    })
            
            if brand_result["matching_sizes"]:
                results["brand_recommendations"].append(brand_result)
        
        return results
    


# Initialize predictors
shirt_predictor = ShirtPredictor()
shirt_predictor.train()
brand_predictor = BrandSizePredictor()

def predict_shirt_measurements(height, weight=None, body_type=None):
    """Gradio interface function for shirt predictions"""
    try:
        predictions = shirt_predictor.predict(height, weight, body_type)
        return json.dumps(predictions, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "timestamp_utc": CURRENT_TIME,
            "user": CURRENT_USER
        }, indent=2)

def predict_brand_sizes(chest, waist, shoulder):
    """Gradio interface function for brand size predictions"""
    try:
        measurements = {
            "chest": float(chest),
            "waist": float(waist),
            "shoulder": float(shoulder)
        }
        predictions = brand_predictor.find_matching_sizes(measurements)
        return json.dumps(predictions, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "timestamp_utc": CURRENT_TIME,
            "user": CURRENT_USER
        }, indent=2)
    


# Create Gradio interface with tabs
with gr.Blocks(title="Body Measurements Predictor") as demo:
    gr.Markdown(f"""
    # Body Measurements Predictor
    Created by: {CURRENT_USER}
    Last Updated: {CURRENT_TIME}
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
        """)
    
    with gr.Tab("Brand Size Finder"):
        with gr.Row():
            with gr.Column():
                chest_input = gr.Number(
                    label="Chest Circumference (cm)",
                    minimum=80,
                    maximum=120,
                    step=0.5,
                    value=95
                )
                waist_input = gr.Number(
                    label="Waist Circumference (cm)",
                    minimum=60,
                    maximum=110,
                    step=0.5,
                    value=80
                )
                shoulder_input = gr.Number(
                    label="Shoulder Width (cm)",
                    minimum=35,
                    maximum=55,
                    step=0.5,
                    value=43
                )
                brand_predict_button = gr.Button("Find Matching Sizes")
            
            with gr.Column():
                brand_output_json = gr.JSON(label="Brand Size Recommendations")
        
        brand_predict_button.click(
            fn=predict_brand_sizes,
            inputs=[chest_input, waist_input, shoulder_input],
            outputs=brand_output_json
        )
        
        gr.Markdown("""
        ### Instructions:
        1. Enter your measurements:
           - Chest circumference
           - Waist circumference
           - Shoulder width
        2. Click "Find Matching Sizes" to see which sizes fit you across different brands
        """)

if __name__ == "__main__":
    logger.info("Starting Gradio interface...")
    demo.launch()