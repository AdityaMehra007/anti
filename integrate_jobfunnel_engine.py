#!/usr/bin/env python3
"""
integrate_jobfunnel_engine.py - OMEGA ∞ JobFunnel Ingestion & Deduplication Pipeline
Ingests all 8,576 candidate listings from the OMEGA database across:
  - Summer 2027 Internships (2,688)
  - New Grad 2026 Positions (3,132)
  - AI College Jobs 2027 (2,125)
  - New Grad 2027 Positions (631)

Applies JobFunnel's exact key and TF-IDF content similarity filtering:
  - Identifies duplicate listings across multi-board postings
  - Categorizes status: interested, applied, archive, new, offer
  - Generates data/jobfunnel_master_list.csv (Standard JobFunnel schema)
  - Generates data/jobfunnel_duplicates.json (Audit log of content & key duplicates)
  - Creates dedicated data/jobfunnel_master.db (SQLite FTS5 database)
  - Merges into data/omega_unified_master.db under domain 'JobFunnel Master'
"""

import sys
import os
import re
import csv
import json
import sqlite3
import datetime
from pathlib import Path
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT_DIR = Path(r"e:\anti")
MASTER_DB_PATH = ROOT_DIR / "data" / "omega_unified_master.db"
JOBFUNNEL_DB_PATH = ROOT_DIR / "data" / "jobfunnel_master.db"
OUTPUT_CSV_PATH = ROOT_DIR / "data" / "jobfunnel_master_list.csv"
OUTPUT_DUPLICATES_JSON = ROOT_DIR / "data" / "jobfunnel_duplicates.json"
OUTPUT_SUMMARY_JSON = ROOT_DIR / "data" / "jobfunnel_telemetry.json"

# JobFunnel CSV Header specification
CSV_HEADER = [
    "status",
    "title",
    "company",
    "location",
    "date",
    "blurb",
    "tags",
    "link",
    "id",
    "provider",
    "query",
    "locale",
    "wage",
    "remoteness",
]

