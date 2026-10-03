"""
Unit test for Target 300 Dispatch Cycle Runner
"""
import os
import sys
import sqlite3
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.run_target_300_dispatch_cycle import run_dispatch_cycle, init_tables

def test_dispatch_cycle_dry_run():
    """Verify that dry-run mode simulates advancement without changing state."""
    db_path = os.path.join(ROOT_DIR, "data", "outreach_tracker.db")
    assert os.path.exists(db_path), "outreach_tracker.db must exist"

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM strike_300_dossiers WHERE status = 'STAGED_READY_FOR_DISPATCH'")
    before_count = cur.fetchone()[0]
    conn.close()

    result = run_dispatch_cycle(batch_size=5, dry_run=True)
    assert result["status"] == "success"
    assert result["dry_run"] is True
    assert result["processed"] <= 5

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM strike_300_dossiers WHERE status = 'STAGED_READY_FOR_DISPATCH'")
    after_count = cur.fetchone()[0]
    conn.close()

    assert before_count == after_count, "Dry run must not mutate database"

def test_dispatch_cycle_execution():
    """Verify that dispatch cycle advances targets with cryptographic SHA-256 hashes."""
    result = run_dispatch_cycle(batch_size=2, dry_run=False)
    assert result["status"] == "success"
    assert result["processed"] == 2

    for t in result["advanced_targets"]:
        assert t["new_status"] == "TOUCH1_DISPATCHED"
        assert t["proof_hash"].startswith("sha256:")

    db_path = os.path.join(ROOT_DIR, "data", "outreach_tracker.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM strike_300_events")
    events_count = cur.fetchone()[0]
    conn.close()

    assert events_count >= 2, "Event ledger must record dispatch transitions"
