# 🔊 Sonar Rock vs Mine Prediction — Django ML Web App

A Django web application that uses a trained scikit-learn model to classify sonar signals as **Rock** or **Mine** based on 60 frequency-band features.

---

## 📁 Project Structure

```
sonar_django/
├── sonar_model.pkl              ← Your trained scikit-learn model (place here)
├── requirements.txt
├── Procfile                     ← For Render / Railway deployment
├── .env.example                 ← Copy to .env and fill in values
├── .gitignore
├── README.md
└── sonar_project/
    ├── manage.py
    ├── db.sqlite3               ← Created after migrate (auto)
    ├── staticfiles/             ← Created after collectstatic (auto)
    ├── sonar_project/           ← Django project config
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── sonar_app/               ← Main application
        ├── __init__.py
        ├── views.py
        ├── urls.py
        └── templates/
            └── sonar_app/
                └── home.html
```

---

## ⚙️ Features

- **60-feature input form** — inputs auto-generated via Django template loop
- **Live charts** that update as you type:
  - Signal Waveform (line chart across all 60 features)
  - Band Energy Distribution (10 averaged bands, bar chart)
  - Frequency Radar (spider chart, 10 key points)
  - Signal Statistics (mean, std, min, max, energy, high-band count)
- **Real confidence bars** using `predict_proba` from your model
- **Sample buttons** — load verified Rock or Mine samples from UCI dataset
- **Random button** — generates realistic noisy samples
- **Clear** — resets all inputs and hides result
- **Reset Page** — navigates to a clean page with no prediction shown (fixes browser POST-replay)
- **Color-coded inputs** — green = low energy, red = high energy

---

## 🚀 Local Setup (Step by Step)

### Step 1 — Clone or unzip the project

```bash
cd sonar_django
```

### Step 2 — Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Place your model file

Copy your trained model file to the project root:

```
sonar_django/sonar_model.pkl    ← must be here
```

> **Important:** The model must be trained on 60-feature sonar data. It should predict `'R'` / `'M'` or `'Rock'` / `'Mine'` or `0` / `1`.

### Step 5 — Run migrations

```bash
cd sonar_project
python manage.py migrate
```

### Step 6 — Start the development server

```bash
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000**

---

## 🧪 Testing the App

### Using sample data (recommended first test)

1. Click **🪨 Rock Sample** — fills all 60 inputs with a verified UCI dataset rock reading
2. Click **⬡ PREDICT** — should return "ROCK"
3. Click **💣 Mine Sample** — fills all 60 inputs with a verified UCI dataset mine reading
4. Click **⬡ PREDICT** — should return "MINE"

### Testing Reset Page

1. Make a prediction
2. Click **↺ Reset Page**
3. The page should load completely clean — no result shown, all inputs empty

### Using the Random button

Generates a random sample based on either a Rock or Mine distribution with small noise added. Results may vary depending on your model.

---

## 🔌 Model Requirements

Your `sonar_model.pkl` must:

- Be a scikit-learn model saved with `pickle.dump(model, file)`
- Accept input shape `(1, 60)` — a single row of 60 float values (0.0 to 1.0)
- Predict one of: `'R'` / `'M'`, or `'Rock'` / `'Mine'`, or `0` / `1`
- Optionally have `predict_proba()` for confidence percentage display

### Saving your model correctly

```python
import pickle
from sklearn.linear_model import LogisticRegression  # or any model

# After training...
model.fit(X_train, y_train)

