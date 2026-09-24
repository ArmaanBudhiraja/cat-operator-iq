import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "CAT OperatorIQ"
    assert "advisory_disclaimer" in data

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_safety_live_endpoint():
    response = client.get("/api/safety/live")
    assert response.status_code == 200
    data = response.json()
    assert "safety_score" in data
    assert "risk_level" in data
    assert "radar_objects" in data
    assert "advisory_disclaimer" in data

def test_simulation_inject_hazard():
    response = client.post("/api/simulation/inject", json={"hazard_type": "worker_proximity", "machine_id": "EXC001"})
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["status"] == "Injected"

    # Reset
    reset_resp = client.post("/api/simulation/reset")
    assert reset_resp.status_code == 200

def test_assistant_query_endpoint():
    response = client.post("/api/assistant/query", json={"query": "How long will my task take?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "evidence" in data
    assert "recommended_next_step" in data
    assert "safety_disclaimer" in data
    assert "is_fallback" in data
    assert "ai_provider" in data

def test_assistant_status_endpoint():
    response = client.get("/api/assistant/status")
    assert response.status_code == 200
    data = response.json()
    assert "ai_configured" in data
    assert "fallback_available" in data

def test_dashboard_endpoint_weather():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "weather" in data
    assert "condition" in data["weather"]
    assert "temperature_c" in data["weather"]
    assert "is_live" in data["weather"]
