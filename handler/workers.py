import os
from celery import Celery
from ml.score_reports import ScoreReportsDummyModel

app = Celery()

app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@app.task(ignore_result=False)
def create_task():
    return True

@app.task(ignore_result=False)
def get_score():
    model = ScoreReportsDummyModel()
    return model.predict()
