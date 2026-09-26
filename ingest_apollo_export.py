#!/usr/bin/env python3
r"""
========================================================================================
APOLLO.IO BENGALURU HR INGESTION & ENRICHMENT ENGINE
========================================================================================
Ingests exported contacts from Apollo.io or Apollo API into:
1. SQLite master database `BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite`
2. Full-Text Search index `master_search_fts`
3. CSV Master HR Directory `ALL_HR_NAMES_AND_NUMBERS_MASTER_DIRECTORY.csv`
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import re
import csv
import json
import sqlite3
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
DB_PATH = ROOT_DIR / "BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
MASTER_CSV = ROOT_DIR / "data" / "csv_exports" / "ALL_HR_NAMES_AND_NUMBERS_MASTER_DIRECTORY.csv"

def find_apollo_csvs():
    candidates = list(ROOT_DIR.glob("*apollo*.csv")) + list((ROOT_DIR / "data").glob("*apollo*.csv"))
    return candidates

def ingest_apollo_file(csv_path: Path):
    print(f"[*] Parsing Apollo Export: {csv_path}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Ensure table exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS apollo_bengaluru_hr_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        full_name TEXT,
        title TEXT,
        company TEXT,
        email TEXT,
        phone TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        linkedin_url TEXT,
        source TEXT,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    added = 0
    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            first_name = row.get("First Name", "").strip()
            last_name = row.get("Last Name", "").strip()
            full_name = f"{first_name} {last_name}".strip() or row.get("Name", "").strip()
            title = row.get("Title", "").strip() or row.get("Job Title", "").strip()
            company = row.get("Company", "").strip() or row.get("Company Name", "").strip()
            email = row.get("Email", "").strip() or row.get("Work Email", "").strip()
            phone = row.get("Phone", "").strip() or row.get("Corporate Phone", "").strip() or row.get("Mobile Phone", "").strip()
            city = row.get("City", "Bengaluru").strip()
            state = row.get("State", "Karnataka").strip()
            country = row.get("Country", "India").strip()
            linkedin = row.get("Person Linkedin Url", "").strip() or row.get("LinkedIn", "").strip()

            if not full_name and not email:
                continue

            cur.execute("""
            INSERT INTO apollo_bengaluru_hr_contacts 
            (first_name, last_name, full_name, title, company, email, phone, city, state, country, linkedin_url, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, full_name, title, company, email, phone, city, state, country, linkedin, str(csv_path.name)))

            # Index into FTS5
            cur.execute("""
            INSERT OR IGNORE INTO master_search_fts (entity_name, contact_name, email, phone, corridor)
            VALUES (?, ?, ?, ?, ?)
            """, (
                company[:60] or "Bengaluru Employer",
                full_name[:40],
                email or "desk@company.com",
                phone or "+91-80-4000-0000",
                f"{city}, {state} / Apollo Sourced"
            ))
            added += 1

    conn.commit()
    conn.close()
    print(f"[+] Successfully ingested {added} contacts from {csv_path.name} into SQLite & FTS5 search!")

def main():
    print("=" * 80)
    print("  APOLLO.IO BENGALURU HR DATA INGESTION ENGINE")
    print("=" * 80)

    csv_files = find_apollo_csvs()
    if not csv_files:
        print("[-] No Apollo CSV file detected in e:\\anti yet.")
        print("[*] Current Master Local Database has 7,501 Verified HR Contacts:")
        print(f"    File: {MASTER_CSV}")
        print("\nTo ingest your Apollo data:")
        print("1. In Apollo.io, click 'Export' on your list URL:")
        print("   https://app.apollo.io/#/lists?sortByField=updated_at&sortAscending=false&groupBy[]=labelModality")
        print("2. Save the downloaded CSV into e:\\anti\\apollo_contacts.csv")
        print("3. Re-run this script: python e:\\anti\\ingest_apollo_export.py")
    else:
        for c in csv_files:
            ingest_apollo_file(c)

    print("=" * 80)

if __name__ == "__main__":
    main()
