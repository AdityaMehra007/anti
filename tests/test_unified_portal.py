"""
Unit test for Unified Executive HUD (index.html and unified_portal.js)
"""
import os
import re
import pytest

DASHBOARD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "aios", "dashboards"))
INDEX_HTML = os.path.join(DASHBOARD_DIR, "index.html")
PORTAL_JS = os.path.join(DASHBOARD_DIR, "unified_portal.js")

def test_dashboard_files_exist():
    assert os.path.exists(INDEX_HTML), f"Missing {INDEX_HTML}"
    assert os.path.exists(PORTAL_JS), f"Missing {PORTAL_JS}"

def test_portal_js_has_subsystem_health_checks():
    with open(PORTAL_JS, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Must contain subsystem ports and names
    assert "8090" in content, "Missing AI Gateway port (8090)"
    assert "8000" in content, "Missing TradeNexus port (8000)"
    assert "5678" in content, "Missing n8n port (5678)"
    assert "checkSubsystemHealth" in content or "pollSubsystems" in content
    assert "switchTab" in content or "selectSubsystem" in content

def test_index_html_has_unified_navigation_tabs():
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    assert "unified_portal.js" in content, "index.html must reference unified_portal.js"
    assert "subsystem-nav" in content or "portal-nav" in content
    assert "Plane CE" in content
    assert "TradeNexus" in content
    assert "HR 1781" in content or "Job Strike" in content
    assert "Target 300 Strike" in content
    assert "7,656 Workforce" in content

def test_strike_300_dossiers_and_workforce_inventory():
    """Verify that Target 300 dossiers and master workforce explorer are compiled."""
    import sqlite3
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "outreach_tracker.db"))
    assert os.path.exists(db_path), "Missing outreach_tracker.db"
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM strike_300_dossiers")
    row = cur.fetchone()
    conn.close()
    
    assert row is not None and row[0] == 300, f"Expected 300 dossiers, found {row[0] if row else 0}"

