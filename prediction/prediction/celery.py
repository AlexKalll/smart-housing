import os
from celery import Celery
from datetime import timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prediction.settings")

app = Celery("prediction")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Celery Beat schedule (every 24 hours)
app.conf.beat_schedule = {
    "retrain-model-hourly": {
        "task": "predict.tasks.retrain_model",
        "schedule": timedelta(hours=1),  # Every hour
    },
}
