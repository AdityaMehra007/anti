"""
OMEGA ∞ Unit & Integration Test Suite: Autonomous Commercial Outbound Engine
=============================================================================
Validates:
- Ledger ingestion of all 546 accounts (₹4.37B ARR pipeline)
- Cryptographic SHA-256 dispatch receipt signing
- SOW & pitch deck verification gates
- Idempotent duplicate-dispatch prevention
- Multi-touch progression (InMail -> Cold Email -> Executive Followup)
- Token bucket rate limiter enforcement
- Real-time pipeline funnel metrics calculations
"""

import os
import sys
import tempfile
import json
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_outbound_execution_engine import (
    CommercialOutboundEngine,
    TokenBucketRateLimiter,
    OutboundDispatchRecord,
    DispatchReceipt
)


def test_outbound_engine_ledger_ingestion():
    engine = CommercialOutboundEngine()
    assert len(engine.records) == 546, f"Expected 546 accounts in ledger, found {len(engine.records)}"

    metrics = engine.compute_funnel_metrics()
    assert metrics.total_accounts == 546
    assert metrics.total_pipeline_arr_inr > 4_000_000_000, f"Expected >4B ARR, got {metrics.total_pipeline_arr_inr}"
    assert metrics.total_pilot_po_inr > 200_000_000, f"Expected >200M pilot POs, got {metrics.total_pilot_po_inr}"


def test_sow_asset_verification():
    engine = CommercialOutboundEngine()
    # Walmart Global Tech India has a verified SOW staged in docs/contracts_and_sows/
    walmart_rec = next((r for r in engine.records.values() if "walmart" in r.company_name.lower()), None)
    assert walmart_rec is not None
    assert engine.verify_sow_asset(walmart_rec) is True


def test_dispatch_touch1_receipt_cryptography():
    engine = CommercialOutboundEngine()
    first_rec = list(engine.records.values())[0]

    receipt = engine.dispatch_touch(first_rec, touch_number=1, dry_run=True)
    assert receipt.status == "MOCKED"
    assert receipt.channel == "INMAIL"
    assert receipt.dispatch_id == first_rec.dispatch_id
    assert receipt.account_id == first_rec.account_id
    assert len(receipt.verification_hash) == 64
    assert receipt.message_length > 50
    assert receipt.receipt_id.startswith("RCPT-")


def test_idempotency_prevents_duplicate_dispatch():
    # Use isolated temporary files
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as f_ledger:
        dummy_data = [{
            "dispatch_id": "DISP-TEST-001",
            "account_id": "BLR-TEST-001",
            "company_name": "TestCorp India",
            "priority_tier": "Tier 1 (Immediate Strike)",
            "target_contact": "VP Engineering",
            "warm_referral_path": "Direct",
            "pilot_po_inr": 485000,
            "contract_value_inr": 8500000,
            "procurement_bypass": "Sub-Threshold PO (< INR 5L)",
            "sow_document": "docs/contracts_and_sows/SOW_Walmart_Global_Tech_India.md",
            "touch_1_inmail": "Hello VP Engineering...",
            "touch_2_email": "Subject: Followup...",
            "dispatch_status": "STAGED_READY",
            "touch_stage": 0,
            "attempts_count": 0
        }]
        json.dump(dummy_data, f_ledger)
        f_ledger_path = f_ledger.name

    with tempfile.NamedTemporaryFile("w+", suffix=".jsonl", delete=False) as f_audit:
        f_audit_path = f_audit.name

    try:
        engine = CommercialOutboundEngine(ledger_path=f_ledger_path, audit_path=f_audit_path)
        rec = engine.records["DISP-TEST-001"]

        # First dispatch (real execution)
        rcpt1 = engine.dispatch_touch(rec, touch_number=1, dry_run=False)
        assert rcpt1.status == "DELIVERED"
        assert rec.dispatch_status == "DISPATCHED_TOUCH1"
        assert rec.touch_stage == 1
        assert rec.attempts_count == 1

        # Second dispatch of same touch (must be blocked by idempotency guard)
        rcpt2 = engine.dispatch_touch(rec, touch_number=1, dry_run=False)
        assert rcpt2.status == "ALREADY_DISPATCHED"
        assert rec.attempts_count == 1  # Unchanged!

    finally:
        if os.path.exists(f_ledger_path):
            os.remove(f_ledger_path)
        if os.path.exists(f_audit_path):
            os.remove(f_audit_path)


def test_multi_touch_progression():
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as f_ledger:
        dummy_data = [{
            "dispatch_id": "DISP-TEST-002",
            "account_id": "BLR-TEST-002",
            "company_name": "ScaleUp Tech",
            "priority_tier": "Tier 1 (Immediate Strike)",
            "target_contact": "CTO",
            "warm_referral_path": "Direct",
            "pilot_po_inr": 450000,
            "contract_value_inr": 6000000,
            "procurement_bypass": "Sub-Threshold PO (< INR 5L)",
            "sow_document": "",
            "touch_1_inmail": "InMail Pitch...",
            "touch_2_email": "Subject: Full SOW proposal...",
            "dispatch_status": "STAGED_READY",
            "touch_stage": 0,
            "attempts_count": 0
        }]
        json.dump(dummy_data, f_ledger)
        f_ledger_path = f_ledger.name

    with tempfile.NamedTemporaryFile("w+", suffix=".jsonl", delete=False) as f_audit:
        f_audit_path = f_audit.name

    try:
        engine = CommercialOutboundEngine(ledger_path=f_ledger_path, audit_path=f_audit_path)
        rec = engine.records["DISP-TEST-002"]

        # Touch 1: InMail
        rcpt1 = engine.dispatch_touch(rec, touch_number=1, dry_run=False)
        assert rcpt1.channel == "INMAIL"
        assert rec.dispatch_status == "DISPATCHED_TOUCH1"

        # Touch 2: Cold Email
        rcpt2 = engine.dispatch_touch(rec, touch_number=2, dry_run=False)
        assert rcpt2.channel == "EMAIL"
        assert rec.dispatch_status == "DISPATCHED_TOUCH2"
        assert rec.touch_stage == 2
        assert rec.attempts_count == 2

    finally:
        if os.path.exists(f_ledger_path):
            os.remove(f_ledger_path)
        if os.path.exists(f_audit_path):
            os.remove(f_audit_path)


def test_batch_dispatch_filtering():
    engine = CommercialOutboundEngine()
    # Dry-run batch of 5 Tier 1 accounts
    receipts = engine.dispatch_batch(tier="Tier 1", limit=5, touch_number=1, dry_run=True)
    assert len(receipts) == 5
    for r in receipts:
        assert r.status == "MOCKED"
        rec = engine.records[r.dispatch_id]
        assert "tier 1" in rec.priority_tier.lower()


def test_token_bucket_rate_limiter():
    limiter = TokenBucketRateLimiter(max_tokens=3, refill_time_sec=100.0)
    assert limiter.acquire() is True
    assert limiter.acquire() is True
    assert limiter.acquire() is True
    # 4th immediate token request must fail
    assert limiter.acquire() is False


def test_pipeline_funnel_metrics():
    engine = CommercialOutboundEngine()
    metrics = engine.compute_funnel_metrics()
    assert metrics.total_accounts == 546
    assert metrics.staged_ready + metrics.dispatched_touch1 + metrics.dispatched_touch2 == metrics.total_accounts
    assert metrics.total_pipeline_arr_inr > 0
    assert metrics.total_pilot_po_inr > 0
