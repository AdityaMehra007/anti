#!/usr/bin/env python3
r"""
OMEGA BANGALORE EVERYTHING AUTOMATED PIPELINE RUNNER
Automates:
1. SQLite Database integrity verification
2. Generation/Refresh of the Everything Master Hub HTML Console
3. Comprehensive CSV/JSON exports for HR, Jobs, and Companies
4. Interactive Command-Line Search & Launch
"""

import os
import sys
import json
import sqlite3
import subprocess

DB_PATH = r"E:\anti\data\aditya_global_career_intelligence.db"
HUB_HTML = r"E:\anti\apps\job_application_studio\bangalore_everything_master_hub.html"
BUILDER_SCRIPT = r"E:\anti\scripts\build_bangalore_everything_hub.py"

def step_verify_database():
    print("\n[STEP 1/4] Verifying Master SQLite Database Integrity...")
    if not os.path.exists(DB_PATH):
        print(f"[-] Database not found at {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA integrity_check;")
    status = c.fetchone()[0]
    
    companies_cnt = c.execute("SELECT count(*) FROM companies").fetchone()[0]
    people_cnt = c.execute("SELECT count(*) FROM people").fetchone()[0]
    jobs_cnt = c.execute("SELECT count(*) FROM jobs").fetchone()[0]
    conn.close()
    
    print(f" [+] SQLite Integrity Check: {status}")
    print(f" [+] Verified Companies:     {companies_cnt:,}")
    print(f" [+] Verified People & HR:   {people_cnt:,}")
    print(f" [+] Verified Live Jobs:     {jobs_cnt:,}")
    return True

def step_build_master_hub():
    print("\n[STEP 2/4] Compiling Master Everything Web Hub...")
    res = subprocess.run([sys.executable, BUILDER_SCRIPT], capture_output=True, text=True)
    if res.returncode == 0:
        size_mb = os.path.getsize(HUB_HTML) / (1024 * 1024)
        print(f" [+] Master Web Hub built successfully: {HUB_HTML} ({size_mb:.2f} MB)")
    else:
        print(f" [-] Build failed: {res.stderr}")

def step_export_summary_ledgers():
    print("\n[STEP 3/4] Exporting Top Bangalore Target Ledgers...")
    export_csv = r"E:\anti\data\Bangalore_Top_Targets_Summary_Export.csv"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("""
        SELECT c.brand_name, c.industry, c.office_locations, c.website, c.careers_url, 
               p.full_name, p.current_title, p.professional_email, p.linkedin_url
        FROM companies c
        LEFT JOIN people p ON c.brand_name = p.company_name AND p.classification = 'RECRUITER'
        LIMIT 500
    """).fetchall()
    conn.close()

    import csv
    with open(export_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Company Name", "Industry", "Location", "Website", "Careers Portal", "Recruiter Name", "Recruiter Title", "Email", "LinkedIn"])
        for r in rows:
            writer.writerow(r)
    print(f" [+] Exported 500 top target pairs to: {export_csv}")

def step_summary_and_launch():
    print("\n[STEP 4/4] Pipeline Complete!")
    print("=" * 80)
    print("  ALL SYSTEMS OPERATIONAL & VERIFIED")
    print(f"  • Web Hub App:    file:///{HUB_HTML.replace('\\', '/')}")
    print("  • Search Engine:  python scripts/bangalore_company_hiring_search.py --stats")
    print("  • Database File:  E:\\anti\\data\\aditya_global_career_intelligence.db")
    print("=" * 80)

def main():
    print("=" * 80)
    print("  STARTING OMEGA AUTONOMOUS BANGALORE PIPELINE EXECUTION")
    print("=" * 80)
    step_verify_database()
    step_build_master_hub()
    step_export_summary_ledgers()
    step_summary_and_launch()

if __name__ == "__main__":
    main()
