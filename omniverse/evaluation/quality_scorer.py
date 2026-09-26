"""
ANTIGRAVITY OMNIVERSE: QUALITY INDEX & READINESS SCORER
=======================================================
Computes the multi-dimensional Omniverse Quality Index (OQI) and
evaluates production readiness across 8 categorical gates.
"""
from typing import Dict, Any, List

class QualityScorer:
    WEIGHTS = {
        "reliability": 0.15,
        "accuracy": 0.15,
        "latency": 0.10,
        "cost_efficiency": 0.10,
        "security": 0.15,
        "scalability": 0.05,
        "maintainability": 0.10,
        "usability": 0.05,
        "automation": 0.10,
        "observability": 0.05
    }

    @classmethod
    def compute_oqi(cls, scores: Dict[str, float]) -> float:
        """
        Calculates normalized Omniverse Quality Index (OQI) between 0.0 and 100.0.
        """
        total = 0.0
        for dim, weight in cls.WEIGHTS.items():
            s = scores.get(dim, 85.0)
            total += weight * max(0.0, min(100.0, s))
        return round(total, 2)

    @classmethod
    def evaluate_readiness(cls, gates: Dict[str, bool]) -> Dict[str, Any]:
        """
        Evaluates 8 categorical readiness gates.
        """
        required_gates = [
            "technical", "security", "data", "operational",
            "financial", "compliance", "user", "recovery"
        ]
        passed = [g for g in required_gates if gates.get(g, False)]
        score = (len(passed) / len(required_gates)) * 100.0
        return {
            "passed_gates": passed,
            "total_gates": len(required_gates),
            "readiness_percentage": round(score, 1),
            "production_ready": len(passed) == len(required_gates)
        }
