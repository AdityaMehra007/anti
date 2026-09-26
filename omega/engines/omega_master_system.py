# -*- coding: utf-8 -*-
"""
??? ANTIGRAVITY OMEGA: UNIFIED MASTER CAREER OPERATING SYSTEM (v3.0)
Candidate & Operator: Aditya Mehra | Location: Bengaluru, Karnataka, India
"""

import os
import sys
import json
import sqlite3
import datetime
import argparse
import webbrowser
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = Path("E:/anti")
DB_PATH = BASE_DIR / "data" / "omega_career_database.sqlite" if (BASE_DIR / "data" / "omega_career_database.sqlite").exists() else BASE_DIR / "omega_career_database.sqlite"
PROFILE_PATH = BASE_DIR / "data" / "verified_profile.json" if (BASE_DIR / "data" / "verified_profile.json").exists() else BASE_DIR / "verified_profile.json"
DASHBOARD_PATH = BASE_DIR / "omega_titan" / "dashboard.html"

def load_profile():
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

def get_db():
    return sqlite3.connect(DB_PATH)

def cmd_status():
    conn = get_db()
    cur = conn.cursor()
    v_profile = load_profile()
    cand = v_profile['candidate']
    edu = v_profile['education'][0]

    print("=" * 85)
    print("??? ANTIGRAVITY OMEGA: UNIFIED MASTER SYSTEM STATUS")
    print("=" * 85)
    print(f"?? Candidate: {cand['full_name']} | Location: {cand['location']}")
    print(f"?? Education: {edu['degree']} ({edu['duration']}) - {edu['institution']}")
    print(f"?? Positioning: AI-Enabled Business Operations, Business Analysis & International Trade")
    print(f"?? Target CTC: ?{cand['target_compensation_inr']['entry_min']:,} - ?{cand['target_compensation_inr']['aspirational_max']:,} (Median: ?{cand['target_compensation_inr']['target_median']:,})")
    print("-" * 85)

    rows = cur.execute('SELECT tier, company, title, fit_score, eov_score, interview_prob, status FROM job_pipeline ORDER BY eov_score DESC').fetchall()
    print(f"?? ACTIVE PIPELINE TELEMETRY ({len(rows)} Staged Target Roles):\n")
    print(f"{'#':<3} {'TIER':<5} {'COMPANY':<16} {'ROLE TITLE':<38} {'FIT':<7} {'EOV':<7} {'PROB':<6} {'STATUS'}")
    print("-" * 85)
    for i, r in enumerate(rows, 1):
        print(f"{i:<3} [{r[0]:<2}] {r[1]:<16} {r[2][:36]:<38} {r[3]:<6.1f}% {r[4]:<6.1f}% {r[5]:<6.2f} {r[6]}")

    print("=" * 85)
    conn.close()

def cmd_dashboard():
    print(f"?? Launching OMEGA-TITAN Web Command Center: {DASHBOARD_PATH}")
    if DASHBOARD_PATH.exists():
        webbrowser.open(str(DASHBOARD_PATH))
    else:
        print("Error: Dashboard HTML not found. Run --stage first.")

def cmd_interview():
    star_path = BASE_DIR / "Aditya_Mehra_STAR_Interview_Pack.md"
    print("=" * 85)
    print("??? OMEGA MASTER INTERVIEW DRILL & STAR FRAMEWORKS")
    print("=" * 85)
    if star_path.exists():
        print(star_path.read_text(encoding="utf-8"))
    else:
        print("STAR pack not found.")
    print("=" * 85)

def cmd_all():
    cmd_status()
    print("\n[1/3] Refreshing Live Opportunities...")
    # Trigger Titan Engine
    titan_engine = BASE_DIR / "omega_titan" / "omega_titan.py"
    if titan_engine.exists():
        os.system(f"python {titan_engine}")
    
    print("\n[2/3] Generating Master Telemetry Summary...")
    cmd_status()
    
    print("\n[3/3] Launching Web Dashboard...")
    cmd_dashboard()

def main():
    parser = argparse.ArgumentParser(description="Omega Master Career System")
    parser.add_argument("--status", action="store_true", help="Print pipeline status")
    parser.add_argument("--dashboard", action="store_true", help="Open visual web dashboard")
    parser.add_argument("--interview", action="store_true", help="Display interview STAR stories")
    parser.add_argument("--all", action="store_true", help="Run full system refresh & launch dashboard")
    
    args = parser.parse_args()
    if args.dashboard:
        cmd_dashboard()
    elif args.interview:
        cmd_interview()
    elif args.status:
        cmd_status()
    else:
        cmd_all()

if __name__ == '__main__':
    main()
