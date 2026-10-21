"""
FORTUNE 500 ECOSYSTEM END-TO-END TEST SUITE
===========================================
Pytest integration suite verifying:
  1. REST API Server Routing & JSON Endpoints
  2. Live Dynamic Engine Execution over HTTP POST
  3. Parallel Swarm Batch Orchestration Concurrency
  4. C-Suite Proposal & Statement of Work Integrity
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import threading
import pytest

from fortune_500_server import ThreadingHTTPServer, Fortune500RequestHandler
from fortune_500_swarm_orchestrator import run_swarm_batch, execute_single_project
from fortune_500_proposal_generator import generate_executive_proposal

TEST_HOST = "127.0.0.1"
TEST_PORT = 8991
_server_thread = None
_httpd = None


@pytest.fixture(scope="module", autouse=True)
def setup_test_server():
    global _httpd, _server_thread
    server_address = (TEST_HOST, TEST_PORT)
    _httpd = ThreadingHTTPServer(server_address, Fortune500RequestHandler)
    _server_thread = threading.Thread(target=_httpd.serve_forever, daemon=True)
    _server_thread.start()
    time.sleep(0.3)  # Allow server to bind and start
    yield
    if _httpd:
        _httpd.shutdown()
        _httpd.server_close()


def test_server_health_endpoint():
    url = f"http://{TEST_HOST}:{TEST_PORT}/health"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "ONLINE"
        assert data["total_projects"] == 500


def test_server_projects_query_and_search():
    # Test all projects pagination
    url = f"http://{TEST_HOST}:{TEST_PORT}/api/projects?limit=10"
    with urllib.request.urlopen(url) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["total_matched"] == 500
        assert len(data["projects"]) == 10

    # Test sector filter
    url_sec = f"http://{TEST_HOST}:{TEST_PORT}/api/projects?sector=financials"
    with urllib.request.urlopen(url_sec) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        assert data["total_matched"] > 0
        assert "Financials" in data["projects"][0]["sector"]

    # Test keyword search
    url_q = f"http://{TEST_HOST}:{TEST_PORT}/api/projects?q=apple"
    with urllib.request.urlopen(url_q) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        assert any(p["ticker"] == "AAPL" for p in data["projects"])


def test_server_single_project_lookup():
    url = f"http://{TEST_HOST}:{TEST_PORT}/api/projects/1"
    with urllib.request.urlopen(url) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["rank"] == 1
        assert data["company"] == "Walmart"
        assert data["ticker"] == "WMT"


def test_server_dynamic_project_execution_post():
    # Test POST /api/execute/12 (JPMorgan Chase)
    url = f"http://{TEST_HOST}:{TEST_PORT}/api/execute/12"
    req = urllib.request.Request(url, data=b"{}", method="POST")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        result = json.loads(resp.read().decode("utf-8"))
        assert result["rank"] == 12
        assert result["ticker"] == "JPM"
        assert result["success"] is True
        assert result["status"] == "EXECUTED"
        assert result["latency_us"] > 0


def test_swarm_orchestrator_parallel_slice():
    report = run_swarm_batch(max_workers=4, limit=10)
    meta = report["metadata"]
    assert meta["total_projects_dispatched"] == 10
    assert meta["successful_executions"] == 10
    assert meta["execution_rate_pct"] == 100.0
    assert meta["total_batch_duration_seconds"] > 0


def test_proposal_generator_contract_structure():
    mock_proj = {
        "company": "Tesla",
        "ticker": "TSLA",
        "rank": 50,
        "project_codename": "PROJECT TITAN-TSLA",
        "sector": "Consumer Discretionary",
        "quantified_enterprise_impact_billion_usd": 6.0,
        "architectural_paradigm": "Autonomous High-Concurrency Distributed Systems",
        "core_deep_modules": [
            "Battery Cell Thermodynamic Mesh",
            "Full Self-Driving Fleet Invariant Bus",
            "Megapack Grid Frequency Balancer",
            "Zero-Trust Telemetry Sentinel"
        ],
        "tech_stack": "Rust, CUDA, C++20, ROS2"
    }
    proposal = generate_executive_proposal(mock_proj)
    assert "# EXECUTIVE STATEMENT OF WORK (SOW)" in proposal
    assert "PROJECT TITAN-TSLA" in proposal
    assert "+$6.0 Billion USD" in proposal
    assert "90-Day Enterprise Execution Roadmap" in proposal
    assert "Service Level Agreement (SLA)" in proposal
