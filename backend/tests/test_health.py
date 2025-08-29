from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_auth_health():
    response = client.get("/auth/health")
    assert response.status_code == 200
    assert response.json()["service"] == "auth"

def test_telemetry_health():
    response = client.get("/telemetry/health")
    assert response.status_code == 200
    assert response.json()["service"] == "telemetry"

def test_ai_health():
    response = client.get("/ai/health")
    assert response.status_code == 200
    assert response.json()["service"] == "conversational_ai"
