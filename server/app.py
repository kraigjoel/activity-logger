from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/activities/{activity_name}")
def get_activity(activity_name: str):
    return {
        "activity": activity_name,
        "message": f"You requested {activity_name}"
    }