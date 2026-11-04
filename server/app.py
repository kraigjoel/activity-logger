from fastapi import FastAPI
from .database import get_all_activities, insert_activity
from pydantic import BaseModel, Field

app = FastAPI()

class ActivityCreate(BaseModel):
    activity: str
    duration: int = Field(gt=0)
    notes: str | None = None

@app.get("/health")
def get_health():
    return {"status" : "healthy"}

@app.get("/activities")
def get_activities():
    activities = get_all_activities()
    return activities

@app.post("/activities")
def create_activity(activity: ActivityCreate):
    log_id = insert_activity(activity.activity, activity.duration, activity.notes)

    return {"log_id": log_id}