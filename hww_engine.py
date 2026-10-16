#!/usr/bin/env python3
"""
hww_engine.py — Hiring Without Whiteboards Autonomous CLI Engine
Search 767+ engineering companies by real-world interview style, remote status, and location.
"""

import sys
import json
import sqlite3
import webbrowser
from pathlib import Path

# Ensure UTF-8 output across Windows consoles
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

DB_PATH = Path(r"e:\anti\data\omega_unified_master.db")
JSON_PATH = Path(r"e:\anti\data\hiring_without_whiteboards.json")
HTML_PATH = Path(r"e:\anti\hiring_without_whiteboards_dashboard.html")

def search_companies(query: str, limit: int = 10):
    if not DB_PATH.exists():
        print("[-] Master database not found.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    try:
        results = c.execute("""
            SELECT name, location, interview_process, styles_json, url
            FROM hww_companies
            WHERE name LIKE ? OR location LIKE ? OR interview_process LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", limit)).fetchall()
    except Exception as e:
        print("[-] Query error:", e)
        conn.close()
        return
    conn.close()

    print(f"\nFound {len(results)} Hiring-Without-Whiteboards companies matching '{query}':")
    print("=" * 85)
    for name, loc, proc, s_json, url in results:
        styles = json.loads(s_json) if s_json else []
        print(f"• {name} [{loc}] -> {url}")
        print(f"  Styles : {', '.join(styles)}")
        clean_p = proc[:180].replace("\n", " ").strip() if proc else "Real-world engineering evaluation."
        print(f"  Process: {clean_p}...")
        print("-" * 85)

def show_stats():
    if not JSON_PATH.exists():
        print("[-] Companies JSON not found.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        comps = json.load(f)

    print("\nHIRING WITHOUT WHITEBOARDS METRICS:")
    print("=" * 60)
    print(f"Total Companies Cataloged : {len(comps):,d}")
    print(f"Remote-Friendly           : {sum(1 for c in comps if c.get('is_remote')):,d}")
    print(f"India Engineering Hubs    : {sum(1 for c in comps if c.get('is_india')):,d}")
    print("=" * 60)

def open_dashboard():
    if HTML_PATH.exists():
        print(f"[+] Opening {HTML_PATH} in browser...")
        webbrowser.open(HTML_PATH.as_uri())

def main():
    if len(sys.argv) < 2:
        print("""Hiring Without Whiteboards CLI Engine
Usage:
  python hww_engine.py --dashboard      # Launch Interactive Visual Web Directory
  python hww_engine.py --search <query>  # Search 767 companies by name, location, or process
  python hww_engine.py --stats           # Show global distribution metrics
        """)
        return

    cmd = sys.argv[1].lower()
    if cmd in ["--dashboard", "-d", "dashboard", "--web"]:
        open_dashboard()
    elif cmd in ["--search", "-s", "search"]:
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not q:
            print("Please specify a search query.")
            return
        search_companies(q)
    elif cmd in ["--stats", "stats"]:
        show_stats()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
