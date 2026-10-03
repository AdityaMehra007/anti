import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.auto_corrector import DocketAutoCorrector
from src.audit_ledger import CryptographicAuditLedger

@pytest.fixture(autouse=True)
def clean_ledger():
    CryptographicAuditLedger.reset_ledger()

def test_auto_corrector_fixes_uom_and_hs():
    inv_data = {
        "invoice_number": "TEST-INV-101",
        "exporter_name": "Test Exporter Pvt Ltd",
        "destination_country": "DE",
        "buyer_tax_id": "",
        "line_items": [
            {
                "item_number": 1,
                "description": "Steel Radial Bearings",
                "hs_code": "848210",
                "quantity": 100,
                "unit_of_measure": "PCS",
                "unit_price": 50.0,
                "total_price": 5000.0
            }
        ]
    }
    report = DocketAutoCorrector.analyze_and_correct(inv_data)
    assert report.invoice_number == "TEST-INV-101"
    assert report.total_issues_found >= 3
    assert report.auto_correctable >= 2
    uom_sugg = next(s for s in report.suggestions if s.issue_type == "UNIT_OF_MEASURE")
    assert uom_sugg.suggested_value == "NOS"
    hs_sugg = next(s for s in report.suggestions if s.issue_type == "TARIFF_PREFIX")
    assert hs_sugg.suggested_value == "84821010"

def test_cryptographic_audit_ledger_chaining():
    inv_data1 = {
        "invoice_number": "INV-2027-001",
        "exporter_name": "Sansera Engineering",
        "destination_country": "DE",
        "line_items": [{"hs_code": "73269099"}]
    }
    audit_data = {"status": "PASSED", "compliance_score": 98.5}
    entry1 = CryptographicAuditLedger.record_audit(inv_data1, audit_data)
    assert entry1.entry_id == "LE-2027-00001"
    assert entry1.previous_block_hash == CryptographicAuditLedger.GENESIS_HASH

    inv_data2 = {
        "invoice_number": "INV-2027-002",
        "exporter_name": "Dynamatic Technologies",
        "destination_country": "FR",
        "line_items": [{"hs_code": "88033000"}]
    }
    entry2 = CryptographicAuditLedger.record_audit(inv_data2, audit_data)
    assert entry2.entry_id == "LE-2027-00002"
    assert entry2.previous_block_hash == entry1.current_block_hash

    cert = CryptographicAuditLedger.verify_entry("LE-2027-00001")
    assert cert is not None
    assert cert.invoice_number == "INV-2027-001"
    assert cert.is_valid is True
    assert cert.chain_height == 1

def test_api_ledger_and_corrector_endpoints():
    from fastapi.testclient import TestClient
    from src.api import app
    client = TestClient(app)
    payload = {
        "invoice_number": "INV-API-999",
        "exporter_name": "Maini Precision Products",
        "exporter_iec": "0798012345",
        "exporter_gstin": "29AABCM1234F1Z1",
        "consignee_name": "Bosch GmbH",
        "consignee_country": "DE",
        "port_of_loading": "INBLR4",
        "port_of_discharge": "DEHAM",
        "total_amount": 2500.0,
        "incoterm": "FOB",
        "items": [
            {
                "item_id": "ITM-01",
                "description": "Precision Machined Steel Shaft",
                "quantity": 50,
                "unit": "PCS",
                "unit_price": 50.0,
                "total_value": 2500.0,
                "currency": "EUR",
                "declared_hs_code": "732690",
                "weight_kg": 120.0
            }
        ]
    }
    resp = client.post("/api/v1/docket/auto-correct", json=payload)
    assert resp.status_code == 200
    assert resp.json()["total_issues_found"] >= 2

    resp_ledger = client.post("/api/v1/ledger/record", json=payload)
    assert resp_ledger.status_code == 200
    ledger_data = resp_ledger.json()
    entry_id = ledger_data["entry_id"]

    resp_verify = client.get(f"/api/v1/ledger/verify/{entry_id}")
    assert resp_verify.status_code == 200
    assert resp_verify.json()["is_valid"] is True
