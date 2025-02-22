from datasets import load_dataset
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


# Load dataset
df = pd.read_csv("datasetPrepairation/rawDatasets/Clothes-Size-Prediction.csv")  # Update with the actual filename

# Encode categorical variable
le = LabelEncoder()
df["size"] = le.fit_transform(df["size"])

# Split data
X = df[["age", "height"]]
y_weight = df["weight"]
y_size = df["size"]

X_train, X_test, y_weight_train, y_weight_test = train_test_split(
    X, y_weight, test_size=0.2, random_state=42
)
X_train_size, X_test_size, y_size_train, y_size_test = train_test_split(
    X, y_size, test_size=0.2, random_state=42
)

# Train models
weight_model = RandomForestRegressor()
weight_model.fit(X_train, y_weight_train)

size_model = RandomForestClassifier()
size_model.fit(X_train_size, y_size_train)

# Prediction function
def predict_weight_size(age, height):
    weight_pred = weight_model.predict([[age, height]])[0]
    size_pred = size_model.predict([[age, height]])[0]
    size_label = le.inverse_transform([int(size_pred)])[0]
    return round(weight_pred, 2), size_label  # Removed rounding on size_label since it's categorical

# Load dataset
dataset = load_dataset(
    "csv", data_files="./datasetPrepairation/rawDatasets/bdm.csv", split="train"
)

# Convert measurements to cm
def convert_to_cm(example):
    for key in [
        "ShoulderWidth", "ChestWidth", "Belly", "Waist", "Hips", "ArmLength",
        "WaistToKnee", "ShoulderToWaist", "LegLength", "HeadCircumference", "TotalHeight"
    ]:
        example[key] = round(example[key] * 2.54, 2)
    return example

def add_weight_height(example):
    res = list(predict_weight_size(example["Age"], example["TotalHeight"]))
    example["Size"] = res[1]
    if(res[1] == "XXS" or res[1] == "XS"):
        res[1] = "Slim"
    elif(res[1] == "S" or res[1] == "M"):
        res[1] = "Regular"
    else:
        res[1] = "Loose"

    example["Weight"] = res[0]
    example["Fit"] = res[1]
    return example

# Apply transformations
dataset = dataset.map(convert_to_cm)
dataset = dataset.map(add_weight_height)

# Convert dataset to pandas dataframe
dataset = dataset.to_pandas()

# Save dataset to CSV
dataset.to_csv("./datasetPrepairation/processedDatasets/bdm.csv", index=False)

print(dataset)
