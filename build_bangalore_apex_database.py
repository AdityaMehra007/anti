#!/usr/bin/env python3
"""
BANGALORE APEX GLOBAL CAREER DATABASE BUILDER
Consolidates all Bengaluru datasets into a single, high-performance,
indexed SQLite database with Full-Text Search (FTS5).
"""
import os
import csv
import json
import sqlite3
from pathlib import Path

ROOT = Path(r"e:\anti")
DB_PATH = ROOT / "BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"

def init_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    
    # 1. Tech Parks
    cur.execute("""
    CREATE TABLE tech_parks (
        id TEXT PRIMARY KEY,
        name TEXT,
        zone TEXT,
        corridor TEXT,
        address TEXT,
        nearest_metro TEXT,
        transit_friction_index INTEGER,
        campus_area_sqft TEXT
    )
    """)
    
    # 2. Top Funded Startups & Global MNCs
    cur.execute("""
    CREATE TABLE top_employers (
        id TEXT PRIMARY KEY,
        company_name TEXT,
        category TEXT,
        country_of_origin TEXT,
        funding_scale TEXT,
        location TEXT,
        target_role TEXT,
        experience_level TEXT,
        base_salary_lpa TEXT,
        total_ctc_lpa TEXT,
        est_monthly_inhand TEXT,
        hr_contact TEXT,
        hr_email TEXT,
        phone TEXT,
        careers_url TEXT,
        strategic_fit TEXT
    )
    """)
    
    # 3. Staffing & Executive Placement Agencies
    cur.execute("""
    CREATE TABLE placement_agencies (
        agency_id TEXT PRIMARY KEY,
        agency_name TEXT,
        tier_category TEXT,
        location_hub TEXT,
        specializations TEXT,
        candidate_portal TEXT,
        email TEXT,
        phone TEXT,
        pitch_summary TEXT
    )
    """)
    
    # 4. Master HR Directory (7,500 contacts)
    cur.execute("""
    CREATE TABLE master_hr_contacts (
        contact_id TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        corridor TEXT,
        hr_name TEXT,
        designation TEXT,
        contact_category TEXT,
        phone TEXT,
        email TEXT,
        recruitment_desk_email TEXT,
        linkedin_url TEXT,
        target_track TEXT,
        pitch_angle TEXT,
        verification_status TEXT
    )
    """)
    
    # 5. Founder & Company Gaps (4,500 companies)
    cur.execute("""
    CREATE TABLE company_founder_gaps (
        id TEXT PRIMARY KEY,
        company TEXT,
        sector TEXT,
        corridor TEXT,
        founder_ceo_name TEXT,
        founder_ceo_title TEXT,
        hr_name TEXT,
        hr_designation TEXT,
        hr_email TEXT,
        careers_email TEXT,
        hr_phone TEXT,
        linkedin_search_url TEXT,
        identified_company_gap TEXT,
        candidate_solution TEXT,
        pitch_angle TEXT,
        fit_score INTEGER,
        status TEXT
    )
    """)
    
    conn.commit()
    return conn

