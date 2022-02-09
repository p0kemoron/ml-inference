import os
import time
from celery import Celery
from utils.ml.ml_utils import ScoreReportsDummyModel

cel_app = Celery()

cel_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
cel_app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@cel_app.task(ignore_result=False)
def get_score(pred_data):
    # Waits for 2 seconds to simulate realtime lag and 
    # then generates a random score between 0 and 1 
    model = ScoreReportsDummyModel()
    time.sleep(2)
    return model.predict(pred_data)
