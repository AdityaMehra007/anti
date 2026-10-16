"""
test_52_week_calendar_and_auto_apply.py
=======================================
Unit & Integration tests verifying the 52-Week Recruitment Calendar
and the Autonomous Auto-Apply Pipeline for Aditya Mehra.
"""

import sqlite3
import json
from pathlib import Path
import pytest

DB_PATH = Path("data/aditya_global_career_intelligence.db")
CALENDAR_PACKAGES_DIR = Path("applications_generated/52_weeks_calendar")

@pytest.fixture
def db_conn():
    conn = sqlite3.connect(DB_PATH)
    yield conn
    conn.close()

def test_hiring_calendar_table_exists(db_conn):
    cur = db_conn.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    assert "hiring_calendar_52_weeks" in tables

def test_all_52_weeks_present(db_conn):
    cur = db_conn.cursor()
    count = cur.execute("SELECT COUNT(*) FROM hiring_calendar_52_weeks").fetchone()[0]
    assert count == 52

    week_nums = [r[0] for r in cur.execute("SELECT week_number FROM hiring_calendar_52_weeks ORDER BY week_number ASC").fetchall()]
    assert week_nums == list(range(1, 53))

def test_quarters_and_months_valid(db_conn):
    cur = db_conn.cursor()
    rows = cur.execute("SELECT DISTINCT quarter, month FROM hiring_calendar_52_weeks").fetchall()
    quarters = {r[0] for r in rows}
    assert quarters == {"Q1", "Q2", "Q3", "Q4"}
    
    months = {r[1] for r in rows}
    expected_months = {
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    }
    assert months == expected_months

def test_verified_seams_comply_with_ground_truth(db_conn):
    valid_seams = {"EXP-001", "EXP-002", "EXP-003", "EXP-004", "EXP-005"}
    cur = db_conn.cursor()
    seams = cur.execute("SELECT DISTINCT verified_seam FROM hiring_calendar_52_weeks").fetchall()
    for s in seams:
        assert s[0] in valid_seams

def test_target_companies_json_structure(db_conn):
    cur = db_conn.cursor()
    rows = cur.execute("SELECT week_number, target_companies FROM hiring_calendar_52_weeks").fetchall()
    for week_num, comp_json in rows:
        companies = json.loads(comp_json)
        assert isinstance(companies, list)
        assert len(companies) >= 1
        for c in companies:
            assert "company" in c
            assert "location" in c
            assert "role" in c
            assert "portal" in c

def test_staged_application_packages_exist():
    assert CALENDAR_PACKAGES_DIR.exists()
    staged_dirs = list(CALENDAR_PACKAGES_DIR.glob("week_*"))
    assert len(staged_dirs) >= 52

    # Check sample week 1 (Boeing)
    sample_dir = next((d for d in staged_dirs if "week_01_boeing" in d.name), None)
    assert sample_dir is not None
    assert (sample_dir / "tailored_ats_resume.md").exists()
    assert (sample_dir / "recruiter_inmail.txt").exists()
    assert (sample_dir / "ats_autofill_payload.json").exists()

    # Verify JSON content
    payload = json.loads((sample_dir / "ats_autofill_payload.json").read_text(encoding="utf-8"))
    assert payload["candidate"]["full_name"] == "Aditya Mehra"
    assert "DSU" in payload["candidate"]["university"] or "Dayananda Sagar" in payload["candidate"]["university"]
    assert payload["application_target"]["company"] == "Boeing India"

def test_applications_and_outreach_registered(db_conn):
    cur = db_conn.cursor()
    cal_apps = cur.execute("SELECT COUNT(*) FROM applications WHERE application_id LIKE 'APP-CAL-%'").fetchone()[0]
    assert cal_apps >= 52

    cal_outreach = cur.execute("SELECT COUNT(*) FROM outreach WHERE outreach_id LIKE 'OUT-CAL-%'").fetchone()[0]
    assert cal_outreach >= 52
