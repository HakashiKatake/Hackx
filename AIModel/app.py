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
# Constants
CURRENT_TIME = "2025-02-22 21:39:09"
CURRENT_USER = "RohanVashisht1234"
CSV_PATH = 'bdm.csv'
SHIRT_SIZE_CHARTS_PATH = 'shirt_size_charts.json'
PANTS_SIZE_CHARTS_PATH = 'pants_size_charts.json'

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
        with open(SHIRT_SIZE_CHARTS_PATH, 'r') as f:
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
    



# pants
class PantsPredictor:
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.scaler = StandardScaler()
        self.categorical_columns = ['Size', 'Fit']
        self.numerical_columns = [
            'Waist', 'Hips', 'LegLength',
            'WaistToKnee', 'Belly'
        ]
        self.accuracies = {}
        self.units = {
            'Waist': 'cm',
            'Hips': 'cm',
            'LegLength': 'cm',
            'WaistToKnee': 'cm',
            'Belly': 'cm',
            'Weight': 'kg',
            'TotalHeight': 'cm'
        }
    
    def train(self):
        logger.info("Loading and preparing pants prediction models...")
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
        
        logger.info("Pants prediction models trained successfully")
    
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
            "pants_predictions": {},
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
            predictions["pants_predictions"][col] = {
                "value": str(pred)
            }
            predictions["model_accuracies"][col] = self.accuracies[col]
        
        # Predict numerical values
        for col in self.numerical_columns:
            pred = self.models[col].predict(features_scaled)[0]
            predictions["pants_predictions"][col] = {
                "value": round(float(pred), 2),
                "unit": self.units.get(col, "")
            }
            predictions["model_accuracies"][col] = self.accuracies[col]
        
        return predictions

class PantsSizePredictor:
    def __init__(self, size_charts_path=PANTS_SIZE_CHARTS_PATH):
        try:
            with open(size_charts_path, 'r') as f:
                self.brand_charts = json.load(f)
                logger.info(f"Successfully loaded {len(self.brand_charts)} brands from size charts")
                # Add debug logging for loaded size charts
                for brand in self.brand_charts:
                    logger.info(f"Loaded size chart for {brand['brand']}")
        except Exception as e:
            logger.error(f"Failed to load pants size charts: {str(e)}")
            self.brand_charts = []
    
    def find_matching_sizes(self, measurements):
        logger.info(f"Finding sizes for measurements: {measurements}")
        results = {
            "input_measurements": {
                "waist": measurements["waist"],
                "hips": measurements["hips"],
                "leg_length": measurements["leg_length"],
                "unit": "cm",
                "timestamp_utc": CURRENT_TIME,
                "user": CURRENT_USER
            },
            "brand_recommendations": []
        }
        
        for brand in self.brand_charts:
            brand_result = {
                "brand": brand["brand"],
                "matching_sizes": []
            }
            
            for size in brand["sizes"]:
                # Add tolerance of ±2cm for better matching
                waist_min = size["waist"][0] - 2
                waist_max = size["waist"][1] + 2
                hips_min = size["hips"][0] - 2
                hips_max = size["hips"][1] + 2
                leg_min = size["leg_length"][0] - 2
                leg_max = size["leg_length"][1] + 2
                
                # Debug logging for size checks
                logger.debug(f"""
                Checking {brand['brand']} size {size['label']}:
                Waist: {measurements['waist']} in range {waist_min}-{waist_max}
                Hips: {measurements['hips']} in range {hips_min}-{hips_max}
                Leg: {measurements['leg_length']} in range {leg_min}-{leg_max}
                """)
                
                # Check if measurements fall within the size ranges (with tolerance)
                if (waist_min <= measurements["waist"] <= waist_max and
                    hips_min <= measurements["hips"] <= hips_max and
                    leg_min <= measurements["leg_length"] <= leg_max):
                    
                    size_match = {
                        "size": size["label"],
                        "fit_details": {
                            "waist_range": f"{size['waist'][0]}-{size['waist'][1]} cm",
                            "hips_range": f"{size['hips'][0]}-{size['hips'][1]} cm",
                            "leg_length_range": f"{size['leg_length'][0]}-{size['leg_length'][1]} cm"
                        },
                        "fit_quality": {
                            "waist": "Perfect" if size["waist"][0] <= measurements["waist"] <= size["waist"][1] else "Slightly loose/tight",
                            "hips": "Perfect" if size["hips"][0] <= measurements["hips"] <= size["hips"][1] else "Slightly loose/tight",
                            "leg_length": "Perfect" if size["leg_length"][0] <= measurements["leg_length"] <= size["leg_length"][1] else "Slightly long/short"
                        }
                    }
                    brand_result["matching_sizes"].append(size_match)
                    logger.info(f"Found matching size {size['label']} for {brand['brand']}")
            
            if brand_result["matching_sizes"]:
                results["brand_recommendations"].append(brand_result)
        
        # Add debugging information
        if not results["brand_recommendations"]:
            logger.warning(f"No matching sizes found for measurements: {measurements}")
            results["debug_info"] = {
                "message": "No exact matches found. Consider these suggestions:",
                "suggestions": [
                    "Try measurements within these ranges:",
                    "Waist: 72-91 cm",
                    "Hips: 90-110 cm",
                    "Leg Length: 97-106 cm"
                ],
                "closest_matches": self._find_closest_matches(measurements)
            }
        
        return results
    
    def _find_closest_matches(self, measurements):
        closest_matches = []
        for brand in self.brand_charts:
            for size in brand["sizes"]:
                # Calculate how close this size is to the measurements
                waist_diff = min(abs(measurements["waist"] - size["waist"][0]), 
                               abs(measurements["waist"] - size["waist"][1]))
                hips_diff = min(abs(measurements["hips"] - size["hips"][0]),
                              abs(measurements["hips"] - size["hips"][1]))
                leg_diff = min(abs(measurements["leg_length"] - size["leg_length"][0]),
                             abs(measurements["leg_length"] - size["leg_length"][1]))
                
                if waist_diff <= 5 and hips_diff <= 5 and leg_diff <= 5:
                    closest_matches.append({
                        "brand": brand["brand"],
                        "size": size["label"],
                        "adjustments_needed": {
                            "waist": f"{waist_diff:+.1f} cm",
                            "hips": f"{hips_diff:+.1f} cm",
                            "leg_length": f"{leg_diff:+.1f} cm"
                        }
                    })
        
        return closest_matches[:3]  # Return top 3 closest matches



