"""
OMEGA CONTROL PLANE - Immutable Transaction Ledger
Append-only state machine tracking external gateway actions with SHA-256 hashing.
"""
import sqlite3
import hashlib
import json
import time
from pathlib import Path
from enum import Enum
from typing import Dict, Any, Optional, List

DB_PATH = Path(r"e:\anti\data\omega_ledger.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

class TransactionState(str, Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    APPROVED = "APPROVED"
    QUEUED = "QUEUED"
    ATTEMPTED = "ATTEMPTED"
    EXTERNAL_ACK = "EXTERNAL_ACK"
    EXTERNAL_REFERENCE = "EXTERNAL_REFERENCE"
    RESPONSE_RECEIVED = "RESPONSE_RECEIVED"
    RECONCILED = "RECONCILED"
    VERIFIED = "VERIFIED"
    # Failure branches
    FAILED = "FAILED"
    RETRY_PENDING = "RETRY_PENDING"
    RETRYING = "RETRYING"
    ESCALATED = "ESCALATED"
    CANCELLED = "CANCELLED"

class ImmutableTransactionLedger:
    VALID_TRANSITIONS = {
        TransactionState.CREATED: [TransactionState.VALIDATED, TransactionState.FAILED, TransactionState.CANCELLED],
        TransactionState.VALIDATED: [TransactionState.APPROVAL_REQUIRED, TransactionState.QUEUED, TransactionState.FAILED],
        TransactionState.APPROVAL_REQUIRED: [TransactionState.APPROVED, TransactionState.CANCELLED, TransactionState.ESCALATED],
        TransactionState.APPROVED: [TransactionState.QUEUED, TransactionState.CANCELLED],
        TransactionState.QUEUED: [TransactionState.ATTEMPTED, TransactionState.CANCELLED],
        TransactionState.ATTEMPTED: [TransactionState.EXTERNAL_ACK, TransactionState.FAILED, TransactionState.RETRY_PENDING],
        TransactionState.EXTERNAL_ACK: [TransactionState.EXTERNAL_REFERENCE, TransactionState.RESPONSE_RECEIVED, TransactionState.FAILED],
        TransactionState.EXTERNAL_REFERENCE: [TransactionState.RESPONSE_RECEIVED, TransactionState.RECONCILED, TransactionState.FAILED],
        TransactionState.RESPONSE_RECEIVED: [TransactionState.RECONCILED, TransactionState.FAILED],
        TransactionState.RECONCILED: [TransactionState.VERIFIED, TransactionState.FAILED],
        TransactionState.RETRY_PENDING: [TransactionState.RETRYING, TransactionState.CANCELLED],
        TransactionState.RETRYING: [TransactionState.ATTEMPTED, TransactionState.FAILED]
    }

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
        cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            gateway TEXT NOT NULL,
            environment TEXT NOT NULL, -- LOCAL, SANDBOX, LIVE
            action_type TEXT NOT NULL,
            created_at REAL NOT NULL,
            executed_at REAL,
            actor TEXT NOT NULL,
            agent TEXT NOT NULL,
            approval_id TEXT,
            request_hash TEXT NOT NULL,
            external_reference TEXT,
            response_code INT,
            response_hash TEXT,
            status TEXT NOT NULL,
            reconciliation_status TEXT DEFAULT 'PENDING',
            evidence_location TEXT,
            error_message TEXT,
            retry_count INT DEFAULT 0,
            final_state TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS transaction_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT NOT NULL,
            previous_state TEXT,
            new_state TEXT NOT NULL,
            timestamp REAL NOT NULL,
            actor TEXT NOT NULL,
            payload_snapshot TEXT,
            FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
        )''')
        conn.commit()
        conn.close()

    def create_transaction(
        self,
        transaction_id: str,
        gateway: str,
        environment: str,
        action_type: str,
        actor: str,
        agent: str,
        request_payload: Dict[str, Any],
        approval_id: Optional[str] = None
    ) -> Dict[str, Any]:
        req_hash = hashlib.sha256(json.dumps(request_payload, sort_keys=True).encode()).hexdigest()
        now = time.time()

        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('''INSERT OR REPLACE INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (transaction_id, gateway, environment, action_type, now, None, actor, agent,
                     approval_id, req_hash, None, None, None, TransactionState.CREATED.value, "PENDING", None, None, 0, None))
        
        cur.execute('''INSERT INTO transaction_events (transaction_id, previous_state, new_state, timestamp, actor, payload_snapshot)
                       VALUES (?,?,?,?,?,?)''',
                    (transaction_id, None, TransactionState.CREATED.value, now, actor, json.dumps(request_payload)))
        conn.commit()
        conn.close()

        return {"transaction_id": transaction_id, "status": TransactionState.CREATED.value, "request_hash": req_hash}

    def transition_state(
        self,
        transaction_id: str,
        new_state: TransactionState,
        actor: str,
        external_reference: Optional[str] = None,
        response_payload: Optional[Dict[str, Any]] = None,
        response_code: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> Dict[str, Any]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT status, retry_count FROM transactions WHERE transaction_id = ?", (transaction_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"Transaction '{transaction_id}' not found.")

        current_state = TransactionState(row["status"])
        
        # Validate transition rule
        valid_next = self.VALID_TRANSITIONS.get(current_state, [])
        if new_state not in valid_next and new_state not in [TransactionState.FAILED, TransactionState.CANCELLED]:
            conn.close()
            raise ValueError(f"Illegal state transition from {current_state.value} to {new_state.value}")

        resp_hash = hashlib.sha256(json.dumps(response_payload or {}, sort_keys=True).encode()).hexdigest() if response_payload else None
        now = time.time()

        cur.execute('''UPDATE transactions SET
            status = ?,
            external_reference = COALESCE(?, external_reference),
            response_code = COALESCE(?, response_code),
            response_hash = COALESCE(?, response_hash),
            error_message = COALESCE(?, error_message),
            executed_at = COALESCE(executed_at, ?),
            final_state = CASE WHEN ? IN ('VERIFIED', 'FAILED', 'CANCELLED') THEN ? ELSE final_state END
            WHERE transaction_id = ?''',
            (new_state.value, external_reference, response_code, resp_hash, error_message, now, new_state.value, new_state.value, transaction_id))

        cur.execute('''INSERT INTO transaction_events (transaction_id, previous_state, new_state, timestamp, actor, payload_snapshot)
                       VALUES (?,?,?,?,?,?)''',
                    (transaction_id, current_state.value, new_state.value, now, actor, json.dumps(response_payload or {})))
        conn.commit()
        conn.close()

        return {"transaction_id": transaction_id, "previous_state": current_state.value, "new_state": new_state.value}

    def get_transaction(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

if __name__ == "__main__":
    ledger = ImmutableTransactionLedger()
    tx = ledger.create_transaction("TX-DEMO-001", "RAZORPAY", "SANDBOX", "CREATE_PAYMENT_LINK", "SYSTEM", "OMEGA_FINANCE", {"amount": 1000})
    print("[LEDGER] Created TX:", tx)
    tr = ledger.transition_state("TX-DEMO-001", TransactionState.VALIDATED, "OMEGA_TRUTH")
    print("[LEDGER] Transitioned to:", tr["new_state"])
