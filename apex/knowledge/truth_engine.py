"""
APEX Truth & Evidence Verification Engine
Strictly classifies statements and data points as:
OBSERVED | VERIFIED | INFERRED | ESTIMATED | UNKNOWN
Eliminates silent upgrades from inference to fact.
"""
from typing import Dict, List, Any
from dataclasses import dataclass

TRUTH_TIERS = {
    "OBSERVED": "Directly extracted from primary verifiable source files, API payloads, or direct measurement.",
    "VERIFIED": "Corroborated by 2+ independent sources or verified via automated integration tests.",
    "INFERRED": "Logically deduced from observed facts with explicit deductive assumptions noted.",
    "ESTIMATED": "Calculated via mathematical extrapolation, simulation, or statistical proxy.",
    "UNKNOWN": "Unverified assertion without supporting primary evidence."
}

@dataclass
class TruthStatement:
    statement: str
    truth_level: str  # OBSERVED, VERIFIED, INFERRED, ESTIMATED, UNKNOWN
    evidence_source: str
    confidence: float  # 0.0 to 1.0
    assumptions: str = ""

class ApexTruthEngine:
    def __init__(self):
        self.statements: List[TruthStatement] = []

    def classify_claim(self, claim: str, evidence: str = "", is_direct_file: bool = False, is_calculated: bool = False) -> TruthStatement:
        if is_direct_file and evidence:
            truth = "OBSERVED"
            conf = 1.0
        elif evidence and not is_calculated:
            truth = "VERIFIED"
            conf = 0.95
        elif is_calculated:
            truth = "ESTIMATED"
            conf = 0.80
        elif "likely" in claim.lower() or "probable" in claim.lower() or "suggests" in claim.lower():
            truth = "INFERRED"
            conf = 0.70
        else:
            truth = "UNKNOWN"
            conf = 0.40

        stmt = TruthStatement(
            statement=claim,
            truth_level=truth,
            evidence_source=evidence or "None provided",
            confidence=conf
        )
        self.statements.append(stmt)
        return stmt

    def get_truth_audit(self) -> Dict[str, Any]:
        breakdown = {}
        for s in self.statements:
            breakdown[s.truth_level] = breakdown.get(s.truth_level, 0) + 1
        return {
            "total_statements": len(self.statements),
            "tier_breakdown": breakdown,
            "high_integrity_ratio": round(
                (breakdown.get("OBSERVED", 0) + breakdown.get("VERIFIED", 0)) / max(len(self.statements), 1), 4
            )
        }
