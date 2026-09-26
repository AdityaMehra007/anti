"""Capital Commander - Primary Orchestrator for GLOBAL CAPITAL OS.

Responsible for overall liquidity health, capital preservation,
multi-asset telemetry, and synthesizing decision-ready capital actions.
Never independently moves material money.
"""

from typing import Any
from datetime import datetime
from .base_agent import BaseFinancialAgent
from ..core.config import settings
from ..core.models import ActionTier, RiskLevel, CurrencyCode, LegalCheckStatus
from ..core.database import db


class CapitalCommander(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="CapitalCommander",
            role_description="Primary capital orchestrator responsible for capital allocation, liquidity defense, and executive decision preparation."
        )

    def get_master_financial_posture(self) -> dict[str, Any]:
        """Calculates total cash, liquid reserves, debt, and runway across all accounts."""
        self.check_permission(ActionTier.READ)

        with db.get_connection() as conn:
            cur = conn.cursor()
            # 1. Bank Accounts Balances
            cur.execute("""
                SELECT category, currency, balance, balance_inr
                FROM bank_accounts WHERE is_active = 1
            """)
            accounts = cur.fetchall()

            total_cash_inr = sum(r["balance_inr"] for r in accounts if r["category"] != "INVESTMENT")
            liquid_investments_inr = sum(r["balance_inr"] for r in accounts if r["category"] == "INVESTMENT")

            # 2. Total Debt
            cur.execute("SELECT COALESCE(SUM(principal_inr), 0.0) FROM debt_facilities")
            total_debt_inr = float(cur.fetchone()[0])

            # 3. Monthly Burn (Operating Costs in last 30 days)
            cur.execute("""
                SELECT COALESCE(SUM(amount_inr), 0.0) FROM transactions
                WHERE category IN ('COST_AI', 'COST_INFRA', 'COST_SOFTWARE', 'COST_PAYMENT_FEE', 'COST_TAX', 'COST_PROFESSIONAL')
                AND timestamp >= date('now', '-30 days')
            """)
            monthly_burn_inr = float(cur.fetchone()[0])
            if monthly_burn_inr <= 0.0:
                monthly_burn_inr = 5000.0  # Baseline conservative operating floor

            # 4. Revenue & Profit MTD
            cur.execute("""
                SELECT COALESCE(SUM(amount_inr), 0.0) FROM transactions
                WHERE category IN ('REVENUE_CUSTOMER', 'REVENUE_PILOT')
                AND status IN ('RECONCILED', 'APPROVED')
                AND timestamp >= strftime('%Y-%m-01', 'now')
            """)
            revenue_mtd_inr = float(cur.fetchone()[0])
            profit_mtd_inr = revenue_mtd_inr - monthly_burn_inr

            # 5. Runway
            runway_months = (total_cash_inr + liquid_investments_inr) / monthly_burn_inr

            # 6. Pipeline Value
            cur.execute("SELECT COALESCE(SUM(expected_value_inr), 0.0), COUNT(*) FROM deals WHERE stage NOT IN ('WON', 'LOST')")
            row_deals = cur.fetchone()
            pipeline_value_inr = float(row_deals[0])
            active_deals_count = int(row_deals[1])

            # 7. Pending Approvals
            cur.execute("SELECT COUNT(*) FROM approvals WHERE status = 'PENDING'")
            pending_approvals_count = int(cur.fetchone()[0])

        posture = {
            "total_cash_inr": total_cash_inr,
            "liquid_assets_inr": liquid_investments_inr,
            "total_debt_inr": total_debt_inr,
            "net_capital_inr": (total_cash_inr + liquid_investments_inr) - total_debt_inr,
            "monthly_burn_inr": monthly_burn_inr,
            "runway_months": round(runway_months, 1),
            "revenue_mtd_inr": revenue_mtd_inr,
            "profit_mtd_inr": profit_mtd_inr,
            "pipeline_value_inr": pipeline_value_inr,
            "active_deals_count": active_deals_count,
            "pending_approvals_count": pending_approvals_count,
            "emergency_reserve_met": total_cash_inr >= (monthly_burn_inr * settings.EMERGENCY_RESERVE_MONTHS),
            "timestamp": datetime.utcnow().isoformat()
        }
        self.log_action("FINANCIAL_POSTURE_CALCULATED", posture)
        return posture

    def evaluate_capital_deployment(self, target: str, amount_inr: float, expected_roi_pct: float) -> dict[str, Any]:
        """Strictly tests whether funds can be safely deployed without breaching liquidity."""
        self.check_permission(ActionTier.ANALYZE, amount_inr)
        posture = self.get_master_financial_posture()

        emergency_buffer_needed = posture["monthly_burn_inr"] * settings.EMERGENCY_RESERVE_MONTHS
        free_cash = max(0.0, posture["total_cash_inr"] - emergency_buffer_needed)

        if amount_inr > free_cash:
            decision = {
                "allowed": False,
                "reason": f"Deployment of ₹{amount_inr:,.2f} would violate the 6-month Emergency Reserve requirement (Buffer: ₹{emergency_buffer_needed:,.2f}, Free: ₹{free_cash:,.2f}).",
                "recommendation": "REJECT OR DELAY until customer collections increase free cash."
            }
        else:
            decision = {
                "allowed": True,
                "reason": f"Free cash of ₹{free_cash:,.2f} exceeds required deployment. Expected ROI: {expected_roi_pct}%.",
                "recommendation": "PREPARE APPROVAL CARD for Founder Sign-Off."
            }

        self.log_action("CAPITAL_DEPLOYMENT_EVALUATED", {"target": target, "amount_inr": amount_inr, "decision": decision})
        return decision


capital_commander = CapitalCommander()
