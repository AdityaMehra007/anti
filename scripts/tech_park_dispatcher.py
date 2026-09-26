#!/usr/bin/env python3
"""
tech_park_dispatcher.py

Command-Line Interface and Dispatcher for Bangalore Tech Parks & Campus Directory.
Quick querying, metro filtering, company search, and browser studio launcher.
"""

import sys
import json
import webbrowser
import argparse
import os
from pathlib import Path

# Safe Unicode output for Windows Console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
TECH_PARKS_JSON = DATA_DIR / "bangalore_tech_parks_master.json"
TECH_PARKS_CSV = ROOT_DIR / "BANGALORE_TECH_PARKS_AND_COMPANIES_DIRECTORY.csv"
STUDIO_HTML = ROOT_DIR / "apps" / "job_application_studio" / "bangalore_tech_parks_studio.html"

def load_data():
    if not TECH_PARKS_JSON.exists():
        print(f"[!] Error: {TECH_PARKS_JSON} not found. Run scripts/compile_bangalore_tech_parks_and_agent_catalog.py first.")
        sys.exit(1)
    with open(TECH_PARKS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def list_parks(data):
    print("\n" + "=" * 90)
    print(f"BANGALORE TECH PARKS & COMMERCIAL CAMPUS MASTER DIRECTORY ({len(data)} TECH PARKS)")
    print("=" * 90)
    print(f"{'ID':<6} | {'Tech Park Name':<35} | {'Zone / Corridor':<25} | {'Metro Distance':<18}")
    print("-" * 90)
    for p in data:
        metro_short = p['nearest_metro'].split('(')[0].strip()
        print(f"{p['id']:<6} | {p['name'][:35]:<35} | {p['zone'][:25]:<25} | {metro_short[:18]:<18}")
    print("=" * 90 + "\n")

def view_park(data, query):
    query_lower = query.lower()
    matches = [p for p in data if query_lower in p["name"].lower() or query_lower in p["id"].lower() or query_lower in p["corridor"].lower()]
    if not matches:
        print(f"[!] No tech park found matching '{query}'")
        return
    for p in matches:
        print("\n" + "=" * 80)
        print(f"[{p['id']}] {p['name']} ({p['zone']})")
        print("=" * 80)
        print(f"Address:      {p['address']}")
        print(f"Nearest Metro: {p['nearest_metro']}")
        print(f"Transit Score: {p['transit_friction_index']}/100 Friction")
        print(f"Campus Size:   {p['campus_area_sqft']}")
        print(f"Amenities:     {', '.join(p['campus_amenities'])}")
        print("\nCompanies Housed:")
        for c in p["companies"]:
            sal = c['salary_lpa'].replace('\u20b9', 'Rs. ')
            print(f"  * {c['company_name']} ({c['building_block']})")
            print(f"    Role:    {c['target_role']} ({sal})")
            print(f"    HR Lead: {c['hr_name']} | Email: {c['hr_email']} | Phone: {c['desk_phone']}")
            print(f"    Portal:  {c['direct_careers_url']}")
        print("-" * 80)

def search_company(data, query):
    query_lower = query.lower()
    print(f"\n[*] Searching for companies matching: '{query}' across all Tech Parks...")
    found = 0
    for p in data:
        for c in p["companies"]:
            if query_lower in c["company_name"].lower() or query_lower in c["sector"].lower() or query_lower in c["target_role"].lower():
                found += 1
                sal = c['salary_lpa'].replace('\u20b9', 'Rs. ')
                print(f"\n[{found}] {c['company_name']} @ {p['name']}")
                print(f"    Location: {c['building_block']}, {p['corridor']}")
                print(f"    Metro:    {p['nearest_metro']}")
                print(f"    Role:     {c['target_role']} ({sal})")
                print(f"    Contact:  {c['hr_name']} <{c['hr_email']}> | Tel: {c['desk_phone']}")
                print(f"    Careers:  {c['direct_careers_url']}")
    if found == 0:
        print("[!] No matching company found.")
    else:
        print(f"\nTotal matches found: {found}\n")

def open_studio():
    url = f"http://localhost:9119/apps/job_application_studio/bangalore_tech_parks_studio.html"
    print(f"[*] Opening Tech Parks Studio in browser: {url}")
    webbrowser.open(url)

def open_csv():
    if TECH_PARKS_CSV.exists():
        print(f"[*] Opening CSV: {TECH_PARKS_CSV}")
        os.startfile(str(TECH_PARKS_CSV))
    else:
        print(f"[!] CSV not found at {TECH_PARKS_CSV}")

def main():
    parser = argparse.ArgumentParser(description="Bangalore Tech Parks Directory CLI")
    parser.add_argument("--list-parks", action="store_true", help="List all 20 Bangalore Tech Parks")
    parser.add_argument("--park", type=str, help="View detailed companies inside a specific Tech Park")
    parser.add_argument("--company", type=str, help="Search company or role across all Tech Parks")
    parser.add_argument("--open-studio", action="store_true", help="Open web studio in browser")
    parser.add_argument("--open-csv", action="store_true", help="Open master CSV in Excel")

    args = parser.parse_args()
    data = load_data()

    if args.list_parks:
        list_parks(data)
    elif args.park:
        view_park(data, args.park)
    elif args.company:
        search_company(data, args.company)
    elif args.open_studio:
        open_studio()
    elif args.open_csv:
        open_csv()
    else:
        list_parks(data)
        print("Usage examples:")
        print("  python scripts/tech_park_dispatcher.py --park Manyata")
        print("  python scripts/tech_park_dispatcher.py --company Cisco")
        print("  python scripts/tech_park_dispatcher.py --open-studio")

if __name__ == "__main__":
    main()
