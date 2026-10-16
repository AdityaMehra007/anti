#!/usr/bin/env python3
"""
ingest_new_grad.py — Normalize and index SimplifyJobs/New-Grad-Positions into SQLite & JSON
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

SRC_JSON = Path(r"e:\anti\New-Grad-Positions\.github\scripts\listings.json")
OUT_ACTIVE_JSON = Path(r"e:\anti\data\new_grad_active.json")
OUT_ACTIVE_CSV = Path(r"e:\anti\data\new_grad_active.csv")
MASTER_DB = Path(r"e:\anti\data\omega_unified_master.db")
DOMAIN_DB = Path(r"e:\anti\data\new_grad_positions.db")

def main():
    print("[+] Ingesting SimplifyJobs/New-Grad-Positions...")
    with open(SRC_JSON, "r", encoding="utf-8") as f:
        listings = json.load(f)

    active_listings = [item for item in listings if item.get("active", False)]
    print(f"[+] Total listings parsed: {len(listings):,d}")
    print(f"[+] Active new grad roles: {len(active_listings):,d}")

    OUT_ACTIVE_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_ACTIVE_JSON, "w", encoding="utf-8") as f:
        json.dump(active_listings, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved active listings to {OUT_ACTIVE_JSON}")

    # Export CSV
    fieldnames = [
        "id", "company_name", "title", "category", "locations", 
        "sponsorship", "degrees", "url", "company_url", "date_posted", "date_updated"
    ]
    with open(OUT_ACTIVE_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for item in active_listings:
            row = dict(item)
            if isinstance(row.get("locations"), list):
                row["locations"] = "; ".join(row["locations"])
            if isinstance(row.get("degrees"), list):
                row["degrees"] = "; ".join(row["degrees"])
            writer.writerow(row)
    print(f"[+] Saved CSV to {OUT_ACTIVE_CSV}")

    # Build standalone Domain DB
    build_db(DOMAIN_DB, active_listings, standalone=True)
    # Merge into Master Unified DB
    build_db(MASTER_DB, active_listings, standalone=False)
    print("[+] Database ingestion & FTS5 indexing completed successfully.")

def build_db(db_path: Path, active_listings: list, standalone: bool = False):
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS new_grad_listings (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            title TEXT,
            category TEXT,
            locations TEXT,
            sponsorship TEXT,
            degrees TEXT,
            url TEXT,
            company_url TEXT,
            date_posted INTEGER,
            date_updated INTEGER
        )
    """)

    # Populate table
    for item in active_listings:
        locs = "; ".join(item.get("locations", [])) if isinstance(item.get("locations"), list) else str(item.get("locations", ""))
        degs = "; ".join(item.get("degrees", [])) if isinstance(item.get("degrees"), list) else str(item.get("degrees", ""))
        c.execute("""
            INSERT OR REPLACE INTO new_grad_listings 
            (id, company_name, title, category, locations, sponsorship, degrees, url, company_url, date_posted, date_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get("id"),
            item.get("company_name"),
            item.get("title"),
            item.get("category", "Software"),
            locs,
            item.get("sponsorship", ""),
            degs,
            item.get("url", ""),
            item.get("company_url", ""),
            item.get("date_posted", 0),
            item.get("date_updated", 0)
        ))

    if standalone:
        c.execute("DROP TABLE IF EXISTS new_grad_fts")
        c.execute("""
            CREATE VIRTUAL TABLE new_grad_fts USING fts5(
                id, company_name, title, category, locations, sponsorship, degrees
            )
        """)
        c.execute("""
            INSERT INTO new_grad_fts (id, company_name, title, category, locations, sponsorship, degrees)
            SELECT id, company_name, title, category, locations, sponsorship, degrees FROM new_grad_listings
        """)
    else:
        # Also index into unified_search_fts in master DB
        c.execute("DELETE FROM unified_search_fts WHERE domain = 'New Grad 2026'")
        for item in active_listings:
            locs = "; ".join(item.get("locations", [])) if isinstance(item.get("locations"), list) else str(item.get("locations", ""))
            content = f"{item.get('company_name', '')} {item.get('title', '')} {item.get('category', '')} {locs} {item.get('sponsorship', '')} {item.get('url', '')}"
            c.execute("""
                INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
                VALUES (?, ?, ?, ?, ?)
            """, (
                "New Grad 2026",
                item.get("id", ""),
                f"{item.get('company_name', '')} - {item.get('title', '')}",
                item.get("category", "New Grad"),
                content
            ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
