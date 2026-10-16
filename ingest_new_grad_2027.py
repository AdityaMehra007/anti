#!/usr/bin/env python3
"""
ingest_new_grad_2027.py — Ingest and index vanshb03/New-Grad-2027 into JSON, CSV, and SQLite FTS5.
"""

import sys
import json
import sqlite3
import csv
from pathlib import Path
from datetime import datetime

# UTF-8 console output
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = Path(r"e:\anti\New-Grad-2027")
SRC_JSON = REPO_DIR / ".github" / "scripts" / "listings.json"
OUT_ALL_JSON = Path(r"e:\anti\data\new_grad_2027_all.json")
OUT_ACTIVE_JSON = Path(r"e:\anti\data\new_grad_2027_active.json")
OUT_ACTIVE_CSV = Path(r"e:\anti\data\new_grad_2027_active.csv")
MASTER_DB = Path(r"e:\anti\data\omega_unified_master.db")
DOMAIN_DB = Path(r"e:\anti\data\new_grad_2027.db")

def main():
    print("[+] Ingesting vanshb03/New-Grad-2027 listings...")
    with open(SRC_JSON, "r", encoding="utf-8") as f:
        listings = json.load(f)

    active_listings = [item for item in listings if item.get("active", False)]
    print(f"[+] Total listings parsed: {len(listings):,d}")
    print(f"[+] Active New Grad 2027 roles: {len(active_listings):,d}")

    # Ensure output directories exist
    OUT_ACTIVE_JSON.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUT_ALL_JSON, "w", encoding="utf-8") as f:
        json.dump(listings, f, indent=2, ensure_ascii=False)
        
    with open(OUT_ACTIVE_JSON, "w", encoding="utf-8") as f:
        json.dump(active_listings, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved active listings to {OUT_ACTIVE_JSON}")

    # Export CSV
    fieldnames = [
        "id", "company_name", "title", "locations", 
        "sponsorship", "url", "company_url", "source", "date_posted", "date_updated"
    ]
    with open(OUT_ACTIVE_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for item in active_listings:
            row = dict(item)
            if isinstance(row.get("locations"), list):
                row["locations"] = "; ".join(row["locations"])
            writer.writerow(row)
    print(f"[+] Saved CSV to {OUT_ACTIVE_CSV}")

    # Build standalone Domain DB
    build_domain_db(DOMAIN_DB, active_listings)
    
    # Merge into Master Unified DB
    merge_master_db(MASTER_DB, active_listings)
    print("[+] Database ingestion & FTS5 indexing completed successfully.")

def build_domain_db(db_path: Path, active_listings: list):
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS new_grad_2027 (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            title TEXT,
            locations TEXT,
            sponsorship TEXT,
            url TEXT,
            company_url TEXT,
            source TEXT,
            date_posted INTEGER,
            date_updated INTEGER
        )
    """)
    for item in active_listings:
        locs = "; ".join(item.get("locations", [])) if isinstance(item.get("locations"), list) else str(item.get("locations", ""))
        c.execute("""
            INSERT OR REPLACE INTO new_grad_2027
            (id, company_name, title, locations, sponsorship, url, company_url, source, date_posted, date_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get("id"),
            item.get("company_name"),
            item.get("title"),
            locs,
            item.get("sponsorship", ""),
            item.get("url", ""),
            item.get("company_url", ""),
            item.get("source", ""),
            item.get("date_posted", 0),
            item.get("date_updated", 0)
        ))

    c.execute("DROP TABLE IF EXISTS new_grad_2027_fts")
    c.execute("""
        CREATE VIRTUAL TABLE new_grad_2027_fts USING fts5(
            id, company_name, title, locations, sponsorship, url
        )
    """)
    c.execute("""
        INSERT INTO new_grad_2027_fts (id, company_name, title, locations, sponsorship, url)
        SELECT id, company_name, title, locations, sponsorship, url FROM new_grad_2027
    """)
    conn.commit()
    conn.close()
    print(f"[+] Domain DB {db_path.name} built with FTS5 search index.")

def merge_master_db(db_path: Path, active_listings: list):
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS new_grad_2027 (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            title TEXT,
            locations TEXT,
            sponsorship TEXT,
            url TEXT,
            company_url TEXT,
            source TEXT,
            date_posted INTEGER,
            date_updated INTEGER
        )
    """)
    for item in active_listings:
        locs = "; ".join(item.get("locations", [])) if isinstance(item.get("locations"), list) else str(item.get("locations", ""))
        c.execute("""
            INSERT OR REPLACE INTO new_grad_2027
            (id, company_name, title, locations, sponsorship, url, company_url, source, date_posted, date_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get("id"),
            item.get("company_name"),
            item.get("title"),
            locs,
            item.get("sponsorship", ""),
            item.get("url", ""),
            item.get("company_url", ""),
            item.get("source", ""),
            item.get("date_posted", 0),
            item.get("date_updated", 0)
        ))

    c.execute("DELETE FROM unified_search_fts WHERE domain = 'New Grad 2027'")
    for item in active_listings:
        locs = "; ".join(item.get("locations", [])) if isinstance(item.get("locations"), list) else str(item.get("locations", ""))
        content = f"{item.get('company_name', '')} {item.get('title', '')} {locs} {item.get('sponsorship', '')} {item.get('url', '')} {item.get('source', '')}"
        c.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "New Grad 2027",
            item.get("id", ""),
            f"{item.get('company_name', '')} - {item.get('title', '')}",
            "New Grad 2027 Role",
            content
        ))
    conn.commit()
    conn.close()
    print(f"[+] Merged {len(active_listings):,d} records into Master Unified DB ({db_path.name}).")

if __name__ == "__main__":
    main()
