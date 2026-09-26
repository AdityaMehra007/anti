"""Tamper-Evident Cryptographic Audit Chain for GLOBAL CAPITAL OS.

Maintains an immutable SHA-256 hash-linked log of all financial decisions,
consequential action submissions, approvals, and system state modifications.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from .config import settings
from .security import SecurityManager
from .database import db

GENESIS_HASH = "0" * 64


class AuditChain:
    def __init__(self):
        self.log_file = settings.AUDIT_LOG_PATH
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _get_latest_hash(self) -> str:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT current_hash FROM audit_chain ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            if row and row[0]:
                return row[0]
        return GENESIS_HASH

    def log_event(self, agent_name: str, action_type: str, details: dict[str, Any]) -> str:
        """Records a sanitized financial event into the cryptographic hash chain."""
        sanitized_details = SecurityManager.sanitize_payload(details)
        details_str = json.dumps(sanitized_details, sort_keys=True, default=str)
        now_str = datetime.utcnow().isoformat()
        prev_hash = self._get_latest_hash()

        # Compute tamper-evident current hash
        hasher = hashlib.sha256()
        hasher.update(prev_hash.encode("utf-8"))
        hasher.update(now_str.encode("utf-8"))
        hasher.update(agent_name.encode("utf-8"))
        hasher.update(action_type.encode("utf-8"))
        hasher.update(details_str.encode("utf-8"))
        curr_hash = hasher.hexdigest()

        # Store in database
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO audit_chain (event_time, agent_name, action_type, details_json, previous_hash, current_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (now_str, agent_name, action_type, details_str, prev_hash, curr_hash))
            conn.commit()

        # Append to jsonl audit log file
        record = {
            "timestamp": now_str,
            "agent": agent_name,
            "action": action_type,
            "details": sanitized_details,
            "previous_hash": prev_hash,
            "hash": curr_hash
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        return curr_hash

    def verify_chain_integrity(self) -> dict[str, Any]:
        """Validates the entire cryptographic chain to detect any tampering."""
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, event_time, agent_name, action_type, details_json, previous_hash, current_hash FROM audit_chain ORDER BY id ASC")
            rows = cur.fetchall()

        if not rows:
            return {"valid": True, "count": 0, "message": "Audit chain is empty and valid."}

        expected_prev = GENESIS_HASH
        for row in rows:
            row_id, ev_time, agent, act, details, prev_h, curr_h = (
                row["id"], row["event_time"], row["agent_name"], row["action_type"],
                row["details_json"], row["previous_hash"], row["current_hash"]
            )
            if prev_h != expected_prev:
                return {
                    "valid": False,
                    "corrupted_id": row_id,
                    "error": f"Broken link at row {row_id}: previous_hash mismatch."
                }

            hasher = hashlib.sha256()
            hasher.update(prev_h.encode("utf-8"))
            hasher.update(ev_time.encode("utf-8"))
            hasher.update(agent.encode("utf-8"))
            hasher.update(act.encode("utf-8"))
            hasher.update(details.encode("utf-8"))
            computed_curr = hasher.hexdigest()

            if computed_curr != curr_h:
                return {
                    "valid": False,
                    "corrupted_id": row_id,
                    "error": f"Content tampering detected at row {row_id}: hash mismatch."
                }

            expected_prev = curr_h

        return {
            "valid": True,
            "count": len(rows),
            "latest_hash": expected_prev,
            "message": "All cryptographic audit chain blocks verified successfully."
        }


audit = AuditChain()
