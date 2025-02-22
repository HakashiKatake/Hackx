from sanic import Sanic, json
from sanic_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor

# Load dataset from CSV
data = pd.read_csv("/Users/rohanvashisht/Hackx/datasetPrepairation/processedDatasets/bdm.csv")

# Drop rows with NaN values
data = data.dropna()

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



app = Sanic("ip")
CORS(app)






@app.route("/get_proxy")
async def ip_api(request):
    ip = "XXXXXX"
    return json({"ip": ip})

if __name__ == '__main__':
    
    app.run(host="127.0.0.1", port=5050)