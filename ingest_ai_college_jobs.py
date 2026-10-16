#!/usr/bin/env python3
"""
ingest_ai_college_jobs.py — Parse speedyapply/2027-AI-College-Jobs into JSON, CSV, and SQLite FTS5.
Combines:
  1. README.md (USA Internships)
  2. INTERN_INTL.md (International Internships)
  3. NEW_GRAD_USA.md (USA New Grad AI roles)
  4. NEW_GRAD_INTL.md (International New Grad AI roles)
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

REPO_DIR = Path(r"e:\anti\2027-AI-College-Jobs")
OUT_JSON = Path(r"e:\anti\data\ai_college_jobs_2027.json")
OUT_CSV = Path(r"e:\anti\data\ai_college_jobs_2027.csv")
MASTER_DB = Path(r"e:\anti\data\omega_unified_master.db")
DOMAIN_DB = Path(r"e:\anti\data\ai_college_jobs.db")

FILES = [
    ("README.md", "Internship", "USA"),
    ("INTERN_INTL.md", "Internship", "International"),
    ("NEW_GRAD_USA.md", "New Grad", "USA"),
    ("NEW_GRAD_INTL.md", "New Grad", "International"),
]

def parse_markdown_table(file_name, role_type, region):
    file_path = REPO_DIR / file_name
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_tier = "Other"
    jobs = []

    for line in lines:
        line_str = line.strip()
        if line_str.startswith("### "):
            current_tier = line_str.replace("### ", "").strip()
            continue
        
        if not line_str.startswith("|") or line_str.startswith("|---") or "Company" in line_str:
            continue

        parts = [p.strip() for p in line_str.split("|")]
        filtered = [p for p in parts if p != ""]
        if len(filtered) < 4:
            continue

        company_raw = filtered[0]
        position_raw = filtered[1]
        location_raw = filtered[2]
        salary_raw = filtered[3] if len(filtered) > 3 else "-"
        posting_raw = filtered[4] if len(filtered) > 4 else ""
        age_raw = filtered[5] if len(filtered) > 5 else ""

        # Extract company name & url
        comp_name = company_raw
        comp_url = ""
        # Often <a href="..."><strong>Company</strong></a>
        m_comp = re.search(r'href="([^"]+)".*?<strong>(.*?)</strong>', company_raw)
        if m_comp:
            comp_url = m_comp.group(1).strip()
            comp_name = m_comp.group(2).strip()
        else:
            # Markdown link or plain text
            m_comp_md = re.search(r'\[([^\]]+)\]\(([^)]+)\)', company_raw)
            if m_comp_md:
                comp_name = m_comp_md.group(1).strip()
                comp_url = m_comp_md.group(2).strip()
            else:
                comp_name = re.sub(r'<[^>]+>', '', company_raw).strip()

        # Extract posting apply link
        apply_url = ""
        m_app = re.search(r'href="([^"]+)"', posting_raw)
        if m_app:
            apply_url = m_app.group(1).strip()
        else:
            m_app_md = re.search(r'\((https?://[^)]+)\)', posting_raw)
            if m_app_md:
                apply_url = m_app_md.group(1).strip()

        # Clean HTML tags
        clean_pos = re.sub(r'<[^>]+>', '', position_raw).strip()
        clean_loc = re.sub(r'<[^>]+>', '', location_raw).strip()
        clean_sal = re.sub(r'<[^>]+>', '', salary_raw).strip()

        jobs.append({
            "company_name": comp_name,
            "company_url": comp_url,
            "position": clean_pos,
            "location": clean_loc,
            "salary": clean_sal,
            "apply_url": apply_url,
            "tier": current_tier,
            "role_type": role_type,
            "region": region,
            "age": age_raw
        })

    return jobs

def main():
    print("[+] Parsing 2027-AI-College-Jobs...")
    all_jobs = []
    
    for fname, rtype, reg in FILES:
        parsed = parse_markdown_table(fname, rtype, reg)
        print(f"  • {fname:16s} -> {len(parsed):4d} roles ({rtype} - {reg})")
        all_jobs.extend(parsed)

    print(f"[+] Total AI College Jobs parsed: {len(all_jobs):,d}")

    # Assign IDs
    for idx, item in enumerate(all_jobs, 1):
        item["id"] = f"AI-27-{idx:04d}"

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved JSON to {OUT_JSON}")

    fieldnames = ["id", "company_name", "position", "tier", "role_type", "region", "location", "salary", "apply_url", "company_url", "age"]
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_jobs)
    print(f"[+] Saved CSV to {OUT_CSV}")

    # Build Standalone DB
    conn_d = sqlite3.connect(str(DOMAIN_DB))
    c_d = conn_d.cursor()
    c_d.execute("""
        CREATE TABLE IF NOT EXISTS ai_college_jobs (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            position TEXT,
            tier TEXT,
            role_type TEXT,
            region TEXT,
            location TEXT,
            salary TEXT,
            apply_url TEXT,
            company_url TEXT,
            age TEXT
        )
    """)
    for j in all_jobs:
        c_d.execute("""
            INSERT OR REPLACE INTO ai_college_jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (j["id"], j["company_name"], j["position"], j["tier"], j["role_type"], j["region"], j["location"], j["salary"], j["apply_url"], j["company_url"], j["age"]))

    c_d.execute("DROP TABLE IF EXISTS ai_college_jobs_fts")
    c_d.execute("""
        CREATE VIRTUAL TABLE ai_college_jobs_fts USING fts5(
            id, company_name, position, tier, role_type, region, location, salary, apply_url
        )
    """)
    c_d.execute("""
        INSERT INTO ai_college_jobs_fts
        SELECT id, company_name, position, tier, role_type, region, location, salary, apply_url FROM ai_college_jobs
    """)
    conn_d.commit()
    conn_d.close()

    # Integrate into OMEGA Master DB
    conn_m = sqlite3.connect(str(MASTER_DB))
    c_m = conn_m.cursor()
    c_m.execute("""
        CREATE TABLE IF NOT EXISTS ai_college_jobs (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            position TEXT,
            tier TEXT,
            role_type TEXT,
            region TEXT,
            location TEXT,
            salary TEXT,
            apply_url TEXT,
            company_url TEXT,
            age TEXT
        )
    """)
    for j in all_jobs:
        c_m.execute("""
            INSERT OR REPLACE INTO ai_college_jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (j["id"], j["company_name"], j["position"], j["tier"], j["role_type"], j["region"], j["location"], j["salary"], j["apply_url"], j["company_url"], j["age"]))

    c_m.execute("DELETE FROM unified_search_fts WHERE domain = 'AI College Jobs 2027'")
    for j in all_jobs:
        content = f"{j['company_name']} {j['position']} {j['tier']} {j['role_type']} {j['region']} {j['location']} {j['salary']} {j['apply_url']}"
        c_m.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "AI College Jobs 2027",
            j["id"],
            f"{j['company_name']} - {j['position']}",
            f"{j['role_type']} ({j['tier']})",
            content
        ))
    conn_m.commit()
    conn_m.close()
    print("[+] Unified Master SQLite FTS5 database updated with AI College Jobs.")

if __name__ == "__main__":
    main()
