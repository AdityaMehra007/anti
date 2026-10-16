#!/usr/bin/env python3
"""
ai_college_jobs_engine.py — Dedicated Command Line Interface for 2027 AI College Jobs
"""

import sys
import json
import sqlite3
import webbrowser
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

DB_PATH = Path(r"e:\anti\data\ai_college_jobs.db")
DASHBOARD_PATH = Path(r"e:\anti\ai_college_jobs_dashboard.html")

def search_jobs(query: str, limit: int = 15):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    try:
        results = c.execute("""
            SELECT id, company_name, position, tier, role_type, region, location, salary, apply_url
            FROM ai_college_jobs_fts
            WHERE ai_college_jobs_fts MATCH ?
            LIMIT ?
        """, (query, limit)).fetchall()
    except Exception:
        results = c.execute("""
            SELECT id, company_name, position, tier, role_type, region, location, salary, apply_url
            FROM ai_college_jobs
            WHERE company_name LIKE ? OR position LIKE ? OR location LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", limit)).fetchall()
    conn.close()

    print(f"\n[AI COLLEGE JOBS 2027] Found {len(results)} roles matching '{query}':")
    print("=" * 85)
    for jid, comp, pos, tier, rtype, reg, loc, sal, url in results:
        sal_str = f"| {sal}" if sal and sal != "-" else ""
        print(f"• [{jid}] {comp} — {pos} ({rtype} • {tier} • {reg}) {sal_str}")
        print(f"  Location: {loc}")
        print(f"  Apply: {url}")
        print("-" * 85)

def show_stats():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    total = c.execute("SELECT count(*) FROM ai_college_jobs").fetchone()[0]
    by_type = c.execute("SELECT role_type, count(*) FROM ai_college_jobs GROUP BY role_type").fetchall()
    by_region = c.execute("SELECT region, count(*) FROM ai_college_jobs GROUP BY region").fetchall()
    by_tier = c.execute("SELECT tier, count(*) FROM ai_college_jobs GROUP BY tier ORDER BY count(*) DESC").fetchall()
    conn.close()

    print("\n=======================================================")
    print("        2027 AI COLLEGE JOBS INTELLIGENCE STATS        ")
    print("=======================================================")
    print(f"  Total Indexed Positions : {total:,d}")
    print("\n  By Role Type:")
    for rt, cnt in by_type:
        print(f"    - {rt:15s}: {cnt:,d}")
    print("\n  By Region:")
    for rg, cnt in by_region:
        print(f"    - {rg:15s}: {cnt:,d}")
    print("\n  By Prestige Tier:")
    for tr, cnt in by_tier:
        print(f"    - {tr:15s}: {cnt:,d}")
    print("=======================================================\n")

def main():
    if len(sys.argv) < 2:
        print("""2027 AI College Jobs CLI Engine
Usage:
  python ai_college_jobs_engine.py --stats              # View role distribution
  python ai_college_jobs_engine.py --search <keyword>   # Search positions or companies
  python ai_college_jobs_engine.py --dashboard          # Launch Web Command Center
        """)
        return

    cmd = sys.argv[1].lower()
    if cmd in ["--stats", "-s", "stats"]:
        show_stats()
    elif cmd in ["--search", "search"]:
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not q:
            print("Please specify a search query.")
            return
        search_jobs(q)
    elif cmd in ["--dashboard", "-d", "dashboard"]:
        if DASHBOARD_PATH.exists():
            print(f"[+] Opening {DASHBOARD_PATH} in browser...")
            webbrowser.open(DASHBOARD_PATH.as_uri())
        else:
            print("Dashboard file not found.")

if __name__ == "__main__":
    main()
