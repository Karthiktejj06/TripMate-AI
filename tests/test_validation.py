from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_plan_rejects_invalid_days():
    response = client.post("/api/plan", json={
        "origin": "Hyderabad",
        "destination": "Goa",
        "days": 0,
        "travellers": 2,
        "budget": 20000,
        "currency": "INR",
        "preferences": ""
    })
    assert response.status_code == 422
