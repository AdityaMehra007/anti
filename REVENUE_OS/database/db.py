"""
Database Manager for REVENUE OS
Handles SQLite connections, schema initialization, CRUD operations,
audit logging, and approval queuing.
"""

import sqlite3
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from contextlib import contextmanager

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
DEFAULT_DB_PATH = Path(__file__).resolve().parent / "revenue_os.db"

class DatabaseManager:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        if self._conn is None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False,
                isolation_level=None  # autocommit mode
            )
            self._conn.row_factory = sqlite3.Row
            # Enable WAL mode and foreign keys
            self._conn.execute("PRAGMA foreign_keys = ON;")
            self._conn.execute("PRAGMA journal_mode = WAL;")
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    @contextmanager
    def get_cursor(self):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def initialize(self):
        """Execute schema.sql to ensure all tables exist."""
        conn = self.connect()
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            script = f.read()
        conn.executescript(script)

    # --- AUDIT LOGS ---
    def log_audit(self, agent_name: str, action_tier: str, action_name: str, details: Dict[str, Any]) -> int:
        with self.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO audit_logs (agent_name, action_tier, action_name, payload_json)
                VALUES (?, ?, ?, ?)
                """,
                (agent_name, action_tier, action_name, json.dumps(details))
            )
            return cur.lastrowid

    def get_recent_audit_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_cursor() as cur:
            cur.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
            return [dict(row) for row in cur.fetchall()]

    # --- APPROVAL REQUESTS ---
    def create_approval_request(
        self,
        requester_agent: str,
        request_type: str,
        title: str,
        reason: str,
        cost_inr: float,
        upside_inr: float,
        risk_level: str,
        recommendation: str
    ) -> int:
        with self.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO approval_requests (
                    requester_agent, request_type, title, reason,
                    cost_inr, upside_inr, risk_level, recommendation, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
                """,
                (requester_agent, request_type, title, reason, cost_inr, upside_inr, risk_level, recommendation)
            )
            req_id = cur.lastrowid
            self.log_audit(
                agent_name=requester_agent,
                action_tier="RECOMMEND",
                action_name="queue_approval_request",
                details={"id": req_id, "title": title, "cost_inr": cost_inr}
            )
            return req_id

    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        with self.get_cursor() as cur:
            cur.execute("SELECT * FROM approval_requests WHERE status = 'PENDING' ORDER BY id ASC")
            return [dict(row) for row in cur.fetchall()]

    def resolve_approval(self, request_id: int, decision: str, notes: str = ""):
        with self.get_cursor() as cur:
            cur.execute(
                """
                UPDATE approval_requests
                SET status = ?, decision_notes = ?, resolved_at = datetime('now')
                WHERE id = ?
                """,
                (decision, notes, request_id)
            )
            self.log_audit(
                agent_name="Founder",
                action_tier="APPROVE" if decision == "APPROVED" else "RECOMMEND",
                action_name="resolve_approval",
                details={"id": request_id, "decision": decision, "notes": notes}
            )

    # --- GENERAL QUERY UTILITIES ---
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return [dict(row) for row in cur.fetchall()]

    def execute_write(self, query: str, params: tuple = ()) -> int:
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return cur.lastrowid

_default_db: Optional[DatabaseManager] = None

def get_db(db_path: Optional[Path] = None) -> DatabaseManager:
    global _default_db
    if db_path is not None:
        return DatabaseManager(db_path)
    if _default_db is None:
        _default_db = DatabaseManager()
        _default_db.initialize()
    return _default_db
