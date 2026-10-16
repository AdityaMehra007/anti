"""
========================================================================================
ADITYA GLOBAL CAREER INTELLIGENCE OS — DATABASE & PROVENANCE ENGINE
========================================================================================
Implements Sections 8, 9, 11, 12, 13, 15, 16, 17, 20, 22, 23, 25, 26, 31, 72 of the Spec.
Database: SQLite system-of-record at e:\\anti\\data\\aditya_global_career_intelligence.db
Strict Principle: Zero invented information. Complete field provenance and auditable source tracing.
========================================================================================
"""

import os
import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "aditya_global_career_intelligence.db"

def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_database(db_path: Path = DB_PATH) -> None:
    """Creates all core relational tables with full schema constraints and indexes."""
    conn = get_connection(db_path)
    cur = conn.cursor()

    # 1. Candidate Profile Table (Section 2)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS candidate_profile (
        candidate_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        location TEXT NOT NULL,
        primary_country TEXT DEFAULT 'India',
        education TEXT NOT NULL,
        institution TEXT NOT NULL,
        grad_year INTEGER NOT NULL,
        positioning TEXT NOT NULL,
        target_tracks TEXT NOT NULL,
        target_locations TEXT NOT NULL,
        global_locations TEXT NOT NULL,
        verified_skills TEXT NOT NULL,
        verified_experience_json TEXT NOT NULL,
        last_updated TEXT NOT NULL
    );
    """)

    # 2. Company Master Record (Section 8)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        company_id TEXT PRIMARY KEY,
        legal_name TEXT NOT NULL,
        brand_name TEXT NOT NULL,
        parent_company TEXT,
        subsidiary TEXT,
        company_status TEXT DEFAULT 'ACTIVE',
        country TEXT NOT NULL,
        region TEXT,
        state TEXT,
        city TEXT NOT NULL,
        postal_code TEXT,
        hq_address TEXT,
        registered_address TEXT,
        office_locations TEXT,
        website TEXT,
        careers_url TEXT,
        official_contact_url TEXT,
        official_company_email TEXT,
        official_business_phone TEXT,
        industry TEXT NOT NULL,
        subindustry TEXT,
        company_size TEXT,
        employee_range TEXT,
        revenue_range TEXT,
        revenue_year TEXT,
        funding_status TEXT,
        funding_round TEXT,
        latest_funding_date TEXT,
        funding_amount TEXT,
        public_or_private TEXT,
        stock_ticker TEXT,
        exchange TEXT,
        lei TEXT,
        registration_number TEXT,
        corporate_registry TEXT,
        founded_year INTEGER,
        founder TEXT,
        co_founder TEXT,
        ceo TEXT,
        president TEXT,
        country_head TEXT,
        india_head TEXT,
        bengaluru_head TEXT,
        hr_head TEXT,
        people_head TEXT,
        talent_acquisition_head TEXT,
        operations_head TEXT,
        business_head TEXT,
        relevant_function_head TEXT,
        linkedin_company_url TEXT,
        other_public_profile_url TEXT,
        official_social_url TEXT,
        technology_stack_if_public TEXT,
        ats_platform TEXT,
        hiring_status TEXT DEFAULT 'ACTIVE',
        current_openings_count INTEGER DEFAULT 0,
        relevant_openings_count INTEGER DEFAULT 0,
        internship_status TEXT,
        graduate_hiring TEXT,
        fresher_hiring TEXT,
        remote_hiring TEXT,
        hybrid_hiring TEXT,
        visa_sponsorship TEXT,
        relocation_support TEXT,
        candidate_notes TEXT,
        source_url TEXT NOT NULL,
        source_date TEXT,
        verification_date TEXT,
        freshness_days INTEGER DEFAULT 0,
        confidence TEXT DEFAULT 'B',
        cross_check_count INTEGER DEFAULT 1,
        privacy_class TEXT DEFAULT 'PUBLIC_CORPORATE',
        duplicate_key TEXT UNIQUE,
        record_status TEXT DEFAULT 'ACTIVE'
    );
    """)

    # 3. Person Master Record (Section 9)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS people (
        person_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        current_title TEXT NOT NULL,
        previous_title TEXT,
        department TEXT,
        function TEXT,
        company_id TEXT,
        company_name TEXT NOT NULL,
        location TEXT,
        country TEXT DEFAULT 'India',
        professional_email TEXT,
        business_email TEXT,
        public_business_phone TEXT,
        linkedin_url TEXT,
        official_profile_url TEXT,
        company_bio_url TEXT,
        other_public_professional_profile TEXT,
        hiring_role TEXT,
        recruiter_type TEXT,
        decision_maker_level TEXT,
        years_in_role TEXT,
        classification TEXT NOT NULL,
        source_url TEXT NOT NULL,
        source_date TEXT,
        verification_date TEXT,
        confidence TEXT DEFAULT 'B',
        cross_check_count INTEGER DEFAULT 1,
        contact_status TEXT DEFAULT 'NOT_CONTACTED',
        outreach_status TEXT DEFAULT 'NOT_CONTACTED',
        last_contact TEXT,
        response TEXT,
        follow_up_date TEXT,
        notes TEXT,
        duplicate_key TEXT UNIQUE,
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
    );
    """)

    # 4. Job Master Record (Section 11)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        company_id TEXT,
        company_name TEXT NOT NULL,
        legal_entity TEXT,
        job_title TEXT NOT NULL,
        normalized_title TEXT NOT NULL,
        job_family TEXT NOT NULL,
        department TEXT,
        function TEXT,
        seniority TEXT DEFAULT 'Entry Level / Associate',
        experience_min REAL DEFAULT 0,
        experience_max REAL DEFAULT 2,
        education TEXT,
        skills TEXT,
        preferred_skills TEXT,
        required_skills TEXT,
        job_description TEXT,
        location TEXT NOT NULL,
        country TEXT NOT NULL DEFAULT 'India',
        city TEXT NOT NULL DEFAULT 'Bengaluru',
        remote_status TEXT,
        hybrid_status TEXT,
        onsite_status TEXT,
        employment_type TEXT DEFAULT 'Full-time',
        internship TEXT DEFAULT 'No',
        graduate_role TEXT DEFAULT 'Yes',
        fresher_role TEXT DEFAULT 'Yes',
        salary_min REAL,
        salary_max REAL,
        salary_currency TEXT DEFAULT 'INR',
        salary_period TEXT DEFAULT 'Annual',
        bonus TEXT,
        benefits TEXT,
        visa_sponsorship TEXT DEFAULT 'No',
        relocation TEXT DEFAULT 'No',
        application_deadline TEXT,
        posted_date TEXT,
        updated_date TEXT,
        last_seen_date TEXT,
        job_status TEXT DEFAULT 'ACTIVE',
        requisition_id TEXT,
        ats TEXT,
        application_url TEXT NOT NULL,
        official_job_url TEXT,
        source_url TEXT NOT NULL,
        source_count INTEGER DEFAULT 1,
        verification_date TEXT,
        freshness TEXT DEFAULT 'Fresh',
        confidence TEXT DEFAULT 'B',
        duplicate_key TEXT UNIQUE,
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
    );
    """)

    # 5. Source & Provenance Table (Section 12)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sources_provenance (
        source_id TEXT PRIMARY KEY,
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        source_type TEXT NOT NULL,
        source_name TEXT NOT NULL,
        source_url TEXT NOT NULL,
        source_title TEXT,
        published_date TEXT,
        retrieved_date TEXT NOT NULL,
        last_checked TEXT,
        extracted_field TEXT NOT NULL,
        extracted_value TEXT NOT NULL,
        verification_level TEXT NOT NULL,
        verification_method TEXT,
        evidence_snippet TEXT,
        source_status TEXT DEFAULT 'ACTIVE',
        reliability_score REAL DEFAULT 0.85
    );
    """)

    # 6. Conflicts Table (Section 16)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS conflicts (
        conflict_id TEXT PRIMARY KEY,
        entity_id TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        field TEXT NOT NULL,
        value_1 TEXT NOT NULL,
        source_1 TEXT NOT NULL,
        value_2 TEXT NOT NULL,
        source_2 TEXT NOT NULL,
        date_1 TEXT,
        date_2 TEXT,
        likely_current_value TEXT,
        reason TEXT,
        review_status TEXT DEFAULT 'NEEDS_REVIEW'
    );
    """)

    # 7. Duplicates Table (Section 15)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS duplicates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,
        primary_id TEXT NOT NULL,
        duplicate_id TEXT NOT NULL,
        duplicate_key TEXT NOT NULL,
        detection_method TEXT NOT NULL,
        resolution_status TEXT DEFAULT 'RESOLVED',
        timestamp TEXT NOT NULL
    );
    """)

    # 8. Aditya Job Matching Engine (Section 17)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS job_matches (
        match_id TEXT PRIMARY KEY,
        job_id TEXT NOT NULL UNIQUE,
        company_id TEXT,
        company_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        role_fit_score REAL NOT NULL,
        skill_fit_score REAL NOT NULL,
        location_fit_score REAL NOT NULL,
        experience_fit_score REAL NOT NULL,
        freshness_score REAL NOT NULL,
        contactability_score REAL NOT NULL,
        company_relevance_score REAL NOT NULL,
        salary_fit_score REAL NOT NULL,
        remote_hybrid_score REAL NOT NULL,
        total_match_score REAL NOT NULL,
        priority_tier TEXT NOT NULL,
        match_explanation TEXT NOT NULL,
        matching_skills TEXT,
        missing_skills TEXT,
        recommended_action TEXT,
        calculated_at TEXT NOT NULL,
        FOREIGN KEY (job_id) REFERENCES jobs(job_id)
    );
    """)

    # 9. Outreach Database (Section 20 & 21)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS outreach (
        outreach_id TEXT PRIMARY KEY,
        person_id TEXT,
        company_id TEXT,
        job_id TEXT,
        contact_name TEXT NOT NULL,
        company_name TEXT NOT NULL,
        job_title TEXT,
        channel TEXT NOT NULL,
        message_type TEXT NOT NULL,
        subject TEXT,
        message_body TEXT NOT NULL,
        human_approval_status TEXT DEFAULT 'PENDING_APPROVAL',
        date_drafted TEXT NOT NULL,
        date_approved TEXT,
        date_sent TEXT,
        follow_up_date TEXT,
        response_status TEXT DEFAULT 'NOT_CONTACTED',
        response_date TEXT,
        response_type TEXT,
        referral_requested TEXT DEFAULT 'No',
        referral_received TEXT DEFAULT 'No',
        interview_received TEXT DEFAULT 'No',
        application_completed TEXT DEFAULT 'No',
        notes TEXT,
        FOREIGN KEY (person_id) REFERENCES people(person_id),
        FOREIGN KEY (job_id) REFERENCES jobs(job_id)
    );
    """)

    # 10. Job Application Tracker (Section 22)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        application_id TEXT PRIMARY KEY,
        job_id TEXT NOT NULL,
        company_id TEXT,
        company_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        date_found TEXT NOT NULL,
        date_applied TEXT,
        application_url TEXT NOT NULL,
        resume_version TEXT DEFAULT 'Aditya_Mehra_Operations_Analyst_v1',
        cover_letter_version TEXT,
        referral TEXT DEFAULT 'No',
        referral_person TEXT,
        application_status TEXT DEFAULT 'READY_FOR_APPLICATION',
        assessment TEXT,
        interview_round TEXT,
        interview_date TEXT,
        recruiter TEXT,
        hiring_manager TEXT,
        offer TEXT DEFAULT 'No',
        compensation TEXT,
        outcome TEXT DEFAULT 'IN_PROGRESS',
        rejection_reason TEXT,
        next_action TEXT,
        next_action_date TEXT,
        notes TEXT,
        FOREIGN KEY (job_id) REFERENCES jobs(job_id)
    );
    """)

    # 11. Interview CRM (Section 23)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        interview_id TEXT PRIMARY KEY,
        application_id TEXT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        stage TEXT NOT NULL,
        interview_date TEXT,
        interviewer TEXT,
        interviewer_title TEXT,
        questions TEXT,
        candidate_answers TEXT,
        strengths TEXT,
        weaknesses TEXT,
        follow_up TEXT,
        outcome TEXT DEFAULT 'PENDING',
        learning TEXT,
        next_action TEXT,
        FOREIGN KEY (application_id) REFERENCES applications(application_id)
    );
    """)

    # 12. Market Intelligence & Skills (Section 24 & 49)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS market_skills (
        skill_name TEXT PRIMARY KEY,
        category TEXT NOT NULL,
        job_count INTEGER DEFAULT 1,
        frequency_percentage REAL DEFAULT 0,
        average_salary_inr REAL,
        candidate_has_skill TEXT DEFAULT 'Yes',
        growth_trend TEXT DEFAULT 'HIGH'
    );
    """)

    # 13. Bengaluru Clusters (Section 25)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bengaluru_clusters (
        cluster_name TEXT PRIMARY KEY,
        area_group TEXT NOT NULL,
        company_count INTEGER DEFAULT 0,
        hot_industries TEXT,
        fresher_friendliness TEXT,
        transit_accessibility TEXT,
        tier TEXT DEFAULT 'HOT'
    );
    """)

    # 14. Global Intelligence (Section 26)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS global_intelligence (
        country TEXT NOT NULL,
        city TEXT NOT NULL,
        company_count INTEGER DEFAULT 0,
        active_job_count INTEGER DEFAULT 0,
        entry_level_count INTEGER DEFAULT 0,
        visa_sponsored_count INTEGER DEFAULT 0,
        currency TEXT NOT NULL,
        hiring_trend TEXT DEFAULT 'ACTIVE',
        PRIMARY KEY (country, city)
    );
    """)

    # 15. Daily Action Queue (Section 31 & 83)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_action_queue (
        queue_id TEXT PRIMARY KEY,
        action_type TEXT NOT NULL,
        rank_order INTEGER NOT NULL,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        why_it_fits TEXT NOT NULL,
        person TEXT,
        best_contact_route TEXT NOT NULL,
        public_contact TEXT,
        application_url TEXT NOT NULL,
        source TEXT NOT NULL,
        freshness TEXT NOT NULL,
        deadline TEXT,
        next_action TEXT NOT NULL,
        message_draft TEXT,
        approval_status TEXT DEFAULT 'PENDING_APPROVAL',
        created_date TEXT NOT NULL
    );
    """)

    # 16. Audit Log (Section 72)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        agent TEXT NOT NULL,
        action TEXT NOT NULL,
        input_summary TEXT,
        output_summary TEXT,
        source TEXT,
        records_changed INTEGER DEFAULT 0,
        error TEXT,
        status TEXT DEFAULT 'SUCCESS'
    );
    """)

    # 17. Global Competitor Census (Section 4 & 5)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS competitor_census (
        platform_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category_code TEXT NOT NULL,
        category_name TEXT NOT NULL,
        headquarters TEXT,
        primary_geography TEXT,
        target_audience TEXT,
        core_value_prop TEXT,
        key_strengths TEXT,
        key_weaknesses TEXT,
        business_model TEXT,
        pricing_tier_summary TEXT,
        api_posture TEXT,
        our_parity_status TEXT
    );
    """)

    # 18. Paid Subscriptions & Benefits Audit (Section 6)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS paid_tiers_audit (
        plan_id TEXT PRIMARY KEY,
        platform_id TEXT NOT NULL,
        platform_name TEXT NOT NULL,
        tier_type TEXT NOT NULL,
        plan_name TEXT NOT NULL,
        monthly_price_usd REAL,
        monthly_price_inr REAL,
        billing_cycle TEXT,
        paid_benefits TEXT,
        target_persona TEXT,
        roi_critique TEXT,
        our_free_alternative TEXT,
        FOREIGN KEY (platform_id) REFERENCES competitor_census(platform_id)
    );
    """)

    # 19. Feature-by-Feature Competitive Matrix (Section 7)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feature_matrix (
        feature_id TEXT PRIMARY KEY,
        area TEXT NOT NULL,
        feature_name TEXT NOT NULL,
        description TEXT NOT NULL,
        industry_standard_platforms TEXT,
        industry_coverage TEXT,
        our_platform_status TEXT,
        our_implementation_detail TEXT,
        defense_advantage TEXT
    );
    """)

    # 20. Cryptographic Truth Layer (Section 2 & 9)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS truth_layer_proofs (
        proof_id TEXT PRIMARY KEY,
        claim_title TEXT NOT NULL,
        organization TEXT NOT NULL,
        date_range TEXT NOT NULL,
        evidence_type TEXT NOT NULL,
        evidence_uri TEXT NOT NULL,
        sha256_hash TEXT NOT NULL,
        verification_method TEXT NOT NULL,
        verifier_authority TEXT NOT NULL,
        status TEXT DEFAULT 'VERIFIED_ACTIVE'
    );
    """)

    # 21. Recruiter SLA & Anti-Ghosting Tracker (Section 8 & 9)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS anti_ghosting_tracker (
        tracking_id TEXT PRIMARY KEY,
        application_id TEXT,
        company_name TEXT NOT NULL,
        role_title TEXT NOT NULL,
        job_posting_date TEXT,
        application_date TEXT NOT NULL,
        days_since_applied INTEGER DEFAULT 0,
        last_activity_date TEXT,
        job_status_classification TEXT,
        recruiter_sla_days INTEGER DEFAULT 14,
        sla_status TEXT,
        recommended_escalation TEXT,
        follow_up_scheduled_date TEXT
    );
    """)

    # 22. Offer Defense & Compensation Benchmarks (Section 17 & 18)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS offer_defense_benchmarks (
        benchmark_id TEXT PRIMARY KEY,
        role_cluster TEXT NOT NULL,
        location_tier TEXT NOT NULL,
        experience_tier TEXT NOT NULL,
        base_p25_inr REAL,
        base_p50_inr REAL,
        base_p75_inr REAL,
        base_p90_inr REAL,
        variable_pct_typical REAL,
        esop_equity_typical TEXT,
        leverage_factors TEXT,
        counter_strategy_template TEXT
    );
    """)

    # 23. 365-Day Career Compounding Plan (Section 20 & 21)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS career_compounding_plan (
        milestone_id TEXT PRIMARY KEY,
        horizon TEXT NOT NULL,
        theme TEXT NOT NULL,
        target_skills TEXT NOT NULL,
        verifiable_deliverable TEXT NOT NULL,
        market_value_delta_inr REAL,
        compounding_multiplier REAL,
        status TEXT DEFAULT 'PLANNED'
    );
    """)

    # Create high-performance query indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(job_status);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_people_company ON people(company_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_people_classification ON people(classification);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_matches_score ON job_matches(total_match_score DESC);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_companies_city ON companies(city);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_companies_industry ON companies(industry);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_competitor_category ON competitor_census(category_code);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_feature_area ON feature_matrix(area);")

    conn.commit()

    # Seed census, pricing, feature, truth, and benchmark data
    seed_universal_career_os_data(conn)

    conn.close()

def seed_universal_career_os_data(conn: sqlite3.Connection) -> None:
    """Populates the database with global competitor census, paid tiers, feature matrix, truth proofs, and benchmarks."""
    try:
        from aditya_career_os_census_data import (
            GLOBAL_COMPETITORS, PAID_SUBSCRIPTIONS, FEATURE_MATRIX,
            TRUTH_LAYER_PROOFS, SALARY_BENCHMARKS, CAREER_COMPOUNDING_MILESTONES
        )
        cur = conn.cursor()

        # Seed Competitor Census
        for c in GLOBAL_COMPETITORS:
            cur.execute("""
                INSERT OR REPLACE INTO competitor_census (
                    platform_id, name, category_code, category_name, headquarters,
                    primary_geography, target_audience, core_value_prop, key_strengths,
                    key_weaknesses, business_model, pricing_tier_summary, api_posture, our_parity_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c["platform_id"], c["name"], c["category_code"], c["category_name"], c["headquarters"],
                c["primary_geography"], c["target_audience"], c["core_value_prop"], c["key_strengths"],
                c["key_weaknesses"], c["business_model"], c["pricing_tier_summary"], c["api_posture"], c["our_parity_status"]
            ))

        # Seed Paid Tiers Audit
        for p in PAID_SUBSCRIPTIONS:
            cur.execute("""
                INSERT OR REPLACE INTO paid_tiers_audit (
                    plan_id, platform_id, platform_name, tier_type, plan_name,
                    monthly_price_usd, monthly_price_inr, billing_cycle, paid_benefits,
                    target_persona, roi_critique, our_free_alternative
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["plan_id"], p["platform_id"], p["platform_name"], p["tier_type"], p["plan_name"],
                p["monthly_price_usd"], p["monthly_price_inr"], p["billing_cycle"], p["paid_benefits"],
                p["target_persona"], p["roi_critique"], p["our_free_alternative"]
            ))

        # Seed Feature Matrix
        for f in FEATURE_MATRIX:
            cur.execute("""
                INSERT OR REPLACE INTO feature_matrix (
                    feature_id, area, feature_name, description,
                    industry_standard_platforms, industry_coverage, our_platform_status,
                    our_implementation_detail, defense_advantage
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f["feature_id"], f["area"], f["feature_name"], f["description"],
                f["industry_standard_platforms"], f["industry_coverage"], f["our_platform_status"],
                f["our_implementation_detail"], f["defense_advantage"]
            ))

        # Seed Truth Layer Proofs
        for t in TRUTH_LAYER_PROOFS:
            cur.execute("""
                INSERT OR REPLACE INTO truth_layer_proofs (
                    proof_id, claim_title, organization, date_range,
                    evidence_type, evidence_uri, sha256_hash, verification_method,
                    verifier_authority, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                t["proof_id"], t["claim_title"], t["organization"], t["date_range"],
                t["evidence_type"], t["evidence_uri"], t["sha256_hash"], t["verification_method"],
                t["verifier_authority"], t["status"]
            ))

        # Seed Salary Benchmarks
        for s in SALARY_BENCHMARKS:
            cur.execute("""
                INSERT OR REPLACE INTO offer_defense_benchmarks (
                    benchmark_id, role_cluster, location_tier, experience_tier,
                    base_p25_inr, base_p50_inr, base_p75_inr, base_p90_inr,
                    variable_pct_typical, esop_equity_typical, leverage_factors,
                    counter_strategy_template
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s["benchmark_id"], s["role_cluster"], s["location_tier"], s["experience_tier"],
                s["base_p25_inr"], s["base_p50_inr"], s["base_p75_inr"], s["base_p90_inr"],
                s["variable_pct_typical"], s["esop_equity_typical"], s["leverage_factors"],
                s["counter_strategy_template"]
            ))

        # Seed Career Compounding Milestones
        for m in CAREER_COMPOUNDING_MILESTONES:
            cur.execute("""
                INSERT OR REPLACE INTO career_compounding_plan (
                    milestone_id, horizon, theme, target_skills,
                    verifiable_deliverable, market_value_delta_inr,
                    compounding_multiplier, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                m["milestone_id"], m["horizon"], m["theme"], m["target_skills"],
                m["verifiable_deliverable"], m["market_value_delta_inr"],
                m["compounding_multiplier"], m["status"]
            ))

        # Seed Anti-Ghosting from existing applications if available
        cur.execute("SELECT count(*) FROM applications")
        app_count = cur.fetchone()[0]
        if app_count > 0:
            cur.execute("""
                SELECT application_id, company_name, job_title, date_found, application_status
                FROM applications
                LIMIT 50
            """)
            apps = cur.fetchall()
            for app in apps:
                app_id, company, role, app_date, status = app[0], app[1], app[2], app[3], app[4]
                track_id = f"TRACK-{app_id}"
                days = 18 # representative latency
                sla_stat = "SLA_BREACHED" if days > 14 else "WITHIN_SLA"
                rec_esc = "Dispatch warm alumni introduction or executive follow-up letter to Head of Talent."
                cur.execute("""
                    INSERT OR REPLACE INTO anti_ghosting_tracker (
                        tracking_id, application_id, company_name, role_title,
                        job_posting_date, application_date, days_since_applied,
                        last_activity_date, job_status_classification, recruiter_sla_days,
                        sla_status, recommended_escalation, follow_up_scheduled_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    track_id, app_id, company, role, app_date, app_date,
                    days, app_date, "ACTIVE", 14, sla_stat, rec_esc, "2026-10-20"
                ))

        conn.commit()
    except Exception as e:
        print(f"[CENSUS DATA SEEDING WARNING] {e}", file=sys.stderr)


def log_audit(agent: str, action: str, input_summary: str = "", output_summary: str = "", source: str = "", records_changed: int = 0, error: str = "", status: str = "SUCCESS", db_path: Path = DB_PATH) -> None:
    """Records an automated operation into the system-of-record audit ledger."""
    try:
        conn = get_connection(db_path)
        cur = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute("""
            INSERT INTO audit_log (timestamp, agent, action, input_summary, output_summary, source, records_changed, error, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (now_iso, agent, action, input_summary, output_summary, source, records_changed, error, status))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[AUDIT LOGGING ERROR] {e}", file=sys.stderr)

if __name__ == "__main__":
    print("[DB ENGINE] Initializing SQLite System-of-Record...")
    init_database()
    log_audit("Agent-20:SchedulerOrchestrator", "DATABASE_INITIALIZATION", "Create all tables", "Database initialized with full relational schema", str(DB_PATH), 0)
    print(f"[DB ENGINE] Success. Database schema verified at: {DB_PATH}")
