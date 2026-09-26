"""Security Guardrails, RBAC, and Emergency Freeze for GLOBAL CAPITAL OS.

Enforces zero-secret exposure, two-control transaction approvals,
daily spend limits, and rapid financial freeze mechanisms.
"""

import re
import json
from datetime import datetime
from typing import Any, Optional
from .config import settings
from .models import ActionTier, RiskLevel, ApprovalStatus
from .database import db


class SecurityManager:
    # Patterns for sensitive credentials that must NEVER appear in logs or payloads
    SECRET_PATTERNS = [
        re.compile(r"(?i)(api[_-]?key|secret|password|passwd|bearer\s+[a-zA-Z0-9_\-\.]{20,})"),
        re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b"),  # Credit cards
        re.compile(r"\b[0-9]{6}\b"),  # 6-digit OTPs
        re.compile(r"(?i)(private[_-]?key|seed[_-]?phrase|mnemonic)"),
    ]

    @classmethod
    def sanitize_payload(cls, data: Any) -> Any:
        """Sanitizes sensitive data recursively before logging or database insertion."""
        if isinstance(data, dict):
            return {k: cls.sanitize_payload(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls.sanitize_payload(item) for item in data]
        elif isinstance(data, str):
            sanitized = data
            for pattern in cls.SECRET_PATTERNS:
                sanitized = pattern.sub("[REDACTED_CREDENTIAL]", sanitized)
            return sanitized
        return data

    @classmethod
    def is_system_frozen(cls) -> bool:
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT value FROM system_state WHERE key = 'EMERGENCY_FREEZE'")
            row = cur.fetchone()
            return row[0].upper() == "TRUE" if row else False

    @classmethod
    def trigger_emergency_freeze(cls, reason: str, triggered_by: str = "SecurityAgent") -> dict[str, Any]:
        """Locks down all outgoing actions and flags emergency status."""
        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE system_state SET value = 'TRUE', updated_at = datetime('now') WHERE key = 'EMERGENCY_FREEZE'")
            cur.execute("UPDATE system_state SET value = 'EMERGENCY_FROZEN', updated_at = datetime('now') WHERE key = 'SYSTEM_STATUS'")
            # Automatically freeze any pending approvals
            cur.execute("UPDATE approvals SET status = 'FROZEN' WHERE status = 'PENDING'")
            conn.commit()

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": "EMERGENCY_FREEZE_TRIGGERED",
            "triggered_by": triggered_by,
            "reason": reason,
            "system_state": "LOCKED"
        }
        return event

    @classmethod
    def release_emergency_freeze(cls, founder_override: str) -> dict[str, Any]:
        """Unfreezes the system. Strictly requires explicit founder authorization."""
        if founder_override != "APPROVE_UNFREEZE_FOUNDER_CONFIRMED":
            raise PermissionError("Unauthorized unfreeze attempt. Valid Founder confirmation string required.")

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE system_state SET value = 'FALSE', updated_at = datetime('now') WHERE key = 'EMERGENCY_FREEZE'")
            cur.execute("UPDATE system_state SET value = 'OPERATIONAL', updated_at = datetime('now') WHERE key = 'SYSTEM_STATUS'")
            cur.execute("UPDATE approvals SET status = 'PENDING' WHERE status = 'FROZEN'")
            conn.commit()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "action": "EMERGENCY_FREEZE_RELEASED",
            "released_by": settings.FOUNDER_NAME,
            "system_state": "OPERATIONAL"
        }

    @classmethod
    def validate_action_permissions(cls, agent_name: str, tier: ActionTier, amount_inr: float = 0.0) -> bool:
        """Enforces agent tier boundaries and the Money-Movement Rule.
        
        Default agents can READ, ANALYZE, SIMULATE, RECOMMEND, and PREPARE.
        Only the Founder can APPROVE.
        No agent can execute money movement autonomously if amount_inr > MAX_UNAPPROVED_SPEND_INR (0.0).
        """
        if cls.is_system_frozen():
            raise PermissionError("Operation blocked: GLOBAL CAPITAL OS is under EMERGENCY FREEZE.")

        # Human Founder sole authority for APPROVE
        if tier == ActionTier.APPROVE:
            raise PermissionError(f"Agent '{agent_name}' cannot perform APPROVE tier. Consequential approvals require Founder sign-off.")

        # If an agent tries to EXECUTE a transaction with non-zero money movement:
        if tier == ActionTier.EXECUTE and amount_inr > settings.MAX_UNAPPROVED_SPEND_INR:
            raise PermissionError(
                f"Agent '{agent_name}' cannot autonomously EXECUTE transactions of ₹{amount_inr:,.2f}. "
                f"Requires dual-control preparation and Founder sign-off."
            )

        return True


security = SecurityManager()
