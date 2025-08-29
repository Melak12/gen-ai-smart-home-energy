import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_token():
    email = "aiuser@example.com"
    password = "aipass"
    client.post("/auth/register", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    return resp.json()["access_token"]

def test_ai_query(monkeypatch, auth_token):
    def fake_gemini(prompt):
        return "This is a mock Gemini response."
    monkeypatch.setattr("utils.gemini.query_gemini", fake_gemini)
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"question": "How much energy did I use last week?"}
    resp = client.post("/ai/query", json=data, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["answer"] == "This is a mock Gemini response."
