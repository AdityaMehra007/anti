"""
Test Suite for OMEGA Omniverse Supreme REST API Server & Pitch Deck Generator.
Validates all endpoints, startup retrieval, deal pipeline, and presentation assets.
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

ROOT_DIR = "E:/anti"
sys.path.insert(0, ROOT_DIR)

from omega_omniverse_api import app

client = TestClient(app)

def test_api_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPERATIONAL"
    assert data["verified_tests_passed"] >= 117
    assert len(data["active_subsystems"]) == 9

def test_startups_endpoint_and_filtering():
    # Fetch default list
    res = client.get("/api/startups?limit=5")
    assert res.status_code == 200
    d = res.json()
    assert d["total"] == 500
    assert len(d["results"]) == 5

    # Search for Zerodha
    res_search = client.get("/api/startups?q=Zerodha")
    assert res_search.status_code == 200
    d_search = res_search.json()
    assert d_search["total"] == 1
    assert d_search["results"][0]["company_name"] == "Zerodha"

def test_startup_detail_and_prompt():
    res = client.get("/api/startups/BLR-STARTUP-001")
    assert res.status_code == 200
    detail = res.json()
    assert detail["company_name"] == "Flipkart"
    assert "TitanGrid" in detail["biggest_project"]["project_name"]

    res_prm = client.get("/api/startups/BLR-STARTUP-001/prompt")
    assert res_prm.status_code == 200
    assert len(res_prm.text) >= 1500

def test_deals_endpoint_and_pipeline_value():
    res = client.get("/api/deals?limit=10")
    assert res.status_code == 200
    data = res.json()
    assert data["total_accounts"] >= 500
    assert data["total_pipeline_inr"] > 4000000000, "Pipeline should be > INR 4 Billion"
    assert len(data["accounts"]) == 10

def test_fortune500_endpoint():
    res = client.get("/api/fortune500")
    assert res.status_code == 200
    data = res.json()
    assert data["total_corporations"] == 500
    assert len(data["sample_architectures"]) == 4

def test_telemetry_simulation_endpoint():
    res = client.get("/api/telemetry/simulate")
    assert res.status_code == 200
    sim = res.json()
    assert 9000 <= sim["tps"] <= 12000
    assert sim["p99_latency_ms"] < 1.0

def test_pitch_decks_generation():
    deck_dir = os.path.join(ROOT_DIR, "reports", "pitch_decks")
    assert os.path.exists(deck_dir), "Pitch decks directory must exist"
    decks = [f for f in os.listdir(deck_dir) if f.startswith("PITCH_DECK_") and f.endswith(".html")]
    assert len(decks) >= 20, f"Expected at least 20 pitch decks, found {len(decks)}"

def test_outbound_api_endpoints():
    # 1. Metrics endpoint
    res_m = client.get("/api/outbound/metrics")
    assert res_m.status_code == 200
    metrics = res_m.json()
    assert metrics["total_accounts"] == 546
    assert metrics["total_pipeline_arr_inr"] > 4_000_000_000

    # 2. Ledger endpoint
    res_l = client.get("/api/outbound/ledger?limit=10")
    assert res_l.status_code == 200
    ledger = res_l.json()
    assert ledger["total"] == 546
    assert len(ledger["results"]) == 10

    # 3. Dispatch endpoint (dry run)
    res_d = client.post("/api/outbound/dispatch?limit=5&dry_run=true")
    assert res_d.status_code == 200
    dispatch_res = res_d.json()
    assert dispatch_res["dispatched_count"] == 5
    assert dispatch_res["dry_run"] is True
    assert len(dispatch_res["receipts"]) == 5
    assert dispatch_res["receipts"][0]["status"] == "MOCKED"
