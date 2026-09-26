"""Portfolio Analyst - Holdings & Asset Quality Monitor.

Monitors approved liquid treasury holdings, asset allocation percentages,
unrealized gains/losses, concentration risk, and kill condition breaches.
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.models import ActionTier
from ..core.database import db


class PortfolioAnalyst(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="PortfolioAnalyst",
            role_description="Portfolio monitor tracking treasury holdings, mark-to-market valuations, and concentration risks."
        )

    def get_portfolio_summary(self) -> dict[str, Any]:
        """Calculates current portfolio allocation, value, and unrealized returns."""
        self.check_permission(ActionTier.READ)

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, asset_name, asset_type, cost_basis_inr, current_value_inr,
                       unrealized_pnl_inr, allocation_pct, thesis, kill_condition
                FROM investments WHERE is_authorized = 1
            """)
            holdings = [dict(r) for r in cur.fetchall()]

        total_cost = sum(h["cost_basis_inr"] for h in holdings)
        total_val = sum(h["current_value_inr"] for h in holdings)
        unrealized_pnl = total_val - total_cost

        summary = {
            "total_holdings_count": len(holdings),
            "total_cost_basis_inr": total_cost,
            "total_current_value_inr": total_val,
            "unrealized_pnl_inr": unrealized_pnl,
            "holdings": holdings,
            "concentration_status": "DIVERSIFIED" if len(holdings) >= 3 else "CONCENTRATED",
            "statutory_mandate": "Never hide operating business performance behind treasury investment gains."
        }
        self.log_action("PORTFOLIO_SUMMARY_GENERATED", summary)
        return summary


portfolio_analyst = PortfolioAnalyst()
