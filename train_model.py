"""
Train and save the Logistic Regression model for healthcare demand prediction.
Run this script once to generate model.pkl before starting the web app.
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score

DATA_PATH = "../final_dataset.csv"

df = pd.read_csv(DATA_PATH)
df = df.drop(columns=["SEQN"])

FEATURES = [
    "gender", "age", "ethnicity", "education_level", "marital_status",
    "income_poverty_ratio", "arthritis", "pulmonary_disease", "cancer",
    "high_cholesterol", "diabetes", "chest_pain", "shortness_breath",
    "cardio_disease", "hypertension_status", "smoking_status"
]
TARGET = "healthcare_demand"

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

model = LogisticRegression(
    C=0.01,
    solver="lbfgs",
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)
model.fit(X_train_sc, y_train)

y_pred = model.predict(X_test_sc)
y_prob = model.predict_proba(X_test_sc)[:, 1]

print("=== Model Evaluation ===")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")

with open("model.pkl", "wb") as f:
    pickle.dump({"model": model, "scaler": scaler, "features": FEATURES}, f)

print("\nModel saved to model.pkl")
