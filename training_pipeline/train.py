import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (mean_absolute_error,mean_squared_error,r2_score)
import pickle
import os

# Load dataset
df = pd.read_csv(
    r"C:\Users\HP\Desktop\ML-ml\End-to-End-ML-Platform\data\raw\RELIANCE.csv"
)

# Select important features
X = df[[
    "Open",
    "High",
    "Low",
    "Volume",
    "Prev Close"
]]

# Target column
y = df["Close"]

# Remove missing values
X = X.dropna()
y = y.loc[X.index]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LinearRegression()

model.fit(X_train, y_train)

# Prediction
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)

rmse = np.sqrt(
    mean_squared_error(y_test, preds)
)

r2 = r2_score(y_test, preds)

print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)


# Create models folder
os.makedirs("models", exist_ok=True)

# Save model
pickle.dump(
    model,
    open("C:/Users/HP/Desktop\ML-ml/End-to-End-ML-Platform/models/model.pkl", "wb")
)

print("Model Saved Successfully")
# SAVE METRICS
metrics = {
    "MAE": mae,
    "RMSE": rmse,
    "R2": r2
}

with open("models/metrics.pkl", "wb") as f:
    pickle.dump(metrics, f)