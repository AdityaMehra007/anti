"""
Unit test for TradeNexus live pilot delivery engine and batch processing across 7 enterprise accounts.
"""
import pytest
import os
import sys

ENGINEERING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ENGINEERING_DIR)

from src.pilot_processor import PilotProductionProcessor
from src.models import CommercialInvoice, LineItem

def test_pilot_processor_single_docket():
    inv = CommercialInvoice(
        invoice_number="EXP-TEST-001",
        exporter_name="Tata Motors Limited",
        exporter_iec="0388012345",
        exporter_gstin="27AAACT1234F1Z1",
        consignee_name="Jaguar Land Rover UK",
        consignee_country="GB",
        port_of_loading="INNSA1",
        port_of_discharge="GBSOU",
        total_amount=95000.0,
        incoterm="CIF",
        items=[
            LineItem(
                item_id="ITM-TM-01",
                description="Automotive Aluminum Chassis Assemblies",
                quantity=40,
                unit="PCS",
                unit_price=2000.0,
                total_value=80000.0,
                currency="GBP",
                declared_hs_code="87082900",
                weight_kg=2400.0
            )
        ]
    )
    bundle = PilotProductionProcessor.process_export_docket(inv, apply_auto_corrections=True)
    assert bundle.bundle_id.startswith("BUNDLE-")
    assert bundle.compliance_score > 0
    assert bundle.cryptographic_seal is not None
    assert len(bundle.icegate_flatfile_content) > 0

def test_batch_pilot_processing_all_accounts():
    CUSTOMERS_DIR = os.path.abspath(os.path.join(ENGINEERING_DIR, "..", "03_CUSTOMERS"))
    sys.path.insert(0, CUSTOMERS_DIR)
    
    from pilot_delivery_engine import process_all_pilot_accounts
    results = process_all_pilot_accounts()
    
    assert len(results) >= 7, "Must process all 7 enterprise accounts"
    account_names = [r["exporter"] for r in results]
    assert any("Sansera" in name for name in account_names)
    assert any("Tata" in name or "Motors" in name for name in account_names)
    assert any("Bharat Forge" in name for name in account_names)
    assert any("Reddy" in name for name in account_names)
