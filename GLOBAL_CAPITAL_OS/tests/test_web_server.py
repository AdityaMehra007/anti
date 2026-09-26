"""Test FastAPI endpoints for GLOBAL CAPITAL OS Command Center."""

import pytest
from fastapi.testclient import TestClient
from GLOBAL_CAPITAL_OS.web.server import app

client = TestClient(app)


def test_dashboard_html_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "GLOBAL CAPITAL OS" in response.text
    assert "Founder Capital Engine" in response.text


def test_api_telemetry():
    response = client.get("/api/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert "posture" in data
    assert "scores" in data
    assert "ladder" in data
    assert data["operator"] == "Aditya Mehra"


def test_api_treasury():
    response = client.get("/api/treasury")
    assert response.status_code == 200
    data = response.json()
    assert "total_treasury_inr" in data
    assert "accounts" in data
    assert len(data["accounts"]) >= 5


def test_api_deals():
    response = client.get("/api/revenue/deals")
    assert response.status_code == 200
    deals = response.json()
    assert len(deals) > 0
    assert "deal_value_inr" in deals[0]


def test_api_opportunities():
    response = client.get("/api/opportunities")
    assert response.status_code == 200
    opps = response.json()
    assert len(opps) == 15
    assert opps[0]["zero_capital_score"] > 80.0


def test_api_reconciliation():
    response = client.get("/api/reconciliation")
    assert response.status_code == 200
    recon = response.json()
    assert recon["audit_chain_valid"] is True


def test_api_daily_brief():
    response = client.get("/api/daily-brief")
    assert response.status_code == 200
    brief = response.json()
    assert "financial_summary" in brief
    assert "top_3_actions" in brief
    assert len(brief["top_3_actions"]) == 3
