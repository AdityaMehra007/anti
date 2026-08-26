"""
OMEGA CONTROL PLANE - Reconciliation Engine
Compares Local Records vs External Records vs Expected Results and creates incident logs on mismatch.
"""
import time
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

class ReconciliationStatus(str, Enum):
    MATCH = "MATCH"
    MISMATCH = "MISMATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    UNKNOWN = "UNKNOWN"

@dataclass
class ReconciliationIncident:
    incident_id: str
    transaction_id: str
    gateway: str
    mismatch_fields: List[str]
    local_value: Any
    external_value: Any
    severity: str # CRITICAL, WARNING, INFO
    created_at: float = field(default_factory=time.time)
    resolved: bool = False

class OmegaReconciliationEngine:
    def __init__(self):
        self.incidents: List[ReconciliationIncident] = []

    def reconcile_transaction(
        self,
        transaction_id: str,
        gateway: str,
        local_record: Dict[str, Any],
        external_record: Optional[Dict[str, Any]],
        expected_fields: List[str]
    ) -> Dict[str, Any]:
        """Performs a deep field-by-field reconciliation audit."""
        if not external_record:
            return {
                "transaction_id": transaction_id,
                "status": ReconciliationStatus.UNKNOWN.value,
                "reason": "No external record available for reconciliation."
            }

        mismatches = []
        for f in expected_fields:
            loc = local_record.get(f)
            ext = external_record.get(f)
            if loc != ext:
                mismatches.append(f"{f}: Local '{loc}' != External '{ext}'")

        if len(mismatches) == 0:
            return {
                "transaction_id": transaction_id,
                "gateway": gateway,
                "status": ReconciliationStatus.MATCH.value,
                "audit_timestamp": time.time()
            }
        elif len(mismatches) < len(expected_fields):
            incident = ReconciliationIncident(
                incident_id=f"INC-{transaction_id}",
                transaction_id=transaction_id,
                gateway=gateway,
                mismatch_fields=mismatches,
                local_value=local_record,
                external_value=external_record,
                severity="WARNING"
            )
            self.incidents.append(incident)
            return {
                "transaction_id": transaction_id,
                "gateway": gateway,
                "status": ReconciliationStatus.PARTIAL_MATCH.value,
                "mismatches": mismatches,
                "incident_id": incident.incident_id
            }
        else:
            incident = ReconciliationIncident(
                incident_id=f"INC-{transaction_id}",
                transaction_id=transaction_id,
                gateway=gateway,
                mismatch_fields=mismatches,
                local_value=local_record,
                external_value=external_record,
                severity="CRITICAL"
            )
            self.incidents.append(incident)
            return {
                "transaction_id": transaction_id,
                "gateway": gateway,
                "status": ReconciliationStatus.MISMATCH.value,
                "mismatches": mismatches,
                "incident_id": incident.incident_id
            }

if __name__ == "__main__":
    rec = OmegaReconciliationEngine()
    loc = {"amount": 5000, "currency": "INR", "status": "PAID"}
    ext = {"amount": 5000, "currency": "INR", "status": "PAID"}
    res = rec.reconcile_transaction("TX-101", "RAZORPAY", loc, ext, ["amount", "currency", "status"])
    print("[RECONCILIATION] Match Test:", res["status"])
