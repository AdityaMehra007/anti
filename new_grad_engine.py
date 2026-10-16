#!/usr/bin/env python3
"""
new_grad_engine.py — Dedicated Command Line Interface for New Grad 2026 Positions
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

DB_PATH = Path(r"e:\anti\data\new_grad_positions.db")
DASHBOARD_PATH = Path(r"e:\anti\new_grad_dashboard.html")

def search_roles(query: str, limit: int = 15):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    try:
        results = c.execute("""
            SELECT company_name, title, category, locations, sponsorship, url
            FROM new_grad_fts
            WHERE new_grad_fts MATCH ?
            LIMIT ?
        """, (query, limit)).fetchall()
    except Exception:
        results = c.execute("""
            SELECT company_name, title, category, locations, sponsorship, url
            FROM new_grad_listings
            WHERE company_name LIKE ? OR title LIKE ? OR locations LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", limit)).fetchall()
    conn.close()

    print(f"\n[NEW GRAD 2026] Found {len(results)} roles matching '{query}':")
    print("=" * 85)
    for company, title, cat, locs, sponsor, url in results:
        sp_tag = f"[{sponsor}]" if sponsor else ""
        print(f"• {company} — {title} ({cat}) {sp_tag}")
        print(f"  Location: {locs}")
        print(f"  Apply: {url}")
        print("-" * 85)

def show_stats():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    total = c.execute("SELECT count(*) FROM new_grad_listings").fetchone()[0]
    cats = c.execute("SELECT category, count(*) FROM new_grad_listings GROUP BY category ORDER BY count(*) DESC").fetchall()
    conn.close()

    print("\n=======================================================")
    print("        SIMPLIFYJOBS NEW GRAD 2026 STATS              ")
    print("=======================================================")
    print(f"  Total Active Roles: {total:,d}")
    print("\n  Roles by Category:")
    for cat, count in cats:
        print(f"    - {cat:20s}: {count:,d}")
    print("=======================================================\n")

def main():
    if len(sys.argv) < 2:
        print("""New Grad 2026 CLI Engine
Usage:
  python new_grad_engine.py --stats              # View distribution of roles
  python new_grad_engine.py --search <keyword>   # Search companies, roles, locations
  python new_grad_engine.py --dashboard          # Launch Web Command Center
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
        search_roles(q)
    elif cmd in ["--dashboard", "-d", "dashboard"]:
        if DASHBOARD_PATH.exists():
            print(f"[+] Opening {DASHBOARD_PATH} in browser...")
            webbrowser.open(DASHBOARD_PATH.as_uri())
        else:
            print("Dashboard file not found.")

if __name__ == "__main__":
    main()
