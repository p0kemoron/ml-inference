import uvicorn
import logging

from typing import List
from utils import RequestBody, SubmittedTask, FetchedScore, get_pred_df
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from workers import get_score, create_task
from celery.result import AsyncResult

app = FastAPI()

# Define the heartbeat
@app.get('/heartbeat')
def heartbeat():
  return { "message": "Service Ok" }


@app.post('/submit')
async def get_task_id(data: List[RequestBody], status_code=201, response_model=SubmittedTask):
  pred_data = get_pred_df()
  task = get_score.delay()
  return JSONResponse({"task_id":task.id, "status": str(task.status)})


@app.post('/task/{task_id}', status_code=200, response_model=FetchedScore, responses={202: {'model': SubmittedTask}})
async def get_report_score(task_id):
  task = AsyncResult(task_id)
  if not task.ready():
    return JSONResponse(status_code=201, content={'task_id': str(task_id), 'status': 'Processing'})

  return {"task_id": str(task_id), "status": str(task.status), "score": task.result}
