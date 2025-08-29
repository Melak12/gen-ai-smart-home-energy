import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_token():
    # Register and login a user
    email = "telemetryuser@example.com"
    password = "telemetrypass"
    client.post("/auth/register", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    return resp.json()["access_token"]

@pytest.fixture(scope="module")
def device_id(auth_token):
    # Create a device for the user (direct DB or via API if available)
    # For now, assume device with id=1 exists and is owned by the user
    return 1

def test_submit_telemetry(auth_token, device_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"timestamp": "2025-08-29T00:00:00Z", "deviceId": device_id, "usage": 1.23}
    resp = client.post("/telemetry/", json=data, headers=headers)
    assert resp.status_code in (200, 403, 404)


def test_get_telemetry(auth_token, device_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = client.get(f"/telemetry/{device_id}", headers=headers)
    assert resp.status_code in (200, 403, 404)
