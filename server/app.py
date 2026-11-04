from fastapi import FastAPI
from .database import get_all_activities

app = FastAPI()

@app.get("/health")
def get_health():
    return {"status" : "healthy"}

@app.get("/activities")
def get_activities():
    activities = get_all_activities()
    return activities