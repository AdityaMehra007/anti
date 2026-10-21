"""
Bangalore Top 500 Master Quality & Verification Test Suite
Validates database schema, completeness, prompt corpus integrity,
and execution engine functionality across the entire 500 startups ecosystem.
"""

import os
import sys
import json
import csv
import pytest

ROOT_DIR = "E:/anti"
sys.path.insert(0, ROOT_DIR)

DATA_JSON = os.path.join(ROOT_DIR, "data", "BANGALORE_TOP_500_STARTUPS_PROJECTS_PROMPTS_MASTER.json")
DATA_CSV = os.path.join(ROOT_DIR, "data", "BANGALORE_TOP_500_STARTUPS_PROJECTS_PROMPTS_MASTER.csv")
PROMPTS_DIR = os.path.join(ROOT_DIR, "prompts", "bangalore_top_500")
SCAFFOLDS_DIR = os.path.join(ROOT_DIR, "projects", "bangalore_top_500", "scaffolds")
COCKPIT_HTML = os.path.join(ROOT_DIR, "bangalore_top_500_cockpit.html")

def test_master_json_integrity():
    assert os.path.exists(DATA_JSON), "Master JSON must exist"
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 500, f"Expected 500 startups, got {len(data)}"

    ids = set()
    ranks = set()
    names = set()

    for item in data:
        assert item["id"].startswith("BLR-STARTUP-"), f"Invalid ID format {item['id']}"
        ids.add(item["id"])
        ranks.add(item["rank"])
        names.add(item["company_name"])

        # Check project fields
        proj = item["biggest_project"]
        assert len(proj["project_name"]) > 5, "Project name must be descriptive"
        assert len(proj["architecture_pillar"]) > 3, "Pillar must be defined"
        assert len(proj["tech_stack"]) > 3, "Tech stack must be specified"
        assert len(proj["impact_metrics"]) > 5, "KPIs must be specified"

        # Check prompt depth
        prompt = item["biggest_prompt"]
        assert len(prompt) >= 1500, f"Prompt for {item['company_name']} is too brief ({len(prompt)} chars)"
        assert "## 1. " in prompt or "# ROLE:" in prompt, "Prompt must contain standard structural sections"

    assert len(ids) == 500, "IDs must be uniquely assigned"
    assert len(ranks) == 500, "Ranks must be 1 to 500 unique"
    assert len(names) == 500, "Company names must be completely unique"

def test_master_csv_integrity():
    assert os.path.exists(DATA_CSV), "Master CSV must exist"
    with open(DATA_CSV, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    # 1 header row + 500 data rows = 501 rows
    assert len(reader) == 501, f"Expected 501 CSV rows, got {len(reader)}"
    header = reader[0]
    assert "Company Name" in header
    assert "Project Name" in header
    assert "Tech Stack" in header

def test_markdown_prompts_directory():
    assert os.path.exists(PROMPTS_DIR), "Prompts directory must exist"
    files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith(".md")]
    assert len(files) == 500, f"Expected 500 markdown files, found {len(files)}"

def test_scaffolds_directory():
    assert os.path.exists(SCAFFOLDS_DIR), "Scaffolds directory must exist"
    index_file = os.path.join(SCAFFOLDS_DIR, "SCAFFOLD_INDEX.json")
    assert os.path.exists(index_file), "Scaffold index must exist"
    with open(index_file, "r", encoding="utf-8") as f:
        idx = json.load(f)
    assert len(idx) == 500, f"Expected 500 indexed scaffolds, found {len(idx)}"

def test_cockpit_html_exists_and_valid():
    assert os.path.exists(COCKPIT_HTML), "Cockpit HTML must exist"
    size_mb = os.path.getsize(COCKPIT_HTML) / 1024 / 1024
    assert size_mb >= 1.5, f"Cockpit HTML should be >= 1.5MB (currently {size_mb:.2f}MB)"

def test_cli_engine_search_and_stats():
    from bangalore_startup_engine import search_startups, load_database
    db = load_database()
    assert len(db) == 500

    # Search by decacorn name
    res = search_startups("Zerodha")
    assert len(res) == 1
    assert res[0]["company_name"] == "Zerodha"
    assert "NanoTrader" in res[0]["biggest_project"]["project_name"]

    # Filter by FinTech sector
    fintechs = search_startups("", sector="FinTech")
    assert len(fintechs) >= 50

def test_deal_crm_500_dataset():
    crm_path = os.path.join(ROOT_DIR, "data", "bangalore_enterprise_crm_master_500.json")
    assert os.path.exists(crm_path), "500-CRM JSON must exist"
    with open(crm_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) >= 500, f"Expected at least 500 accounts, got {len(data)}"
    for acc in data:
        assert "company_name" in acc
        assert "contract_value_inr" in acc
        assert acc["entry_pilot_po_inr"] < 500000, "Pilot PO must be sub-threshold (< 5L)"

def test_flagship_sows_generated():
    sow_dir = os.path.join(ROOT_DIR, "docs", "contracts_and_sows")
    assert os.path.exists(sow_dir), "Contracts and SOWs directory must exist"
    files = [f for f in os.listdir(sow_dir) if f.startswith("SOW_") and f.endswith(".md")]
    assert len(files) >= 15, f"Expected at least 15 SOWs, got {len(files)}"

def test_supreme_command_center_html():
    supreme_html = os.path.join(ROOT_DIR, "omega_supreme_command_center.html")
    assert os.path.exists(supreme_html), "Supreme Command Center HTML must exist"
    assert os.path.getsize(supreme_html) > 10000, "HTML must be fully populated"

