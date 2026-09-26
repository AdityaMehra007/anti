"""
Sovereign Core — Security Gates & Autonomy Tier Manager
Enforces least-privilege boundaries and Human Checkpoint authorization.
"""

class AutonomyTier:
    OBSERVE_ONLY = 0
    ANALYZE_RECOMMEND = 1
    DRAFT_ARTIFACTS = 2
    REVERSIBLE_EXECUTION = 3
    APPROVED_EXTERNAL = 4
    HIGH_AUTONOMY_SANDBOX = 5

class SecurityGate:
    @staticmethod
    def check_authorization(action_name: str, required_tier: int, current_tier: int, is_human_approved: bool = False) -> bool:
        if required_tier >= AutonomyTier.APPROVED_EXTERNAL:
            return is_human_approved
        return current_tier >= required_tier

    @staticmethod
    def sanitize_untrusted_input(content: str) -> str:
        """Strips prompt injection triggers and flags override attempts."""
        lowered = content.lower()
        forbidden_phrases = [
            "ignore previous instructions",
            "ignore all instructions",
            "system prompt override",
            "disregard safety guidelines",
            "reveal system prompt"
        ]
        for phrase in forbidden_phrases:
            if phrase in lowered:
                return f"[UNTRUSTED CONTENT FLAGGED & NEUTRALIZED: Detected prompt injection phrase '{phrase}']"
        return content
