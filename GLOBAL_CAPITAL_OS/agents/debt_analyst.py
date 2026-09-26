"""Debt Analyst - Borrowing Scrutiny & Leverage Safety Auditor.

Enforces absolute anti-leverage discipline: Borrowing is a tool, not income.
Never borrow merely to look bigger. Expected return must significantly exceed
all-in cost of capital, and downside must remain survivable.
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.models import ActionTier
from ..core.database import db


class DebtAnalyst(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="DebtAnalyst",
            role_description="Prudential debt analyst stress-testing borrowing proposals, cost of capital, and covenant safety."
        )

    def evaluate_borrowing_proposal(
        self,
        lender: str,
        principal_inr: float,
        interest_rate_apr: float,
        tenure_months: int,
        processing_fee_pct: float,
        projected_incremental_monthly_profit: float
    ) -> dict[str, Any]:
        """Evaluates whether borrowing is mathematically, strategically, and safely justified."""
        self.check_permission(ActionTier.ANALYZE)

        # Monthly EMI calculation (standard amortization)
        r = (interest_rate_apr / 100.0) / 12.0
        n = tenure_months
        emi_inr = (principal_inr * r * ((1 + r)**n)) / (((1 + r)**n) - 1) if r > 0 else (principal_inr / n)
        total_interest_inr = (emi_inr * n) - principal_inr
        processing_fee_inr = principal_inr * (processing_fee_pct / 100.0)
        all_in_cost_inr = total_interest_inr + processing_fee_inr
        effective_apr = ((all_in_cost_inr / principal_inr) / (tenure_months / 12.0)) * 100.0

        # DSCR (Debt Service Coverage Ratio)
        dscr = projected_incremental_monthly_profit / emi_inr if emi_inr > 0 else 0.0

        # Downside stress test: What if incremental profit is 50% lower?
        stressed_dscr = (projected_incremental_monthly_profit * 0.50) / emi_inr if emi_inr > 0 else 0.0

        is_approved = (dscr >= 2.0) and (stressed_dscr >= 1.2)

        verdict = {
            "lender": lender,
            "principal_inr": principal_inr,
            "interest_rate_apr": interest_rate_apr,
            "effective_all_in_apr": round(effective_apr, 2),
            "monthly_emi_inr": round(emi_inr, 2),
            "total_all_in_cost_inr": round(all_in_cost_inr, 2),
            "dscr_normal": round(dscr, 2),
            "dscr_stressed_50pct_downside": round(stressed_dscr, 2),
            "recommendation": "APPROVED_FOR_REVIEW" if is_approved else "REJECT_EXCESSIVE_LEVERAGE_RISK",
            "statutory_reminder": "Borrowing is a liability, not income. Debt proceeds must never be recognized as revenue or profit."
        }
        self.log_action("DEBT_PROPOSAL_ANALYZED", verdict)
        return verdict


debt_analyst = DebtAnalyst()
