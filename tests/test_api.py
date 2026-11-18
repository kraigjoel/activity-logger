
import pytest
from fastapi.testclient import TestClient

from server import database
from server.app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Create an isolated database for each test
    test_db = tmp_path / "test_activities.db"

    # Redirect database operations to our test database
    monkeypatch.setattr(database, "DB_PATH", test_db)

    # Run FastAPI's startup and shutdown lifecycle
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_activity(client):
    response = client.post(
        "/activities",
        json={
            "activity": "CCNA Study",
            "duration": 60,
            "notes": "Subnetting practice"
        }
    )

    assert response.status_code == 201
    assert response.json()["log_id"] == 1


def test_reject_empty_activity(client):
    response = client.post(
        "/activities",
        json={
            "activity": "   ",
            "duration": 30
        }
    )

    assert response.status_code == 422


def test_reject_invalid_duration(client):
    response = client.post(
        "/activities",
        json={
            "activity": "Gym",
            "duration": 0
        }
    )

    assert response.status_code == 422


def test_retrieve_activities(client):
    client.post(
        "/activities",
        json={
            "activity": "Muay Thai",
            "duration": 90
        }
    )

    response = client.get("/activities")

    assert response.status_code == 200

    activities = response.json()

    assert len(activities) == 1
    assert activities[0]["activity"] == "Muay Thai"
    assert activities[0]["duration"] == 90


def test_activity_persists(client):
    client.post(
        "/activities",
        json={
            "activity": "Programming",
            "duration": 45
        }
    )

    # Read directly from SQLite to verify storage
    activities = database.get_all_activities()

    assert len(activities) == 1
    assert activities[0]["activity"] == "Programming"
