"""
Unit test for HR Outreach Orchestrator & Funnel Tracking (scripts/hr_outreach_orchestrator.py)
"""
import os
import pytest
import sqlite3
from scripts.hr_outreach_orchestrator import HROutreachOrchestrator

def test_hr_outreach_orchestrator_init(tmp_path):
    db_path = str(tmp_path / "test_outreach.db")
    orchestrator = HROutreachOrchestrator(db_path=db_path)
    
    # DB schema initialized
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='outreach_cadence'")
    assert cur.fetchone() is not None
    conn.close()

def test_generate_daily_batch(tmp_path):
    db_path = str(tmp_path / "test_outreach.db")
    orchestrator = HROutreachOrchestrator(db_path=db_path)
    
    # Generate a batch of size 5
    batch = orchestrator.generate_daily_batch(batch_size=5)
    assert len(batch) <= 5
    if len(batch) > 0:
        first = batch[0]
        assert "contact_id" in first
        assert "name" in first
        assert "status" in first
        assert first["status"] == "STAGED"

def test_record_status_transitions(tmp_path):
    db_path = str(tmp_path / "test_outreach.db")
    orchestrator = HROutreachOrchestrator(db_path=db_path)
    batch = orchestrator.generate_daily_batch(batch_size=2)
    if not batch:
        pytest.skip("No contacts to test transitions")
    
    cid = batch[0]["contact_id"]
    orchestrator.update_contact_status(cid, "SENT")
    status = orchestrator.get_contact_status(cid)
    assert status == "SENT"

    stats = orchestrator.get_funnel_stats()
    assert stats["sent"] >= 1
