"""
OMEGA CONTROL PLANE - Truth Engine
Enforces the Zero-Trust Protocol, distinguishes Local vs External evidence,
and rejects unsupported operational claims.
"""
import time
from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

class EvidenceTier(str, Enum):
    LEVEL_1_PAYMENT_TRANSACTION = "LEVEL_1_PAYMENT_TRANSACTION"
    LEVEL_2_VERIFIED_USAGE = "LEVEL_2_VERIFIED_USAGE"
    LEVEL_3_CUSTOMER_STATEMENT = "LEVEL_3_CUSTOMER_STATEMENT"
    LEVEL_4_MARKET_DEMAND = "LEVEL_4_MARKET_DEMAND"
    LEVEL_5_COMPETITOR_TRACTION = "LEVEL_5_COMPETITOR_TRACTION"
    LEVEL_6_SEARCH_PUBLIC_SIGNAL = "LEVEL_6_SEARCH_PUBLIC_SIGNAL"
    LEVEL_7_EXPERT_OPINION = "LEVEL_7_EXPERT_OPINION"
    LEVEL_8_AI_ASSUMPTION = "LEVEL_8_AI_ASSUMPTION"

class GatewayState(str, Enum):
    LOCAL = "LOCAL"
    SIMULATED = "SIMULATED"
    SANDBOX = "SANDBOX"
    CONNECTED = "CONNECTED"
    LIVE = "LIVE"
    LIVE_VERIFIED = "LIVE_VERIFIED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    REAUTH_REQUIRED = "REAUTH_REQUIRED"
    BLOCKED = "BLOCKED"

@dataclass
class TruthAssertion:
    assertion_id: str
    claim: str
    gateway: str
    is_external: bool
    evidence_tier: EvidenceTier
    gateway_state: GatewayState
    evidence_payload: Dict[str, Any]
    verified: bool = False
    rejection_reason: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

class OmegaTruthEngine:
    def __init__(self):
        self.assertions_log: List[TruthAssertion] = []

    def evaluate_claim(
        self,
        assertion_id: str,
        claim: str,
        gateway: str,
        gateway_state: GatewayState,
        evidence_tier: EvidenceTier,
        evidence_payload: Dict[str, Any]
    ) -> TruthAssertion:
        """Evaluates an operational claim with strict evidence verification."""
        is_external = gateway_state in [GatewayState.CONNECTED, GatewayState.LIVE, GatewayState.LIVE_VERIFIED]
        
        # Rule 1: A claim of LIVE_VERIFIED requires Level 1 or 2 evidence with external transaction reference
        if gateway_state == GatewayState.LIVE_VERIFIED:
            has_ext_ref = bool(evidence_payload.get("external_reference"))
            is_valid_tier = evidence_tier in [EvidenceTier.LEVEL_1_PAYMENT_TRANSACTION, EvidenceTier.LEVEL_2_VERIFIED_USAGE]
            if not (has_ext_ref and is_valid_tier):
                assertion = TruthAssertion(
                    assertion_id=assertion_id,
                    claim=claim,
                    gateway=gateway,
                    is_external=is_external,
                    evidence_tier=evidence_tier,
                    gateway_state=GatewayState.SANDBOX if "sandbox" in str(evidence_payload).lower() else GatewayState.LOCAL,
                    evidence_payload=evidence_payload,
                    verified=False,
                    rejection_reason="Rejected LIVE_VERIFIED claim: Missing external reference or insufficient evidence tier."
                )
                self.assertions_log.append(assertion)
                return assertion

        # Rule 2: Cannot claim PAID or SUBMITTED on LOCAL or SIMULATED state
        if gateway_state in [GatewayState.LOCAL, GatewayState.SIMULATED]:
            if any(forbidden in claim.upper() for forbidden in ["PAID", "SUBMITTED_TO_ICEGATE", "APPLICATION_DELIVERED"]):
                assertion = TruthAssertion(
                    assertion_id=assertion_id,
                    claim=claim,
                    gateway=gateway,
                    is_external=False,
                    evidence_tier=evidence_tier,
                    gateway_state=gateway_state,
                    evidence_payload=evidence_payload,
                    verified=False,
                    rejection_reason=f"Cannot assert external action '{claim}' on a {gateway_state.value} gateway."
                )
                self.assertions_log.append(assertion)
                return assertion

        # Validated assertion
        assertion = TruthAssertion(
            assertion_id=assertion_id,
            claim=claim,
            gateway=gateway,
            is_external=is_external,
            evidence_tier=evidence_tier,
            gateway_state=gateway_state,
            evidence_payload=evidence_payload,
            verified=True,
            rejection_reason=None
        )
        self.assertions_log.append(assertion)
        return assertion

    def get_audit_summary(self) -> Dict[str, Any]:
        total = len(self.assertions_log)
        verified = sum(1 for a in self.assertions_log if a.verified)
        rejected = total - verified
        return {
            "total_assertions_evaluated": total,
            "verified_truthful": verified,
            "rejected_delusions": rejected,
            "compliance_rate_pct": round((verified / total * 100) if total > 0 else 100.0, 2)
        }

if __name__ == "__main__":
    te = OmegaTruthEngine()
    # Test valid sandbox claim
    res1 = te.evaluate_claim("A1", "Razorpay Sandbox Link Generated", "RAZORPAY", GatewayState.SANDBOX, EvidenceTier.LEVEL_4_MARKET_DEMAND, {"short_url": "https://rzp.io/test"})
    print("[TRUTH_ENGINE] Valid Claim:", res1.verified, res1.gateway_state)
    # Test invalid live claim
    res2 = te.evaluate_claim("A2", "Customs Filing PAID and Accepted", "ICEGATE", GatewayState.LOCAL, EvidenceTier.LEVEL_8_AI_ASSUMPTION, {})
    print("[TRUTH_ENGINE] False Claim Rejection:", res2.verified, res2.rejection_reason)
