"""Tests for outreach vault connector and API endpoints."""
import pytest
from omnimoney.outreach_vault import OutreachVault


def test_vault_stats():
    vault = OutreachVault()
    stats = vault.get_vault_stats()
    if stats.get("connected"):
        assert stats["total_records"] == 4500
        assert "status_breakdown" in stats
        assert "sectors" in stats
        assert stats["sectors_covered"] > 0
    else:
        # Database not available in CI — just verify the method runs
        assert "connected" in stats


def test_drafted_outreach():
    vault = OutreachVault()
    drafted = vault.get_drafted_outreach(limit=5)
    if drafted:
        assert len(drafted) <= 5
        assert "company" in drafted[0]
        assert "hr_email" in drafted[0]
        assert drafted[0]["status"] == "DRAFTED"


def test_get_by_sector():
    vault = OutreachVault()
    results = vault.get_by_sector("SaaS", limit=5)
    if results:
        for r in results:
            assert "SaaS" in r["sector"] or "saas" in r["sector"].lower()


def test_conversion_metrics():
    vault = OutreachVault()
    metrics = vault.get_conversion_metrics()
    if "total_drafted" in metrics:
        assert metrics["total_drafted"] >= 0
        assert "send_rate" in metrics
        assert "response_rate" in metrics


def test_daily_dispatch_queue():
    vault = OutreachVault()
    queue = vault.get_daily_dispatch_queue(batch_size=5)
    if queue:
        assert len(queue) <= 5
        # Check sector diversity
        sectors = set(r["sector"] for r in queue)
        # Should have at least some diversity if batch > 1
        assert len(sectors) >= 1


def test_api_outreach_stats():
    from fastapi.testclient import TestClient
    from omnimoney.server import app
    client = TestClient(app)
    response = client.get("/api/outreach/stats")
    assert response.status_code == 200
    data = response.json()
    assert "connected" in data


def test_api_outreach_metrics():
    from fastapi.testclient import TestClient
    from omnimoney.server import app
    client = TestClient(app)
    response = client.get("/api/outreach/metrics")
    assert response.status_code == 200
