#!/usr/bin/env python3
"""
ingest_frontend_challenges.py — Parse felipefialho/frontend-challenges into JSON, CSV, SQLite FTS5,
and integrate into OMEGA Master Nexus.
"""

import sys
import re
import json
import sqlite3
import csv
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

README_PATH = Path(r"e:\anti\frontend-challenges\readme.md")
OUT_JSON = Path(r"e:\anti\data\frontend_challenges.json")
OUT_CSV = Path(r"e:\anti\data\frontend_challenges.csv")
MASTER_DB = Path(r"e:\anti\data\omega_unified_master.db")
DOMAIN_DB = Path(r"e:\anti\data\frontend_challenges.db")

def parse_readme():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    challenges = []
    
    # Table pattern: | lang | Company | Stack | Challenge | Jobs on LinkedIn |
    for line in lines:
        line_str = line.strip()
        if not line_str.startswith("|") or line_str.startswith("| ----") or "Company" in line_str:
            continue
        
        parts = [p.strip() for p in line_str.split("|")]
        # After split by '|', first element is '' and last element is ''
        # [' ', 'lang', 'Company', 'Stack', 'Challenge', 'Jobs', ' ']
        filtered_parts = [p for p in parts if p != '']
        if len(filtered_parts) < 4:
            continue

        lang = filtered_parts[0].strip()
        company_raw = filtered_parts[1].strip()
        stack = filtered_parts[2].strip()
        challenge_raw = filtered_parts[3].strip()
        jobs_raw = filtered_parts[4].strip() if len(filtered_parts) > 4 else "-"

        # Extract company name & url
        company_name = company_raw
        company_url = ""
        # Handle country flags like :brazil: or 🇧🇷
        country_match = re.search(r'(:[a-z_]+:|[\U0001F1E6-\U0001F1FF]{2})', company_raw)
        country = country_match.group(0) if country_match else ""
        clean_company = re.sub(r'(:[a-z_]+:|[\U0001F1E6-\U0001F1FF]{2})', '', company_raw).strip()

        comp_link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', clean_company)
        if comp_link_match:
            company_name = comp_link_match.group(1).strip()
            company_url = comp_link_match.group(2).strip()
        else:
            company_name = clean_company.strip()

        # Extract challenge code url
        code_url = ""
        code_match = re.search(r'\((https?://[^)]+)\)', challenge_raw)
        if code_match:
            code_url = code_match.group(1).strip()

        # Extract jobs url
        jobs_url = ""
        job_match = re.search(r'\((https?://[^)]+)\)', jobs_raw)
        if job_match:
            jobs_url = job_match.group(1).strip()

        # Clean stack
        clean_stack = stack.replace("&", ",").replace("  ", " ")

        challenges.append({
            "id": f"FEC-{len(challenges)+1:03d}",
            "company_name": company_name,
            "company_url": company_url,
            "country": country,
            "lang": lang,
            "stack": clean_stack,
            "challenge_url": code_url,
            "jobs_url": jobs_url
        })

    return challenges

def main():
    print("[+] Ingesting felipefialho/frontend-challenges...")
    challenges = parse_readme()
    print(f"[+] Total frontend challenges parsed: {len(challenges)}")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(challenges, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved JSON to {OUT_JSON}")

    fieldnames = ["id", "company_name", "company_url", "country", "lang", "stack", "challenge_url", "jobs_url"]
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(challenges)
    print(f"[+] Saved CSV to {OUT_CSV}")

    # Build Standalone DB
    conn_domain = sqlite3.connect(str(DOMAIN_DB))
    c_d = conn_domain.cursor()
    c_d.execute("""
        CREATE TABLE IF NOT EXISTS frontend_challenges (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            company_url TEXT,
            country TEXT,
            lang TEXT,
            stack TEXT,
            challenge_url TEXT,
            jobs_url TEXT
        )
    """)
    for c in challenges:
        c_d.execute("""
            INSERT OR REPLACE INTO frontend_challenges VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (c["id"], c["company_name"], c["company_url"], c["country"], c["lang"], c["stack"], c["challenge_url"], c["jobs_url"]))
    
    c_d.execute("DROP TABLE IF EXISTS frontend_challenges_fts")
    c_d.execute("""
        CREATE VIRTUAL TABLE frontend_challenges_fts USING fts5(
            id, company_name, country, lang, stack, challenge_url
        )
    """)
    c_d.execute("""
        INSERT INTO frontend_challenges_fts
        SELECT id, company_name, country, lang, stack, challenge_url FROM frontend_challenges
    """)
    conn_domain.commit()
    conn_domain.close()

    # Integrate into OMEGA Master Unified DB
    conn_m = sqlite3.connect(str(MASTER_DB))
    c_m = conn_m.cursor()
    c_m.execute("""
        CREATE TABLE IF NOT EXISTS frontend_challenges (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            company_url TEXT,
            country TEXT,
            lang TEXT,
            stack TEXT,
            challenge_url TEXT,
            jobs_url TEXT
        )
    """)
    for c in challenges:
        c_m.execute("""
            INSERT OR REPLACE INTO frontend_challenges VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (c["id"], c["company_name"], c["company_url"], c["country"], c["lang"], c["stack"], c["challenge_url"], c["jobs_url"]))

    c_m.execute("DELETE FROM unified_search_fts WHERE domain = 'Frontend Challenges'")
    for c in challenges:
        content = f"{c['company_name']} {c['stack']} {c['country']} {c['lang']} {c['challenge_url']}"
        c_m.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "Frontend Challenges",
            c["id"],
            f"{c['company_name']} Frontend Coding Challenge",
            c["stack"][:30],
            content
        ))
    conn_m.commit()
    conn_m.close()
    print("[+] Master SQLite FTS5 database updated with Frontend Challenges successfully.")

if __name__ == "__main__":
    main()
