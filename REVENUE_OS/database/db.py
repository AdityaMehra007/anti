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

    # --- DAILY CASH TRANSACTIONS & PROFIT LEDGER ---
    def record_cash_transaction(
        self,
        client_or_customer: str,
        source_type: str,
        description: str,
        gross_amount_inr: float,
        currency: str = "INR",
        original_currency_amount: Optional[float] = None,
        variable_cost_inr: float = 0.0,
        payment_rail: str = "UPI_HDFC",
        payment_status: str = "COMPLETED",
        reference_id: Optional[str] = None,
        notes: str = ""
    ) -> int:
        if original_currency_amount is None:
            original_currency_amount = gross_amount_inr
        net_profit_inr = gross_amount_inr - variable_cost_inr
        profit_margin_pct = round((net_profit_inr / gross_amount_inr * 100.0), 2) if gross_amount_inr > 0 else 0.0
        from datetime import datetime
        now = datetime.now()
        t_date = now.strftime("%Y-%m-%d")
        t_time = now.strftime("%H:%M:%S")

        with self.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO daily_cash_transactions (
                    transaction_date, transaction_time, source_type, client_or_customer,
                    description, gross_amount_inr, currency, original_currency_amount,
                    variable_cost_inr, net_profit_inr, profit_margin_pct,
                    payment_rail, payment_status, reference_id, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    t_date, t_time, source_type, client_or_customer,
                    description, gross_amount_inr, currency, original_currency_amount,
                    variable_cost_inr, net_profit_inr, profit_margin_pct,
                    payment_rail, payment_status, reference_id, notes
                )
            )
            txn_id = cur.lastrowid
            self.log_audit(
                agent_name="DailyProfitEngine",
                action_tier="EXECUTE",
                action_name="record_cash_transaction",
                details={
                    "txn_id": txn_id,
                    "client": client_or_customer,
                    "gross_amount_inr": gross_amount_inr,
                    "net_profit_inr": net_profit_inr,
                    "margin": profit_margin_pct
                }
            )
            return txn_id

    def get_daily_transactions(self, date_str: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_cursor() as cur:
            if date_str:
                cur.execute(
                    "SELECT * FROM daily_cash_transactions WHERE transaction_date = ? ORDER BY id DESC LIMIT ?",
                    (date_str, limit)
                )
            else:
                cur.execute(
                    "SELECT * FROM daily_cash_transactions ORDER BY id DESC LIMIT ?",
                    (limit,)
                )
            return [dict(row) for row in cur.fetchall()]

    def get_daily_financial_summary(self, date_str: Optional[str] = None) -> Dict[str, Any]:
        from datetime import datetime
        t_date = date_str or datetime.now().strftime("%Y-%m-%d")
        with self.get_cursor() as cur:
            cur.execute(
                """
                SELECT 
                    COUNT(*) as tx_count,
                    COALESCE(SUM(gross_amount_inr), 0.0) as total_gross,
                    COALESCE(SUM(variable_cost_inr), 0.0) as total_costs,
                    COALESCE(SUM(net_profit_inr), 0.0) as total_profit
                FROM daily_cash_transactions
                WHERE transaction_date = ? AND payment_status = 'COMPLETED'
                """,
                (t_date,)
            )
            row = cur.fetchone()
            gross = float(row["total_gross"]) if row else 0.0
            costs = float(row["total_costs"]) if row else 0.0
            profit = float(row["total_profit"]) if row else 0.0
            margin = round((profit / gross * 100.0), 1) if gross > 0 else 0.0
            count = int(row["tx_count"]) if row else 0
            
            daily_target = 14500.0
            target_pct = round((profit / daily_target * 100.0), 1) if daily_target > 0 else 0.0

            return {
                "date": t_date,
                "transaction_count": count,
                "gross_revenue_inr": gross,
                "variable_costs_inr": costs,
                "net_profit_inr": profit,
                "profit_margin_pct": margin,
                "daily_target_inr": daily_target,
                "target_achievement_pct": target_pct,
                "target_remaining_inr": max(0.0, daily_target - profit)
            }

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
