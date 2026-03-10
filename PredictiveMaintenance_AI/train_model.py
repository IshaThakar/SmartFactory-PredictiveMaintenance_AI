import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("ai4i2020.csv")

# Remove unnecessary columns
data = data.drop(columns=["UDI","Product ID","Type","TWF","HDF","PWF","OSF","RNF"])

# Features
X = data.drop("Machine failure", axis=1)

# Target
y = data["Machine failure"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model,"machine_model.pkl")

print("Model trained successfully")