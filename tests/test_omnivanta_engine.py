import os
import sys
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from omnivanta_engine import OmniVantaAuditEngine, AuditConfig

@pytest.fixture
def sample_rate_card():
    return {
        "ITEM_LOGISTICS_SHUTTLE": {
            "vendor": "Bangalore Express Logistics",
            "category": "Fleet Operations",
            "contracted_rate_inr": 50000.0,
            "grace_period_minutes": 15.0,
            "penalty_per_hour_delay_pct": 10.0,
            "max_penalty_pct": 30.0
        },
        "ITEM_FABRICATION_STAGING": {
            "vendor": "Apex Staging and AV Works",
            "category": "Stage Engineering",
            "contracted_rate_inr": 100000.0,
            "grace_period_minutes": 30.0,
            "penalty_per_hour_delay_pct": 5.0,
            "max_penalty_pct": 25.0
        }
    }

@pytest.fixture
def sample_invoices():
    return [
        {
            "invoice_id": "INV-2026-001",
            "item_code": "ITEM_LOGISTICS_SHUTTLE",
            "invoiced_amount_inr": 60000.0,
            "scheduled_time": "2026-03-01 08:00:00",
            "actual_delivery_time": "2026-03-01 08:10:00",
            "quality_score_pct": 100.0
        },
        {
            "invoice_id": "INV-2026-002",
            "item_code": "ITEM_FABRICATION_STAGING",
            "invoiced_amount_inr": 100000.0,
            "scheduled_time": "2026-03-01 06:00:00",
            "actual_delivery_time": "2026-03-01 08:30:00",
            "quality_score_pct": 95.0
        },
        {
            "invoice_id": "INV-2026-001",
            "item_code": "ITEM_LOGISTICS_SHUTTLE",
            "invoiced_amount_inr": 60000.0,
            "scheduled_time": "2026-03-01 08:00:00",
            "actual_delivery_time": "2026-03-01 08:10:00",
            "quality_score_pct": 100.0
        }
    ]

def test_rate_card_variance_detection(sample_rate_card):
    engine = OmniVantaAuditEngine(sample_rate_card)
    invoices = [
        {
            "invoice_id": "INV-TEST-RATE",
            "item_code": "ITEM_LOGISTICS_SHUTTLE",
            "invoiced_amount_inr": 65000.0,
            "scheduled_time": "2026-03-01 08:00:00",
            "actual_delivery_time": "2026-03-01 08:00:00",
            "quality_score_pct": 100.0
        }
    ]
    report = engine.audit_batch(invoices)
    assert report["summary"]["total_disallowed_overcharge_inr"] == 15000.0
    assert report["summary"]["total_approved_payable_inr"] == 50000.0

def test_sla_delay_penalty_calculation(sample_rate_card):
    engine = OmniVantaAuditEngine(sample_rate_card)
    invoices = [
        {
            "invoice_id": "INV-TEST-DELAY",
            "item_code": "ITEM_FABRICATION_STAGING",
            "invoiced_amount_inr": 100000.0,
            "scheduled_time": "2026-03-01 06:00:00",
            "actual_delivery_time": "2026-03-01 08:30:00",
            "quality_score_pct": 100.0
        }
    ]
    report = engine.audit_batch(invoices)
    assert report["summary"]["total_sla_penalties_recovered_inr"] == 10000.0
    assert report["summary"]["total_approved_payable_inr"] == 90000.0

def test_duplicate_invoice_detection(sample_rate_card, sample_invoices):
    engine = OmniVantaAuditEngine(sample_rate_card)
    report = engine.audit_batch(sample_invoices)
    duplicates = [r for r in report["records"] if r["is_duplicate"]]
    assert len(duplicates) == 1
    assert duplicates[0]["invoice_id"] == "INV-2026-001"

def test_contingency_fee_calculation(sample_rate_card):
    config = AuditConfig(contingency_fee_pct=20.0)
    engine = OmniVantaAuditEngine(sample_rate_card, config=config)
    invoices = [
        {
            "invoice_id": "INV-FEE-TEST",
            "item_code": "ITEM_LOGISTICS_SHUTTLE",
            "invoiced_amount_inr": 70000.0,
            "scheduled_time": "2026-03-01 08:00:00",
            "actual_delivery_time": "2026-03-01 08:00:00",
            "quality_score_pct": 100.0
        }
    ]
    report = engine.audit_batch(invoices)
    assert report["summary"]["total_margin_savings_inr"] == 20000.0
    assert report["contingency_fee_inr"] == 4000.0

def test_cryptographic_audit_hash(sample_rate_card, sample_invoices):
    engine = OmniVantaAuditEngine(sample_rate_card)
    report = engine.audit_batch(sample_invoices)
    assert "audit_hash_sha256" in report
    assert len(report["audit_hash_sha256"]) == 64
