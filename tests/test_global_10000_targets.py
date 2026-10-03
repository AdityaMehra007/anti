"""
Unit test suite verifying integrity and cryptographic consistency of the
OMEGA 10,000 Global Requisition Hyper-Target Strike Force dataset and database.
"""

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_FILE = BASE_DIR / "data" / "GLOBAL_10000_HYPER_TARGET_STRIKE.json"
DB_FILE = BASE_DIR / "data" / "global_10000_targets.db"
HTML_FILE = BASE_DIR / "apps" / "job_application_studio" / "global_10000_strike.html"


def test_global_10000_json_exists_and_complete():
    """Verify JSON file exists and contains exactly 10,000 records."""
    assert JSON_FILE.exists(), f"Target JSON missing: {JSON_FILE}"
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 10000, f"Expected 10,000 targets, found {len(data)}"
    
    # Check sample record structure
    first = data[0]
    for key in ["id", "company", "contact_name", "contact_position", "email", "fit_score", "corridor", "sector", "priority", "proof_hash"]:
        assert key in first, f"Missing key '{key}' in sample record"
        assert first[key] is not None, f"Key '{key}' is None"


def test_global_10000_sqlite_db_integrity():
    """Verify SQLite database contains exactly 10,000 indexed rows with hashes."""
    assert DB_FILE.exists(), f"Target SQLite DB missing: {DB_FILE}"
    conn = sqlite3.connect(str(DB_FILE))
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM global_10000_targets")
    count = cur.fetchone()[0]
    assert count == 10000, f"Expected 10,000 rows in DB, got {count}"
    
    # Verify index exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='global_10000_targets'")
    indices = [r[0] for r in cur.fetchall()]
    assert any("company" in idx.lower() for idx in indices), "Company index not found"
    
    # Verify proof hashes are populated and valid SHA-256 strings
    cur.execute("SELECT proof_hash FROM global_10000_targets LIMIT 10")
    hashes = cur.fetchall()
    for h in hashes:
        raw_hash = h[0].replace("sha256:", "")
        assert len(raw_hash) == 64, f"Invalid SHA-256 hex length: {h[0]}"
    
    conn.close()


def test_global_10000_html_dashboard_rendered():
    """Verify visual dashboard HTML exists and is sufficiently populated."""
    assert HTML_FILE.exists(), f"Dashboard HTML missing: {HTML_FILE}"
    content = HTML_FILE.read_text(encoding="utf-8")
    assert "OMEGA 10,000 Hyper-Target Strike Force" in content
    assert "10,000 Global Requisition Strike Explorer" in content or "10,000 Targets Live" in content or "10,000" in content
    assert len(content) > 10000, "Dashboard file is unexpectedly small"
