#!/usr/bin/env python3
"""
jobfunnel_engine.py - OMEGA Dedicated CLI & Runner for JobFunnel Master Funnel
Supports:
  --stats               Display Funnel telemetry and duplicate audit metrics
  --search <query>      Instant FTS5 search across 6,910 clean listings
  --duplicates          Inspect cross-board duplicates flagged by TF-IDF & Key matching
  --ui                  Launch the standalone interactive JobFunnel dashboard
"""

import sys
import json
import sqlite3
import webbrowser
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
DB_PATH = ROOT_DIR / "data" / "jobfunnel_master.db"
TELEMETRY_PATH = ROOT_DIR / "data" / "jobfunnel_telemetry.json"
DUPLICATES_PATH = ROOT_DIR / "data" / "jobfunnel_duplicates.json"
DASHBOARD_PATH = ROOT_DIR / "jobfunnel_dashboard.html"

def show_stats():
    if not TELEMETRY_PATH.exists():
        print("Telemetry file not found. Run integrate_jobfunnel_engine.py first.")
        return
    t = json.load(open(TELEMETRY_PATH, "r", encoding="utf-8"))
    print("\n" + "="*65)
    print("        JOBFUNNEL MULTI-BOARD DEDUPLICATION & FUNNEL TELEMETRY")
    print("="*65)
    print(f"  Total Raw Ingested Postings : {t['total_raw_listings']:,}")
    print(f"  Duplicate Listings Blocked  : {t['total_duplicates_filtered']:,}")
    print(f"    - Exact Metadata Match    : {t['exact_duplicates']:,}")
    print(f"    - TF-IDF Cosine Match     : {t['tfidf_duplicates']:,}")
    print(f"  Clean Master Funnel Listings: {t['total_unique_listings']:,}")
    print("\n  Status Progression:")
    for k, v in t["status_breakdown"].items():
        print(f"    • {k.upper():<14}: {v:,} roles")
    print("\n  Workplace Remoteness Distribution:")
    for k, v in t["remoteness_breakdown"].items():
        print(f"    • {k:<14}: {v:,} roles")
    print("\n  Ecosystem Sourcing Distribution:")
    for k, v in t["provider_breakdown"].items():
        print(f"    • {k:<25}: {v:,} roles")
    print(f"  Master FTS5 Total Entities  : {t['omega_unified_master_total']:,}")
    print("="*65 + "\n")

def search_leads(query: str, limit: int = 15):
    if not DB_PATH.exists():
        print("Database not found. Run integrate_jobfunnel_engine.py first.")
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    clean_q = "".join(ch for ch in query if ch.isalnum() or ch in " _-").strip()
    if not clean_q:
        print("Invalid search query.")
        return

    tokens = clean_q.split()
    fts_match = " AND ".join(f'"{t}"*' for t in tokens)

    try:
        sql = """
            SELECT id, status, title, company, location, remoteness, provider, url
            FROM jobfunnel_fts
            WHERE jobfunnel_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """
        c.execute(sql, (fts_match, limit))
        rows = c.fetchall()
    except sqlite3.OperationalError:
        sql = """
            SELECT id, status, title, company, location, remoteness, provider, url
            FROM jobfunnel_listings
            WHERE title LIKE ? OR company LIKE ? OR location LIKE ?
            LIMIT ?
        """
        wc = f"%{clean_q}%"
        c.execute(sql, (wc, wc, wc, limit))
        rows = c.fetchall()

    conn.close()

    print(f"\n[JOBFUNNEL FTS5] Found {len(rows)} matches for '{query}':")
    print("="*80)
    for r in rows:
        rid, status, title, company, loc, remoteness, provider, url = r
        print(f"[{status.upper():<10}] {company} - {title} ({remoteness}) -> {rid}")
        print(f"   Provider: {provider} | Location: {loc or 'Unspecified'}")
        if url:
            print(f"   Portal  : {url[:80]}...")
        print("-" * 80)
    print()

def inspect_duplicates(limit: int = 10):
    if not DUPLICATES_PATH.exists():
        print("Duplicates audit log not found.")
        return
    dupes = json.load(open(DUPLICATES_PATH, "r", encoding="utf-8"))
    print(f"\n[JOBFUNNEL DUPLICATE AUDIT] Displaying {min(limit, len(dupes))} of {len(dupes):,} flagged duplicates:")
    print("="*80)
    for d in dupes[:limit]:
        print(f"[{d['type']}] Similarity: {d.get('similarity', 1.0)}")
        print(f"  Target: {d['company']} - {d['title']} ({d['location']})")
        print(f"  Origin: {d['original_provider']} ({d['original_id']}) -> Duplicate: {d['duplicate_provider']} ({d['duplicate_id']})")
        print("-" * 80)
    print()

def launch_ui():
    if DASHBOARD_PATH.exists():
        webbrowser.open(DASHBOARD_PATH.as_uri())
    else:
        print(f"Dashboard not found at {DASHBOARD_PATH}")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("""
OMEGA ∞ JobFunnel Dedicated CLI Engine
Usage:
  python jobfunnel_engine.py --stats               # View full funnel metrics & deduplication audit
  python jobfunnel_engine.py --search <query>      # Instant FTS5 search across 6,910 clean roles
  python jobfunnel_engine.py --duplicates          # Audit sample cross-board blocked duplicates
  python jobfunnel_engine.py --ui                  # Launch standalone interactive web dashboard
        """)
        return

    cmd = sys.argv[1].lower()
    if cmd in ["--stats", "-s"]:
        show_stats()
    elif cmd in ["--search", "-q"]:
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not q:
            print("Please specify a search term.")
            return
        search_leads(q)
    elif cmd in ["--duplicates", "-d"]:
        inspect_duplicates()
    elif cmd in ["--ui", "-u"]:
        launch_ui()
    else:
        print(f"Unknown option: {cmd}")

if __name__ == "__main__":
    main()
