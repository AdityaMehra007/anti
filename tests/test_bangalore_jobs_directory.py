"""
Unit test suite verifying integrity and structure of the
Bangalore Current Month Job Requisitions Engine and Directory.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_FILE = BASE_DIR / "data" / "BANGALORE_CURRENT_MONTH_JOBS.json"
HTML_FILE = BASE_DIR / "apps" / "job_application_studio" / "bangalore_current_month_jobs.html"


def test_bangalore_jobs_json_dataset():
    """Verify JSON file exists and contains all 3,144 Bangalore openings."""
    assert JSON_FILE.exists(), f"Bangalore Jobs JSON missing: {JSON_FILE}"
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 3144, f"Expected 3,144 Bangalore jobs, got {len(data)}"
    
    first = data[0]
    required_keys = ["requisition_id", "title", "company", "location", "hr_contact", "hr_email", "gmail_compose_url", "fit_score"]
    for k in required_keys:
        assert k in first, f"Missing key {k} in Bangalore job record"
        assert first[k] is not None, f"Key {k} is None"


def test_bangalore_jobs_html_dashboard():
    """Verify HTML directory exists and contains proper headers and action triggers."""
    assert HTML_FILE.exists(), f"Bangalore Jobs HTML missing: {HTML_FILE}"
    content = HTML_FILE.read_text(encoding="utf-8")
    assert "3,144 BANGALORE JOBS LIVE" in content
    assert "Aditya Mehra" in content
    assert "1-Click Gmail Apply" in content
    assert len(content) > 20000, "HTML directory file is too small"