# Initialize pants predictors
pants_predictor = PantsPredictor()
pants_predictor.train()
pants_size_predictor = PantsSizePredictor()

def predict_pants_measurements(height, weight=None, body_type=None):
    """Gradio interface function for pants predictions based on height"""
    try:
        predictions = pants_predictor.predict(height, weight, body_type)
        return json.dumps(predictions, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "timestamp_utc": CURRENT_TIME,
            "user": CURRENT_USER
        }, indent=2)

def predict_pants_sizes(waist, leg_length, hips):
    """Gradio interface function for pants size predictions"""
    try:
        measurements = {
            "waist": float(waist),
            "leg_length": float(leg_length),
            "hips": float(hips)
        }
        predictions = pants_size_predictor.find_matching_sizes(measurements)
        return json.dumps(predictions, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "timestamp_utc": CURRENT_TIME,
            "user": CURRENT_USER
        }, indent=2)


def format_shirt_predictions(predictions):
    formatted = "### Shirt Measurements Predictions\n"
    formatted += f"**Height:** {predictions['input']['height']} cm\n"
    if 'weight' in predictions['input']:
        formatted += f"**Weight:** {predictions['input']['weight']} kg\n"
    if 'body_type' in predictions['input']:
        formatted += f"**Body Type:** {predictions['input']['body_type']}\n"
    formatted += "\n**Predictions:**\n"
    for key, value in predictions['shirt_predictions'].items():
        formatted += f"- **{key}:** {value['value']} {value.get('unit', '')}\n"
    return formatted

