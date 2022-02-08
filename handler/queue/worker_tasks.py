import logging
from celery import Task
from .worker_config import app
from .ml.score_reports import ScoreReportsDummyModel

@app.task(ignore_result=False)
def create_task(pred_data):
    return True

@app.task(ignore_result=False)
def get_score():
    model = ScoreReportsDummyModel()
    return model.predict()
