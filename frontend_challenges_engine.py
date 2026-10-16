#!/usr/bin/env python3
"""
frontend_challenges_engine.py — Dedicated Command Line Interface for Frontend Challenges
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

DB_PATH = Path(r"e:\anti\data\frontend_challenges.db")
DASHBOARD_PATH = Path(r"e:\anti\frontend_challenges_dashboard.html")

def search_challenges(query: str, limit: int = 15):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    try:
        results = c.execute("""
            SELECT id, company_name, country, lang, stack, challenge_url, jobs_url
            FROM frontend_challenges_fts
            WHERE frontend_challenges_fts MATCH ?
            LIMIT ?
        """, (query, limit)).fetchall()
    except Exception:
        results = c.execute("""
            SELECT id, company_name, country, lang, stack, challenge_url, jobs_url
            FROM frontend_challenges
            WHERE company_name LIKE ? OR stack LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit)).fetchall()
    conn.close()

    print(f"\n[FRONTEND CHALLENGES] Found {len(results)} matches for '{query}':")
    print("=" * 85)
    for cid, company, country, lang, stack, code_url, jobs_url in results:
        flag = country if country else ""
        print(f"• [{cid}] {flag} {company} ({lang.upper()})")
        print(f"  Stack: {stack}")
        print(f"  Challenge: {code_url}")
        if jobs_url and jobs_url != "-":
            print(f"  Careers: {jobs_url}")
        print("-" * 85)

def show_stats():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    total = c.execute("SELECT count(*) FROM frontend_challenges").fetchone()[0]
    react_c = c.execute("SELECT count(*) FROM frontend_challenges WHERE stack LIKE '%React%'").fetchone()[0]
    vue_c = c.execute("SELECT count(*) FROM frontend_challenges WHERE stack LIKE '%Vue%'").fetchone()[0]
    ts_c = c.execute("SELECT count(*) FROM frontend_challenges WHERE stack LIKE '%Type%' OR stack LIKE '%TS%'").fetchone()[0]
    node_c = c.execute("SELECT count(*) FROM frontend_challenges WHERE stack LIKE '%Node%'").fetchone()[0]
    conn.close()

    print("\n=======================================================")
    print("        FRONT-END CHALLENGES KNOWLEDGE STATS           ")
    print("=======================================================")
    print(f"  Total Challenges Indexed : {total}")
    print(f"  React Challenges         : {react_c}")
    print(f"  TypeScript Challenges    : {ts_c}")
    print(f"  Vue.js Challenges        : {vue_c}")
    print(f"  Node.js Challenges       : {node_c}")
    print("=======================================================\n")

def main():
    if len(sys.argv) < 2:
        print("""Frontend Challenges CLI Engine
Usage:
  python frontend_challenges_engine.py --stats              # View stack distribution
  python frontend_challenges_engine.py --search <keyword>   # Search companies or stacks
  python frontend_challenges_engine.py --dashboard          # Launch Web Command Center
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
        search_challenges(q)
    elif cmd in ["--dashboard", "-d", "dashboard"]:
        if DASHBOARD_PATH.exists():
            print(f"[+] Opening {DASHBOARD_PATH} in browser...")
            webbrowser.open(DASHBOARD_PATH.as_uri())
        else:
            print("Dashboard file not found.")

if __name__ == "__main__":
    main()
