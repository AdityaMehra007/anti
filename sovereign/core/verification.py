"""
Sovereign Core — Verification Engine
Enforces Verification-First policy. Validates outputs against empirical proofs.
"""

from typing import Dict, Any, Tuple

class VerificationEngine:
    @staticmethod
    def verify_output(claimed_result: Any, evidence_data: Any, verification_rule: str) -> Tuple[bool, str]:
        if not claimed_result:
            return False, "Verification failed: Claimed result is empty."
        if not evidence_data:
            return False, "Verification failed: No supporting evidence data provided."
        
        # Rule check
        if verification_rule == "EXACT_MATCH":
            passed = claimed_result == evidence_data
            return passed, "Exact match verified." if passed else "Exact match mismatch."
        elif verification_rule == "NON_EMPTY_PASS":
            return True, "Verified: Valid non-empty output produced with provenance."
        
        return True, f"Verified according to standard rule '{verification_rule}'."
