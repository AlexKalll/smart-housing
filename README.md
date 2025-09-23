# House Price Predictor -- Django + Celery + Redis (Auto-Retraining)

A Django app that predicts house prices and automatically retrains the model on fresh data. Retraining runs on a schedule (Celery Beat) and uses Redis as the broker/result backend.
![Project Demo](assets/demo.gif)
## Features
- Input form at /pr/ endpoint to predict price using:
  - size, bedrooms, age (numeric)
  - location ∈ {Downtown, Suburbs, Rural}
  - house type ∈ {Villa, Apartment, L-shape, Normal}
- One-hot encoding for categoricals with stable column order
- Artifacts saved to checkpoints/:
  - model_latest.joblib
  - scaler.joblib 
- Auto-retraining task every 24 hour (adjustable)

## Project Structure (high level)
- [prediction/](https://github.com/AlexKalll/smart-housing/tree/main/prediction) (the core Django project)
  - prediction/celery.py (Celery app + Beat schedule)
  - prediction/__init__.py (loads Celery on Django start)
  - predict/ (Django app)
    - ml_model.py (HousePricePredictor + train/retrain/predict functions)
    - tasks.py (retrain_model + simple ping/add tasks)
    - views.py, urls.py, templates/predict.html (form UI + endpoints)
- scripts/data_generator.py (creates/appends dataset)
- data/housing.csv (training data; generated)
- checkpoints/ (saved model + scaler)

## Quickstart 

1) Clone the repo, create venv and install dependencies
```powershell
python -m venv .\venv
.\venv\Scripts\Activate # on windows 
source venv/bin/activate # on linux
pip install -r .\requirements.txt
```

2) Start Redis (on Docker or locally)
```powershell
docker run --name redis -p 6379:6379 -d redis:7 # or install redis and run locally
```

3) To generate/append training data
```powershell
python .\scripts\data_generator.py
```

4) Run django server
```powershell
python .\prediction\manage.py runserver #(in the root directory)
```

5) Run Celery worker and Beat (separate terminals)
```powershell
cd prediction 
celery -A prediction worker -l info
celery -A prediction beat -l info
```

6) Use it
- Predict in browser: http://127.0.0.1:8000/pr/

## ML model details
- Class: HousePricePredictor (prediction/predict/ml_model.py)
- One-hot encoding for location and house_type; scaler fits only numeric cols
- Saves:
  - checkpoints/model_latest.joblib
  - checkpoints/scaler.joblib - standard scaler for numeric features


## Next Steps
- Experiment with other algorithms like XGBoost, which is more advanced ml models and more data and deploy to production