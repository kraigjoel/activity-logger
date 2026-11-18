# Activity Logger

A lightweight, self-hosted activity tracking application built with Python, FastAPI, SQLite and Docker.

Activity Logger allows users to record activities, track time spent on tasks, and retrieve their activity history through a terminal-based client. The backend runs independently as a REST API, allowing clients on other devices to interact with a central database.

## Features

- Log activities with a name, duration and optional notes
- View previously recorded activities
- Validate activity names and durations
- REST API built with FastAPI
- SQLite database for persistent storage
- Docker deployment with persistent volumes
- Configurable API URL and database location
- Automated API tests using pytest
- Self-hosted deployment with Caddy reverse proxy

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API backend |
| Pydantic | Request validation |
| SQLite | Database |
| Requests | HTTP client |
| Docker / Docker Compose | Containerisation and deployment |
| pytest | Automated testing |
| Caddy | Reverse proxy |

## Architecture

```text
Client Device
    |
    | Python CLI (HTTP requests)
    v
Caddy Reverse Proxy
    |
    | Docker network
    v
FastAPI Server
    |
    v
SQLite Database
    |
    v
Docker Persistent Volume
```

The CLI and backend are separate components. The client communicates with the server through HTTP requests, while the server handles validation, database operations and API responses.

In the homelab deployment, Caddy routes requests from `activity.home` to the FastAPI container over a shared Docker network.

## Project Structure

```text
activity-logger/
├── client/
│   └── main.py
├── server/
│   ├── app.py
│   └── database.py
├── tests/
│   └── test_api.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .dockerignore
└── README.md
```

## Installation

### Prerequisites

- Python 3.10 or newer
- pip
- Docker and Docker Compose (for container deployment)

### 1. Clone the repository

```bash
git clone https://github.com/kraigjoel/activity-logger.git
cd activity-logger
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running Locally

Start the FastAPI server:

```bash
uvicorn server.app:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

Launch the terminal client in a separate terminal:

```bash
python client/main.py
```

The client connects to the local API by default.

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Docker Deployment

Build and start the application:

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

Verify the API:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

View logs:

```bash
docker compose logs --tail=50
```

Stop the application:

```bash
docker compose down
```

### Persistent Storage

The SQLite database is stored in a Docker named volume, allowing activity records to survive container restarts and recreation.

The database path can be configured through:

```text
ACTIVITY_DB_PATH=/data/activities.db
```

**Note:** `docker compose down -v` removes Compose-managed named volumes, including the database volume. Persistent storage is not a substitute for backups.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/activities` | Retrieve activity records |
| POST | `/activities` | Create an activity |

### Create an Activity

Request:

```bash
curl -X POST http://127.0.0.1:8000/activities \
  -H "Content-Type: application/json" \
  -d '{
    "activity": "CCNA Study",
    "duration": 60,
    "notes": "Practised VLAN configuration"
  }'
```

Example response:

```json
{
  "log_id": 1
}
```

A successful creation returns HTTP status `201 Created`.

### Retrieve Activities

```bash
curl http://127.0.0.1:8000/activities
```

### Input Validation

The API enforces the following rules:

- Activity names must not be empty or consist only of whitespace.
- Duration must be a positive integer representing minutes.
- Notes are optional.

Invalid requests are rejected by FastAPI's validation system.

## Connecting a Remote Client

The CLI supports a configurable API address through the `ACTIVITY_API_URL` environment variable.

Example:

```bash
ACTIVITY_API_URL=http://activity.home python client/main.py
```

This allows the terminal client to run on a separate computer while storing activity records on the central server.

The `activity.home` hostname is specific to the author's homelab. Replace it with your own server address or hostname.

## Homelab Deployment

The application is deployed on an Ubuntu Docker VM hosted by Proxmox VE.

The deployment uses:

- Docker Compose for application management
- A Docker named volume for SQLite storage
- A shared `proxy` Docker network
- Caddy for HTTP reverse proxying
- Pi-hole for local DNS resolution

Example Caddy configuration:

```caddyfile
http://activity.home {
    reverse_proxy activity-logger:8000
}
```

The hostname is intended for private network use, not public internet exposure.

### Security

The current API does not implement user authentication or authorisation.

It should only be exposed to trusted clients on a restricted private network. Public deployment would require additional access controls.

## Testing

Install the testing dependencies if necessary:

```bash
pip install pytest httpx
```

Run the automated tests:

```bash
python -m pytest -v
```

The API test suite covers health checks, activity creation, input validation, retrieval and database persistence.

## Future Improvements

- Authentication and user accounts
- Automated SQLite backups
- Activity editing and deletion
- Activity summaries and statistics
- Web-based dashboard
- Export activity records to CSV
- CI workflow for automated testing

## What I Learned

This project provided practical experience with:

- Designing REST API endpoints using FastAPI
- Handling HTTP requests and responses
- Validating data using Pydantic
- Implementing CRUD-related database operations with SQLite
- Separating client and server responsibilities
- Writing automated API tests
- Containerising a Python application
- Managing persistent data with Docker volumes
- Deploying and networking services in a self-hosted environment

## Author

Developed by [kraigjoel](https://github.com/kraigjoel).
