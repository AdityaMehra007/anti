"""
OMEGA CAREER WAR ROOM DATABASE
Normalized SQLite storage for the 18 core entities of the career operating system:
1. companies, 2. jobs, 3. contacts, 4. applications, 5. outreach, 6. followups,
7. interviews, 8. offers, 9. skills, 10. documents, 11. model_runs, 12. tool_runs,
13. truth_events, 14. approvals, 15. job_sources, 16. job_evidence, 17. job_changes, 18. job_runs
"""
import sqlite3
import os
import json
import time
from typing import Dict, Any, List, Optional

DB_PATH = "E:/anti/omega/data/omega_master.db"

class CareerWarRoomDB:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            # 1. Companies
            cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                industry TEXT,
                tier TEXT,
                bangalore_office TEXT,
                other_india_offices TEXT,
                global_presence TEXT,
                career_page_url TEXT,
                active_hiring_signal BOOLEAN,
                departments TEXT,
                estimated_career_value REAL,
                source TEXT NOT NULL,
                source_evidence TEXT,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 2. Jobs
            cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                company_id TEXT,
                company_name TEXT NOT NULL,
                role_title TEXT NOT NULL,
                location TEXT NOT NULL,
                category TEXT,
                employment_type TEXT,
                experience_required TEXT,
                skills TEXT,
                salary_text TEXT,
                salary_min REAL,
                salary_max REAL,
                source TEXT NOT NULL,
                source_url TEXT NOT NULL,
                application_url TEXT NOT NULL,
                dedup_hash TEXT UNIQUE NOT NULL,
                date_found TEXT NOT NULL,
                date_verified TEXT,
                verification_status TEXT NOT NULL,
                ats_score REAL,
                opportunity_score REAL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 3. Contacts
            cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                contact_id TEXT PRIMARY KEY,
                company_id TEXT,
                company_name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role_title TEXT,
                channel TEXT,
                profile_url TEXT,
                email_address TEXT,
                phone_number TEXT,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 4. Applications (13-stage truth state machine)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                application_id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                company_name TEXT NOT NULL,
                role_title TEXT NOT NULL,
                current_stage TEXT NOT NULL,
                resume_variant TEXT,
                custom_notes TEXT,
                ats_score REAL,
                submission_proof_ref TEXT,
                submitted_at TEXT,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 5. Outreach Messages
            cur.execute("""
            CREATE TABLE IF NOT EXISTS outreach (
                outreach_id TEXT PRIMARY KEY,
                application_id TEXT,
                contact_id TEXT,
                company_name TEXT NOT NULL,
                target_person TEXT,
                channel TEXT NOT NULL,
                subject TEXT,
                body_text TEXT NOT NULL,
                status TEXT NOT NULL,
                dispatch_authorized BOOLEAN DEFAULT 0,
                approved_by TEXT,
                sent_at TEXT,
                reply_received_at TEXT,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 6. Follow-ups
            cur.execute("""
            CREATE TABLE IF NOT EXISTS followups (
                followup_id TEXT PRIMARY KEY,
                application_id TEXT NOT NULL,
                company_name TEXT NOT NULL,
                cadence_days INTEGER NOT NULL,
                scheduled_date TEXT NOT NULL,
                status TEXT NOT NULL,
                message_draft TEXT,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 7. Interviews
            cur.execute("""
            CREATE TABLE IF NOT EXISTS interviews (
                interview_id TEXT PRIMARY KEY,
                application_id TEXT NOT NULL,
                company_name TEXT NOT NULL,
                round_name TEXT NOT NULL,
                scheduled_time TEXT,
                interviewer_name TEXT,
                prep_briefing TEXT,
                star_answers TEXT,
                questions_to_ask TEXT,
                status TEXT NOT NULL,
                evidence_reference TEXT,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 8. Offers
            cur.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                offer_id TEXT PRIMARY KEY,
                application_id TEXT NOT NULL,
                company_name TEXT NOT NULL,
                role_title TEXT NOT NULL,
                ctc_annual REAL,
                base_salary REAL,
                variable_pay REAL,
                joining_bonus REAL,
                benefits_summary TEXT,
                probation_months INTEGER,
                notice_period_days INTEGER,
                offer_letter_verified BOOLEAN DEFAULT 0,
                negotiation_strategy TEXT,
                status TEXT NOT NULL,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 9. Skills
            cur.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                skill_id TEXT PRIMARY KEY,
                skill_name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                candidate_proficiency TEXT NOT NULL,
                market_demand_weight REAL DEFAULT 1.0,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 10. Documents
            cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                variant_type TEXT NOT NULL,
                target_role TEXT,
                content_markdown TEXT NOT NULL,
                integrity_hash TEXT NOT NULL,
                zero_fabrication_audit_pass BOOLEAN DEFAULT 1,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 11. Model Runs
            cur.execute("""
            CREATE TABLE IF NOT EXISTS model_runs (
                run_id TEXT PRIMARY KEY,
                model_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                task_tier TEXT NOT NULL,
                input_tokens INTEGER,
                output_tokens INTEGER,
                latency_ms REAL,
                execution_mode TEXT NOT NULL,
                verified BOOLEAN NOT NULL,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 12. Tool Runs
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tool_runs (
                tool_run_id TEXT PRIMARY KEY,
                server_name TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                target_url_or_param TEXT,
                success BOOLEAN NOT NULL,
                latency_ms REAL,
                sanitized_output_summary TEXT,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 13. Truth Events
            cur.execute("""
            CREATE TABLE IF NOT EXISTS truth_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                subject_entity TEXT NOT NULL,
                claimed_state TEXT NOT NULL,
                verified_state TEXT NOT NULL,
                evidence_summary TEXT NOT NULL,
                delusion_detected BOOLEAN NOT NULL,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 14. Approvals
            cur.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                approval_id TEXT PRIMARY KEY,
                action_type TEXT NOT NULL,
                target_entity TEXT NOT NULL,
                details_json TEXT NOT NULL,
                status TEXT NOT NULL,
                approved_by TEXT,
                approved_at TEXT,
                source TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 15. Job Sources (Live discovery endpoints)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS job_sources (
                source_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                source_type TEXT NOT NULL,
                base_url TEXT NOT NULL,
                target_company TEXT,
                health_status TEXT NOT NULL,
                last_scanned_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 16. Job Evidence (Cryptographic verification logs)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS job_evidence (
                evidence_id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                source_url TEXT NOT NULL,
                final_url TEXT NOT NULL,
                page_title TEXT,
                retrieved_at TEXT NOT NULL,
                http_status INTEGER,
                evidence_hash TEXT NOT NULL,
                raw_payload_snippet TEXT,
                created_at TEXT NOT NULL
            );
            """)

            # 17. Job Changes (Audit trail of job modifications)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS job_changes (
                change_id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                change_type TEXT NOT NULL,
                previous_state TEXT,
                new_state TEXT,
                detected_at TEXT NOT NULL
            );
            """)

            # 18. Job Runs (Discovery execution telemetry)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS job_runs (
                run_id TEXT PRIMARY KEY,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                status TEXT NOT NULL,
                sources_checked INTEGER NOT NULL,
                jobs_found INTEGER NOT NULL,
                jobs_verified INTEGER NOT NULL,
                jobs_changed INTEGER NOT NULL,
                jobs_removed INTEGER NOT NULL,
                errors TEXT,
                next_run TEXT NOT NULL
            );
            """)

            conn.commit()

war_room_db = CareerWarRoomDB()
