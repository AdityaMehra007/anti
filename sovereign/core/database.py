import os, sqlite3, json
from datetime import datetime

class SovereignDB:
    '''Unified SQLite3 Database for Antigravity Sovereign Platform.'''
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(r"e:\anti", "sovereign", "sovereign_platform.db")
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 1. Projects Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    status TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            # 2. Agents Registry Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    mission TEXT NOT NULL,
                    permission_level INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'IDLE',
                    created_at TEXT NOT NULL
                )
            ''')
            # 3. Tasks Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    project_id TEXT,
                    parent_task_id TEXT,
                    title TEXT NOT NULL,
                    assigned_agent TEXT,
                    priority TEXT DEFAULT 'MEDIUM',
                    status TEXT DEFAULT 'PENDING',
                    input_data TEXT,
                    output_data TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )
            ''')
            # 4. Multi-Layer Memory Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    layer TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    key_tag TEXT NOT NULL,
                    content TEXT NOT NULL,
                    confidence REAL DEFAULT 1.0,
                    provenance TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            # 5. Audit Log Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT,
                    action TEXT NOT NULL,
                    permission_level INTEGER,
                    status TEXT NOT NULL,
                    details TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
            # 6. Telemetry & Cost Metrics Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT,
                    agent_id TEXT,
                    duration_seconds REAL,
                    tokens_estimated INTEGER DEFAULT 0,
                    cost_estimated_usd REAL DEFAULT 0.0,
                    timestamp TEXT NOT NULL
                )
            ''')
            # 7. Career Jobs Table (Section 13 & 41)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS career_jobs (
                    id TEXT PRIMARY KEY,
                    source TEXT,
                    source_job_id TEXT,
                    company TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    location TEXT,
                    work_model TEXT,
                    experience_min REAL,
                    experience_max REAL,
                    salary_min REAL,
                    salary_max REAL,
                    salary_currency TEXT,
                    posted_at TEXT,
                    application_url TEXT,
                    role_family TEXT,
                    sales_risk_score INTEGER,
                    fit_score REAL,
                    eligibility_score REAL,
                    hiring_probability REAL,
                    company_quality REAL,
                    status TEXT,
                    tailored_profile TEXT,
                    ats_match_pct REAL,
                    executive_view_json TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            # 8. Career Applications Table (Section 18 & 19)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS career_applications (
                    application_id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    current_state TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    history_json TEXT,
                    FOREIGN KEY (job_id) REFERENCES career_jobs(id)
                )
            ''')
            # 9. Recruiter Contacts CRM Table (Section 23)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recruiter_contacts (
                    contact_id TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    company TEXT NOT NULL,
                    title TEXT NOT NULL,
                    channel TEXT,
                    relationship TEXT,
                    email TEXT,
                    profile_url TEXT,
                    is_decision_maker INTEGER DEFAULT 0,
                    referral_potential TEXT,
                    last_contact_date TEXT,
                    next_action_due TEXT,
                    status TEXT,
                    notes_json TEXT
                )
            ''')
            conn.commit()
