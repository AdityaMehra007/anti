"""Base Agent Architecture for GLOBAL CAPITAL OS Financial Agents.

Enforces strict permission boundaries, tamper-evident audit logging,
and standardized consequential action proposal structures.
"""

from typing import Any, Optional
from datetime import datetime
from ..core.config import settings
from ..core.models import ActionTier, RiskLevel, ApprovalStatus, LegalCheckStatus, CurrencyCode
from ..core.security import security
from ..core.audit import audit
from ..core.database import db


class BaseFinancialAgent:
    def __init__(self, agent_name: str, role_description: str):
        self.agent_name = agent_name
        self.role_description = role_description
        self.allowed_tiers = [
            ActionTier.READ, ActionTier.ANALYZE, ActionTier.SIMULATE,
            ActionTier.RECOMMEND, ActionTier.PREPARE
        ]

    def check_permission(self, tier: ActionTier, amount_inr: float = 0.0) -> bool:
        """Verifies that the agent is permitted to perform this action tier."""
        security.validate_action_permissions(self.agent_name, tier, amount_inr)
        return True

    def log_action(self, action_name: str, details: dict[str, Any]) -> str:
        """Logs an event to the immutable audit chain."""
        return audit.log_event(self.agent_name, action_name, details)

    def prepare_approval_request(
        self,
        action_type: str,
        amount: float,
        currency: CurrencyCode,
        source_account: str,
        destination: str,
        purpose: str,
        expected_benefit: str,
        worst_case_loss: str,
        legal_status: LegalCheckStatus,
        tax_considerations: str,
        risk_level: RiskLevel,
        recommendation: str,
        alternatives: str
    ) -> dict[str, Any]:
        """Creates a standardized Money Approval Card for Founder review."""
        self.check_permission(ActionTier.PREPARE, amount * settings.DEFAULT_FX_RATES.get(currency.value, 1.0))
        
        amount_inr = amount * settings.DEFAULT_FX_RATES.get(currency.value, 1.0)
        approval_id = f"APPR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{self.agent_name[:4].upper()}"

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO approvals (
                    id, requester_agent, action_type, amount, currency, amount_inr,
                    source_account, destination, purpose, expected_benefit, worst_case_loss,
                    legal_status, tax_considerations, risk_level, recommendation, alternatives, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
            """, (
                approval_id, self.agent_name, action_type, amount, currency.value, amount_inr,
                source_account, destination, purpose, expected_benefit, worst_case_loss,
                legal_status.value, tax_considerations, risk_level.value, recommendation, alternatives
            ))
            conn.commit()

        req_payload = {
            "id": approval_id,
            "requester": self.agent_name,
            "action_type": action_type,
            "amount": amount,
            "currency": currency.value,
            "amount_inr": amount_inr,
            "source": source_account,
            "destination": destination,
            "purpose": purpose,
            "benefit": expected_benefit,
            "worst_case_loss": worst_case_loss,
            "legal_status": legal_status.value,
            "risk_level": risk_level.value,
            "status": "PENDING_FOUNDER_DECISION"
        }
        self.log_action("APPROVAL_REQUEST_PREPARED", req_payload)
        return req_payload
