"""
Cadence Engine for REVENUE OS
Adheres strictly to Directives 78, 79, 80, 81, 82, 145, 146, 147, 148.
Generates:
- Daily Revenue Brief & Founder One-Thing
- Weekly Revenue Review
- Monthly Revenue Review
- Quarterly Strategic Review
"""

from typing import Any, Dict, List, Optional
from REVENUE_OS.database.db import DatabaseManager, get_db

class CadenceEngine:
    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or get_db()

    def get_founder_one_thing(self, pipeline_focus: str) -> str:
        """Directive 78 & 145: Single highest-value revenue action today."""
        return f"Review and send 5 personalized intelligence dossiers to priority accounts in: '{pipeline_focus}'."

    def generate_daily_brief(
        self,
        revenue_yesterday_inr: float,
        revenue_month_inr: float,
        pipeline_inr: float,
        best_lead: str,
        biggest_risk: str,
        highest_roi_opp: str,
        one_thing_to_stop: str
    ) -> Dict[str, Any]:
        """Directive 79: Daily Revenue Brief format."""
        top_3 = [
            f"Dispatch personalized sample dossier to '{best_lead}'.",
            "Clear pending items in Founder Approval Center to unblock outbound sequences.",
            f"Review automated prospect qualification queue for '{highest_roi_opp}'."
        ]
        
        return {
            "date_generated": "2026-09-15",
            "revenue_yesterday": f"₹{revenue_yesterday_inr:,.2f}",
            "revenue_this_month": f"₹{revenue_month_inr:,.2f}",
            "pipeline": f"₹{pipeline_inr:,.2f}",
            "best_lead": best_lead,
            "biggest_risk": biggest_risk,
            "highest_roi_opportunity": highest_roi_opp,
            "top_3_actions": top_3,
            "one_thing_to_stop": one_thing_to_stop,
            "founder_one_thing": self.get_founder_one_thing(highest_roi_opp),
            "daily_question": "What can I do today that can continue making money after today?"
        }

    def generate_weekly_review(
        self,
        revenue_week_inr: float,
        growth_pct: float,
        active_customers: int,
        cac_inr: float,
        conversion_pct: float,
        churn_pct: float,
        profit_inr: float,
        best_channel: str,
        worst_channel: str,
        biggest_bottleneck: str,
        next_experiment: str
    ) -> Dict[str, Any]:
        """Directive 80: Weekly Revenue Review format."""
        return {
            "revenue_week": f"₹{revenue_week_inr:,.2f}",
            "growth": f"{growth_pct:+.1f}%",
            "customers": active_customers,
            "cac": f"₹{cac_inr:,.2f}",
            "conversion": f"{conversion_pct:.1f}%",
            "churn": f"{churn_pct:.1f}%",
            "profit": f"₹{profit_inr:,.2f}",
            "best_channel": best_channel,
            "worst_channel": worst_channel,
            "biggest_bottleneck": biggest_bottleneck,
            "next_experiment": next_experiment,
            "weekly_question": "What worked without me? And what still depends on me?"
        }