with open('sonar_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved!")
```

### Verifying your model works

```python
import pickle
import numpy as np

with open('sonar_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Test with 60 zeros
test = np.zeros((1, 60))
print("Prediction:", model.predict(test))
print("Classes:", model.classes_)

# Test predict_proba if available
if hasattr(model, 'predict_proba'):
    print("Probabilities:", model.predict_proba(test))
```

---

## 🌐 Deployment

### Option A — Deploy to Render (Recommended for beginners)

Render has a free tier and is the easiest option.

**Step 1: Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/sonar-django.git
git push -u origin main
```

> Make sure `sonar_model.pkl` is committed — it is NOT in `.gitignore`.

**Step 2: Create a Web Service on Render**

1. Go to [render.com](https://render.com) → Sign up → **New +** → **Web Service**
2. Connect your GitHub repository
3. Fill in these settings:

| Field | Value |
|-------|-------|
| Environment | Python 3 |
| Root Directory | `sonar_project` |
| Build Command | `pip install -r ../requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate` |
| Start Command | `gunicorn sonar_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2` |

**Step 3: Set Environment Variables**

In Render dashboard → your service → **Environment** tab:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | A long random string (generate below) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |

**Generate a SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Step 4: Deploy**

Click **Manual Deploy** → **Deploy latest commit**. Your app will be live at:
`https://your-app-name.onrender.com`

> ⚠️ Free tier apps sleep after 15 minutes of inactivity. First load after sleep takes ~30 seconds.

---

### Option B — Deploy to Railway

**Step 1: Push to GitHub** (same as Render Step 1 above)

**Step 2: Create project on Railway**

1. Go to [railway.app](https://railway.app) → Log in → **New Project**
2. Choose **Deploy from GitHub repo** → select your repository

**Step 3: Configure settings**

In Railway dashboard → your project → **Settings**:

- **Root Directory:** `sonar_project`
- **Build Command:** `pip install -r ../requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
- **Start Command:** `gunicorn sonar_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2`

**Step 4: Set environment variables**

In Railway → **Variables** tab:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Your secret key |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.up.railway.app` |

**Step 5: Generate domain**

Settings → **Networking** → **Generate Domain**

Your app: `https://your-app-name.up.railway.app`

---

### Option C — Local Production Test (Gunicorn)

Test exactly how production will behave before deploying:

```bash
cd sonar_project

# Collect static files
python manage.py collectstatic --no-input

# Run with gunicorn (set DEBUG=False first in settings or via env)
DEBUG=False gunicorn sonar_project.wsgi:application --bind 127.0.0.1:8000 --workers 2
```

---

## 🔒 Security Checklist (Before Going Live)

- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` loaded from environment variable (not hardcoded)
- [ ] `.env` file is in `.gitignore` — never commit it
- [ ] `ALLOWED_HOSTS` set to your actual domain only
- [ ] `sonar_model.pkl` is included in git (it's not secret, just your trained weights)
- [ ] Run `python manage.py collectstatic` before deploying

---

## 🐛 Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError: sonar_model.pkl` | Model not in project root | Place `sonar_model.pkl` in `sonar_django/sonar_project/` (same folder as `manage.py`) |
| `ModuleNotFoundError: No module named 'sonar_app'` | App not registered | Add `'sonar_app'` to `INSTALLED_APPS` in `settings.py` |
| `DisallowedHost` error | Domain not in ALLOWED_HOSTS | Add your domain to `ALLOWED_HOSTS` in `settings.py` or `.env` |
| Static files not loading in production | WhiteNoise not set up | Run `collectstatic` and verify `WhiteNoiseMiddleware` is in `MIDDLEWARE` |
| CSRF verification failed | Missing token | Make sure `{% csrf_token %}` is inside your `<form>` tag |
| Prediction always wrong class | `model.classes_` order issue | Check `print(model.classes_)` — views.py handles `M/R`, `0/1`, `Mine/Rock` automatically |
| Reset Page still shows prediction | Old browser cache | Clear browser cache or hard refresh (Ctrl+Shift+R) |

---

## 💡 Optional Improvements

### Add CSV batch prediction

Create a second view that accepts a CSV file with multiple rows (each row = 60 features):

```python
# views.py addition
import csv, io

def predict_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        file = request.FILES['csv_file']
        decoded = file.read().decode('utf-8')
        reader = csv.reader(io.StringIO(decoded))
        results = []
        for row in reader:
            if len(row) != 60:
                continue
            data = np.array([float(x) for x in row]).reshape(1, 60)
            pred = model.predict(data)[0]
            label = 'Rock' if str(pred).upper() in ('R','ROCK','1') else 'Mine'
            results.append({'values': row, 'prediction': label})
        return render(request, 'sonar_app/csv_results.html', {'results': results})
```

### Display model accuracy in header

Train your model and save accuracy alongside it:

```python
# In your training script
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, model.predict(X_test))
with open('sonar_model.pkl', 'wb') as f:
    pickle.dump({'model': model, 'accuracy': round(accuracy * 100, 2)}, f)
```

Then update `views.py` to load it:

```python
saved = pickle.load(f)
model = saved['model']
MODEL_ACCURACY = saved['accuracy']  # pass to template context
```

---

## 📊 About the Data

The app uses the **UCI Machine Learning Repository — Sonar Dataset**:

- 208 samples (111 Mine, 97 Rock)
- 60 features per sample — energy in a frequency band integrated over a time window (0.0 to 1.0)
- Binary classification: **R** (Rock) or **M** (Mine)

Dataset: [archive.ics.uci.edu/ml/datasets/connectionist+bench+(sonar,+mines+vs.+rocks)](https://archive.ics.uci.edu/ml/datasets/connectionist+bench+(sonar,+mines+vs.+rocks))

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | Django 4.2 |
| ML Model | scikit-learn (any classifier) |
| Numerics | NumPy |
| Frontend | Bootstrap 5.3, Chart.js 4.4 |
| Static Files | WhiteNoise |
| Production Server | Gunicorn |
| Deployment | Render / Railway |