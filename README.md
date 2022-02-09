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

Alternatively, it can be tested using the curl command as below example:

```
curl -X 'POST' \
  'http://localhost:8081/submit' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "abuse_type": "MSG",
    "report_text_len": 0,
    "profile_rating": 0,
    "popularity": 0,
    "lifetime_matches_created": 0
  },
  {
    "abuse_type": "MSG",
    "report_text_len": 0,
    "profile_rating": 0,
    "popularity": 0,
    "lifetime_matches_created": 1
  }
]'
```

## API Calls
The following API calls are available as a part of this app:  

Method | URL | Parameter | Description
--- | --- | --- | ---
POST | http://127.0.0.1:8081/predict | abuse_type, report_text_len, profile_rating, popularity, lifetime_matches_created | Submits a task job to the API to fetch scores for the report
GET | http://127.0.0.1:8081/task/<task_id> | - | Returns info for a particular task_id 
GET | http://127.0.0.1:8081/heartbeat | - | Checks if API is active



## Design considerations
While building this application, the motivations were to keep things simple but scalable at the same time. Since, the choice of architecture depends on the usecase and other infra-setup, I've tried to stick to Bumble infra that I learnt during the initial discussions, for a seamless integration.   
` `  

The application is designed to be asynchronous. This allows it to be freely available to multiple clients without being 'held up' with a long computational task. Quick explainer: client sends the data via POST request and immediately receives a task_id which the client can then use to make a GET response and inquire its status and the scores.
` `  
  
Although not a lot of information was provided specific to the usecase, I can safely assume the data is related to profile and message reports submitted by users. In these cases, corrective steps taken with a delay of order of minutes should generally be okay.
` `  
  
Moving on to the architecture, there five services built. Gateway to parse incoming requests: 'handler', a queue to store submitted jobs and track, workers to actually do the computation, backend database to persist incoming data and predictions, and a monitoring dashboard. All of the parts are decoupled from each other and containerized separately, if one were to fail, the rest of the app works fine.
` `  

**Handler**
I am using FastAPI because of its significant performance improvement with Python apps as compared to Flask. Additionally, FastAPI works out of the box with async calls and is designed to be optimized for the same. There are also other significant advantages such as extension of pydantic for data validation, automated openAPI docs creation etc.

**Task handling**
I am using Celery (+ Redis broker) to communicate between submitted jobs and compute workers. Celery is the go-to choice for python apps as it is written in Python and still used widely, it should fit in this architecture. I initially considered using MLflow but Celery is much more feature complete (currently at least). Although for the purpose of this PoC, both should have been alright. 

**Backend**
Backend is based on PostgreSQL. I initially used Redis both as a broker and backend for simplicity's sake but I thought using Postgresql primarily because it offers better reliability wrt Redis.
Also, ideally we'd like to keep our broker and backend separate. Again, it's already in use and would reduce the overhead in bringing it together. Using Postgres also allowed me to stick to best practices in terms of defining a data model and using an ORM library.

**Monitoring**
For monitoring, Flower dashboard is being used. I do not have very strong reasons to be using this. I've been used to cloud native monitoring solutions so I spent some time reading about what generally works with Celery in absence of cloud environment, and arrived at Flower because it was suggested in Celery's official documentation. I think MLFLow's monitoring library

![Basic Architecture Diagram](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)  
A very crude architecture diagram showing the working parts


## Current limitations
There are definitely a lot of shortcomings in this version of the app as it is designed to be a "sensible proof-of-concept" but if I could take some immediate steps I'd do the following:

1. Expanding test cases and coverage. Although, this version of the app has been tested thoroughly (edge cases etc), they are not a match for an automated testing framework
2. Models are currently being loaded by celery workers in memory (assumming this path file is coming from a GCS bucket or similar). This may be inefficient and I would like to deploy it using an Endpoint so for each task, it is not loaded in memory again
3. Logging: Logs are being generated in the `logs/` directory for workers and also available via docker-composer logs for all of the services. While these are sufficient for troubleshooting, granular INFO level logs need to be included in order to make sure the REST APIs logs are production ready.


## Path towards production
In addition to the above to-do items, there are some other considerations to be made while pushing this to production.

### Scalability
Postgres scales really well for general use cases, but we'd need a scheduled batch job to persist data from RDBMS to either cloud(Google/Amazon buckets) or on-prem big data tools (HDFS etc)

Additionally, these pipelines would need to perform ETL as the current version of the app dumps the input request as a string instead of defining a column for each parameter.

Number of workers can be extended depending on the traffic. Even more sophisticated solution would be building it using Kubernetes to automatically scale up/down based on the demand.

API gateway can be introduced (currently this is same as 'handler') as the API matures and has multiple end-points which may be using multiple calls in order to get result.

### Efficiency
The API can be made a lot more efficient in case our requests are repetitive in nature (i.e. similar kinds of profiles being reported maybe?), it might make sense for us to make use of cache stores.

As mentioned above, the models are being loaded into memory and it may not be feasible to do that as models grow complex and there should be deployed via an endpoint (hosted over cloud or on-prem) which our workers can make calls to.

### Model Deployment
CI/CD workflows with automated tests (both unit tests for functions as well as integration tests) would be necessary. In this repo, I've stored a dummy model class in `handler/app/utils/ml`. In production environment, this should have a separate pipeline (triggered via push to remote branch) which would automatically compile and build artifacts for the trained model, and make it ready to be deployed once human approval is provided.

The model performance should be evaluated based on the incoming requests (preds vs actual) once the 'ground truth' is realized. If this a problem where it may never be realized, the relevant online metrics should be tracked and course correction automated if drift is deteceted or model performance degrades.


## Developer's Notes
Admittedly, this took me a little extra time than the suggested duration of 2 hours. Most of the extra time was spent in brainstorming and designing the architecture and writing this documentation, rather than actively coding :)
However, I think if only considering the development time, it should still make the cut.

It was an interesting exercise and I picked up some basic concepts about Flower dashboard along the way. Designing systems like these is usually based on past experience, so if there are some challenges very specific to this use case, it's possible I may have missed some considerations. I'll be happy to answer any questions if they arise. Thank you for this oppportunity.
