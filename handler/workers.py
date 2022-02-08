import os
from celery import Celery
from ml.score_reports import ScoreReportsDummyModel

BROKER_URI = os.getenv('BROKER_URI')
BACKEND_URI = os.getenv('BACKEND_URI')

app = Celery(
    'queue',
    broker=BROKER_URI,
    backend=BACKEND_URI
)

@app.task(ignore_result=False)
def create_task():
    return True

@app.task(ignore_result=False)
def get_score():
    model = ScoreReportsDummyModel()
    return model.predict()
