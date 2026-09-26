"""Credit Monitor - Credit-Readiness & Financing Radar.

Monitors banking relationship tenure, invoice cleanliness,
statutory tax filing track record, and non-dilutive credit eligibility.
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.models import ActionTier
from ..core.database import db


class CreditMonitor(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="CreditMonitor",
            role_description="Credit-readiness evaluator preparing transparent, auditable borrowing profiles without financial fabrication."
        )

    def assess_credit_readiness(self) -> dict[str, Any]:
        """Assesses corporate creditworthiness and non-dilutive financing eligibility."""
        self.check_permission(ActionTier.ANALYZE)

        with db.get_connection() as conn:
            cur = conn.cursor()
            # 1. Check existing debt defaults
            cur.execute("SELECT COUNT(*) FROM debt_facilities WHERE principal_inr > 0")
            existing_facilities = cur.fetchone()[0]

            # 2. Check reconciled revenue history
            cur.execute("""
                SELECT COUNT(*), COALESCE(SUM(amount_inr), 0.0)
                FROM transactions WHERE category IN ('REVENUE_CUSTOMER', 'REVENUE_PILOT') AND status = 'RECONCILED'
            """)
            rev_row = cur.fetchone()
            completed_invoices = rev_row[0]
            total_rev_inr = rev_row[1]

            # 3. Tax compliance
            cur.execute("SELECT balance_inr FROM bank_accounts WHERE id = 'ACC-IN-TAX-01'")
            tax_bal = cur.fetchone()[0]

        # Scoring metrics
        score = 50.0  # Base score for clean legal entity
        if completed_invoices >= 1:
            score += 15.0
        if completed_invoices >= 5:
            score += 15.0
        if tax_bal > 0:
            score += 10.0
        if existing_facilities == 0:
            score += 10.0  # Debt-free bonus

        readiness = {
            "credit_readiness_score": min(100.0, score),
            "completed_verified_invoices": completed_invoices,
            "total_verified_revenue_inr": total_rev_inr,
            "existing_debt_obligations": existing_facilities,
            "tax_reserve_healthy": tax_bal > 0,
            "eligible_financing_categories": [
                "Invoice Discounting (once B2B volume exceeds ₹5L/mo)",
                "Non-dilutive Revenue-Based Financing (RBF)",
                "Bank Working Capital Overdraft against Term Deposits"
            ],
            "governance_rule": "NEVER fabricate financial records to obtain credit. Transparency is non-negotiable."
        }
        self.log_action("CREDIT_READINESS_ASSESSED", readiness)
        return readiness


credit_monitor = CreditMonitor()
