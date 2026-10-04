"""
Unit and integration tests for OMEGA Phase 8:
- Inbound Recruiter Event Webhook Ingestion (Port 8092)
- Recruiter SQLite Event Persistence (data/outreach_tracker.db)
- Offer Counter-Negotiation Engine & Bangalore GCC CTC Benchmark (scripts/offer_negotiator.py)
"""

import json
import sqlite3
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

from omega.orchestration.plane_agent_reactor import PlaneAgentReactor
from scripts.offer_negotiator import OfferNegotiator, BANGALORE_GCC_BENCHMARKS


def test_recruiter_touchpoint_ingestion_and_db_persistence():
    """Verify recruiter events are properly processed and saved to database."""
    reactor = PlaneAgentReactor(dry_run=True)
    payload = {
        "event_id": "TEST-REC-001",
        "company": "Amazon India",
        "recruiter_name": "Sreeja Govindankutty",
        "email": "sreeja.govindankutty@amazon.com",
        "role": "Operations & Vendor Management Specialist",
        "stage": "HIRING_MANAGER_INVITE",
        "message": "Reviewed operational profile and Aero India 2025 logistics coordinator background.",
        "ctc_lpa": 10.0
    }

    res = reactor.handle_recruiter_touchpoint(payload)
    assert res["action"] == "recruiter_touchpoint_ingested"
    assert res["company"] == "Amazon India"
    assert res["status"] == "INGESTED_ACTIVE"

    # Verify retrieval
    events = reactor.get_recent_recruiter_events(limit=10)
    assert len(events) >= 1
    found = any(e["event_id"] == "TEST-REC-001" for e in events)
    assert found, "Expected TEST-REC-001 in retrieved recruiter events"


def test_offer_negotiator_evaluation_metrics():
    """Verify offer calculation percentiles and suggested counter-offer logic."""
    negotiator = OfferNegotiator()

    # Case 1: Below Market (< 6.5)
    below = negotiator.evaluate_offer(5.5)
    assert below["standing"] == "BELOW_MARKET"
    assert below["suggested_counter_ctc_lpa"] == BANGALORE_GCC_BENCHMARKS["P50_MEDIAN"]

    # Case 2: Market Entry (6.5 to 8.5)
    entry = negotiator.evaluate_offer(7.5)
    assert entry["standing"] == "MARKET_ENTRY"
    assert entry["suggested_counter_ctc_lpa"] == 9.0  # 7.5 * 1.20 = 9.0
    assert entry["percentage_bump"] == 20.0
    assert entry["net_gain_inr"] == 150_000

    # Case 3: Competitive Median (8.5 to 10.5)
    median = negotiator.evaluate_offer(9.5)
    assert median["standing"] == "COMPETITIVE_MEDIAN"
    assert median["suggested_counter_ctc_lpa"] <= BANGALORE_GCC_BENCHMARKS["P75_PREMIUM"]


def test_offer_counter_letter_generation_ground_truth():
    """Verify formal counter-offer letters anchor only in verified credentials."""
    negotiator = OfferNegotiator()
    letter = negotiator.generate_counter_letter(
        company="Deloitte USI",
        role="Risk & Business Operations Advisory Associate",
        offered_ctc=8.0,
        hiring_manager="Sneha Patel"
    )

    assert "Aditya Mehra" in letter
    assert "Deloitte USI" in letter
    assert "99.2% QA Precision" in letter
    assert "AERO India 2025" in letter
    assert "Dayananda Sagar University" in letter
    assert "₹9.60L CTC" in letter
    assert "Warm regards" in letter
