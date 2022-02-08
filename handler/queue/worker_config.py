import os
from celery import Celery

BROKER_URI = os.environ['BROKER_URI']
BACKEND_URI = os.environ['BACKEND_URI']

app = Celery(
    'queue',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['queue.worker_tasks']
)