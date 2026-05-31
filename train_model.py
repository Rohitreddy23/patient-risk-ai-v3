import pandas as pd
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("realtime_patient_data.csv")

features = [
    "Age",
    "Systolic_BP",
    "Diastolic_BP",
    "Cholesterol_Lvl",
    "Glucose_Lvl"
]

X = df[features]

encoder = LabelEncoder()
y = encoder.fit_transform(df["Test_Results"])

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Model saved successfully")