from celery import shared_task
from .ml_model import retrain_and_save_model

@shared_task(name="predict.tasks.retrain_model")
def retrain_model():
    retrain_and_save_model()
    
    return "\n\n  [OK] Model Retrained Successfully!"
