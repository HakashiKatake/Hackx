import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor

# Load dataset from CSV
data = pd.read_csv("./datasetPrepairation/processedDatasets/bdm.csv")

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

# Function to predict based on input height
def predict_parameters(height):
    height_scaled = scaler.transform([[height]])
    prediction = model.predict(height_scaled)
    
    # Convert prediction to DataFrame
    pred_df = pd.DataFrame(prediction, columns=y.columns)
    
    # Decode 'Size' back to original labels
    pred_df["Size"] = label_encoder.inverse_transform(pred_df["Size"].round().astype(int))
    
    # Display results
    print("\nPredicted Parameters:")
    print(pred_df.to_string(index=False))

# Get user input for height
try:
    input_height = int(input("Enter height (in cm): "))
    predict_parameters(input_height)
except ValueError:
    print("Invalid input. Please enter an integer height.")
