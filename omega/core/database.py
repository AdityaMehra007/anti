import os, sqlite3, json
from datetime import datetime

class OmegaDB:
    '''High-Performance SQLite3 WAL Database for Omega Autonomous Platform.'''
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(r"e:\anti", "omega", "omega_platform.db")
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
            # 1. Missions Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS missions (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    goal TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )
            ''')
            # 2. Tasks Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    mission_id TEXT,
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
            # 3. Agents Registry Table
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
            # 6. Telemetry & Cost Table
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
            conn.commit()