def format_brand_predictions(predictions):
    formatted = "### Brand Size Recommendations\n"
    formatted += f"**Chest:** {predictions['input_measurements']['chest']} cm\n"
    formatted += f"**Waist:** {predictions['input_measurements']['waist']} cm\n"
    formatted += f"**Shoulder:** {predictions['input_measurements']['shoulder']} cm\n"
    formatted += "\n**Recommendations:**\n"
    for brand in predictions['brand_recommendations']:
        formatted += f"- **Brand:** {brand['brand']}\n"
        for size in brand['matching_sizes']:
            formatted += f"  - **Size:** {size['size']}\n"
            formatted += f"    - **Chest Range:** {size['fit_details']['chest_range']}\n"
            formatted += f"    - **Waist Range:** {size['fit_details']['waist_range']}\n"
            formatted += f"    - **Shoulder Range:** {size['fit_details']['shoulder_range']}\n"
    return formatted

def format_pants_predictions(predictions):
    formatted = "### Pants Measurements Predictions\n"
    formatted += f"**Height:** {predictions['input']['height']} cm\n"
    if 'weight' in predictions['input']:
        formatted += f"**Weight:** {predictions['input']['weight']} kg\n"
    if 'body_type' in predictions['input']:
        formatted += f"**Body Type:** {predictions['input']['body_type']}\n"
    formatted += "\n**Predictions:**\n"
    for key, value in predictions['pants_predictions'].items():
        formatted += f"- **{key}:** {value['value']} {value.get('unit', '')}\n"
    return formatted

def format_pants_brand_predictions(predictions):
    formatted = "### Pants Size Recommendations\n"
    formatted += f"**Waist:** {predictions['input_measurements']['waist']} cm\n"
    formatted += f"**Hips:** {predictions['input_measurements']['hips']} cm\n"
    formatted += f"**Leg Length:** {predictions['input_measurements']['leg_length']} cm\n"
    formatted += "\n**Recommendations:**\n"
    for brand in predictions['brand_recommendations']:
        formatted += f"- **Brand:** {brand['brand']}\n"
        for size in brand['matching_sizes']:
            formatted += f"  - **Size:** {size['size']}\n"
            formatted += f"    - **Waist Range:** {size['fit_details']['waist_range']}\n"
            formatted += f"    - **Hips Range:** {size['fit_details']['hips_range']}\n"
            formatted += f"    - **Leg Length Range:** {size['fit_details']['leg_length_range']}\n"
    return formatted

