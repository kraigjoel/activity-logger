from fastapi import FastAPI
from .database import get_all_activities, insert_activity, initialise_database
from pydantic import BaseModel, Field, field_validator
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_database()
    yield
    

app = FastAPI(lifespan=lifespan)

class ActivityCreate(BaseModel):
    activity: str = Field(min_length=1)
    duration: int = Field(gt=0)
    notes: str | None = None

    @field_validator("activity")
    @classmethod
    def validate_activity(cls,value):
        activity = value.strip()

        if not activity:
            raise ValueError("Activity name cannot be empty")

        return activity


@app.get("/health")
def get_health():
    return {"status" : "healthy"}

@app.get("/activities")
def get_activities():
    activities = get_all_activities()
    return activities

@app.post("/activities", status_code=201)
def create_activity(activity: ActivityCreate):
    log_id = insert_activity(activity.activity, activity.duration, activity.notes)

    return {"log_id": log_id}