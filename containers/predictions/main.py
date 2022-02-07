from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define the main route
@app.get('/')
def root_route():
  return { 'error': 'Use GET /prediction instead of the root route!' }


# Define the heartbeat
@app.get('/hearbeat')
def heartbeat():
  return { 'heartbeat': 'Service Ok' }