# Update Gradio interface to use formatted predictions
with gr.Blocks(title="Body Measurements Predictor") as demo:
    gr.Markdown(f"""
    # Body Measurements Predictor
    Created by: {CURRENT_USER}
    Last Updated: {CURRENT_TIME}
    """)
    
    with gr.Tabs():
        # First Tab - Shirt Measurements
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
                    output_markdown = gr.Markdown(label="Shirt Measurements Predictions")
                with gr.Column(scale=2, min_width=300):
                    model3d = gr.Model3D(
                        value="jacket.glb",  # Path to your .glb file on server
                        clear_color=[0.0, 0.0, 0.0, 0.0],  # Transparent background
                        camera_position=[0, 0, 5],  # Initial camera position
                        visible=False  # Initially hidden
                    )
            
            def update_model_visibility(height, weight, body_type):
                predictions = format_shirt_predictions(
                    json.loads(predict_shirt_measurements(height, weight, body_type))
                )
                return predictions, gr.update(visible=True)
            
            predict_button.click(
                fn=update_model_visibility,
                inputs=[height_input, weight_input, body_type_input],
                outputs=[output_markdown, model3d]
            )
            
            gr.Markdown("""
            ### Instructions:
            1. Enter your height (required)
            2. Optionally enter your weight and select your body type
            3. Click "Predict Shirt Measurements" to get detailed predictions
            """)
        
        # Second Tab - Brand Size Finder (Shirts)
        with gr.Tab("Shirt Size Finder"):
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
                    brand_output_markdown = gr.Markdown(label="Brand Size Recommendations")
                with gr.Column(scale=2, min_width=300):
                    model3d = gr.Model3D(
                        value="jacket.glb",  # Path to your .glb file on server
                        clear_color=[0.0, 0.0, 0.0, 0.0],  # Transparent background
                        camera_position=[0, 0, 5],  # Initial camera position
                        visible=False  # Initially hidden
                    )
            
            def update_model_visibility(chest, waist, shoulder):
                predictions = format_brand_predictions(
                    json.loads(predict_brand_sizes(chest, waist, shoulder))
                )
                return predictions, gr.update(visible=True)
            
            brand_predict_button.click(
                fn=update_model_visibility,
                inputs=[chest_input, waist_input, shoulder_input],
                outputs=[brand_output_markdown, model3d]
            )
            
            gr.Markdown("""
            ### Instructions:
            1. Enter your measurements:
               - Chest circumference
               - Waist circumference
               - Shoulder width
            2. Click "Find Matching Sizes" to see which sizes fit you across different brands
            """)
        
        # Third Tab - Pants Measurements
        with gr.Tab("Pants Measurements"):
            with gr.Row():
                with gr.Column():
                    pants_height_input = gr.Number(
                        label="Height (cm) *",
                        minimum=50,
                        maximum=250,
                        step=1,
                        value=170
                    )
                    pants_weight_input = gr.Number(
                        label="Weight (kg) (optional)",
                        minimum=30,
                        maximum=200,
                        step=0.1
                    )
                    pants_body_type_input = gr.Dropdown(
                        label="Body Type (optional)",
                        choices=["Slim", "Regular", "Athletic", "Large"],
                        value=None
                    )
                    pants_predict_button = gr.Button("Predict Pants Measurements")
                
                with gr.Column():
                    pants_output_markdown = gr.Markdown(label="Pants Measurements Predictions")
                with gr.Column():
                    model3d = gr.Model3D(
                        value="pants.glb",  # Path to your .glb file on server
                        clear_color=[0.0, 0.0, 0.0, 0.0],  # Transparent background
                        camera_position=[0, 0, 5],  # Initial camera position
                        visible=False  # Initially hidden
                    )
            
            def update_model_visibility(height, weight, body_type):
                predictions = format_pants_predictions(
                    json.loads(predict_pants_measurements(height, weight, body_type))
                )
                return predictions, gr.update(visible=True)
            
            pants_predict_button.click(
                fn=update_model_visibility,
                inputs=[pants_height_input, pants_weight_input, pants_body_type_input],
                outputs=[pants_output_markdown, model3d]
            )
            
            gr.Markdown("""
            ### Instructions:
            1. Enter your height (required)
            2. Optionally enter your weight and select your body type
            3. Click "Predict Pants Measurements" to get detailed predictions
            """)
        
        # Fourth Tab - Pants Size Finder
        with gr.Tab("Pants Size Finder"):
            with gr.Row():
                with gr.Column():
                    pants_waist_input = gr.Number(
                        label="Waist Circumference (cm)",
                        minimum=60,
                        maximum=120,
                        step=0.5,
                        value=80
                    )
                    pants_leg_input = gr.Number(
                        label="Leg Length (cm)",
                        minimum=60,
                        maximum=120,
                        step=0.5,
                        value=98
                    )
                    pants_hips_input = gr.Number(
                        label="Hips Circumference (cm)",
                        minimum=80,
                        maximum=140,
                        step=0.5,
                        value=102
                    )
                    pants_brand_predict_button = gr.Button("Find Matching Pants Sizes")
                
                with gr.Column():
                    pants_brand_output_markdown = gr.Markdown(label="Pants Size Recommendations")
                with gr.Column():
                    model3d = gr.Model3D(
                        value="pants.glb",  # Path to your .glb file on server
                        clear_color=[0.0, 0.0, 0.0, 0.0],  # Transparent background
                        camera_position=[0, 0, 5],  # Initial camera position
                        visible=False  # Initially hidden
                    )
            
            def update_model_visibility(waist, leg_length, hips):
                predictions = format_pants_brand_predictions(
                    json.loads(predict_pants_sizes(waist, leg_length, hips))
                )
                return predictions, gr.update(visible=True)  # Fixed syntax error here
            
            pants_brand_predict_button.click(
                fn=update_model_visibility,
                inputs=[pants_waist_input, pants_leg_input, pants_hips_input],
                outputs=[pants_brand_output_markdown, model3d]
            )
            
            gr.Markdown("""
            ### Instructions:
            1. Enter your measurements:
               - Waist circumference
               - Leg length
               - Hips circumference
            2. Click "Find Matching Pants Sizes" to see which sizes fit you across different brands
            """)

if __name__ == "__main__":
    logger.info("Starting Gradio interface...")
    demo.launch()
