#!/usr/bin/env python3
r"""
Bangalore Company, Recruiter & Hiring Intelligence Search Engine
Queries the master SQLite database: E:\anti\data\aditya_global_career_intelligence.db
"""

import sqlite3
import argparse
import sys
import json
import os

DB_PATH = r"E:\anti\data\aditya_global_career_intelligence.db"

def get_connection():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at {DB_PATH}")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)

def print_banner():
    print("=" * 80)
    print("  OMEGA (INFINITY) BANGALORE CORPORATE ECOSYSTEM & HIRING INTELLIGENCE ENGINE")
    print("  7,618+ Companies | 12,800+ HR Contacts | 3,234+ Active Jobs | 6 Corridors")
    print("=" * 80)

def search_companies(keyword, industry=None, limit=20):
    conn = get_connection()
    c = conn.cursor()
    query = """
    SELECT company_id, brand_name, legal_name, industry, office_locations, website, careers_url, ats_platform, hiring_status
    FROM companies
    WHERE 1=1
    """
    params = []
    if keyword:
        query += " AND (brand_name LIKE ? OR legal_name LIKE ? OR technology_stack_if_public LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
    if industry:
        query += " AND industry LIKE ?"
        params.append(f"%{industry}%")
    
    query += " LIMIT ?"
    params.append(limit)

    rows = c.execute(query, params).fetchall()
    print(f"\n[+] Found {len(rows)} Companies matching '{keyword or ''}' (Industry: {industry or 'All'}) (Limit: {limit}):\n")
    for r in rows:
        print(f" * [{r[0]}] {r[1]} ({r[3]})")
        print(f"   Locations: {r[4] or 'Bengaluru'} | ATS: {r[7] or 'N/A'} | Status: {r[8]}")
        print(f"   Website: {r[5] or 'N/A'} | Careers: {r[6] or 'N/A'}")
        print("-" * 70)

def search_recruiters(company=None, keyword=None, classification=None, limit=20):
    conn = get_connection()
    c = conn.cursor()
    query = """
    SELECT full_name, current_title, company_name, classification, professional_email, public_business_phone, linkedin_url
    FROM people
    WHERE 1=1
    """
    params = []
    if company:
        query += " AND company_name LIKE ?"
        params.append(f"%{company}%")
    if keyword:
        query += " AND (full_name LIKE ? OR current_title LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    if classification:
        query += " AND classification = ?"
        params.append(classification.upper())
    
    query += " LIMIT ?"
    params.append(limit)

    rows = c.execute(query, params).fetchall()
    print(f"\n[+] Found {len(rows)} HR / Recruiter contacts (Limit: {limit}):\n")
    for r in rows:
        print(f" * {r[0]} - {r[1]} @ {r[2]} [{r[3]}]")
        print(f"   Email: {r[4] or 'Use pattern matching'} | Phone: {r[5] or 'Campus Board'}")
        print(f"   LinkedIn: {r[6] or 'Search profile'}")
        print("-" * 70)

def search_jobs(keyword=None, seniority=None, limit=20):
    conn = get_connection()
    c = conn.cursor()
    query = """
    SELECT job_id, company_name, job_title, normalized_title, experience_min, experience_max, skills, application_url, ats
    FROM jobs
    WHERE 1=1
    """
    params = []
    if keyword:
        query += " AND (job_title LIKE ? OR skills LIKE ? OR required_skills LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
    if seniority:
        query += " AND seniority LIKE ?"
        params.append(f"%{seniority}%")
    
    query += " LIMIT ?"
    params.append(limit)

    rows = c.execute(query, params).fetchall()
    print(f"\n[+] Found {len(rows)} Openings matching '{keyword or ''}' (Limit: {limit}):\n")
    for r in rows:
        print(f" * [{r[0]}] {r[2]} @ {r[1]}")
        print(f"   Exp: {r[4]}-{r[5]} Yrs | ATS: {r[8] or 'Portal'}")
        skills_str = (r[6][:90] + "...") if r[6] and len(r[6]) > 90 else (r[6] or "Standard domain skills")
        print(f"   Skills: {skills_str}")
        print(f"   Apply URL: {r[7] or 'Check Careers page'}")
        print("-" * 70)

def display_stats():
    conn = get_connection()
    c = conn.cursor()
    total_companies = c.execute("SELECT count(*) FROM companies").fetchone()[0]
    total_people = c.execute("SELECT count(*) FROM people").fetchone()[0]
    total_jobs = c.execute("SELECT count(*) FROM jobs").fetchone()[0]
    recruiters = c.execute("SELECT count(*) FROM people WHERE classification='RECRUITER'").fetchone()[0]
    hiring_managers = c.execute("SELECT count(*) FROM people WHERE classification='HIRING_MANAGER'").fetchone()[0]
    
    print("\n--- MASTER DATABASE METRICS ---")
    print(f"Total Bangalore Companies Indexed: {total_companies:,}")
    print(f"Total Professional Contacts:       {total_people:,}")
    print(f"  * Verified Recruiters:           {recruiters:,}")
    print(f"  * Hiring Managers & VPs:         {hiring_managers:,}")
    print(f"Total Live Indexed Jobs:           {total_jobs:,}")
    print("--------------------------------\n")
    
    print("Top 8 Sectors in Bengaluru:")
    for row in c.execute("SELECT industry, count(*) FROM companies GROUP BY industry ORDER BY count(*) DESC LIMIT 8").fetchall():
        print(f" - {row[0]}: {row[1]} companies")
    print()

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Search Bangalore Company & Hiring Intelligence Engine")
    parser.add_argument("--stats", action="store_true", help="Show overview statistics")
    parser.add_argument("--company", type=str, help="Search companies by name or tech stack")
    parser.add_argument("--industry", type=str, help="Filter companies by industry/sector")
    parser.add_argument("--recruiter", type=str, help="Search recruiters by name/title")
    parser.add_argument("--recruiter-company", type=str, help="Search recruiters at a specific company")
    parser.add_argument("--job", type=str, help="Search jobs by title or required skill")
    parser.add_argument("--limit", type=int, default=15, help="Result limit (default: 15)")

    args = parser.parse_args()

    if len(sys.argv) == 1 or args.stats:
        display_stats()
        return

    if args.company or args.industry:
        search_companies(args.company, args.industry, limit=args.limit)
    elif args.recruiter or args.recruiter_company:
        search_recruiters(company=args.recruiter_company, keyword=args.recruiter, limit=args.limit)
    elif args.job:
        search_jobs(keyword=args.job, limit=args.limit)
    else:
        display_stats()

if __name__ == "__main__":
    main()
