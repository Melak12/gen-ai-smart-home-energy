# Monolithic Backend Service

This folder contains the monolithic FastAPI backend for the Smart Home Energy Monitoring system. All features (authentication, telemetry, conversational AI) are implemented as routers in a single FastAPI app.

- `main.py`: FastAPI app entry point
- `requirements.txt`: Python dependencies
- `Dockerfile`: Containerization for the backend
- `tests/`: All backend tests

## Running Locally

Build and run with Docker Compose (see project root):

```
docker-compose up --build
```

## API Structure
- `/auth/*`: Authentication endpoints
- `/telemetry/*`: Telemetry endpoints
- `/ai/*`: Conversational AI endpoints

API docs available at `/docs` when running.
