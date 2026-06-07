# Deploying to Render

This app is configured for **one-click deployment on [Render](https://render.com)** using
the included `render.yaml` (a Render *Blueprint*). Render's free plan is enough for this
project — no credit card required.

> **What I prepared for you**
> - `render.yaml` — tells Render how to build & run the app
> - `requirements.txt` — dependencies pinned to the versions that trained `model.pkl`
> - `Procfile` — start command (also works on Railway / Heroku-style platforms)
> - `.gitignore` — keeps junk out of git **but keeps `model.pkl`** (needed at runtime)
> - `app.py` — reads `PORT` from the environment so it works behind gunicorn

---

## Step 1 — Put this folder on GitHub

The simplest setup is to make **this `webapp` folder** the root of a GitHub repo
(so `render.yaml` sits at the repo root, where Render expects it).

If I already initialised git for you, you only need to create an empty repo on GitHub
and push:

```bash
# (run inside the webapp folder)
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

If git is **not** initialised yet:

```bash
cd webapp
git init
git add .
git commit -m "Elderly healthcare demand predictor web app"
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

> Make sure `model.pkl` is included in the commit (`git status` should list it).
> Without it the server cannot make predictions.

---

## Step 2 — Deploy on Render

1. Go to <https://dashboard.render.com> and sign up / log in (GitHub login is easiest).
2. Click **New +  →  Blueprint**.
3. Connect your GitHub account and select the repo you just pushed.
4. Render reads `render.yaml` automatically and shows a service named
   **`elderly-healthcare-predictor`**. Click **Apply**.
5. Wait ~2–4 minutes for the first build. When it finishes you get a public URL like:

   ```
   https://elderly-healthcare-predictor.onrender.com
   ```

That's it — share the link with your lecturer / group.

### Alternative: manual setup (no Blueprint)

If you prefer to configure it by hand: **New +  →  Web Service**, pick the repo, then set:

| Field          | Value                                                        |
|----------------|-------------------------------------------------------------|
| Runtime        | Python 3                                                     |
| Build Command  | `pip install -r requirements.txt`                           |
| Start Command  | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| Instance Type  | Free                                                         |

---

## Notes

- **Free plan sleeps after inactivity.** The first visit after a quiet period takes
  ~30–50 s to wake up, then it's fast. This is normal for Render's free tier.
- **Model version lock.** `requirements.txt` pins `scikit-learn==1.9.0` and
  `numpy==2.4.6` to match the environment that created `model.pkl`. If you retrain the
  model with different versions, update these pins to match, or the server may fail to
  load the pickle.
- **Retraining is not needed to deploy.** `model.pkl` is already trained and committed.
  `train_model.py` and the dataset are only needed if you want to rebuild the model.

---

## Local run (for reference)

```bash
cd webapp
pip install flask scikit-learn numpy
python app.py          # http://localhost:5000
```
