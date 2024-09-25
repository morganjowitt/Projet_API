from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Variables pour suivre l'état
service_start_time = datetime.now()
request_count = 0

@app.get("/health")
def health_check():
    global request_count
    uptime = datetime.now() - service_start_time
    return {
        "status": "OK",
        "uptime": str(uptime),
        "requests_served": request_count,
        "message": "The service is healthy and running."
    }
