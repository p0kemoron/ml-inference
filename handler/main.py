import uvicorn
import logging
import json

from typing import List
from utils.data_models import RequestBody, SubmittedTask, FetchedScore
from utils.setup_db import database, task_results, input_features
from utils.ml.ml_utils import get_pred_df
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from workers import get_score
from celery.result import AsyncResult

app = FastAPI()

@app.on_event("startup")
async def setup_backend_db():
  await database.connect()


# Define the heartbeat
@app.get('/heartbeat')
def heartbeat():
  return { "message": "Service Ok" }


@app.post('/submit')
async def get_task_id(data: List[RequestBody], status_code=201, response_model=SubmittedTask):
  
  data_json = json.dumps([x.json() for x in data])
  pred_data = get_pred_df(data)

  task = get_score.delay(pred_data)

  query = input_features.insert().values(id=task.id, features=data_json)
  await database.execute(query)
  
  return JSONResponse({"task_id":task.id, "status": str(task.status)})


@app.get('/task/{task_id}', status_code=200, response_model=FetchedScore, responses={202: {'model': SubmittedTask}})
async def get_report_score(task_id):
  task = AsyncResult(task_id)
  if not task.ready():
    return JSONResponse(status_code=201, content={'task_id': str(task_id), 'status': 'Processing'})
    
  query = task_results.insert().values(id=task.id, scores=str(task.result))
  await database.execute(query)

  return {"task_id": str(task_id), "status": str(task.status), "score": task.result}