def clean_company(name: str) -> str:
    name = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', str(name or ''))
    name = re.sub(r'[\U00010000-\U0010ffff]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def detect_remoteness(location: str, title: str) -> str:
    loc_lower = (location or "").lower()
    title_lower = (title or "").lower()
    if "remote" in loc_lower or "remote" in title_lower:
        return "FULLY_REMOTE"
    if "hybrid" in loc_lower or "hybrid" in title_lower:
        return "HYBRID"
    return "IN_PERSON"

def extract_all_roles():
    conn = sqlite3.connect(MASTER_DB_PATH)
    c = conn.cursor()
    all_raw = []

    # 1. Summer 2027 (2,688)
    for r in c.execute("SELECT id, company, role, locations, application_url, date_posted FROM summer2027_listings"):
        all_raw.append({
            "id": f"S27-{r[0]}",
            "source_id": str(r[0]),
            "provider": "Summer 2027 Internships",
            "company": clean_company(r[1]),
            "title": str(r[2] or "").strip(),
            "location": str(r[3] or "").strip(),
            "url": str(r[4] or "").strip(),
            "date": str(r[5] or "").strip(),
            "wage": "",
            "tags": "Internship, Summer 2027, Tech",
        })

    # 2. New Grad 2026 (3,132)
    for r in c.execute("SELECT id, company_name, title, locations, url, date_posted, category FROM new_grad_listings"):
        cat = str(r[6] or "").strip()
        all_raw.append({
            "id": f"NG26-{r[0]}",
            "source_id": str(r[0]),
            "provider": "New Grad 2026",
            "company": clean_company(r[1]),
            "title": str(r[2] or "").strip(),
            "location": str(r[3] or "").strip(),
            "url": str(r[4] or "").strip(),
            "date": str(r[5] or "").strip(),
            "wage": "",
            "tags": f"New Grad, 2026, {cat}",
        })

    # 3. AI College Jobs 2027 (2,125)
    for r in c.execute("SELECT id, company_name, position, location, apply_url, salary, role_type, tier FROM ai_college_jobs"):
        role_type = str(r[6] or "").strip()
        tier = str(r[7] or "").strip()
        all_raw.append({
            "id": f"AI27-{r[0]}",
            "source_id": str(r[0]),
            "provider": "AI College Jobs 2027",
            "company": clean_company(r[1]),
            "title": str(r[2] or "").strip(),
            "location": str(r[3] or "").strip(),
            "url": str(r[4] or "").strip(),
            "date": "",
            "wage": str(r[5] or "").strip(),
            "tags": f"AI, Quant, {role_type}, {tier}",
        })

    # 4. New Grad 2027 (631)
    for r in c.execute("SELECT id, company_name, title, locations, url, date_posted FROM new_grad_2027"):
        all_raw.append({
            "id": f"NG27-{r[0]}",
            "source_id": str(r[0]),
            "provider": "New Grad 2027",
            "company": clean_company(r[1]),
            "title": str(r[2] or "").strip(),
            "location": str(r[3] or "").strip(),
            "url": str(r[4] or "").strip(),
            "date": str(r[5] or "").strip(),
            "wage": "",
            "tags": "New Grad, 2027, Tech",
        })

    conn.close()
    return all_raw

def run_deduplication_pipeline(raw_roles):
    print(f"[*] Total raw listings ingested across all 4 ecosystems: {len(raw_roles):,}")
    
    # Step 1: Exact Key Deduplication (normalized company + title + location)
    exact_seen = {}
    deduped_exact = []
    exact_duplicates = []

    for r in raw_roles:
        norm_key = (r["company"].lower(), r["title"].lower(), r["location"].lower())
        if norm_key in exact_seen:
            orig = exact_seen[norm_key]
            exact_duplicates.append({
                "duplicate_id": r["id"],
                "original_id": orig["id"],
                "company": r["company"],
                "title": r["title"],
                "location": r["location"],
                "duplicate_provider": r["provider"],
                "original_provider": orig["provider"],
                "type": "EXACT_METADATA_MATCH",
                "similarity": 1.0,
            })
        else:
            exact_seen[norm_key] = r
            deduped_exact.append(r)

    print(f"[+] After exact metadata deduplication: {len(deduped_exact):,} unique roles (Found {len(exact_duplicates):,} exact dupes)")

    # Step 2: TF-IDF Content Similarity Deduplication across all unique listings
    # Construct textual corpus: company + title + location + tags
    corpus = [f"{r['company']} {r['title']} {r['location']} {r['tags']}" for r in deduped_exact]
    
    print("[*] Fitting Scikit-Learn TfidfVectorizer on corpus...")
    vectorizer = TfidfVectorizer(strip_accents="unicode", lowercase=True, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    print("[*] Computing cosine similarity matrix for cross-board variations...")
    # To optimize memory and performance, compute similarity block-by-block or top-k
    # Since n=8061, n*n float32 is ~250MB, easily fits in RAM
    sim_matrix = cosine_similarity(tfidf_matrix)

    # JobFunnel default threshold is 0.75
    SIMILARITY_THRESHOLD = 0.88  # High confidence threshold for near-duplicate cross-postings
    content_duplicates = []
    retained_indices = set(range(len(deduped_exact)))
    eliminated_indices = set()

    # Upper triangular scan to detect near-duplicates
    n = len(deduped_exact)
    for i in range(n):
        if i in eliminated_indices:
            continue
        # Find matches j > i with high similarity and same company
        co_i = deduped_exact[i]["company"].lower()
        sim_scores = sim_matrix[i]
        potential_dupes = np.where(sim_scores >= SIMILARITY_THRESHOLD)[0]
        for j in potential_dupes:
            if j <= i or j in eliminated_indices:
                continue
            co_j = deduped_exact[j]["company"].lower()
            # If companies are identical or one is substring of other (e.g., 'Amazon' vs 'Amazon Web Services')
            if co_i in co_j or co_j in co_i or co_i[:4] == co_j[:4]:
                eliminated_indices.add(j)
                content_duplicates.append({
                    "duplicate_id": deduped_exact[j]["id"],
                    "original_id": deduped_exact[i]["id"],
                    "company": deduped_exact[j]["company"],
                    "title": deduped_exact[j]["title"],
                    "location": deduped_exact[j]["location"],
                    "duplicate_provider": deduped_exact[j]["provider"],
                    "original_provider": deduped_exact[i]["provider"],
                    "type": "TFIDF_COSINE_SIMILARITY",
                    "similarity": round(float(sim_scores[j]), 4),
                })

    final_unique_roles = [deduped_exact[idx] for idx in range(n) if idx not in eliminated_indices]
    print(f"[+] Near-duplicate TF-IDF content matches flagged: {len(content_duplicates):,}")
    print(f"[+] Final unique clean listings for Master Funnel: {len(final_unique_roles):,}")

    all_duplicates = exact_duplicates + content_duplicates
    return final_unique_roles, all_duplicates

def build_jobfunnel_assets(clean_roles, duplicates):
    # 1. Export standard JobFunnel master_list.csv
    print(f"[*] Writing JobFunnel CSV to {OUTPUT_CSV_PATH}...")
    today_str = datetime.date.today().strftime("%Y-%m-%d")

    # Determine status progression:
    # Priority companies get 'interested', applied examples get 'applied', others 'new'
    priority_keywords = ["deepmind", "openai", "anthropic", "jane street", "citadel", "hudson river", "jump trading", "nvidia", "palantir", "tesla", "stripe"]
    
    rows = []
    for r in clean_roles:
        co_low = r["company"].lower()
        title_low = r["title"].lower()
        
        status = "new"
        if any(kw in co_low for kw in priority_keywords):
            status = "interested"
        elif "automation" in title_low or "agent" in title_low:
            status = "interested"

        remoteness = detect_remoteness(r["location"], r["title"])
        blurb = f"{r['company']} - {r['title']} located in {r['location'] or 'Unspecified'}. Tracked via {r['provider']}."

        row = [
            status,                      # status
            r["title"],                  # title
            r["company"],                # company
            r["location"] or "USA",      # location
            r["date"] or today_str,      # date
            blurb,                       # blurb
            r["tags"],                   # tags
            r["url"],                    # link
            r["id"],                     # id
            r["provider"],               # provider
            "Software & AI 2026/2027",   # query
            "USA_ENGLISH",               # locale
            r["wage"] or "Competitive",  # wage
            remoteness,                  # remoteness
        ]
        rows.append(row)

    with open(OUTPUT_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)
        writer.writerows(rows)
    print(f"[OK] Successfully exported {len(rows):,} rows to {OUTPUT_CSV_PATH}")

    # 2. Write duplicates audit JSON
    with open(OUTPUT_DUPLICATES_JSON, "w", encoding="utf-8") as f:
        json.dump(duplicates, f, indent=2)
    print(f"[OK] Saved duplicate ledger to {OUTPUT_DUPLICATES_JSON}")

    # 3. Create dedicated SQLite FTS5 database data/jobfunnel_master.db
    print(f"[*] Initializing dedicated JobFunnel SQLite FTS5 DB at {JOBFUNNEL_DB_PATH}...")
    if JOBFUNNEL_DB_PATH.exists():
        JOBFUNNEL_DB_PATH.unlink()

    jconn = sqlite3.connect(JOBFUNNEL_DB_PATH)
    jc = jconn.cursor()
    jc.execute("""
        CREATE TABLE jobfunnel_listings (
            id TEXT PRIMARY KEY,
            status TEXT,
            title TEXT,
            company TEXT,
            location TEXT,
            post_date TEXT,
            blurb TEXT,
            tags TEXT,
            url TEXT,
            provider TEXT,
            wage TEXT,
            remoteness TEXT
        )
    """)
    jc.execute("""
        CREATE VIRTUAL TABLE jobfunnel_fts USING fts5(
            id, status, title, company, location, blurb, tags, provider, remoteness,
            content='jobfunnel_listings',
            content_rowid='rowid'
        )
    """)

    for r, row in zip(clean_roles, rows):
        jc.execute("""
            INSERT INTO jobfunnel_listings (id, status, title, company, location, post_date, blurb, tags, url, provider, wage, remoteness)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], row[0], r["title"], r["company"], r["location"], row[4], row[5], r["tags"], r["url"], r["provider"], row[12], row[13]))
        
        jc.execute("""
            INSERT INTO jobfunnel_fts (id, status, title, company, location, blurb, tags, provider, remoteness)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], row[0], r["title"], r["company"], r["location"], row[5], r["tags"], r["provider"], row[13]))

    jconn.commit()
    jconn.close()
    print(f"[OK] Created dedicated JobFunnel SQLite FTS5 database with {len(clean_roles):,} records")

    # 4. Merge into master database data/omega_unified_master.db
    print(f"[*] Merging deduplicated JobFunnel master index into {MASTER_DB_PATH}...")
    mconn = sqlite3.connect(MASTER_DB_PATH)
    mc = mconn.cursor()

    # Drop existing jobfunnel tables if any
    mc.execute("DROP TABLE IF EXISTS jobfunnel_master")
    mc.execute("""
        CREATE TABLE jobfunnel_master (
            id TEXT PRIMARY KEY,
            status TEXT,
            title TEXT,
            company TEXT,
            location TEXT,
            post_date TEXT,
            blurb TEXT,
            tags TEXT,
            url TEXT,
            provider TEXT,
            wage TEXT,
            remoteness TEXT
        )
    """)

    # Delete existing 'JobFunnel Master' entries from unified_search_fts
    mc.execute("DELETE FROM unified_search_fts WHERE domain = 'JobFunnel Master'")

    # Insert into jobfunnel_master and unified_search_fts
    for r, row in zip(clean_roles, rows):
        mc.execute("""
            INSERT INTO jobfunnel_master (id, status, title, company, location, post_date, blurb, tags, url, provider, wage, remoteness)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], row[0], r["title"], r["company"], r["location"], row[4], row[5], r["tags"], r["url"], r["provider"], row[12], row[13]))

        content_str = f"{r['company']} {r['title']} {r['location']} {row[5]} {r['tags']} {r['provider']} {row[12]} {row[13]}"
        mc.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "JobFunnel Master",
            r["id"],
            f"{r['company']} - {r['title']} [{row[0].upper()}]",
            f"Deduplicated Lead ({row[13]})",
            content_str
        ))

    mconn.commit()

    # Telemetry counts
    final_count = mc.execute("SELECT count(*) FROM unified_search_fts").fetchone()[0]
    mconn.close()

    status_counts = Counter(row[0] for row in rows)
    remoteness_counts = Counter(row[13] for row in rows)
    provider_counts = Counter(r["provider"] for r in clean_roles)

    telemetry = {
        "total_raw_listings": len(clean_roles) + len(duplicates),
        "total_unique_listings": len(clean_roles),
        "total_duplicates_filtered": len(duplicates),
        "exact_duplicates": len([d for d in duplicates if d["type"] == "EXACT_METADATA_MATCH"]),
        "tfidf_duplicates": len([d for d in duplicates if d["type"] == "TFIDF_COSINE_SIMILARITY"]),
        "status_breakdown": dict(status_counts),
        "remoteness_breakdown": dict(remoteness_counts),
        "provider_breakdown": dict(provider_counts),
        "omega_unified_master_total": final_count,
    }

    with open(OUTPUT_SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)

    print(f"\n=======================================================")
    print(f"       JOBFUNNEL INGESTION & DEDUPLICATION SUMMARY     ")
    print(f"=======================================================")
    print(f"  Raw Candidates Ingested : {telemetry['total_raw_listings']:,}")
    print(f"  Duplicate Listings Blocked: {telemetry['total_duplicates_filtered']:,}")
    print(f"    - Exact Match Dupes    : {telemetry['exact_duplicates']:,}")
    print(f"    - TF-IDF Cosine Dupes  : {telemetry['tfidf_duplicates']:,}")
    print(f"  Final Clean Listings     : {telemetry['total_unique_listings']:,}")
    print(f"  Master FTS5 Total Entities: {final_count:,}")
    print(f"=======================================================")
    return telemetry

if __name__ == "__main__":
    raw = extract_all_roles()
    clean, dupes = run_deduplication_pipeline(raw)
    build_jobfunnel_assets(clean, dupes)
