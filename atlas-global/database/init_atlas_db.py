#!/usr/bin/env python3
r"""
========================================================================================
ATLAS-GLOBAL: DATABASE INITIALIZATION & SCHEMA DEFINITION ENGINE
========================================================================================
Builds the relational SQLite schema with FTS5 virtual search index for ATLAS-GLOBAL:
- companies
- people
- jobs
- sources
- changes
- knowledge_graph_edges
- tool_registry
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import sqlite3
from pathlib import Path

ROOT_DIR = Path(r"e:\anti\atlas-global")
DB_PATH = ROOT_DIR / "database" / "atlas.db"

def init_atlas_db():
    print("=" * 80)
    print("  INITIALIZING ATLAS-GLOBAL RELATIONAL & FTS5 SEARCH DATABASE")
    print(f"  Target Path: {DB_PATH}")
    print("=" * 80)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Companies Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        company_id TEXT PRIMARY KEY,
        company_name TEXT NOT NULL,
        legal_name TEXT,
        brand_name TEXT,
        domain TEXT,
        website TEXT,
        linkedin TEXT,
        industry TEXT,
        subindustry TEXT,
        company_type TEXT,
        startup_status TEXT,
        listed_status TEXT,
        parent_company TEXT,
        country_of_origin TEXT,
        headquarters TEXT,
        bengaluru_presence TEXT,
        bengaluru_address TEXT,
        locality TEXT,
        employee_range TEXT,
        founded_year TEXT,
        funding_status TEXT,
        funding_amount_if_public TEXT,
        latest_funding_date TEXT,
        investors TEXT,
        founders TEXT,
        leadership TEXT,
        careers_url TEXT,
        jobs_url TEXT,
        public_email TEXT,
        public_phone TEXT,
        contact_url TEXT,
        source TEXT,
        source_url TEXT,
        source_date TEXT,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_verified TIMESTAMP,
        verification_status TEXT DEFAULT 'UNVERIFIED',
        confidence REAL DEFAULT 1.0,
        notes TEXT
    )
    """)

    # 2. People Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS people (
        person_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        company TEXT NOT NULL,
        title TEXT,
        department TEXT,
        seniority TEXT,
        location TEXT,
        country TEXT,
        linkedin_url TEXT,
        official_profile TEXT,
        professional_website TEXT,
        public_work_email TEXT,
        public_business_phone TEXT,
        company_phone TEXT,
        employment_status TEXT,
        employment_start_if_public TEXT,
        employment_end_if_public TEXT,
        source TEXT,
        source_url TEXT,
        source_date TEXT,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_verified TIMESTAMP,
        verification_status TEXT DEFAULT 'UNVERIFIED',
        confidence REAL DEFAULT 1.0,
        notes TEXT
    )
    """)

    # 3. Jobs Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        company TEXT NOT NULL,
        title TEXT NOT NULL,
        department TEXT,
        location TEXT,
        country TEXT,
        city TEXT,
        work_mode TEXT,
        employment_type TEXT,
        experience TEXT,
        education TEXT,
        skills TEXT,
        salary TEXT,
        currency TEXT,
        posting_date TEXT,
        closing_date TEXT,
        job_url TEXT,
        application_url TEXT,
        source TEXT,
        source_url TEXT,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_verified TIMESTAMP,
        status TEXT DEFAULT 'ACTIVE',
        notes TEXT
    )
    """)

    # 4. Sources Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sources (
        source_id TEXT PRIMARY KEY,
        source_name TEXT NOT NULL,
        source_type TEXT,
        country TEXT,
        url TEXT,
        official INTEGER DEFAULT 1,
        free INTEGER DEFAULT 1,
        access_type TEXT,
        allowed_usage TEXT,
        terms_notes TEXT,
        data_categories TEXT,
        last_checked TIMESTAMP,
        reliability REAL DEFAULT 1.0,
        status TEXT DEFAULT 'ACTIVE',
        notes TEXT
    )
    """)

    # 5. Changes Tracking Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS changes (
        change_id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        change_type TEXT NOT NULL,
        old_value TEXT,
        new_value TEXT,
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source TEXT,
        notes TEXT
    )
    """)

    # 6. Knowledge Graph Edges Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_graph_edges (
        edge_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_node_type TEXT NOT NULL,
        source_node_id TEXT NOT NULL,
        relationship TEXT NOT NULL,
        target_node_type TEXT NOT NULL,
        target_node_id TEXT NOT NULL,
        weight REAL DEFAULT 1.0,
        established_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        provenance TEXT
    )
    """)

    # 7. Tool Registry Table (for TOOL-HUNTER)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tool_registry (
        tool_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tool_name TEXT NOT NULL UNIQUE,
        publisher TEXT,
        official_url TEXT,
        repository TEXT,
        license TEXT,
        cost TEXT DEFAULT 'FREE',
        free_tier TEXT,
        capabilities TEXT,
        permissions TEXT,
        network_access TEXT,
        filesystem_access TEXT,
        credentials_required TEXT,
        security_risk TEXT DEFAULT 'SAFE_CANDIDATE',
        maintenance_status TEXT,
        last_release TEXT,
        documentation_quality TEXT,
        relevance TEXT,
        installation_status TEXT DEFAULT 'APPROVED',
        approval_required INTEGER DEFAULT 0,
        discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 8. Full-Text Search FTS5 Virtual Table
    cur.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS atlas_search_fts USING fts5(
        entity_id,
        entity_type,
        name_or_title,
        company_or_org,
        location_corridor,
        contact_point,
        keywords,
        tokenize = 'porter unicode61'
    )
    """)

    # Indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_comp_name ON companies(company_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_comp_domain ON companies(domain);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_comp_bengaluru ON companies(bengaluru_presence);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_people_name ON people(full_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_people_comp ON people(company);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_jobs_comp ON jobs(company);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);")

    conn.commit()
    conn.close()
    print(f"[+] Successfully created Atlas-Global relational & FTS5 database at: {DB_PATH}")

if __name__ == "__main__":
    init_atlas_db()
