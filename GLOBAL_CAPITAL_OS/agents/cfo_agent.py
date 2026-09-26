"""CFO Agent - Financial Controller for GLOBAL CAPITAL OS.

Responsible for P&L generation, contribution profit vs operating profit calculation,
burn rate analysis, and monthly closing statements.
"""

from typing import Any
from datetime import datetime
from .base_agent import BaseFinancialAgent
from ..core.models import ActionTier
from ..core.database import db


class CFOAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="CFOAgent",
            role_description="Financial controller overseeing P&L reporting, unit contribution margins, and balance sheet reconciliation."
        )

    def generate_pl_statement(self, period_days: int = 30) -> dict[str, Any]:
        """Calculates Revenue, Variable Costs, Contribution Profit, Fixed Costs, and Operating Profit."""
        self.check_permission(ActionTier.ANALYZE)

        with db.get_connection() as conn:
            cur = conn.cursor()
            # 1. Total Recognized Revenue
            cur.execute("""
                SELECT COALESCE(SUM(amount_inr), 0.0) FROM transactions
                WHERE category IN ('REVENUE_CUSTOMER', 'REVENUE_PILOT')
                AND status IN ('RECONCILED', 'APPROVED')
                AND timestamp >= date('now', ?)
            """, (f"-{period_days} days",))
            gross_revenue_inr = float(cur.fetchone()[0])

            # 2. Variable Costs (AI, Gateway fees, contractor per-unit delivery)
            cur.execute("""
                SELECT COALESCE(SUM(amount_inr), 0.0) FROM transactions
                WHERE category IN ('COST_AI', 'COST_PAYMENT_FEE')
                AND timestamp >= date('now', ?)
            """, (f"-{period_days} days",))
            variable_costs_inr = float(cur.fetchone()[0])

            # 3. Fixed Costs (Infra, Software, Professional/Compliance)
            cur.execute("""
                SELECT COALESCE(SUM(amount_inr), 0.0) FROM transactions
                WHERE category IN ('COST_INFRA', 'COST_SOFTWARE', 'COST_PROFESSIONAL', 'COST_TAX')
                AND timestamp >= date('now', ?)
            """, (f"-{period_days} days",))
            fixed_costs_inr = float(cur.fetchone()[0])

        contribution_profit_inr = gross_revenue_inr - variable_costs_inr
        operating_profit_inr = contribution_profit_inr - fixed_costs_inr
        gross_margin_pct = (contribution_profit_inr / gross_revenue_inr * 100.0) if gross_revenue_inr > 0 else 0.0
        net_margin_pct = (operating_profit_inr / gross_revenue_inr * 100.0) if gross_revenue_inr > 0 else 0.0

        pl_statement = {
            "period_days": period_days,
            "gross_revenue_inr": gross_revenue_inr,
            "variable_costs_inr": variable_costs_inr,
            "contribution_profit_inr": contribution_profit_inr,
            "gross_margin_pct": round(gross_margin_pct, 2),
            "fixed_costs_inr": fixed_costs_inr,
            "operating_profit_inr": operating_profit_inr,
            "net_margin_pct": round(net_margin_pct, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
        self.log_action("PL_STATEMENT_GENERATED", pl_statement)
        return pl_statement


cfo_agent = CFOAgent()
