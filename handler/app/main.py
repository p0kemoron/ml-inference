import uvicorn
import logging
import json

from typing import List
from .utils.data_models import RequestBody, SubmittedTask, FetchedScore
from .utils.setup_db import database, task_results, input_features
from .utils.ml.ml_utils import get_pred_df
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .workers import get_score
from celery.result import AsyncResult

app = FastAPI()


@app.on_event("startup")
async def setup_backend_db():
    # Intialize backend postgres db before the first call is made
    await database.connect()


# Define the heartbeat
@app.get("/heartbeat")
def heartbeat():
    # Returns if api is healthy
    return {"message": "Service Ok"}


@app.post("/submit")
async def get_task_id(
    data: List[RequestBody], status_code=201, response_model=SubmittedTask
):
    """Async API, accepts data from client and returns a task id

    Args:
        data (List[RequestBody]): Incoming data payload

    Returns:
        JSONResponse: task_id and status for the request
    """

    data_json = json.dumps([x.json() for x in data])
    pred_data = get_pred_df(data)

    task = get_score.delay(pred_data)

    # Add incoming request to backend server for later use: evaluation, monitoring
    query = input_features.insert().values(id=task.id, features=data_json)
    await database.execute(query)

    return JSONResponse({"task_id": task.id, "status": str(task.status)})


@app.get(
    "/task/{task_id}",
    status_code=200,
    response_model=FetchedScore,
    responses={202: {"model": SubmittedTask}},
)
async def get_report_score(task_id):
    """Returns the task status and scores (if ready) for a given task_id

    Args:
        task_id (string): Unique task identifier

    Returns:
        JSON(FetchedScore): task_id, status and scores (if ready)
    """    
    task = AsyncResult(task_id)
    # Returns a processing status if the task hasn't completed yet
    # This is asuming the client would have some sort of a polling mechanism configured
    if not task.ready():
        return JSONResponse(
            status_code=201, content={"task_id": str(task_id), "status": "Processing"}
        )
    # If the results are ready, store them in the backend database
    # This is not the cleanest way to do it, but since task_id is primary key,
    # duplicate requests don't create additional rows.
    query = task_results.insert().values(id=task.id, scores=str(task.result))
    await database.execute(query)

    return {"task_id": str(task_id), "status": str(task.status), "score": task.result}
