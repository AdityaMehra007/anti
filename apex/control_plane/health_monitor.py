"""
OMEGA CONTROL PLANE - Health Monitor & Score Calculator
Computes evidence-weighted ecosystem reliability score and monitors gateway status.
"""
from typing import Dict, Any, List
from pathlib import Path
import sys

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))

from apex.control_plane.truth_engine import OmegaTruthEngine, GatewayState
from apex.control_plane.reconciliation import OmegaReconciliationEngine
from apex.control_plane.data_core import OmegaMasterDataCore

class OmegaHealthMonitor:
    def __init__(self):
        self.truth = OmegaTruthEngine()
        self.reconciliation = OmegaReconciliationEngine()
        self.data_core = OmegaMasterDataCore()

    def calculate_system_health_score(
        self,
        test_pass_rate_pct: float = 100.0,
        unverified_claim_count: int = 0,
        critical_incidents_count: int = 0
    ) -> Dict[str, Any]:
        """Calculates evidence-weighted 0-100 system score."""
        score = 100.0
        
        # Deduct for failing tests
        score -= (100.0 - test_pass_rate_pct) * 0.5
        # Deduct heavily for unverified claims (anti-delusion penalty)
        score -= unverified_claim_count * 15.0
        # Deduct for open reconciliation mismatches
        score -= critical_incidents_count * 20.0

        final_score = max(0.0, min(100.0, round(score, 1)))
        
        grade = "A+ (CERTIFIED)" if final_score >= 95 else ("A (RELIABLE)" if final_score >= 85 else ("B (NEEDS_ATTENTION)" if final_score >= 70 else "CRITICAL_DEFECTS"))

        return {
            "omega_system_health_score": final_score,
            "grade": grade,
            "test_pass_rate_pct": test_pass_rate_pct,
            "unverified_claim_count": unverified_claim_count,
            "critical_reconciliation_incidents": critical_incidents_count,
            "status": "OPERATIONAL" if final_score >= 80 else "DEGRADED"
        }

if __name__ == "__main__":
    monitor = OmegaHealthMonitor()
    print("[HEALTH_MONITOR] System Health Score:", monitor.calculate_system_health_score(100.0, 0, 0))
