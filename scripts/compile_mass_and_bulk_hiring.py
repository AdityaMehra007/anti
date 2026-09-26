#!/usr/bin/env python3
"""
========================================================================================
BANGALORE MASS & BULK HIRING GIANTS & STAFFING AGENCIES COMPILER
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Compiles and exports mass/bulk hiring companies and top staffing placement agencies
with complete employee benefits (cabs, insurance, shift allowance, meal pass, etc.).
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import csv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
MASS_DATA_FILE = ROOT_DIR / "data" / "bangalore_mass_and_bulk_hiring.json"
GLOBAL_DATA_FILE = ROOT_DIR / "data" / "bangalore_funded_startups_and_global_mncs.json"
MASS_CSV_FILE = ROOT_DIR / "BANGALORE_MASS_AND_BULK_HIRING_MASTER.csv"
GLOBAL_CSV_FILE = ROOT_DIR / "BANGALORE_FUNDED_STARTUPS_AND_GLOBAL_MNCS_MASTER.csv"

def load_mass_hiring():
    if not MASS_DATA_FILE.exists():
        return []
    with open(MASS_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def export_mass_csv():
    companies = load_mass_hiring()
    if not companies:
        print("[!] No mass hiring companies found.")
        return 0

    headers = [
        "ID",
        "Company / Agency Name",
        "Category",
        "Hiring Volume & Drive Type",
        "Bangalore Corridor",
        "Target Role (Non-Sales)",
        "Experience Level",
        "Fixed Base (LPA)",
        "Total CTC (LPA)",
        "Monthly In-Hand",
        "Free Doorstep Transport",
        "Medical / Health Insurance",
        "Shift Allowance",
        "Food / Cafeteria Perks",
        "Higher Ed / Certifications",
        "Desk Phone",
        "HR Direct Email",
        "Direct Careers Portal",
        "Walk-In / Registration URL"
    ]

    rows = []
    for c in companies:
        b = c.get("benefits_package", {})
        rows.append([
            c.get("id", ""),
            c.get("company_name", ""),
            c.get("category", ""),
            c.get("hiring_type", ""),
            c.get("bangalore_corridor", ""),
            c.get("target_role", ""),
            c.get("experience_level", ""),
            f"₹{c.get('fixed_base_lpa', 0)}L",
            f"₹{c.get('total_ctc_min', 0)}L - ₹{c.get('total_ctc_max', 0)}L",
            f"₹{c.get('monthly_in_hand_est', 0):,}/mo",
            b.get("transport", ""),
            b.get("medical_insurance", ""),
            b.get("shift_allowance", ""),
            b.get("food_perks", ""),
            b.get("higher_education", ""),
            c.get("desk_phone", ""),
            c.get("hr_email", ""),
            c.get("direct_apply_url", ""),
            c.get("walkin_portal_url", "")
        ])

    with open(MASS_CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"[OK] Exported {len(rows)} mass & bulk hiring giants to {MASS_CSV_FILE}")
    return len(rows)

def merge_into_global_master():
    """Merges mass hiring firms into the primary global directory so all 60 are accessible in one place."""
    mass_firms = load_mass_hiring()
    if not GLOBAL_DATA_FILE.exists():
        return
    
    with open(GLOBAL_DATA_FILE, "r", encoding="utf-8") as f:
        global_firms = json.load(f)

    existing_ids = {c.get("id") for c in global_firms}
    added = 0
    for mf in mass_firms:
        if mf.get("id") not in existing_ids:
            # Add formatted entry matching global schema
            entry = {
                "id": mf.get("id"),
                "company_name": mf.get("company_name"),
                "category": mf.get("category"),
                "origin_country": mf.get("origin_country"),
                "funding_status": f"Mass Hiring ({mf.get('hiring_type', '')})",
                "bangalore_corridor": mf.get("bangalore_corridor"),
                "desk_phone": mf.get("desk_phone"),
                "hr_lead": mf.get("hr_lead"),
                "hr_email": mf.get("hr_email"),
                "target_role": mf.get("target_role"),
                "experience_level": mf.get("experience_level"),
                "fixed_base_lpa": mf.get("fixed_base_lpa"),
                "total_ctc_min": mf.get("total_ctc_min"),
                "total_ctc_max": mf.get("total_ctc_max"),
                "avg_ctc_lpa": mf.get("avg_ctc_lpa"),
                "monthly_in_hand_est": mf.get("monthly_in_hand_est"),
                "direct_apply_url": mf.get("direct_apply_url"),
                "workday_lever_greenhouse": mf.get("walkin_portal_url"),
                "strategic_fit_rationale": f"Benefits: {mf.get('benefits_package', {}).get('transport', '')} | {mf.get('benefits_package', {}).get('medical_insurance', '')} | Shift: {mf.get('benefits_package', {}).get('shift_allowance', '')}",
                "sales_risk": False,
                "benefits_package": mf.get("benefits_package", {})
            }
            global_firms.append(entry)
            added += 1

    with open(GLOBAL_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(global_firms, f, indent=2)

    print(f"[OK] Merged {added} mass hiring firms into master JSON. Total now: {len(global_firms)}")
    return len(global_firms)

def sync_to_dashboard_data():
    """Syncs merged data into apps/get_me_hired_dashboard/data.json"""
    dashboard_data_path = ROOT_DIR / "apps" / "get_me_hired_dashboard" / "data.json"
    if not dashboard_data_path.exists():
        return
    with open(dashboard_data_path, "r", encoding="utf-8") as f:
        dash_data = json.load(f)

    with open(GLOBAL_DATA_FILE, "r", encoding="utf-8") as f:
        global_firms = json.load(f)

    with open(MASS_DATA_FILE, "r", encoding="utf-8") as f:
        mass_firms = json.load(f)

    dash_data["funded_startups_and_global_mncs"] = global_firms
    dash_data["mass_and_bulk_hiring"] = mass_firms

    with open(dashboard_data_path, "w", encoding="utf-8") as f:
        json.dump(dash_data, f, indent=2)

    print(f"[OK] Synced {len(global_firms)} enterprises and {len(mass_firms)} mass hiring firms to {dashboard_data_path}")

def main():
    export_mass_csv()
    total = merge_into_global_master()
    
    # Re-export master CSV
    sys.path.insert(0, str(ROOT_DIR))
    from scripts.compile_funded_startups_and_global_mncs import export_csv
    export_csv()

    # Sync to dashboard data.json
    sync_to_dashboard_data()

    # Re-generate HTML studio
    import subprocess
    subprocess.run([sys.executable, str(ROOT_DIR / "scripts" / "generate_global_hub_html.py")], check=True)

    # Refresh dashboard embedded data
    subprocess.run([sys.executable, str(ROOT_DIR / "scripts" / "embed_dashboard_data.py")], check=True)
    print(f"[OK] All systems synchronized with {total} companies!")

if __name__ == "__main__":
    main()
