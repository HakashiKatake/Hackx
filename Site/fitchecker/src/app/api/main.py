import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sanic import Sanic
from sanic.response import json
from sanic.request import Request

# Initialize Sanic app
app = Sanic("BodyMeasurementPredictionAPI")

@app.listener('before_server_start')
async def initialize_model(app, loop):
    global model, scaler, label_encoder, y_columns
    # Load dataset from CSV
    data = pd.read_csv("/Users/rohanvashisht/Hackx/datasetPrepairation/processedDatasets/bdm.csv")

    # Drop rows with NaN values
    data = data.dropna()

    # Encode categorical variable (Size)
    label_encoder = LabelEncoder()
    data["Size"] = label_encoder.fit_transform(data["Size"])

    # Define features and targets
    X = data[["TotalHeight"]]
    y = data.drop(columns=["TotalHeight"])

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize height
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train model
    model = MultiOutputRegressor(RandomForestRegressor(random_state=42))
    model.fit(X_train, y_train)
    
    y_columns = y.columns

# Function to predict based on input height
def predict_parameters(height):
    height_scaled = scaler.transform([[height]])
    prediction = model.predict(height_scaled)
    
    # Convert prediction to DataFrame
    pred_df = pd.DataFrame(prediction, columns=y_columns)
    
    # Decode 'Size' back to original labels
    pred_df["Size"] = label_encoder.inverse_transform(pred_df["Size"].round().astype(int))
    
    return pred_df.iloc[0].to_dict()

@app.route("/predict", methods=["GET"])
async def predict(request: Request):
    try:
        total_height = float(request.args.get("TotalHeight"))
    except (TypeError, ValueError):
        return json({"error": "TotalHeight is a required parameter and must be a float."}, status=400)

    optional_params = [
        "Gender", "Age", "HeadCircumference", "ShoulderWidth", "ChestWidth", "Belly", "Waist", 
        "Hips", "ArmLength", "ShoulderToWaist", "WaistToKnee", "LegLength", "Weight", "Size"
    ]
    
    # Predict parameters based on TotalHeight
    prediction = predict_parameters(total_height)

    # Include optional parameters if provided
    response = {"TotalHeight": total_height}
    for param in optional_params:
        if param in request.args:
            response[param] = request.args.get(param)
        else:
            response[param] = prediction.get(param, None)
    
    return json(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)