"""
Unified CLI for Hiring Intelligence OS (AGHIS-Ω)
Enables interactive inspection of startups, live open roles, decision makers, and outreach campaigns.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from hiring_intelligence.db import get_connection
from hiring_intelligence.live_scanner import scan_and_ingest

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def list_startups():
    conn = get_connection()
    rows = conn.execute("SELECT name, stage, industry, total_funding_usd, headcount, careers_url FROM startups ORDER BY total_funding_usd DESC").fetchall()
    conn.close()

    print("\n" + "=" * 90)
    print(f"{'COMPANY':<24} | {'STAGE':<12} | {'FUNDING':<10} | {'HEADCOUNT':<10} | {'INDUSTRY'}")
    print("=" * 90)
    for r in rows:
        funding = f"${r['total_funding_usd']/1e6:.1f}M" if r['total_funding_usd'] < 1e9 else f"${r['total_funding_usd']/1e9:.2f}B"
        print(f"{r['name']:<24} | {r['stage']:<12} | {funding:<10} | {r['headcount']:<10} | {r['industry']}")
    print("=" * 90 + f"\nTotal Tracked: {len(rows)} Companies\n")


def list_roles(keyword: str = "", limit: int = 25):
    conn = get_connection()
    query = """
    SELECT s.name as company, r.title, r.seniority_level, r.salary_min_usd, r.salary_max_usd, r.tech_stack, r.remote_type, r.direct_apply_url
    FROM open_roles r
    JOIN startups s ON r.startup_id = s.id
    WHERE r.title LIKE ? OR r.tech_stack LIKE ? OR s.name LIKE ?
    ORDER BY r.urgency_score DESC
    LIMIT ?
    """
    param = f"%{keyword}%"
    rows = conn.execute(query, (param, param, param, limit)).fetchall()
    conn.close()

    print("\n" + "=" * 105)
    print(f"{'COMPANY':<18} | {'ROLE TITLE':<35} | {'COMP RANGE':<16} | {'MODALITY':<18} | {'APPLY URL'}")
    print("=" * 105)
    for r in rows:
        comp = f"${r['salary_min_usd']//1000}k-${r['salary_max_usd']//1000}k" if r['salary_min_usd'] > 0 else "Equity / Comm."
        print(f"{r['company']:<18} | {r['title'][:34]:<35} | {comp:<16} | {r['remote_type'][:17]:<18} | {r['direct_apply_url']}")
    print("=" * 105 + f"\nShowing {len(rows)} matching roles\n")


def list_freshers():
    conn = get_connection()
    query = """
    SELECT s.name as company, r.title, r.batch_eligibility, r.min_cgpa, r.test_pattern, r.salary_min_usd, r.salary_max_usd, r.direct_apply_url
    FROM open_roles r
    JOIN startups s ON r.startup_id = s.id
    WHERE r.seniority_level LIKE '%fresher%' OR r.title LIKE '%grad%' OR r.title LIKE '%early career%' OR r.title LIKE '%analyst%' OR r.title LIKE '%genc%' OR r.title LIKE '%ninja%' OR r.title LIKE '%associate%'
    ORDER BY s.total_funding_usd DESC
    """
    rows = conn.execute(query).fetchall()
    conn.close()

    print("\n" + "=" * 120)
    print(f"{'MNC / COMPANY':<20} | {'FRESHER ROLE':<32} | {'BATCH':<16} | {'MIN CRITERIA':<16} | {'APPLY URL'}")
    print("=" * 120)
    for r in rows:
        print(f"{r['company']:<20} | {r['title'][:31]:<32} | {r['batch_eligibility'][:15]:<16} | {r['min_cgpa'][:15]:<16} | {r['direct_apply_url']}")
        print(f"   -> Exam Pattern: {r['test_pattern']}")
        print("-" * 120)
    print(f"\nTotal Fresher Programs Tracked: {len(rows)}\n")


def show_outreach(limit: int = 3):
    conn = get_connection()
    query = """
    SELECT c.subject, c.message_body, s.name as company, dm.full_name as dm_name, dm.title as dm_title, dm.verified_email
    FROM outreach_campaigns c
    JOIN decision_makers dm ON c.decision_maker_id = dm.id
    JOIN startups s ON dm.startup_id = s.id
    LIMIT ?
    """
    rows = conn.execute(query, (limit,)).fetchall()
    conn.close()

    for idx, r in enumerate(rows, 1):
        print("\n" + "#" * 60)
        print(f"OUTREACH PLAYBOOK #{idx}: {r['company']} -> {r['dm_name']} ({r['dm_title']})")
        print(f"Email: {r['verified_email']}")
        print(f"Subject: {r['subject']}")
        print("-" * 60)
        print(r['message_body'])
        print("#" * 60)


def main():
    parser = argparse.ArgumentParser(description="Hiring Intelligence OS CLI")
    parser.add_argument("--startups", action="store_true", help="List all tracked startups and MNCs")
    parser.add_argument("--fresher", action="store_true", help="List all MNC and listed company fresher hiring drives")
    parser.add_argument("--roles", action="store_true", help="List top open roles")
    parser.add_argument("--search", type=str, default="", help="Search roles by title, stack, or company")
    parser.add_argument("--outreach", action="store_true", help="Preview generated cold outreach playbooks")
    parser.add_argument("--scan", action="store_true", help="Run live ATS reconnaissance scanner")
    args = parser.parse_args()

    if args.scan:
        scan_and_ingest()
    elif args.fresher:
        list_freshers()
    elif args.startups:
        list_startups()
    elif args.roles or args.search:
        list_roles(keyword=args.search)
    elif args.outreach:
        show_outreach()
    else:
        list_roles()



if __name__ == "__main__":
    main()
