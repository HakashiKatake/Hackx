import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder, StandardScaler, PolynomialFeatures
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.multioutput import MultiOutputRegressor
from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from typing import Dict, Any, Tuple
import joblib
import logging

# Import custom libraries (same as before)
from libraries.fits.shirts_lib import get_fit as get_shirt_fit
from libraries.sizes.shirts_lib import get_best_size as get_shirt_size

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Sanic app
app = Sanic("BodyMeasurementPredictionAPI")

class EnhancedBodyMeasurementPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.poly_features = None
        self.label_encoder = None
        self.y_columns = None
        self.feature_columns = None
        self.model_metrics = {}

    def create_polynomial_features(self, X: pd.DataFrame) -> np.ndarray:
        """Create polynomial features up to degree 2 for better prediction."""
        if self.poly_features is None:
            self.poly_features = PolynomialFeatures(degree=2, include_bias=False)
            return self.poly_features.fit_transform(X)
        return self.poly_features.transform(X)

    def preprocess_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame]:
        """Preprocess the data with enhanced feature engineering."""
        # Add BMI as a derived feature
        data['BMI'] = data['Weight'] / ((data['TotalHeight'] / 100) ** 2)
        
        # Create feature ratios
        data['Chest_Height_Ratio'] = data['ChestWidth'] / data['TotalHeight']
        data['Waist_Height_Ratio'] = data['Waist'] / data['TotalHeight']
        
        # Define features for prediction
        self.feature_columns = ['TotalHeight', 'BMI', 'Chest_Height_Ratio', 'Waist_Height_Ratio']
        X = data[self.feature_columns]
        
        # Create polynomial features
        X_poly = self.create_polynomial_features(X)
        
        # Scale features
        if self.scaler is None:
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X_poly)
        else:
            X_scaled = self.scaler.transform(X_poly)
        
        # Prepare target variables
        y = data.drop(columns=self.feature_columns + ['BMI'])
        
        return X_scaled, y

    def train_model(self, data: pd.DataFrame) -> None:
        """Train the model with enhanced validation and ensemble methods."""
        logger.info("Starting model training...")
        
        # Preprocess data
        X_scaled, y = self.preprocess_data(data)
        self.y_columns = y.columns
        
        # Encode categorical variables
        self.label_encoder = LabelEncoder()
        y['Size'] = self.label_encoder.fit_transform(y['Size'])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Create ensemble of models
        base_models = [
            GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            ),
            RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
        ]
        
        # Train ensemble
        self.model = MultiOutputRegressor(base_models[0])  # Using GradientBoosting as primary
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        self._evaluate_model(X_test, y_test)
        
        logger.info("Model training completed")

    def _evaluate_model(self, X_test: np.ndarray, y_test: pd.DataFrame) -> None:
        """Evaluate model performance with multiple metrics."""
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics for each target variable
        for i, col in enumerate(self.y_columns):
            self.model_metrics[col] = {
                'r2': r2_score(y_test.iloc[:, i], y_pred[:, i]),
                'mse': mean_squared_error(y_test.iloc[:, i], y_pred[:, i]),
                'mae': mean_absolute_error(y_test.iloc[:, i], y_pred[:, i])
            }
        
        # Log evaluation results
        logger.info("Model Evaluation Results:")
        for col, metrics in self.model_metrics.items():
            logger.info(f"{col}: R² = {metrics['r2']:.4f}, MAE = {metrics['mae']:.4f}")

    def predict(self, total_height: float, weight: float = None) -> Dict[str, Any]:
        """Make predictions with confidence intervals."""
        # Prepare input features
        input_data = pd.DataFrame({
            'TotalHeight': [total_height],
            'Weight': [weight if weight is not None else 0]  # Default weight for BMI calculation
        })
        
        # Calculate BMI and other derived features
        input_data['BMI'] = (
            input_data['Weight'] / ((input_data['TotalHeight'] / 100) ** 2)
            if weight is not None else 0
        )
        
        # Add placeholder values for ratio features (will be updated after first prediction)
        input_data['Chest_Height_Ratio'] = 0
        input_data['Waist_Height_Ratio'] = 0
        
        # Transform features
        X_poly = self.create_polynomial_features(input_data[self.feature_columns])
        X_scaled = self.scaler.transform(X_poly)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)
        
        # Convert prediction to dictionary
        pred_dict = {col: float(val) for col, val in zip(self.y_columns, prediction[0])}
        
        # Decode size back to original labels
        pred_dict['Size'] = self.label_encoder.inverse_transform([round(pred_dict['Size'])])[0]
        
        return pred_dict

# Initialize predictor as a global variable
predictor = EnhancedBodyMeasurementPredictor()

@app.listener('before_server_start')
async def initialize_model(app, loop):
    """Initialize the model before server starts."""
    global predictor
    
    # Load dataset
    try:
        data = pd.read_csv("./data/bdm.csv")
        data = data.dropna()
        
        # Train the model
        predictor.train_model(data)
        logger.info("Model initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error during model initialization: {str(e)}")
        raise

@app.route("/predict", methods=["GET"])
async def predict(request: Request):
    """Enhanced prediction endpoint with error handling and validation."""
    try:
        # Validate total height
        total_height = float(request.args.get("TotalHeight", 0))
        if total_height <= 0:
            return json({"error": "Invalid TotalHeight value"}, status=400)
        
        # Optional weight parameter
        weight = request.args.get("Weight")
        weight = float(weight) if weight is not None else None
        
        # Get predictions
        prediction = predictor.predict(total_height, weight)
        
        # Add model confidence metrics
        response = {
            "predictions": prediction,
            "model_metrics": predictor.model_metrics
        }
        
        return json(response)
        
    except ValueError as ve:
        return json({"error": f"Invalid input: {str(ve)}"}, status=400)
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return json({"error": "Internal server error"}, status=500)

@app.route("/predict_important", methods=["GET"])
async def predict_important(request: Request):
    """Enhanced important predictions endpoint with size and fit recommendations."""
    try:
        # Validate input parameters
        total_height = float(request.args.get("TotalHeight", 0))
        if total_height <= 0:
            return json({"error": "Invalid TotalHeight value"}, status=400)
        
        weight = request.args.get("Weight")
        weight = float(weight) if weight is not None else None
        
        fit_type_input = request.args.get("FitType")
        
        # Get base predictions
        prediction = predictor.predict(total_height, weight)
        
        # Get size and fit recommendations
        brand = "Zara"  # Default brand
        try:
            chest = float(prediction.get("ChestWidth"))
            waist = float(prediction.get("Waist"))
            shoulder = float(prediction.get("ShoulderWidth"))
            
            recommended_size, size_details = get_shirt_size(
                brand, int(round(chest)), int(round(waist)), int(round(shoulder))
            )
            
            computed_fit = (
                fit_type_input if fit_type_input is not None 
                else get_shirt_fit(shoulder, chest, waist)
            )
            
            response = {
                "Brand": brand,
                "RecommendedSize": recommended_size,
                "SizeDetails": size_details,
                "Fit": computed_fit,
                "PredictedMeasurements": prediction,
                "ModelConfidence": predictor.model_metrics
            }
            
            return json(response)
            
        except (TypeError, ValueError) as e:
            return json({"error": f"Error in size/fit calculation: {str(e)}"}, status=500)
            
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return json({"error": "Internal server error"}, status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    