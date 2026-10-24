"""Tests for ApexFlow FastAPI REST Endpoints."""

import pytest
from fastapi.testclient import TestClient
from projects.apex_enterprise_orchestrator.api.server import app

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert "version" in data


def test_metrics_prometheus_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "apexflow_uptime_seconds" in response.text


def test_single_reconcile_with_idempotency():
    payload = {
        "purchase_order": {
            "po_id": "PO-TEST-001",
            "vendor_id": "VEND-10",
            "sku": "SKU-TEST",
            "quantity_ordered": 100,
            "unit_price": 50.0,
        },
        "goods_receipt": {
            "grn_id": "GRN-TEST-001",
            "po_id": "PO-TEST-001",
            "sku": "SKU-TEST",
            "quantity_received": 100,
            "received_timestamp": "2026-10-21T10:00:00Z",
        },
        "invoice": {
            "invoice_id": "INV-TEST-001",
            "po_id": "PO-TEST-001",
            "vendor_id": "VEND-10",
            "sku": "SKU-TEST",
            "billed_quantity": 100,
            "billed_unit_price": 50.0,
        },
    }

    headers = {"X-Idempotency-Key": "TEST-IDEMP-KEY-999"}

    # 1. First execution
    resp1 = client.post("/api/v1/reconcile/single", json=payload, headers=headers)
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["verdict"] == "EXACT_MATCH"
    assert data1["action"] == "AUTO_APPROVE"

    # 2. Second execution (Cache hit via Idempotency Ledger)
    resp2 = client.post("/api/v1/reconcile/single", json=payload, headers=headers)
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2 == data1


def test_simulate_stream_endpoint():
    response = client.post("/api/v1/simulate", json={"record_count": 500})
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] == 500
    assert "throughput_records_per_sec" in data
    assert data["total_exposure_prevented"] > 0
