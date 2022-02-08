import uvicorn
import logging

from typing import List
from .utils import RequestModel, get_pred_df
from fastapi import FastAPI, File, UploadFile, HTTPException
from queue.worker_tasks import get_score, create_task

app = FastAPI()

# Define the main route
@app.get('/')
def index():
  return { "error": "Use GET /prediction instead of the root route!"}

@app.post('/prediction')
async def get_task_id(data: List[RequestModel]):
  pred_data = get_pred_df(data)
  task_id = create_task.delay(pred_data)
  return {"task_id":str(task_id)}


# Define the heartbeat
@app.get('/heartbeat')
def heartbeat():
  return { "message": "Service Ok" }


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)