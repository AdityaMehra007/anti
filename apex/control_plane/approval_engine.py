"""
OMEGA CONTROL PLANE - Approval Engine
Gated authority for production financial transactions, external submissions, and destructive actions.
"""
import sqlite3
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

DB_PATH = Path(r"e:\anti\data\omega_approvals.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

class OmegaApprovalEngine:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS approvals (
            approval_id TEXT PRIMARY KEY,
            requester_agent TEXT NOT NULL,
            action_type TEXT NOT NULL,
            target_system TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            status TEXT DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED, EXPIRED
            approver TEXT,
            decision_reason TEXT,
            created_at REAL NOT NULL,
            decided_at REAL
        )''')
        conn.commit()
        conn.close()

    def request_approval(
        self,
        approval_id: str,
        requester_agent: str,
        action_type: str,
        target_system: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        conn = self._get_conn()
        cur = conn.cursor()
        now = time.time()
        cur.execute('''INSERT OR REPLACE INTO approvals (approval_id, requester_agent, action_type, target_system, payload_json, status, approver, decision_reason, created_at, decided_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?)''',
                    (approval_id, requester_agent, action_type, target_system, json.dumps(payload),
                     "PENDING", None, None, now, None))
        conn.commit()
        conn.close()
        return {"approval_id": approval_id, "status": "PENDING", "action_type": action_type}

    def record_decision(self, approval_id: str, approver: str, decision: str, reason: str) -> Dict[str, Any]:
        conn = self._get_conn()
        cur = conn.cursor()
        now = time.time()
        cur.execute('''UPDATE approvals SET status = ?, approver = ?, decision_reason = ?, decided_at = ?
                       WHERE approval_id = ?''', (decision.upper(), approver, reason, now, approval_id))
        conn.commit()
        conn.close()
        return {"approval_id": approval_id, "status": decision.upper(), "approver": approver, "reason": reason}

    def list_pending_approvals(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM approvals WHERE status = 'PENDING' ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

if __name__ == "__main__":
    engine = OmegaApprovalEngine()
    req = engine.request_approval("APP-901", "OMEGA_FINANCE", "TRANSFER_PRODUCTION_FUNDS", "RAZORPAY", {"amount_inr": 50000})
    print("[APPROVAL_ENGINE] Requested Approval:", req)
    dec = engine.record_decision("APP-901", "HUMAN_OPERATOR", "APPROVED", "Authorized test payout")
    print("[APPROVAL_ENGINE] Decision:", dec)
