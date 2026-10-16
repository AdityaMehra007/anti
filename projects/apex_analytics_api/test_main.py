"""
Unit tests for apex_analytics_api
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "apex_analytics_api"
    assert data["status"] == "ONLINE"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "HEALTHY"}


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "apex_analytics_api"
    assert "total_incidents" in data
    assert data["total_incidents"] == 500
    assert data["sla_breaches"] == 83
    assert data["total_penalty_recovery_inr"] == 3108800.0
