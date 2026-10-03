"""
Unit test suite verifying integrity and execution of the
Universal Autonomous Job Application Engine and Download Bundle.
"""

import sqlite3
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRACKER_DB = BASE_DIR / "data" / "outreach_tracker.db"
BUNDLE_ZIP = BASE_DIR / "applications_generated" / "ADITYA_MEHRA_GLOBAL_APPLICATIONS_BUNDLE.zip"
LAUNCHER_HTML = BASE_DIR / "apps" / "job_application_studio" / "auto_apply_launcher.html"
PACKETS_DIR = BASE_DIR / "applications_generated" / "auto_applied_packets"
DISPATCH_DIR = BASE_DIR / "reports" / "dispatch_queue"


def test_auto_applied_database_records():
    """Verify automated_applications table exists and has staged records."""
    assert TRACKER_DB.exists(), f"Tracker DB missing: {TRACKER_DB}"
    conn = sqlite3.connect(str(TRACKER_DB))
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM automated_applications")
    count = cur.fetchone()[0]
    assert count >= 10, f"Expected at least 10 automated applications, got {count}"
    
    cur.execute("SELECT application_id, proof_hash, gmail_url, eml_path FROM automated_applications LIMIT 5")
    rows = cur.fetchall()
    for row in rows:
        app_id, proof_hash, gmail_url, eml_path = row
        assert app_id.startswith("APP-"), f"Invalid app ID: {app_id}"
        assert proof_hash.startswith("sha256:"), f"Invalid proof hash: {proof_hash}"
        assert "mail.google.com" in gmail_url, f"Invalid Gmail URL: {gmail_url}"
        assert Path(eml_path).exists(), f"EML file does not exist: {eml_path}"
    
    conn.close()


def test_download_bundle_zip_integrity():
    """Verify application export ZIP bundle exists and is valid."""
    assert BUNDLE_ZIP.exists(), f"Bundle ZIP missing: {BUNDLE_ZIP}"
    assert BUNDLE_ZIP.stat().st_size > 50000, "Bundle ZIP unexpectedly small"
    
    with zipfile.ZipFile(BUNDLE_ZIP, "r") as zf:
        names = zf.namelist()
        assert any(n.startswith("applications/") for n in names), "Missing applications/ in ZIP"
        assert any(n.startswith("eml_dispatch_queue/") for n in names), "Missing eml_dispatch_queue/ in ZIP"


def test_auto_apply_launcher_html_rendered():
    """Verify 1-click Web Gmail launcher portal HTML."""
    assert LAUNCHER_HTML.exists(), f"Launcher HTML missing: {LAUNCHER_HTML}"
    content = LAUNCHER_HTML.read_text(encoding="utf-8")
    assert "OMEGA 1-Click Automated Job Application Launcher" in content
    assert "Aditya Mehra" in content
    assert "1-Click Gmail Apply" in content
    assert len(content) > 5000, "Launcher HTML too small"
