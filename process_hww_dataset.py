import os
import json
import re
import csv
import sqlite3

readme_path = r"e:\anti\hiring-without-whiteboards\README.md"
companies = []

with open(readme_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

current_section = ""

for line in lines:
    line_s = line.strip()
    if line_s.startswith("## "):
        current_section = line_s.replace("## ", "").strip()
        continue
    
    # Format: - [Name](url) | Location | Process description
    if line_s.startswith("- [") and "](" in line_s:
        # Regex match: - \[([^\]]+)\]\(([^)]+)\)\s*(?:\|\s*([^|]+))?(?:\|\s*(.*))?
        m = re.match(r"^-\s*\[([^\]]+)\]\(([^)]+)\)\s*(?:\|\s*([^|]+))?(?:\|\s*(.*))?", line_s)
        if m:
            name = m.group(1).strip()
            url = m.group(2).strip()
            location = m.group(3).strip() if m.group(3) else "Unspecified"
            process = m.group(4).strip() if m.group(4) else ""
            
            # Extract tags / interview styles
            styles = []
            p_lower = (process + " " + location).lower()
            if "take home" in p_lower or "take-home" in p_lower or "takehome" in p_lower or "project" in p_lower or "assignment" in p_lower:
                styles.append("Take-Home Project")
            if "pair" in p_lower or "pairing" in p_lower:
                styles.append("Pair Programming")
            if "system design" in p_lower or "architecture" in p_lower or "design" in p_lower:
                styles.append("System Design")
            if "remote" in p_lower:
                styles.append("Remote Friendly")
            if "real world" in p_lower or "real-world" in p_lower:
                styles.append("Real-World Task")
            if not styles:
                styles.append("Discussion & Code Review")

            is_remote = "remote" in location.lower() or "remote" in p_lower
            is_india = any(k in location.lower() for k in ["india", "bangalore", "mumbai", "delhi", "hyderabad", "pune", "gurgaon", "noida"])
            is_us = any(k in location.lower() for k in ["usa", "ca", "ny", "tx", "wa", "remote", "san francisco", "new york", "austin"])

            companies.append({
                "name": name,
                "url": url,
                "location": location,
                "process": process,
                "styles": styles,
                "is_remote": is_remote,
                "is_india": is_india,
                "section": current_section
            })

print(f"Extracted {len(companies)} companies from hiring-without-whiteboards README!")

# 1. Save JSON
json_out = r"e:\anti\data\hiring_without_whiteboards.json"
with open(json_out, "w", encoding="utf-8") as f:
    json.dump(companies, f, indent=2)

# 2. Save CSV
csv_out = r"e:\anti\data\hiring_without_whiteboards.csv"
with open(csv_out, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "url", "location", "process", "styles", "is_remote", "is_india", "section"])
    writer.writeheader()
    for c in companies:
        row = c.copy()
        row["styles"] = ", ".join(row["styles"])
        writer.writerow(row)

# 3. Save into omega_unified_master.db
db_path = r"e:\anti\data\omega_unified_master.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS hww_companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    url TEXT,
    location TEXT,
    interview_process TEXT,
    styles_json TEXT,
    is_remote INTEGER,
    is_india INTEGER,
    section TEXT
)
""")

for c in companies:
    cur.execute("""
        INSERT OR REPLACE INTO hww_companies (name, url, location, interview_process, styles_json, is_remote, is_india, section)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (c["name"], c["url"], c["location"], c["process"], json.dumps(c["styles"]), 1 if c["is_remote"] else 0, 1 if c["is_india"] else 0, c["section"]))

    # Index into unified_search_fts
    cur.execute("""
        INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
        VALUES (?, ?, ?, ?, ?)
    """, ("Hiring No-Whiteboard", f"HWW-{c['name']}", c["name"], "Interview Guide", f"{c['name']} {c['location']} {c['process']} {' '.join(c['styles'])}"))

conn.commit()

cur.execute("SELECT COUNT(*) FROM hww_companies")
print("Total HWW Companies in DB:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM unified_search_fts")
print("Total Unified Master FTS5 Entities:", cur.fetchone()[0])

conn.close()
