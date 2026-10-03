import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.us_cbp_connector import USCustomsConnector
from src.regulatory_synchronizer import RegulatorySynchronizer, GazetteNotification
from src.hs_engine import HSCatalog

def test_us_cbp_connector_audit():
    items = [
        {
            "item_id": "US-LINE-01",
            "description": "Precision Forged Connecting Rods",
            "hs_code": "73269099",
            "value_usd": 50000.0
        },
        {
            "item_id": "US-LINE-02",
            "description": "Radial Ball Bearings",
            "hs_code": "84821010",
            "value_usd": 20000.0
        }
    ]
    report = USCustomsConnector.audit_us_shipment(
        entry_id="CBP-2027-9911",
        importer_name="General Motors LLC",
        port_of_entry="USNYC",
        line_items=items
    )
    assert report.entry_reference == "CBP-2027-9911"
    assert report.total_entered_value_usd == 70000.0
    assert report.status == "PASSED_READY_FOR_CBP_ACE_TRANSMISSION"
    assert len(report.items) == 2
    assert report.items[0].hts_us_code == "7326.90.8688"
    assert report.items[0].section_232_applicable is True
    assert "CBP7501*ENTRY*CBP-2027-9911" in report.customs_entry_flatfile

def test_regulatory_gazette_hot_sync():
    notifs = [
        GazetteNotification(
            notification_number="DGFT-NOTIF-45/2026",
            issuing_authority="DGFT",
            effective_date="2026-10-01",
            subject="High Precision Titanium Aerospace Fasteners",
            amended_hs_code="81089090",
            new_tariff_rate=0.0,
            cbam_status=False,
            scomet_status=True
        )
    ]
    res = RegulatorySynchronizer.process_gazette_notifications(notifs)
    assert res.catalog_entries_updated == 1
    assert res.status == "SUCCESS_CATALOG_HOT_UPDATED"
    
    # Verify HSCatalog was updated in memory
    match = HSCatalog.classify("High Precision Titanium Aerospace Fasteners")
    assert match["hs_code"] == "81089090"
    assert match["scomet_restricted"] is True
