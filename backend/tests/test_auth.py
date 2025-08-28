import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpass123"

@pytest.fixture(scope="module")
def register_user():
    resp = client.post("/auth/register", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    return resp

def test_register(register_user):
    assert register_user.status_code in (200, 400)  # 400 if already registered

def test_login():
    resp = client.post("/auth/login", data={"username": TEST_EMAIL, "password": TEST_PASSWORD})
    assert resp.status_code == 200
    assert "access_token" in resp.json()
