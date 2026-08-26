"""
OMEGA CONTROL PLANE - Master Data Core
Single normalized SQLite database core unifying all 18 enterprise entities across the ecosystem.
"""
import sqlite3
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

CORE_DB_PATH = Path(r"e:\anti\data\omega_master_core.db")
CORE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

class OmegaMasterDataCore:
    def __init__(self, db_path: Path = CORE_DB_PATH):
        self.db_path = db_path
        self._init_core_schema()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_core_schema(self):
        conn = self._get_conn()
        cur = conn.cursor()

        # 1. PERSON
        cur.execute('''CREATE TABLE IF NOT EXISTS people (
            person_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            title TEXT,
            location TEXT,
            profile_json TEXT,
            created_at REAL
        )''')

        # 2. COMPANY
        cur.execute('''CREATE TABLE IF NOT EXISTS companies (
            company_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT,
            industry TEXT,
            headquarters TEXT,
            tier TEXT,
            metadata_json TEXT
        )''')

        # 3. JOB
        cur.execute('''CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            company_id TEXT,
            title TEXT NOT NULL,
            location TEXT,
            salary_range TEXT,
            experience_level TEXT,
            match_score REAL DEFAULT 0.0,
            status TEXT DEFAULT 'DISCOVERED',
            FOREIGN KEY (company_id) REFERENCES companies(company_id)
        )''')

        # 4. APPLICATION
        cur.execute('''CREATE TABLE IF NOT EXISTS applications (
            application_id TEXT PRIMARY KEY,
            job_id TEXT,
            person_id TEXT,
            stage TEXT DEFAULT 'READY_FOR_HUMAN_SUBMISSION', -- READY, SUBMITTED, INTERVIEW, OFFER, REJECTED
            submission_channel TEXT, -- MANUAL, ATS_PORTAL, EMAIL
            submission_ref TEXT,
            applied_at REAL,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        )''')

        # 5. CONTACT
        cur.execute('''CREATE TABLE IF NOT EXISTS contacts (
            contact_id TEXT PRIMARY KEY,
            company_id TEXT,
            name TEXT NOT NULL,
            role TEXT,
            email TEXT,
            linkedin_url TEXT,
            verified BOOLEAN DEFAULT 0
        )''')

        # 6. OUTREACH
        cur.execute('''CREATE TABLE IF NOT EXISTS outreach (
            outreach_id TEXT PRIMARY KEY,
            contact_id TEXT,
            channel TEXT NOT NULL, -- EMAIL, LINKEDIN, WHATSAPP
            status TEXT DEFAULT 'DRAFT', -- DRAFT, READY, APPROVED, QUEUED, DELIVERED, REPLIED, FAILED
            subject TEXT,
            body TEXT,
            created_at REAL,
            delivered_at REAL
        )''')

        # 7. INTERVIEW
        cur.execute('''CREATE TABLE IF NOT EXISTS interviews (
            interview_id TEXT PRIMARY KEY,
            application_id TEXT,
            round_name TEXT,
            scheduled_at REAL,
            status TEXT DEFAULT 'SCHEDULED',
            prep_notes TEXT
        )''')

        # 8. OFFER
        cur.execute('''CREATE TABLE IF NOT EXISTS offers (
            offer_id TEXT PRIMARY KEY,
            application_id TEXT,
            compensation_inr REAL,
            status TEXT DEFAULT 'PENDING_REVIEW',
            received_at REAL
        )''')

        # 9. TRANSACTION (Mirror)
        cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            gateway TEXT,
            amount_inr REAL,
            status TEXT,
            created_at REAL
        )''')

        # 10. GATEWAY
        cur.execute('''CREATE TABLE IF NOT EXISTS gateways (
            gateway_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            environment TEXT NOT NULL, -- LOCAL, SANDBOX, LIVE
            status TEXT NOT NULL, -- LOCAL, SANDBOX_VERIFIED, LIVE_VERIFIED
            last_checked REAL
        )''')

        # 11. AGENT
        cur.execute('''CREATE TABLE IF NOT EXISTS agents (
            agent_id TEXT PRIMARY KEY,
            role_name TEXT NOT NULL,
            status TEXT DEFAULT 'IDLE',
            tasks_completed INT DEFAULT 0
        )''')

        # 12. TASK
        cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            agent_id TEXT,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'QUEUED',
            created_at REAL
        )''')

        # 13. PROJECT
        cur.execute('''CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            status TEXT DEFAULT 'ACTIVE'
        )''')

        # 14. SKILL
        cur.execute('''CREATE TABLE IF NOT EXISTS skills (
            skill_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT
        )''')

        # 15. DOCUMENT
        cur.execute('''CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            doc_type TEXT,
            file_path TEXT
        )''')

        # 16. EVENT
        cur.execute('''CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            source TEXT NOT NULL,
            payload_json TEXT,
            timestamp REAL
        )''')

        # 17. METRIC
        cur.execute('''CREATE TABLE IF NOT EXISTS metrics (
            metric_key TEXT PRIMARY KEY,
            metric_value REAL,
            updated_at REAL
        )''')

        # 18. EXPERIMENT
        cur.execute('''CREATE TABLE IF NOT EXISTS experiments (
            experiment_id TEXT PRIMARY KEY,
            hypothesis TEXT NOT NULL,
            metric TEXT,
            status TEXT DEFAULT 'RUNNING'
        )''')

        conn.commit()
        conn.close()

    def record_event(self, event_type: str, source: str, payload: Dict[str, Any]) -> int:
        conn = self._get_conn()
        cur = conn.cursor()
        now = time.time()
        cur.execute("INSERT INTO events (event_type, source, payload_json, timestamp) VALUES (?,?,?,?)",
                    (event_type, source, json.dumps(payload), now))
        eid = cur.lastrowid
        conn.commit()
        conn.close()
        return eid

    def get_ecosystem_kpis(self) -> Dict[str, Any]:
        conn = self._get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM companies")
        comp_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM jobs")
        job_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM applications")
        app_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM gateways")
        gw_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM events")
        ev_count = cur.fetchone()[0]
        
        conn.close()
        return {
            "companies_indexed": comp_count,
            "jobs_indexed": job_count,
            "applications_tracked": app_count,
            "gateways_registered": gw_count,
            "events_logged": ev_count
        }

if __name__ == "__main__":
    core = OmegaMasterDataCore()
    eid = core.record_event("SYSTEM_BOOT", "OMEGA_CONTROL_PLANE", {"status": "INITIALIZED"})
    print("[DATA_CORE] Initialized 18-Entity Master Database. Event Logged ID:", eid)
    print("[DATA_CORE] KPIs:", core.get_ecosystem_kpis())
