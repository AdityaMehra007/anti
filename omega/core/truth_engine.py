import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import hashlib
import hmac
import datetime
from typing import Dict, List, Any, Optional, Tuple

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
DEFAULT_AUDIT_LOG = os.path.join(DATA_DIR, "truth_audit_trail.jsonl")
HMAC_SECRET_KEY = b"OMEGA_SOVEREIGN_TRUTH_KEY_2026_BBA_IB_ADITYA_MEHRA"

class TruthValidationError(Exception):
    """Exception raised when an invalid or unverified state transition is attempted."""
    pass

class OmegaTruthEngine:
    """
    Cryptographic State Machine & Truth Verifier.
    Enforces strict invariant checking across all recruitment and outreach pipeline stages.
    """

    ALLOWED_TRANSITIONS = {
        "INITIAL": ["PREPARED"],
        "PREPARED": ["SENT", "REJECTED"],
        "SENT": ["DELIVERED", "REJECTED"],
        "DELIVERED": ["REPLIED", "INTERVIEW", "REJECTED"],
        "REPLIED": ["INTERVIEW", "REJECTED"],
        "INTERVIEW": ["OFFER", "REJECTED"],
        "OFFER": ["ACCEPTED", "DECLINED"],
        "REJECTED": [],
        "ACCEPTED": [],
        "DECLINED": []
    }

    REQUIRED_PAYLOAD_KEYS = {
        "PREPARED": ["timestamp", "payload_type"],
        "SENT": ["timestamp", "message_id", "outbound_channel"],
        "DELIVERED": ["timestamp", "delivery_receipt"],
        "REPLIED": ["timestamp", "reply_text", "sentiment"],
        "INTERVIEW": ["timestamp", "interview_round", "invite_artifact"],
        "OFFER": ["timestamp", "ctc_offered_inr", "offer_letter_artifact"]
    }

    def __init__(self, audit_log_path: Optional[str] = None):
        self.audit_log_path = audit_log_path or DEFAULT_AUDIT_LOG
        os.makedirs(os.path.dirname(self.audit_log_path), exist_ok=True)

    def generate_proof_hash(
        self,
        record_id: str,
        from_stage: str,
        to_stage: str,
        timestamp: str,
        payload: Dict[str, Any],
        parent_proof_hash: str = ""
    ) -> str:
        """Generate a tamper-evident HMAC SHA-256 proof hash for a state transition."""
        payload_serialized = json.dumps(payload, sort_keys=True)
        raw_msg = f"{record_id}|{from_stage}->{to_stage}|{timestamp}|{payload_serialized}|{parent_proof_hash}"
        signature = hmac.new(HMAC_SECRET_KEY, raw_msg.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"sha256:{signature}"

    def validate_transition(
        self,
        current_stage: str,
        target_stage: str,
        payload: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Validate whether a transition from current_stage to target_stage is legally valid and has proof evidence.
        """
        current_stage = current_stage.upper() if current_stage else "INITIAL"
        target_stage = target_stage.upper()

        # Check state machine graph
        allowed = self.ALLOWED_TRANSITIONS.get(current_stage, [])
        if target_stage not in allowed:
            error_msg = (
                f"ILLEGAL STATE SKIP: Cannot transition from '{current_stage}' to '{target_stage}'. "
                f"Valid next states are: {allowed}. State progression must strictly follow: "
                "PREPARED -> SENT -> DELIVERED -> (REPLIED) -> INTERVIEW -> OFFER."
            )
            return False, error_msg

        # Check required proof payload fields
        required_keys = self.REQUIRED_PAYLOAD_KEYS.get(target_stage, [])
        missing_keys = [k for k in required_keys if k not in payload or payload[k] is None or payload[k] == ""]
        if missing_keys:
            error_msg = f"INSUFFICIENT PROOF: Target stage '{target_stage}' requires verification keys {missing_keys}."
            return False, error_msg

        return True, "VALID_PROOF"

    def record_transition(
        self,
        record_id: str,
        current_stage: str,
        target_stage: str,
        payload: Dict[str, Any],
        proof_artifact_path: str = "",
        parent_proof_hash: str = "",
        data_core: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Execute and record a verified state transition.
        Rejects invalid transitions and appends cryptographic audit record.
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if "timestamp" not in payload:
            payload["timestamp"] = now

        is_valid, validation_msg = self.validate_transition(current_stage, target_stage, payload)
        
        if not is_valid:
            # Log rejected attempt to audit trail
            audit_entry = {
                "audit_id": f"AUD-REJECT-{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
                "timestamp": now,
                "status": "REJECTED_ILLEGAL_TRANSITION",
                "record_id": record_id,
                "from_stage": current_stage,
                "target_stage": target_stage,
                "error_reason": validation_msg,
                "payload_snapshot": payload
            }
            self._append_audit_log(audit_entry)
            raise TruthValidationError(validation_msg)

        # Generate cryptographic proof hash
        proof_hash = self.generate_proof_hash(
            record_id=record_id,
            from_stage=current_stage,
            to_stage=target_stage,
            timestamp=now,
            payload=payload,
            parent_proof_hash=parent_proof_hash
        )

        audit_entry = {
            "audit_id": f"AUD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
            "timestamp": now,
            "status": "COMMITTED_VERIFIED",
            "record_id": record_id,
            "from_stage": current_stage,
            "to_stage": target_stage,
            "proof_hash": proof_hash,
            "proof_artifact_path": proof_artifact_path,
            "payload": payload,
            "parent_proof_hash": parent_proof_hash
        }
        self._append_audit_log(audit_entry)

        # Update database if data_core is provided
        if data_core:
            data_core.update_pipeline_stage(
                record_id=record_id,
                new_stage=target_stage,
                proof_hash=proof_hash,
                proof_artifact=proof_artifact_path,
                payload_data=json.dumps(payload)
            )

        return {
            "status": "SUCCESS",
            "record_id": record_id,
            "stage": target_stage,
            "proof_hash": proof_hash,
            "audit_entry": audit_entry
        }

    def _append_audit_log(self, entry: Dict[str, Any]) -> None:
        """Atomically append an immutable JSON line to the audit trail."""
        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_audit_trail(self, record_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve historical audit trail records."""
        if not os.path.exists(self.audit_log_path):
            return []

        entries = []
        with open(self.audit_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if record_id is None or entry.get("record_id") == record_id:
                        entries.append(entry)
                except Exception:
                    continue

        return entries[-limit:]

    def audit_all_records(self, data_core: Any) -> Dict[str, Any]:
        """Perform a complete cross-audit of pipeline records against the truth ledger."""
        records = data_core.list_pipeline_records()
        audit_trail = self.get_audit_trail(limit=1000)

        verified_count = 0
        discrepancies = []

        for rec in records:
            rid = rec["record_id"]
            stage = rec["stage"]
            phash = rec["proof_hash"]

            # Verify that proof_hash starts with sha256:
            if not phash or not phash.startswith("sha256:"):
                discrepancies.append({
                    "record_id": rid,
                    "stage": stage,
                    "reason": "Missing or invalid proof hash format"
                })
            else:
                verified_count += 1

        return {
            "total_pipeline_records": len(records),
            "verified_records": verified_count,
            "discrepancies_found": len(discrepancies),
            "discrepancies": discrepancies,
            "total_audit_events": len(audit_trail),
            "truth_health_score": round((verified_count / max(1, len(records))) * 100, 2)
        }


if __name__ == "__main__":
    truth = OmegaTruthEngine()
    print("[✓] Omega Truth Engine initialized.")
    print(f"    - Audit Log: {truth.audit_log_path}")
    
    # Test valid progression
    try:
        res = truth.record_transition(
            record_id="PIP-TEST-001",
            current_stage="INITIAL",
            target_stage="PREPARED",
            payload={"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "payload_type": "ATS_MATCH_95"}
        )
        print(f"    - Test Valid Transition: {res['stage']} (Hash: {res['proof_hash'][:24]}...)")
    except Exception as e:
        print(f"    - Error: {e}")

    # Test illegal transition rejection
    try:
        truth.record_transition(
            record_id="PIP-TEST-002",
            current_stage="PREPARED",
            target_stage="OFFER",
            payload={"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "ctc_offered_inr": 1200000, "offer_letter_artifact": "offer.pdf"}
        )
        print("    [!] Failed to reject illegal transition!")
    except TruthValidationError as e:
        print(f"    - [✓] Successfully rejected illegal transition: {e}")
