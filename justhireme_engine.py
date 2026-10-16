#!/usr/bin/env python3
"""
justhireme_engine.py — Dedicated CLI for JustHireMe Job Fit & Intelligence Engine
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

DB_PATH = Path(r"e:\anti\data\justhireme_leads.db")
DASHBOARD_PATH = Path(r"e:\anti\justhireme_dashboard.html")

def search_leads(query: str, limit: int = 15):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    try:
        results = c.execute("""
            SELECT job_id, title, domain, category, fit_score, quality_score, reason, tech_stack
            FROM justhireme_leads
            WHERE title LIKE ? OR domain LIKE ? OR tech_stack LIKE ? OR reason LIKE ?
            ORDER BY fit_score DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", limit)).fetchall()
    except Exception as e:
        print(f"[-] Search query error: {e}")
        results = []
    conn.close()

    print(f"\n[JUSTHIREME INTEL] Found {len(results)} evaluated roles matching '{query}':")
    print("=" * 90)
    for jid, title, dom, cat, fit, q, reason, stack in results:
        print(f"• [{jid}] {title} ({dom})")
        print(f"  Fit Score: {fit}% | Quality Score: {q}/100 | Stack: {stack}")
        print(f"  Reason: {reason[:120]}...")
        print("-" * 90)

def show_stats():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    total = c.execute("SELECT count(*) FROM justhireme_leads").fetchone()[0]
    avg_fit = c.execute("SELECT round(avg(fit_score)) FROM justhireme_leads").fetchone()[0]
    prime = c.execute("SELECT count(*) FROM justhireme_leads WHERE fit_score >= 70").fetchone()[0]
    adjacent = c.execute("SELECT count(*) FROM justhireme_leads WHERE fit_score >= 50 AND fit_score < 70").fetchone()[0]
    domains = c.execute("SELECT domain, count(*), round(avg(fit_score)) FROM justhireme_leads GROUP BY domain ORDER BY count(*) DESC").fetchall()
    conn.close()

    print("\n=======================================================")
    print("        JUSTHIREME INTELLIGENCE & FIT TELEMETRY        ")
    print("=======================================================")
    print(f"  Total Evaluated Leads: {total:,d}")
    print(f"  Average Candidate Fit: {avg_fit}%")
    print(f"  Prime Fit Matches (>=70%): {prime}")
    print(f"  Adjacent Transferable Matches (50-69%): {adjacent}")
    print("\n  Evaluated Ecosystem Distribution:")
    for dom, count, af in domains:
        print(f"    • {dom:24s}: {count:4d} roles (Avg Fit: {af}%)")
    print("=======================================================\n")

def open_ui():
    if DASHBOARD_PATH.exists():
        print(f"[+] Opening JustHireMe Command Center: {DASHBOARD_PATH}")
        webbrowser.open(DASHBOARD_PATH.as_uri())
    else:
        print(f"[-] Dashboard not found at {DASHBOARD_PATH}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python justhireme_engine.py --stats")
        print("  python justhireme_engine.py --search <term>")
        print("  python justhireme_engine.py --ui")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd in ("--stats", "-st"):
        show_stats()
    elif cmd in ("--search", "-s") and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        search_leads(query)
    elif cmd in ("--ui", "-u"):
        open_ui()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
