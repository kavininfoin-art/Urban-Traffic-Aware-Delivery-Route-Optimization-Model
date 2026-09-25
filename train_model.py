import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

data = pd.DataFrame([
    ["Warehouse", "A", 5.2, 3, 9, "Weekday", "Clear", "Main Road", 18],
    ["Warehouse", "B", 6.8, 4, 10, "Weekday", "Clear", "Main Road", 25],
    ["Warehouse", "C", 8.5, 5, 18, "Weekday", "Rain", "Main Road", 38],
    ["Warehouse", "D", 7.1, 2, 11, "Weekday", "Clear", "Highway", 22],
    ["Warehouse", "E", 3.9, 3, 17, "Weekday", "Cloudy", "City Road", 16],
    ["Warehouse", "F", 5.5, 4, 19, "Weekend", "Clear", "Main Road", 24],
    ["A", "B", 3.1, 4, 18, "Weekday", "Clear", "City Road", 15],
    ["A", "C", 5.0, 5, 19, "Weekday", "Rain", "City Road", 27],
    ["A", "D", 4.2, 3, 10, "Weekday", "Clear", "Main Road", 16],
    ["A", "E", 4.5, 2, 14, "Weekend", "Clear", "City Road", 14],
    ["A", "F", 6.0, 4, 20, "Weekday", "Cloudy", "Main Road", 26],
    ["B", "C", 3.5, 3, 12, "Weekday", "Clear", "Main Road", 14],
    ["B", "D", 4.8, 5, 18, "Weekday", "Rain", "City Road", 25],
    ["B", "E", 5.2, 3, 15, "Weekend", "Clear", "Main Road", 20],
    ["B", "F", 6.3, 4, 19, "Weekday", "Cloudy", "Main Road", 27],
    ["C", "D", 3.7, 2, 9, "Weekday", "Clear", "City Road", 13],
    ["C", "E", 4.1, 4, 17, "Weekday", "Rain", "City Road", 22],
    ["C", "F", 7.0, 5, 18, "Weekday", "Rain", "Main Road", 32],
    ["D", "E", 4.0, 3, 13, "Weekend", "Clear", "Main Road", 17],
    ["D", "F", 6.2, 4, 18, "Weekday", "Cloudy", "Main Road", 26],
    ["E", "F", 5.0, 2, 11, "Weekend", "Clear", "City Road", 18],
], columns=[
    "from_location",
    "to_location",
    "distance_km",
    "traffic_level",
    "time_of_day",
    "day_type",
    "weather",
    "road_type",
    "travel_time"
])

data.to_csv("data/traffic_training_data.csv", index=False)

X = data[
    [
        "distance_km",
        "traffic_level",
        "time_of_day",
        "day_type",
        "weather",
        "road_type"
    ]
]

y = data["travel_time"]

categorical_features = ["day_type", "weather", "road_type"]
numeric_features = ["distance_km", "traffic_level", "time_of_day"]

preprocessor = ColumnTransformer([
    ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ("numeric", "passthrough", numeric_features)
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ))
])

model.fit(X, y)

joblib.dump(model, "models/traffic_prediction_model.pkl")

print("Dataset created successfully.")
print("Model trained successfully.")
print("Saved: data/traffic_training_data.csv")
print("Saved: models/traffic_prediction_model.pkl")