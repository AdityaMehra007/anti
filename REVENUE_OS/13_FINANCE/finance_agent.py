"""
Finance Agent for REVENUE OS
Adheres strictly to Directives 48, 49, 50, 51, 52, 53, 54.
Tracks revenue, costs, contribution margin, CAC/LTV, AI dollar ROI, and founder leverage.
"""

from typing import Any, Dict, Optional
from REVENUE_OS.database.db import DatabaseManager, get_db

class FinanceAgent:
    """
    Calculates P&L, contribution profit, and efficiency metrics.
    """
    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or get_db()

    def calculate_pnl(
        self,
        gross_revenue_inr: float,
        variable_costs_inr: float,
        fixed_costs_inr: float,
        ai_cost_usd: float,
        founder_hours: float,
        fx_usd_to_inr: float = 87.0
    ) -> Dict[str, Any]:
        """
        Directive 50: REVENUE - VARIABLE COST - FIXED COST = CONTRIBUTION / PROFIT
        Directive 51: REVENUE PER FOUNDER HOUR = Net Revenue / Founder Hours
        Directive 52: REVENUE PER AI DOLLAR = Gross Profit Created / AI Cost
        """
        ai_cost_inr = ai_cost_usd * fx_usd_to_inr
        total_costs_inr = variable_costs_inr + fixed_costs_inr
        gross_profit_inr = gross_revenue_inr - variable_costs_inr
        contribution_profit_inr = gross_revenue_inr - total_costs_inr
        
        gross_margin_pct = round((gross_profit_inr / gross_revenue_inr * 100.0), 1) if gross_revenue_inr > 0 else 0.0
        net_margin_pct = round((contribution_profit_inr / gross_revenue_inr * 100.0), 1) if gross_revenue_inr > 0 else 0.0
        
        rev_per_hour = round(contribution_profit_inr / founder_hours, 2) if founder_hours > 0 else 0.0
        rev_per_ai_dollar = round(gross_profit_inr / max(ai_cost_inr, 1.0), 2)
        
        result = {
            "gross_revenue_inr": gross_revenue_inr,
            "variable_costs_inr": variable_costs_inr,
            "fixed_costs_inr": fixed_costs_inr,
            "total_costs_inr": total_costs_inr,
            "gross_profit_inr": gross_profit_inr,
            "contribution_profit_inr": contribution_profit_inr,
            "gross_margin_pct": gross_margin_pct,
            "net_margin_pct": net_margin_pct,
            "ai_cost_usd": ai_cost_usd,
            "ai_cost_inr": ai_cost_inr,
            "founder_hours": founder_hours,
            "revenue_per_founder_hour_inr": rev_per_hour,
            "revenue_per_ai_dollar_ratio": rev_per_ai_dollar
        }
        
        self.db.log_audit(
            agent_name="FinanceAgent",
            action_tier="ANALYZE",
            action_name="calculate_pnl",
            details={"profit_inr": contribution_profit_inr, "margin": net_margin_pct}
        )
        return result
