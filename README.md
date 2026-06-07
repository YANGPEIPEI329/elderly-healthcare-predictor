# Elderly Healthcare Demand Predictor

A machine-learning web app that predicts whether an elderly individual (aged 60–80) is
likely to have **high healthcare demand**, based on demographic, clinical, and lifestyle
factors.

> **WQD7003 Data Analytics · Group 8 · Universiti Malaya**
> Built on NHANES survey data. Model: **Logistic Regression** (ROC-AUC ≈ 0.746) — the
> top performer among Logistic Regression, Decision Tree, and Random Forest.

## 🚀 One-click deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YANGPEIPEI329/elderly-healthcare-predictor)

Click the button → log in to Render → **Apply**. Render reads `render.yaml` and builds the
free service automatically. See [`DEPLOY.md`](DEPLOY.md) for detailed steps.

## 🧠 Model

| | |
|---|---|
| Algorithm | Logistic Regression (`class_weight="balanced"`, `C=0.01`) |
| Features | 16 (demographic, clinical, lifestyle) |
| ROC-AUC | 0.746 |
| Training / Test | 2 737 / 685 samples |
| Data source | NHANES survey, elderly subset (60–80 yrs) |

`model.pkl` is trained and committed, so the app runs without retraining. To rebuild it,
run `python train_model.py` (requires the dataset and pandas).

## 💻 Run locally

```bash
pip install flask scikit-learn numpy
python app.py        # http://localhost:5000
```

## 📁 Structure

```
webapp/
├── app.py              # Flask backend (prediction API + routes)
├── train_model.py      # Model training script
├── model.pkl           # Trained Logistic Regression model (committed)
├── render.yaml         # Render deployment blueprint
├── Procfile            # gunicorn start command
├── requirements.txt    # Pinned dependencies (match model.pkl's env)
├── templates/index.html
└── static/style.css
```

> ⚠ For research and educational purposes only — not a medical diagnosis.
