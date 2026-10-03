import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.models import CommercialInvoice, LineItem
from src.pilot_processor import PilotProductionProcessor
from src.audit_ledger import CryptographicAuditLedger

@pytest.fixture(autouse=True)
def clean_ledger():
    CryptographicAuditLedger.reset_ledger()

def test_pilot_processor_end_to_end_bundle():
    invoice = CommercialInvoice(
        invoice_number="EXP-SANSERA-001",
        exporter_name="Sansera Engineering Limited",
        exporter_iec="0788012345",
        exporter_gstin="29AAACS1234F1Z5",
        consignee_name="Stellantis N.V. / Opel Automobile GmbH",
        consignee_country="DE",
        port_of_loading="INBLR4",
        port_of_discharge="DEHAM",
        total_amount=48500.0,
        incoterm="CIF",
        items=[
            LineItem(
                item_id="ITM-SAN-01",
                description="Precision Forged Steel Connecting Rods",
                quantity=1200,
                unit="PCS",
                unit_price=25.0,
                total_value=30000.0,
                currency="EUR",
                declared_hs_code="73269099",
                weight_kg=1450.0
            ),
            LineItem(
                item_id="ITM-SAN-02",
                description="Radial Ball Bearings for Transmission",
                quantity=370,
                unit="PCS",
                unit_price=50.0,
                total_value=18500.0,
                currency="EUR",
                declared_hs_code="84821010",
                weight_kg=520.0
            )
        ]
    )

    bundle = PilotProductionProcessor.process_export_docket(invoice, apply_auto_corrections=True)

    assert bundle.bundle_id.startswith("BUNDLE-EXP-SANSERA-001")
    assert bundle.client_name == "Sansera Engineering Limited"
    assert bundle.ready_for_customs_filing is True
    assert bundle.auto_corrections_applied >= 1
    assert "<TABLE>CHEXP01" in bundle.icegate_flatfile_content
    assert bundle.cbam_xml_content is not None
    assert "<CBAMDeclaration" in bundle.cbam_xml_content
    assert bundle.ledger_entry_id == "LE-2027-00001"
    assert bundle.cryptographic_seal.startswith("TRADENEXUS-SIG-")

def test_pilot_processor_api_endpoint():
    from fastapi.testclient import TestClient
    from src.api import app
    client = TestClient(app)

    payload = {
        "invoice_number": "EXP-DYN-999",
        "exporter_name": "Dynamatic Technologies Limited",
        "exporter_iec": "0791004321",
        "exporter_gstin": "29AAACD9876E1Z2",
        "consignee_name": "Airbus Commercial Aircraft",
        "consignee_country": "FR",
        "port_of_loading": "INBLR4",
        "port_of_discharge": "FRTLS",
        "total_amount": 75000.0,
        "incoterm": "FOB",
        "items": [
            {
                "item_id": "DYN-AERO-01",
                "description": "Aircraft Flap Track Structural Beam",
                "quantity": 2,
                "unit": "NOS",
                "unit_price": 37500.0,
                "total_value": 75000.0,
                "currency": "EUR",
                "declared_hs_code": "88033000",
                "weight_kg": 320.0
            }
        ]
    }

    resp = client.post("/api/v1/pilot/process-docket", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["client_name"] == "Dynamatic Technologies Limited"
    assert data["ready_for_customs_filing"] is True
    assert data["ledger_entry_id"] is not None
