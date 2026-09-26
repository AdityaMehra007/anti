#!/usr/bin/env python3
"""
agent_skills_inspector.py

Command-Line Inspector & Query Engine for the Complete System AI Workforce.
Enables instant search and domain filtering across all 3,368 Agents, 3,670 Skills,
94 Automation Workflows, and 10 Core Career OS Engines (7,142 Total Assets).
"""

import sys
import json
import webbrowser
import argparse
import os
from pathlib import Path
from collections import Counter

# Safe Unicode output for Windows Console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
INVENTORY_JSON = DATA_DIR / "all_agents_and_skills_inventory.json"
CATALOG_CSV = ROOT_DIR / "AGENTS_AND_SKILLS_MASTER_CATALOG.csv"
EXPLORER_HTML = ROOT_DIR / "apps" / "job_application_studio" / "agents_and_skills_explorer.html"

def load_data():
    if not INVENTORY_JSON.exists():
        print(f"[!] Error: {INVENTORY_JSON} not found. Run scripts/compile_bangalore_tech_parks_and_agent_catalog.py first.")
        sys.exit(1)
    with open(INVENTORY_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def show_summary(data):
    s = data["summary"]
    print("\n" + "=" * 80)
    print("AI WORKFORCE & CAPABILITY INVENTORY SUMMARY")
    print("=" * 80)
    print(f"Total Autonomous Agents:       {s['total_agents']:,}")
    print(f"Total Specialized Skills:      {s['total_skills']:,}")
    print(f"Total Automation Workflows:    {s['total_workflows']:,}")
    print(f"Core Career OS Engines:        {s['total_career_engines']:,}")
    print("-" * 80)
    print(f"GRAND TOTAL CATALOGED ASSETS:  {s['grand_total']:,}")
    print("=" * 80)

    # Domain breakdown for skills
    skill_domains = Counter([item["domain"] for item in data["skills"]])
    print("\nSKILLS BY FUNCTIONAL DOMAIN:")
    for dom, count in skill_domains.most_common(12):
        print(f"  • {dom:<55}: {count} skills")

    # Domain breakdown for agents
    agent_domains = Counter([item["domain"] for item in data["agents"]])
    print("\nAGENTS BY FUNCTIONAL DOMAIN:")
    for dom, count in agent_domains.most_common(12):
        print(f"  • {dom:<55}: {count} agents")

    print("\nCORE CAREER OS EXECUTION ENGINES:")
    for eng in data["career_engines"]:
        print(f"  • {eng['name']:<45} -> {eng['file_name']}")
    print("=" * 80 + "\n")

def search_assets(data, query):
    query_lower = query.lower()
    print(f"\n[*] Searching AI Workforce for keyword: '{query}'...")
    all_items = data["career_engines"] + data["workflows"] + data["agents"] + data["skills"]
    matches = [i for i in all_items if query_lower in i["name"].lower() or query_lower in i["domain"].lower() or query_lower in i["relative_path"].lower()]

    if not matches:
        print(f"[!] No assets found matching '{query}'.")
        return

    print(f"\nFound {len(matches)} matching assets (Displaying up to 30):")
    print(f"{'Category':<22} | {'Name':<35} | {'Domain / Function':<35}")
    print("-" * 96)
    for m in matches[:30]:
        print(f"{m['category'][:22]:<22} | {m['name'][:35]:<35} | {m['domain'][:35]:<35}")
    if len(matches) > 30:
        print(f"... and {len(matches) - 30} more matching assets in catalog.")
    print("-" * 96 + "\n")

def filter_by_category(data, domain_query):
    query_lower = domain_query.lower()
    print(f"\n[*] Filtering assets in domain matching: '{domain_query}'...")
    all_items = data["career_engines"] + data["workflows"] + data["agents"] + data["skills"]
    matches = [i for i in all_items if query_lower in i["domain"].lower()]

    if not matches:
        print(f"[!] No domain matching '{domain_query}'.")
        return

    print(f"\nTotal assets in domain '{domain_query}': {len(matches)}")
    print(f"{'Category':<22} | {'Name':<35} | {'File Path':<35}")
    print("-" * 96)
    for m in matches[:25]:
        print(f"{m['category'][:22]:<22} | {m['name'][:35]:<35} | {m['relative_path'][:35]:<35}")
    if len(matches) > 25:
        print(f"... and {len(matches) - 25} more assets in this domain.")
    print("-" * 96 + "\n")

def open_studio():
    url = "http://localhost:9119/apps/job_application_studio/agents_and_skills_explorer.html"
    print(f"[*] Opening Agents & Skills Explorer in browser: {url}")
    webbrowser.open(url)

def open_csv():
    if CATALOG_CSV.exists():
        print(f"[*] Opening Master Catalog CSV: {CATALOG_CSV}")
        os.startfile(str(CATALOG_CSV))
    else:
        print(f"[!] CSV not found at {CATALOG_CSV}")

def main():
    parser = argparse.ArgumentParser(description="Agents & Skills Inspector CLI")
    parser.add_argument("--summary", action="store_true", help="Display full summary breakdown of workforce")
    parser.add_argument("--search", type=str, help="Search agents, skills, workflows by keyword")
    parser.add_argument("--domain", type=str, help="Filter assets by functional domain (e.g. exim, b2b, finance)")
    parser.add_argument("--open-studio", action="store_true", help="Launch interactive web explorer")
    parser.add_argument("--open-csv", action="store_true", help="Open master catalog CSV in Excel")

    args = parser.parse_args()
    data = load_data()

    if args.summary:
        show_summary(data)
    elif args.search:
        search_assets(data, args.search)
    elif args.domain:
        filter_by_category(data, args.domain)
    elif args.open_studio:
        open_studio()
    elif args.open_csv:
        open_csv()
    else:
        show_summary(data)
        print("Usage examples:")
        print("  python scripts/agent_skills_inspector.py --search 'exim'")
        print("  python scripts/agent_skills_inspector.py --domain 'finance'")
        print("  python scripts/agent_skills_inspector.py --open-studio")

if __name__ == "__main__":
    main()
