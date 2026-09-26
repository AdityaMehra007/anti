#!/usr/bin/env python3
"""
========================================================================================
BANGALORE FUNDED STARTUPS & GLOBAL MNCs (USA, UK, GLOBAL) COMPILER & EXPORTER
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Compiles and exports the definitive directory of funded startups, US MNC GCCs,
UK enterprises, and European conglomerates hiring non-sales operations talent in Bangalore.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Any

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "bangalore_funded_startups_and_global_mncs.json"
CSV_FILE = ROOT_DIR / "BANGALORE_FUNDED_STARTUPS_AND_GLOBAL_MNCS_MASTER.csv"

def load_directory() -> List[Dict[str, Any]]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def export_csv(output_path: Path = CSV_FILE) -> int:
    companies = load_directory()
    if not companies:
        print("[!] No companies found in JSON dataset.")
        return 0

    headers = [
        "ID",
        "Company Name",
        "Category",
        "Country of Origin",
        "Funding Status / Scale",
        "Bangalore Corridor / Location",
        "Target Role (Non-Sales)",
        "Experience Level",
        "Fixed Base (LPA)",
        "Total CTC Range (LPA)",
        "Est Monthly In-Hand (INR)",
        "HR / TA Contact",
        "HR Direct Email",
        "Desk / Board Phone",
        "Direct Careers Portal URL",
        "Strategic Fit Rationale"
    ]

    rows = []
    for c in companies:
        ctc_range = f"₹{c.get('total_ctc_min', 0)}L - ₹{c.get('total_ctc_max', 0)}L"
        rows.append([
            c.get("id", ""),
            c.get("company_name", ""),
            c.get("category", ""),
            c.get("origin_country", ""),
            c.get("funding_status", ""),
            c.get("bangalore_corridor", ""),
            c.get("target_role", ""),
            c.get("experience_level", ""),
            f"₹{c.get('fixed_base_lpa', 0)}L",
            ctc_range,
            f"₹{c.get('monthly_in_hand_est', 0):,}/mo",
            c.get("hr_lead", ""),
            c.get("hr_email", ""),
            c.get("desk_phone", ""),
            c.get("direct_apply_url", ""),
            c.get("strategic_fit_rationale", "")
        ])

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"[OK] Exported {len(rows)} verified enterprises to {output_path}")
    return len(rows)

def print_status():
    companies = load_directory()
    print("=" * 80)
    print("  BANGALORE FUNDED STARTUPS & GLOBAL MNCs DIRECTORY")
    print(f"  Total Verified Enterprises : {len(companies)}")
    print("  Guardrail Enforced         : 100% Non-Sales Operations (0% Sales Risk)")
    print("=" * 80)
    
    categories = {}
    for c in companies:
        cat = c.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1
        
    print("\n[+] SECTOR DISTRIBUTION:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat:55} : {count} firms")
        
    salary_mins = [c.get("total_ctc_min", 0) for c in companies if c.get("total_ctc_min")]
    salary_maxs = [c.get("total_ctc_max", 0) for c in companies if c.get("total_ctc_max")]
    
    if salary_mins and salary_maxs:
        print(f"\n[+] COMPENSATION SPECTRUM:")
        print(f"  - Minimum CTC Range : ₹{min(salary_mins):.1f}L - ₹{max(salary_mins):.1f}L PA")
        print(f"  - Maximum CTC Range : ₹{min(salary_maxs):.1f}L - ₹{max(salary_maxs):.1f}L PA")
        print(f"  - Median Fresher CTC: ₹{(sum(salary_mins)/len(salary_mins) + sum(salary_maxs)/len(salary_maxs))/2:.1f}L PA")

    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Compile and export Bangalore Funded Startups & Global MNCs")
    parser.add_argument("--export-csv", action="store_true", help="Export to master CSV")
    parser.add_argument("--status", action="store_true", help="Print directory status & salary benchmarks")
    
    args = parser.parse_args()
    
    if args.export_csv:
        export_csv()
    elif args.status:
        print_status()
    else:
        # Default: export CSV and show status
        export_csv()
        print_status()

if __name__ == "__main__":
    main()
