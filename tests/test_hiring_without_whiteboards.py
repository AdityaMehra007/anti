#!/usr/bin/env python3
"""
tests/test_hiring_without_whiteboards.py
Unit tests verifying the integrity of the Hiring Without Whiteboards
Autonomous Ecosystem and Data Pipeline.
"""

import sys
import json
import sqlite3
import csv
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import hiring_without_whiteboards_engine as hwwe

def test_json_integrity():
    json_path = ROOT_DIR / "data" / "hiring_without_whiteboards.json"
    assert json_path.exists(), "JSON export file missing"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 761, f"Expected 761 companies, found {len(data)}"
    
    # Check sample company
    airtable = next((c for c in data if c["name"] == "Airtable"), None)
    assert airtable is not None, "Airtable not found in dataset"
    assert airtable["has_take_home"] is True
    assert airtable["is_remote"] is True

def test_csv_integrity():
    csv_path = ROOT_DIR / "data" / "hiring_without_whiteboards.csv"
    assert csv_path.exists(), "CSV export file missing"
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 761, f"Expected 761 rows in CSV, found {len(reader)}"

def test_sqlite_fts():
    db_path = ROOT_DIR / "data" / "hiring_without_whiteboards.sqlite"
    assert db_path.exists(), "SQLite database missing"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT count(*) FROM companies")
    count = cursor.fetchone()[0]
    assert count == 761, f"Expected 761 rows in companies table, found {count}"

    cursor.execute("SELECT count(*) FROM companies_fts")
    fts_count = cursor.fetchone()[0]
    assert fts_count == 761, f"Expected 761 rows in companies_fts table, found {fts_count}"

    # Search query verification
    res = hwwe.search_companies("Automattic", limit=5)
    assert len(res) >= 1
    assert any(r["name"] == "Automattic" for r in res)
    assert res[0]["has_paid_trial"] == 1
    conn.close()

def test_cockpit_html():
    cockpit_path = ROOT_DIR / "hiring_without_whiteboards_cockpit.html"
    assert cockpit_path.exists(), "Cockpit HTML file missing"
    content = cockpit_path.read_text(encoding="utf-8")
    assert "HIRING WITHOUT WHITEBOARDS" in content
    assert "761" in content
    assert "Automattic" in content
    assert "Airtable" in content

if __name__ == "__main__":
    print("[*] Running Hiring Without Whiteboards test suite...")
    test_json_integrity()
    print("  [✓] JSON catalog verification passed.")
    test_csv_integrity()
    print("  [✓] CSV spreadsheet verification passed.")
    test_sqlite_fts()
    print("  [✓] SQLite & FTS5 full-text search verification passed.")
    test_cockpit_html()
    print("  [✓] Interactive Cockpit HTML verification passed.")
    print("[✓] ALL 4 TEST SUITES PASSED (100% GREEN)")
