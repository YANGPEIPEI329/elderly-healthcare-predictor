from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

with open(os.path.join(BASE_DIR, "model.pkl"), "rb") as f:
    bundle = pickle.load(f)

model   = bundle["model"]
scaler  = bundle["scaler"]
FEATURES = bundle["features"]

ETHNICITY_MAP = {
    1: "Mexican American",
    2: "Other Hispanic",
    3: "Non-Hispanic White",
    4: "Non-Hispanic Black",
    6: "Non-Hispanic Asian",
    7: "Other / Multi-racial",
}
EDUCATION_MAP = {
    1: "Less than 9th Grade",
    2: "9th–11th Grade",
    3: "High School / GED",
    4: "Some College or Associate's Degree",
    5: "College Graduate or above",
}
MARITAL_MAP = {
    1: "Married / Living with Partner",
    2: "Widowed / Divorced / Separated",
    3: "Never Married",
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        ethnicity_options=ETHNICITY_MAP,
        education_options=EDUCATION_MAP,
        marital_options=MARITAL_MAP,
    )


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        values = [
            float(data["gender"]),
            float(data["age"]),
            float(data["ethnicity"]),
            float(data["education_level"]),
            float(data["marital_status"]),
            float(data["income_poverty_ratio"]),
            int(data["arthritis"]),
            int(data["pulmonary_disease"]),
            int(data["cancer"]),
            int(data["high_cholesterol"]),
            int(data["diabetes"]),
            int(data["chest_pain"]),
            int(data["shortness_breath"]),
            int(data["cardio_disease"]),
            int(data["hypertension_status"]),
            int(data["smoking_status"]),
        ]

        X = np.array(values).reshape(1, -1)
        X_sc = scaler.transform(X)

        pred = int(model.predict(X_sc)[0])
        prob = float(model.predict_proba(X_sc)[0][1])

        risk_factors = _get_risk_factors(data)

        return jsonify({
            "prediction": pred,
            "probability": round(prob * 100, 1),
            "label": "High Healthcare Demand" if pred == 1 else "Low Healthcare Demand",
            "risk_factors": risk_factors,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


def _get_risk_factors(data):
    factors = []
    conditions = {
        "arthritis": "Arthritis",
        "pulmonary_disease": "Pulmonary Disease (COPD)",
        "cancer": "Cancer History",
        "diabetes": "Diabetes",
        "chest_pain": "Chest Pain (Angina)",
        "shortness_breath": "Shortness of Breath",
        "cardio_disease": "Cardiovascular Disease",
        "hypertension_status": "Hypertension",
    }
    for key, label in conditions.items():
        if int(data.get(key, 0)) == 1:
            factors.append(label)
    if float(data.get("income_poverty_ratio", 5)) < 1.0:
        factors.append("Low Income (below poverty line)")
    if int(data.get("smoking_status", 0)) == 1:
        factors.append("Current / Former Smoker")
    return factors


if __name__ == "__main__":
    # On Render the app is served by gunicorn (see render.yaml), so this block
    # is only used for local development. PORT/DEBUG are read from the env.
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
