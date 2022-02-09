# Sample ML Inference App
Python based ML inference app designed to accept data simulating user reports and returning resulting scores.

## Business Problem
The Data Science Team is currently working on the model, iterating on the best architecture and hyperparameters. They already have a satisfactory model developed using XGBoost (on Scikit-Learn) and are currently looking into possible improvements leveraging a more complicated architecture on Tensorflow.

They asked us to design a solid and scalable server application able to expose the model via HTTP for online inference. The ML-based service will be used to score user generated reports created on our applications in order to rank them based on their relevance/priority.

## Usage
The app can be readily used following the steps below (requires docker and docker-compose installed):

1. Clone the repository to local machine
2. `cd ml-inference`
3. `docker-compose up -d --build`

This will trigger build process for the required services (details below) and setup the containers. The API can be tested by accessing via browser: http://127.0.0.1:8081/docs

Alternatively, it can be tested using the curl command as below:

```
curl -X 'POST' \
  'http://127.0.0.1:8081/prediction' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[{
  "abuse_type": "MSG",
  "report_text_len": 0,
  "profile_rating": 0,
  "popularity": 0
  }]'
```

## API Calls
The following API calls are available as a part of this app:  

Method | URL | Parameter | Description
--- | --- | --- | ---
POST | http://127.0.0.1:8081/predict | - | Returns info on all tasks- past and scheduled
GET | http://127.0.0.1:8081/task/<task_id> | - | Returns info for a particular task_id 
GET | http://127.0.0.1:8081/heartbeat | - | Checks if API is active

## Design considerations
simple + scalable 

diagram here

abstraction design, separation of concerns, data models and orm


Python Flask vs fastapi
celery?
postgresql - orm, current infra

## Current limitations

Expansion of test designs and coverage


## Path towards production

## Developer's Notes