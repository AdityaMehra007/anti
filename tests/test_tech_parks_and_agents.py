"""
test_tech_parks_and_agents.py

Automated Test Suite for:
1. Bangalore 20 Premier Tech Parks Directory & Campus Companies
2. Master AI Workforce & Capabilities Inventory (3,368 Agents, 3,670 Skills, 94 Workflows, 10 Engines)
3. Zero CGPA leakage and 100% Non-Sales operations verification
"""

import json
import csv
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
TECH_PARKS_JSON = DATA_DIR / "bangalore_tech_parks_master.json"
TECH_PARKS_CSV = ROOT_DIR / "BANGALORE_TECH_PARKS_AND_COMPANIES_DIRECTORY.csv"
INVENTORY_JSON = DATA_DIR / "all_agents_and_skills_inventory.json"
CATALOG_CSV = ROOT_DIR / "AGENTS_AND_SKILLS_MASTER_CATALOG.csv"
TECH_PARKS_HTML = ROOT_DIR / "apps" / "job_application_studio" / "bangalore_tech_parks_studio.html"
AGENTS_HTML = ROOT_DIR / "apps" / "job_application_studio" / "agents_and_skills_explorer.html"

def test_tech_parks_dataset_structure():
    assert TECH_PARKS_JSON.exists(), f"Missing {TECH_PARKS_JSON}"
    with open(TECH_PARKS_JSON, "r", encoding="utf-8") as f:
        parks = json.load(f)

    assert len(parks) == 20, f"Expected 20 Tech Parks, found {len(parks)}"

    total_companies = 0
    for park in parks:
        assert "id" in park
        assert "name" in park
        assert "zone" in park
        assert "corridor" in park
        assert "address" in park
        assert "nearest_metro" in park
        assert "transit_friction_index" in park
        assert isinstance(park["transit_friction_index"], int)
        assert "companies" in park
        assert len(park["companies"]) >= 2

        for comp in park["companies"]:
            total_companies += 1
            assert "company_name" in comp
            assert "target_role" in comp
            assert "hr_email" in comp
            assert "@" in comp["hr_email"]
            assert "desk_phone" in comp
            assert "+91-80" in comp["desk_phone"]
            assert "pre_drafted_pitch" in comp

            pitch = comp["pre_drafted_pitch"]
            # Guardrails
            assert "cgpa" not in pitch.lower()
            assert "gpa" not in pitch.lower()
            assert "+91 70034 56624" in pitch
            assert "adityamehra799@gmail.com" in pitch
            assert "Aditya Mehra" in pitch

            # Non-sales
            role_lower = comp["target_role"].lower()
            assert "telecaller" not in role_lower
            assert "cold call" not in role_lower
            assert "b2c sales" not in role_lower

    assert total_companies >= 70, f"Expected >= 70 companies in tech parks, found {total_companies}"

def test_tech_parks_csv():
    assert TECH_PARKS_CSV.exists(), f"Missing {TECH_PARKS_CSV}"
    with open(TECH_PARKS_CSV, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert len(rows) >= 71, f"Expected >= 71 rows (header + 70 companies), got {len(rows)}"
    header = rows[0]
    assert "tech_park_name" in header
    assert "company_name" in header
    assert "nearest_metro" in header
    assert "hr_email" in header

def test_agents_and_skills_inventory():
    assert INVENTORY_JSON.exists(), f"Missing {INVENTORY_JSON}"
    with open(INVENTORY_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = data.get("summary", {})
    assert summary.get("total_agents", 0) >= 3000, f"Expected >= 3000 agents, got {summary.get('total_agents')}"
    assert summary.get("total_skills", 0) >= 3500, f"Expected >= 3500 skills, got {summary.get('total_skills')}"
    assert summary.get("total_workflows", 0) >= 90, f"Expected >= 90 workflows, got {summary.get('total_workflows')}"
    assert summary.get("total_career_engines", 0) >= 10, f"Expected >= 10 engines, got {summary.get('total_career_engines')}"
    assert summary.get("grand_total", 0) >= 7000, f"Expected >= 7000 assets, got {summary.get('grand_total')}"

def test_agents_and_skills_catalog_csv():
    assert CATALOG_CSV.exists(), f"Missing {CATALOG_CSV}"
    with open(CATALOG_CSV, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert len(rows) >= 7000, f"Expected >= 7000 rows in catalog CSV, got {len(rows)}"

def test_html_studios_exist_and_valid():
    assert TECH_PARKS_HTML.exists(), f"Missing {TECH_PARKS_HTML}"
    content_tp = TECH_PARKS_HTML.read_text(encoding="utf-8")
    assert len(content_tp) > 50000
    assert "Manyata Embassy Business Park" in content_tp
    assert "RMZ Ecoworld" in content_tp
    assert "Namma Metro" in content_tp
    assert "Aditya Mehra" in content_tp

    assert AGENTS_HTML.exists(), f"Missing {AGENTS_HTML}"
    content_ag = AGENTS_HTML.read_text(encoding="utf-8")
    assert len(content_ag) > 100000
    assert "Master AI Workforce" in content_ag
    assert "7,142" in content_ag
    assert "EXIM" in content_ag