def populate():
    conn = init_db()
    cur = conn.cursor()
    print("Database schema created. Ingesting datasets...")
    
    # Ingest Tech Parks
    tp_file = ROOT / "data" / "bangalore_tech_parks_master.json"
    if tp_file.exists():
        with open(tp_file, "r", encoding="utf-8") as f:
            tps = json.load(f)
            for tp in tps:
                cur.execute("""
                INSERT OR REPLACE INTO tech_parks VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    tp.get("id"),
                    tp.get("name"),
                    tp.get("zone"),
                    tp.get("corridor"),
                    tp.get("address"),
                    tp.get("nearest_metro"),
                    tp.get("transit_friction_index"),
                    tp.get("campus_area_sqft")
                ))
        print(f"-> Ingested {len(tps)} Tech Parks.")
        
    # Ingest Top Employers
    emp_file = ROOT / "BANGALORE_FUNDED_STARTUPS_AND_GLOBAL_MNCS_MASTER.csv"
    if emp_file.exists():
        with open(emp_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for r in reader:
                cur.execute("""
                INSERT OR REPLACE INTO top_employers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r.get("ID"),
                    r.get("Company Name"),
                    r.get("Category"),
                    r.get("Country of Origin"),
                    r.get("Funding Status / Scale"),
                    r.get("Bangalore Corridor / Location"),
                    r.get("Target Role (Non-Sales)"),
                    r.get("Experience Level"),
                    r.get("Fixed Base (LPA)"),
                    r.get("Total CTC Range (LPA)"),
                    r.get("Est Monthly In-Hand (INR)"),
                    r.get("HR / TA Contact"),
                    r.get("HR Direct Email"),
                    r.get("Desk / Board Phone"),
                    r.get("Direct Careers Portal URL"),
                    r.get("Strategic Fit Rationale")
                ))
                count += 1
        print(f"-> Ingested {count} Top Employers.")

    # Ingest Agencies
    agy_file = ROOT / "BANGALORE_JOB_AGENCIES_MASTER.csv"
    if agy_file.exists():
        with open(agy_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for r in reader:
                cur.execute("""
                INSERT OR REPLACE INTO placement_agencies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r.get("Agency ID"),
                    r.get("Agency Name"),
                    r.get("Tier / Category"),
                    r.get("Bangalore Location Hub"),
                    r.get("Practice Specializations"),
                    r.get("Candidate Portal URL"),
                    r.get("Agency Contact Email"),
                    r.get("Desk Phone"),
                    r.get("Pitch Summary")
                ))
                count += 1
        print(f"-> Ingested {count} Placement Agencies.")

    # Ingest Master HR Contacts (7500)
    hr_file = ROOT / "data" / "csv_exports" / "ALL_HR_NAMES_AND_NUMBERS_MASTER_DIRECTORY.csv"
    if hr_file.exists():
        with open(hr_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for r in reader:
                cur.execute("""
                INSERT OR REPLACE INTO master_hr_contacts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r.get("Contact ID"),
                    r.get("Company Name"),
                    r.get("Sector / Industry"),
                    r.get("Location / Tech Corridor"),
                    r.get("HR / Recruiter Name"),
                    r.get("Designation / Title"),
                    r.get("Contact Category"),
                    r.get("Official Desk / Board Phone"),
                    r.get("Direct HR Email"),
                    r.get("Recruitment Desk Email"),
                    r.get("LinkedIn Search / Profile URL"),
                    r.get("Target Track Alignment"),
                    r.get("Strategic Pitch Angle"),
                    r.get("Verification Status")
                ))
                count += 1
        print(f"-> Ingested {count} Master HR Contacts.")

    # Ingest Founder Gaps (4500)
    gaps_file = ROOT / "data" / "BANGALORE_HR_FOUNDER_GAPS_MASTER.csv"
    if gaps_file.exists():
        with open(gaps_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for r in reader:
                cur.execute("""
                INSERT OR REPLACE INTO company_founder_gaps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r.get("id"),
                    r.get("company"),
                    r.get("sector"),
                    r.get("corridor"),
                    r.get("founder_ceo_name"),
                    r.get("founder_ceo_title"),
                    r.get("hr_name"),
                    r.get("hr_designation"),
                    r.get("hr_email"),
                    r.get("careers_email"),
                    r.get("hr_phone"),
                    r.get("linkedin_search_url"),
                    r.get("identified_company_gap"),
                    r.get("candidate_solution"),
                    r.get("pitch_angle"),
                    int(r.get("fit_score", 90) or 90),
                    r.get("status")
                ))
                count += 1
        print(f"-> Ingested {count} Company & Founder Gaps.")

    # Create Indexes for lightning-fast queries
    cur.execute("CREATE INDEX idx_hr_company ON master_hr_contacts(company_name)")
    cur.execute("CREATE INDEX idx_hr_corridor ON master_hr_contacts(corridor)")
    cur.execute("CREATE INDEX idx_gaps_company ON company_founder_gaps(company)")
    cur.execute("CREATE INDEX idx_gaps_corridor ON company_founder_gaps(corridor)")
    cur.execute("CREATE INDEX idx_top_emp_category ON top_employers(category)")
    
    # Build FTS5 Full-Text Search Virtual Table
    cur.execute("""
    CREATE VIRTUAL TABLE master_search_fts USING fts5(
        source_table,
        entity_name,
        contact_name,
        email,
        phone,
        corridor,
        target_role,
        pitch
    )
    """)
    
    cur.execute("""
    INSERT INTO master_search_fts 
    SELECT 'top_employers', company_name, hr_contact, hr_email, phone, location, target_role, strategic_fit
    FROM top_employers
    """)
    
    cur.execute("""
    INSERT INTO master_search_fts 
    SELECT 'master_hr_contacts', company_name, hr_name, email, phone, corridor, designation, pitch_angle
    FROM master_hr_contacts
    """)
    
    cur.execute("""
    INSERT INTO master_search_fts 
    SELECT 'company_founder_gaps', company, founder_ceo_name, hr_email, hr_phone, corridor, founder_ceo_title, identified_company_gap
    FROM company_founder_gaps
    """)
    
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM master_search_fts")
    fts_count = cur.fetchone()[0]
    print(f"-> Full-Text Search (FTS5) Indexed: {fts_count} total searchable entities.")
    
    conn.close()
    print(f"Consolidated Apex Database built successfully at: {DB_PATH}")

if __name__ == "__main__":
    populate()
