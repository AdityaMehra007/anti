"""
APEX BENGALURU - Database Initialization & Schema Builder
Creates the normalized relational schema for the Bengaluru City Digital Twin & Knowledge Graph.
"""
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(r"e:\anti\apex\projects\bengaluru\data\bengaluru.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_bengaluru_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Companies Table
    cur.execute('''CREATE TABLE IF NOT EXISTS companies (
        company_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL, -- GCC, MNC, STARTUP, ENTERPRISE, PSU
        sector TEXT NOT NULL,
        sub_sector TEXT,
        hq_location TEXT,
        blr_offices TEXT, -- JSON array of locations
        employee_count_blr INT,
        is_gcc BOOLEAN DEFAULT 0,
        gcc_tier TEXT, -- TIER_1, TIER_2, TIER_3
        tech_stack TEXT, -- JSON array
        hiring_status TEXT, -- HIGH, MODERATE, LOW, FREEZE
        health_score REAL,
        momentum_score REAL,
        source TEXT,
        confidence TEXT, -- OBSERVED, VERIFIED, INFERRED
        last_verified TEXT
    )''')

    # 2. Startups Table
    cur.execute('''CREATE TABLE IF NOT EXISTS startups (
        startup_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        founders TEXT,
        sector TEXT NOT NULL,
        stage TEXT NOT NULL, -- SEED, SERIES_A, SERIES_B, UNICORN, BOOTSTRAPPED
        total_funding_usd REAL,
        lead_investors TEXT,
        product_summary TEXT,
        blr_neighborhood TEXT,
        employee_count INT,
        hiring_active BOOLEAN,
        startup_momentum_score REAL,
        source TEXT,
        confidence TEXT,
        last_verified TEXT
    )''')

    # 3. GCCs Table (Global Capability Centers)
    cur.execute('''CREATE TABLE IF NOT EXISTS gccs (
        gcc_id TEXT PRIMARY KEY,
        parent_company TEXT NOT NULL,
        country_origin TEXT,
        establishment_year INT,
        blr_campus_locations TEXT,
        headcount_blr INT,
        core_functions TEXT, -- AI, Engineering, Data, Product, Finance, Cyber
        ai_initiatives TEXT,
        product_ownership_level TEXT, -- HIGH, MEDIUM, LOW
        gcc_momentum_score REAL,
        source TEXT,
        confidence TEXT,
        last_verified TEXT
    )''')

    # 4. Jobs & Roles Table
    cur.execute('''CREATE TABLE IF NOT EXISTS job_postings (
        job_id TEXT PRIMARY KEY,
        company_id TEXT,
        company_name TEXT,
        role_title TEXT NOT NULL,
        domain TEXT NOT NULL, -- AI/ML, SCM/Trade, FinTech, Software, Product
        experience_level TEXT, -- FRESHER, MID, SENIOR, LEAD
        target_degree TEXT, -- BBA, BTech, MBA, MTech
        skills_required TEXT, -- JSON array
        salary_range_inr TEXT,
        work_mode TEXT, -- ONSITE, HYBRID, REMOTE
        location_micro TEXT,
        source_url TEXT,
        source TEXT,
        confidence TEXT,
        posted_date TEXT
    )''')

    # 5. Skills Taxonomy
    cur.execute('''CREATE TABLE IF NOT EXISTS skills_taxonomy (
        skill_id TEXT PRIMARY KEY,
        skill_name TEXT NOT NULL,
        category TEXT NOT NULL,
        demand_score REAL, -- 0-100
        salary_premium_pct REAL,
        growth_trend TEXT, -- SURGING, STEADY, DECLINING
        related_roles TEXT
    )''')

    # 6. Venture Capital & Investors Table
    cur.execute('''CREATE TABLE IF NOT EXISTS investors (
        investor_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT, -- VC, ANGEL, CORPORATE_VC, FAMILY_OFFICE
        blr_office TEXT,
        aum_usd_m REAL,
        sectors_focus TEXT,
        notable_portfolio TEXT,
        source TEXT,
        confidence TEXT
    )''')

    # 7. Funding Rounds
    cur.execute('''CREATE TABLE IF NOT EXISTS funding_rounds (
        round_id TEXT PRIMARY KEY,
        company_name TEXT NOT NULL,
        round_type TEXT,
        amount_usd_m REAL,
        lead_investor TEXT,
        date TEXT,
        sector TEXT,
        source TEXT,
        confidence TEXT
    )''')

    # 8. Micro-Market Real Estate & Neighborhoods
    cur.execute('''CREATE TABLE IF NOT EXISTS neighborhoods (
        neighborhood_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        cluster_type TEXT, -- TECH_CORRIDOR, STARTUP_HUB, HERITAGE, AIRPORT_NORTH
        major_tech_parks TEXT,
        office_rent_sqft_inr REAL,
        residential_rent_2bhk_inr REAL,
        traffic_congestion_index REAL, -- 1-10
        metro_connectivity TEXT
    )''')

    # 9. Real-Time Signals Table
    cur.execute('''CREATE TABLE IF NOT EXISTS intelligence_signals (
        signal_id TEXT PRIMARY KEY,
        timestamp REAL,
        category TEXT, -- GCC_EXPANSION, STARTUP_FUNDING, HIRING_SPIKE, POLICY_UPDATE
        entity_name TEXT,
        headline TEXT,
        details TEXT,
        impact_score REAL,
        classification TEXT -- OBSERVED, VERIFIED, INFERRED
    )''')

    # 10. Government Schemes & Policies
    cur.execute('''CREATE TABLE IF NOT EXISTS policies_programs (
        policy_id TEXT PRIMARY KEY,
        program_name TEXT NOT NULL,
        governing_body TEXT, -- Govt of Karnataka, KDEM, Startup Karnataka
        target_sector TEXT,
        benefits_summary TEXT,
        funding_grant_inr REAL,
        eligibility TEXT,
        source_url TEXT,
        verified_date TEXT
    )''')

    # 11. Historical Time-Series State
    cur.execute('''CREATE TABLE IF NOT EXISTS time_series_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metric_name TEXT NOT NULL,
        entity_id TEXT,
        value REAL,
        recorded_date TEXT
    )''')

    # 12. User Career Matches & Applications
    cur.execute('''CREATE TABLE IF NOT EXISTS user_career_pipeline (
        application_id TEXT PRIMARY KEY,
        target_company TEXT,
        target_role TEXT,
        match_percentage REAL,
        skill_gaps TEXT,
        status TEXT, -- TARGETED, RESUME_ALIGNED, INTERVIEW_PREP, APPLIED
        action_deadline TEXT
    )''')

    conn.commit()
    conn.close()
    print(f"[DB_INIT] Successfully initialized Bengaluru Digital Twin SQLite Schema at: {DB_PATH}")

if __name__ == "__main__":
    init_bengaluru_database()
