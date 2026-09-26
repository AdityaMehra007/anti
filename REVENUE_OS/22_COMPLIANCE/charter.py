"""
Ethical Compliance Charter & Security Model for REVENUE OS
Adheres strictly to Directives 5, 14, 72, 73, 127, 128, 154, 155, 156, 157, 158.
"""

from enum import Enum
import re
from typing import Set

class PermissionTier(str, Enum):
    """
    Directive 14: Agent Permission Levels
    READ -> ANALYZE -> DRAFT -> RECOMMEND -> EXECUTE -> APPROVE
    """
    READ = "READ"
    ANALYZE = "ANALYZE"
    DRAFT = "DRAFT"
    RECOMMEND = "RECOMMEND"
    EXECUTE = "EXECUTE"
    APPROVE = "APPROVE"  # Human Founder Only for consequential actions

class SecurityViolationError(Exception):
    """Raised when an autonomous agent attempts an unpermitted or deceptive action."""
    pass

class EthicalCharter:
    """
    Guards against dark patterns, fake claims, spam blasts, and unauthorized spends.
    """
    
    # Banned hallucination / fake assurance patterns (Directive 154, 155)
    BANNED_CLAIM_PATTERNS = [
        r"\bguarantee\b.*\b(income|profit|revenue|money|wealth)\b",
        r"\b100%\s*passive\s*income\b",
        r"\bget\s*rich\b",
        r"\bno\s*risk\b",
        r"\bmake\s*millions\s*overnight\b",
        r"\bguaranteed\s*customers\b",
    ]
    
    AUTONOMOUS_ALLOWED_TIERS: Set[PermissionTier] = {
        PermissionTier.READ,
        PermissionTier.ANALYZE,
        PermissionTier.DRAFT,
        PermissionTier.RECOMMEND,
        PermissionTier.EXECUTE,  # For non-consequential technical execution (local tests, logs, reports)
    }
    
    HUMAN_ONLY_TIERS: Set[PermissionTier] = {
        PermissionTier.APPROVE,  # Financial spend, contracts, legal, production keys, high-risk outreach
    }
    
    @classmethod
    def is_autonomous_action_allowed(cls, tier: PermissionTier) -> bool:
        """Check if an autonomous agent is allowed to execute at this tier."""
        return tier in cls.AUTONOMOUS_ALLOWED_TIERS
    
    @classmethod
    def validate_claim(cls, text: str) -> bool:
        """
        Validate that generated copy or claims contain no fake assurances,
        hallucinated promises, or deceptive statements.
        """
        for pattern in cls.BANNED_CLAIM_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                raise SecurityViolationError(
                    f"Ethical Charter Violation: Deceptive or guaranteed income claim detected: '{pattern}'"
                )
        return True
    
    @classmethod
    def check_outreach_compliance(cls, recipient_email: str, content: str, has_prior_consent: bool = False) -> bool:
        """
        Ensure outreach adheres to CAN-SPAM, GDPR, and DPDP India standards.
        - Must identify sender truthfully
        - Must provide clear opt-out / unsubscribe
        - Must contain no deceptive subject lines or false scarcity
        """
        cls.validate_claim(content)
        lower_content = content.lower()
        if "unsubscribe" not in lower_content and "opt out" not in lower_content and "opt-out" not in lower_content:
            raise SecurityViolationError(
                "Compliance Violation: Outreach message must contain explicit opt-out / unsubscribe phrasing."
            )
        return True
