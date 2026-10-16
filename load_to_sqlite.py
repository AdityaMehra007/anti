#!/usr/bin/env python3
"""
Loads the complete SimplifyJobs Summer 2027 Internship dataset (17,186 listings)
and the 2027 active cohort into a high-performance SQLite database with Full-Text Search (FTS5).
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

DB_PATH = Path(r"e:\anti\data\summer2027.db")
JSON_PATH = Path(r"e:\anti\Summer2027-Internships\.github\scripts\listings.json")

def load_database():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    if DB_PATH.exists():
        try:
            DB_PATH.unlink()
        except Exception:
            pass

    print(f"[+] Loading dataset from {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        listings = json.load(f)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 1. Main Listings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        id TEXT PRIMARY KEY,
        company_name TEXT,
        title TEXT,
        category TEXT,
        locations TEXT,
        terms TEXT,
        active INTEGER,
        is_visible INTEGER,
        is_remote INTEGER,
        sponsorship TEXT,
        degrees TEXT,
        tier TEXT,
        date_posted TEXT,
        date_updated TEXT,
        apply_url TEXT,
        simplify_url TEXT,
        company_url TEXT,
        source TEXT
    )
    """)

    # 2. FTS5 Full Text Search Table
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS listings_fts USING fts5(
        id UNINDEXED,
        company_name,
        title,
        category,
        locations,
        terms,
        sponsorship,
        degrees,
        content=listings,
        content_rowid=rowid
    )
    """)

    # 3. Summer 2027 Active Cohort Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summer_2027_active (
        id TEXT PRIMARY KEY,
        company_name TEXT,
        title TEXT,
        category TEXT,
        locations TEXT,
        is_remote INTEGER,
        sponsorship TEXT,
        degrees TEXT,
        tier TEXT,
        apply_url TEXT,
        simplify_url TEXT
    )
    """)

    # 4. Target Application Dossiers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS application_dossiers (
        id TEXT PRIMARY KEY,
        company_name TEXT,
        target_role TEXT,
        compensation TEXT,
        location TEXT,
        recruiter TEXT,
        contact_email TEXT,
        status TEXT,
        resume_pdf TEXT,
        cover_letter_pdf TEXT
    )
    """)

    def clean_category(cat: str) -> str:
        if not cat: return "Software"
        cat_lower = cat.lower()
        if "ai" in cat_lower or "ml" in cat_lower or "data" in cat_lower: return "AI/ML/Data"
        if "quant" in cat_lower: return "Quant"
        if "hardware" in cat_lower: return "Hardware"
        if "product" in cat_lower: return "Product"
        if "software" in cat_lower: return "Software"
        return cat

    def determine_tier(company: str, category: str) -> str:
        tier_1 = {
            "Google", "Alphabet", "Meta", "Apple", "Microsoft", "Amazon", "Netflix", "NVIDIA",
            "OpenAI", "Anthropic", "Tesla", "ByteDance", "TikTok", "Uber", "Airbnb", "Stripe",
            "Databricks", "Snowflake", "Palantir", "Salesforce", "Adobe", "Oracle", "Cisco",
            "Jane Street", "Citadel", "Citadel Securities", "Hudson River Trading", "Two Sigma",
            "Jump Trading", "DRW", "Optiver", "SIG", "Susquehanna", "DE Shaw", "D. E. Shaw",
            "Point72", "Five Rings", "Radix Trading", "Valkyrie Trading", "Goldman Sachs",
            "Morgan Stanley", "JPMorgan Chase", "Bank of America", "Royal Bank of Canada",
            "AMD", "Intel", "Qualcomm", "Broadcom", "Marvell", "ASML", "Arm", "Waymo"
        }
        if category == "Quant" or company in {"Jane Street", "Citadel", "Hudson River Trading", "Two Sigma", "Jump Trading"}:
            return "Quant / Prop Trading"
        if company in tier_1:
            return "Tier 1 / Big Tech"
        return "Enterprise / High Growth"

    def format_date(timestamp) -> str:
        if not timestamp: return "Recent"
        try:
            return datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d")
        except Exception:
            return "Recent"

    rows_listings = []
    rows_active2027 = []

    for l in listings:
        lid = l.get("id", "")
        company = l.get("company_name", "Unknown").strip()
        title = l.get("title", "Intern").strip()
        cat = clean_category(l.get("category", "Software"))
        locs = l.get("locations", [])
        if isinstance(locs, str): locs = [locs]
        loc_str = ", ".join(locs) if locs else "United States"
        terms = l.get("terms", [])
        terms_str = ", ".join(terms) if terms else "N/A"
        active = 1 if l.get("active") else 0
        visible = 1 if l.get("is_visible", True) else 0
        remote = 1 if any("remote" in str(x).lower() for x in locs) or "remote" in title.lower() else 0
        spons = l.get("sponsorship", "Other")
        degs = l.get("degrees", [])
        degs_str = ", ".join(degs) if degs else "Any"
        tier = determine_tier(company, cat)
        dt_post = format_date(l.get("date_posted"))
        dt_upd = format_date(l.get("date_updated"))
        url = l.get("url", "")
        sim_url = f"https://simplify.jobs/p/{lid}" if lid else ""
        c_url = l.get("company_url", "")
        src = l.get("source", "Simplify")

        rows_listings.append((
            lid, company, title, cat, loc_str, terms_str, active, visible, remote,
            spons, degs_str, tier, dt_post, dt_upd, url, sim_url, c_url, src
        ))

        if active and visible and any("2027" in t for t in terms):
            rows_active2027.append((
                lid, company, title, cat, loc_str, remote, spons, degs_str, tier, url, sim_url
            ))

    cursor.executemany("""
    INSERT OR REPLACE INTO listings VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, rows_listings)

    cursor.execute("""
    INSERT INTO listings_fts(listings_fts) VALUES('rebuild')
    """)

    cursor.executemany("""
    INSERT OR REPLACE INTO summer_2027_active VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, rows_active2027)

    # Insert Application Dossiers
    dossiers = [
        ("APX-2027-001", "Tesla", "Data Analyst Intern - People Products", "$45 - $60/hr", "Palo Alto / Austin", "Tesla University Talent", "universityrecruiting@tesla.com", "READY", "APX-2027-001_Tesla_Resume.pdf", "APX-2027-001_Tesla_Cover_Letter.pdf"),
        ("APX-2027-002", "TikTok / ByteDance", "AI Governance Strategy PM Intern", "$55 - $72/hr", "San Jose, CA", "TikTok University Relations", "campus-us@tiktok.com", "READY", "APX-2027-002_TikTok___ByteDance_Resume.pdf", "APX-2027-002_TikTok___ByteDance_Cover_Letter.pdf"),
        ("APX-2027-003", "Rivian", "Supply Chain Data & AI Co-op Intern", "$42 - $55/hr", "Normal, IL", "Rivian Campus Recruiting", "talent@rivian.com", "READY", "APX-2027-003_Rivian_Resume.pdf", "APX-2027-003_Rivian_Cover_Letter.pdf"),
        ("APX-2027-004", "Intuit", "Business Data Analyst Intern", "$48 - $62/hr", "Mountain View, CA", "Intuit Campus Recruiting", "university_recruiting@intuit.com", "READY", "APX-2027-004_Intuit_Resume.pdf", "APX-2027-004_Intuit_Cover_Letter.pdf"),
        ("APX-2027-005", "TikTok", "Product Operations Intern - Apps & API", "$50 - $65/hr", "Seattle, WA", "TikTok Developer Platform", "developer-campus@tiktok.com", "READY", "APX-2027-005_TikTok_Resume.pdf", "APX-2027-005_TikTok_Cover_Letter.pdf"),
        ("APX-2027-006", "Tesla", "Software Engineer Intern - Automation", "$50 - $68/hr", "Palo Alto, CA", "Tesla Engineering Recruiting", "engineeringrecruiting@tesla.com", "READY", "APX-2027-006_Tesla_Resume.pdf", "APX-2027-006_Tesla_Cover_Letter.pdf"),
        ("APX-2027-007", "Quantbot Technologies", "Data Trading Analyst Intern", "$55 - $75/hr", "New York, NY", "Quantbot University Talent", "careers@quantbot.com", "READY", "APX-2027-007_Quantbot_Technologies_Resume.pdf", "APX-2027-007_Quantbot_Technologies_Cover_Letter.pdf"),
        ("APX-2027-008", "American Express", "Product Manager / Business Analyst Intern", "$45 - $58/hr", "New York, NY", "Amex Campus Talent", "campusrecruiting@aexp.com", "READY", "APX-2027-008_American_Express_Resume.pdf", "APX-2027-008_American_Express_Cover_Letter.pdf"),
        ("APX-2027-009", "Waymo", "Autonomous Fleet Operations Analyst", "$48 - $64/hr", "Mountain View, CA", "Waymo Campus Talent", "waymo-campus@google.com", "READY", "APX-2027-009_Waymo_(Alphabet)_Resume.pdf", "APX-2027-009_Waymo_(Alphabet)_Cover_Letter.pdf"),
        ("APX-2027-010", "AMD", "Global Supply Chain Operations Intern", "$44 - $56/hr", "Austin, TX", "AMD University Relations", "university.relations@amd.com", "READY", "APX-2027-010_AMD_(Advanced_Micro_Devices)_Resume.pdf", "APX-2027-010_AMD_(Advanced_Micro_Devices)_Cover_Letter.pdf")
    ]

    cursor.executemany("""
    INSERT OR REPLACE INTO application_dossiers VALUES (?,?,?,?,?,?,?,?,?,?)
    """, dossiers)

    conn.commit()

    # Query statistics
    total = cursor.execute("SELECT count(*) FROM listings").fetchone()[0]
    total_active2027 = cursor.execute("SELECT count(*) FROM summer_2027_active").fetchone()[0]
    dossier_count = cursor.execute("SELECT count(*) FROM application_dossiers").fetchone()[0]
    conn.close()

    print(f"[✓] Database successfully populated at {DB_PATH}!")
    print(f"    - Total Listings Indexed: {total:,}")
    print(f"    - Summer 2027 Active Roles: {total_active2027:,}")
    print(f"    - Loaded Application Dossiers: {dossier_count}")

if __name__ == "__main__":
    load_database()
