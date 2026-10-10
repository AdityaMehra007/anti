"""Integration tests for BSU OS FastAPI REST endpoints."""

import pytest
from fastapi.testclient import TestClient
from bsu_os.server import app
from bsu_os.seed_data import seed_database


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_database()


client = TestClient(app)


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_list_startups_endpoint():
    res = client.get("/api/startups")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 5


def test_get_startup_detail_endpoint():
    res = client.get("/api/startups/1")
    assert res.status_code == 200
    data = res.json()
    assert "founders" in data
    assert "funding_rounds" in data
    assert "open_jobs" in data


def test_clusters_endpoint():
    res = client.get("/api/clusters")
    assert res.status_code == 200
    clusters = res.json()
    assert len(clusters) >= 5
    assert any(c["id"] == "koramangala" for c in clusters)


def test_search_endpoint():
    res = client.get("/api/search?q=Zerodha")
    assert res.status_code == 200
    results = res.json()
    assert "startups" in results
    assert len(results["startups"]) > 0


def test_war_room_endpoints():
    for room in ["founder", "investor", "career", "recruiter", "command"]:
        res = client.get(f"/api/war-rooms/{room}")
        assert res.status_code == 200, f"Failed for war room: {room}"


def test_daily_brief_endpoint():
    res = client.get("/api/daily-brief")
    assert res.status_code == 200
    data = res.json()
    assert "opportunities" in data
    assert "emerging_trend" in data


def test_copilot_endpoint():
    payload = {"query": "Tell me about Sarvam AI", "mode": "general"}
    res = client.post("/api/copilot/query", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "verdict" in data
    assert "evidence" in data
    assert "fit_score" in data
