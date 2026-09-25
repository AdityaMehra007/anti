"""Tests for InvoicingEngine and OutreachDispatcher."""
import os
import pytest
from omnimoney.invoicing_engine import InvoicingEngine
from omnimoney.dispatcher import OutreachDispatcher


def test_invoicing_engine(tmp_path):
    inv_dir = str(tmp_path / "invoices")
    engine = InvoicingEngine(invoices_dir=inv_dir)

    res = engine.generate_b2b_invoice(
        client_name="Dr. Sneha Rao",
        client_company="Aura Glow Clinic",
        client_email="director@auraglow.in",
        service_name="AI WhatsApp Qualifier Setup",
        amount_inr=20000.0,
        gst_included=True
    )

    assert res["status"] == "ISSUED"
    assert res["total_inr"] == 23600.0  # 20,000 + 18% GST
    assert os.path.exists(res["file_path"])
    assert "upi://" in res["upi_link"]

    with open(res["file_path"], "r", encoding="utf-8") as f:
        html = f.read()
        assert "Aura Glow Clinic" in html
        assert "Dr. Sneha Rao" in html
        assert "23,600" in html


def test_dispatcher_engine(tmp_path):
    queue_dir = str(tmp_path / "queue")
    dispatcher = OutreachDispatcher(output_dir=queue_dir)

    res = dispatcher.prepare_daily_dispatch_batch(batch_size=3)

    assert res["status"] == "DISPATCH_READY"
    assert res["prospects_processed"] <= 3
    assert res["eml_count"] <= 3
    assert os.path.exists(res["docket_file"])

    with open(res["docket_file"], "r", encoding="utf-8") as f:
        content = f.read()
        assert "1-CLICK DISPATCH DOCKET" in content
        assert "mailto:" in content


def test_api_generate_invoice():
    from fastapi.testclient import TestClient
    from omnimoney.server import app
    client = TestClient(app)
    response = client.post("/api/invoicing/generate", json={
        "client_name": "Karthik N.",
        "client_company": "Peak Form Crossfit",
        "client_email": "karthik@peakform.com",
        "service_name": "AI WhatsApp Booking Bot",
        "amount_inr": 15000.0,
        "gst_included": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ISSUED"
    assert data["total_inr"] == 15000.0
    assert "upi://" in data["upi_link"]


def test_api_prepare_dispatch():
    from fastapi.testclient import TestClient
    from omnimoney.server import app
    client = TestClient(app)
    response = client.post("/api/dispatch/prepare?batch_size=2")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "DISPATCH_READY"
    assert data["prospects_processed"] <= 2

