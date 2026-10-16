#!/usr/bin/env python3
"""
new_grad_2027_engine.py — Dedicated Command Line Interface for New Grad 2027 Positions (vanshb03/New-Grad-2027)
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

DB_PATH = Path(r"e:\anti\data\new_grad_2027.db")
DASHBOARD_PATH = Path(r"e:\anti\new_grad_2027_dashboard.html")

def search_roles(query: str, limit: int = 15):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    try:
        results = c.execute("""
            SELECT company_name, title, locations, sponsorship, url
            FROM new_grad_2027_fts
            WHERE new_grad_2027_fts MATCH ?
            LIMIT ?
        """, (query, limit)).fetchall()
    except Exception:
        results = c.execute("""
            SELECT company_name, title, locations, sponsorship, url
            FROM new_grad_2027
            WHERE company_name LIKE ? OR title LIKE ? OR locations LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", limit)).fetchall()
    conn.close()

    print(f"\n[NEW GRAD 2027] Found {len(results)} roles matching '{query}':")
    print("=" * 85)
    for company, title, locs, sponsor, url in results:
        sp_tag = f"[{sponsor}]" if sponsor else ""
        print(f"• {company} — {title} {sp_tag}")
        print(f"  Location: {locs}")
        print(f"  Apply: {url}")
        print("-" * 85)

def show_stats():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    total = c.execute("SELECT count(*) FROM new_grad_2027").fetchone()[0]
    sponsorships = c.execute("SELECT sponsorship, count(*) FROM new_grad_2027 GROUP BY sponsorship ORDER BY count(*) DESC").fetchall()
    top_cos = c.execute("SELECT company_name, count(*) FROM new_grad_2027 GROUP BY company_name ORDER BY count(*) DESC LIMIT 10").fetchall()
    conn.close()

    print("\n=======================================================")
    print("        NEW GRAD 2027 ARSENAL TELEMETRY                ")
    print("=======================================================")
    print(f"  Total Active Roles: {total:,d}")
    print("\n  Sponsorship Distribution:")
    for sp, count in sponsorships:
        sp_name = sp if sp else "Flexible / Unspecified"
        print(f"    • {sp_name:32s}: {count:4d}")
    print("\n  Top Employers:")
    for co, count in top_cos:
        print(f"    • {co:32s}: {count:4d}")
    print("=======================================================\n")

def open_dashboard():
    if DASHBOARD_PATH.exists():
        print(f"[+] Opening New Grad 2027 Command Center: {DASHBOARD_PATH}")
        webbrowser.open(DASHBOARD_PATH.as_uri())
    else:
        print(f"[-] Dashboard not found at {DASHBOARD_PATH}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python new_grad_2027_engine.py --search <query>")
        print("  python new_grad_2027_engine.py --stats")
        print("  python new_grad_2027_engine.py --ui")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd in ("--search", "-s") and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        search_roles(query)
    elif cmd in ("--stats", "-st"):
        show_stats()
    elif cmd in ("--ui", "-u"):
        open_dashboard()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
