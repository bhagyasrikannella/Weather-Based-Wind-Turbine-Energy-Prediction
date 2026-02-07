import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# Check current folder
print("Current Folder:", os.getcwd())
print("Files in Folder:", os.listdir())

# Load dataset
data = pd.read_csv("wind_data.csv", encoding="latin1")

print("\nColumns in CSV:")
print(data.columns)

# Select features and target
X = data[['windspeed_100m']]   # input
y = data['Power']              # output

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# Predict & evaluate
y_pred = model.predict(X_test)
print("\nR2 Score:", r2_score(y_test, y_pred))

# Save model
pickle.dump(model, open("wind_model.sav", "wb"))

print("\nModel trained & saved as wind_model.sav")
