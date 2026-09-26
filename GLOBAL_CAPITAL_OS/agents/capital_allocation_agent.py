"""Capital Allocation Agent - RAROC Optimizer for GLOBAL CAPITAL OS.

Every rupee must compete among:
1. Cash preservation (Liquidity buffer)
2. Customer acquisition (High-margin sales pipeline)
3. Automation & AI leverage (Compressing delivery turnaround)
4. Infrastructure & Tooling
5. Debt elimination (Risk reduction)
6. Liquid treasury yield (Safe preservation)
Ranks competing capital uses by Risk-Adjusted Return on Capital (RAROC).
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.models import ActionTier


class CapitalAllocationAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="CapitalAllocationAgent",
            role_description="Capital allocation strategist evaluating the highest risk-adjusted economic returns across the business."
        )

    def rank_capital_use_options(self, deployable_amount_inr: float = 10000.0) -> dict[str, Any]:
        """Compares and ranks potential uses of available capital by RAROC."""
        self.check_permission(ActionTier.ANALYZE)

        # Baseline comparative options
        options = [
            {
                "use_case": "Customer Acquisition & Verified Lead Generation",
                "category": "GROWTH_CAC",
                "projected_gross_return_pct": 350.0,
                "risk_penalty_pct": 30.0,
                "liquidity_speed_days": 14,
                "notes": "Direct outreach to verified B2B SaaS ICP with buying triggers. Highly scalable, high margin (90%+)."
            },
            {
                "use_case": "Delivery Automation & Workflow Tooling",
                "category": "INFRA_EFFICIENCY",
                "projected_gross_return_pct": 200.0,
                "risk_penalty_pct": 15.0,
                "liquidity_speed_days": 30,
                "notes": "Reduces founder delivery hours from 10 hrs to 2 hrs per deliverable, freeing capacity for new sales."
            },
            {
                "use_case": "Liquid Treasury (Overnight / T-Bills)",
                "category": "TREASURY_PRESERVATION",
                "projected_gross_return_pct": 6.8,
                "risk_penalty_pct": 0.5,
                "liquidity_speed_days": 1,
                "notes": "Zero credit risk, instantaneous liquidity, but generates modest capital returns."
            },
            {
                "use_case": "Emergency Cash Buffer Reserve",
                "category": "SURVIVAL_DEFENSE",
                "projected_gross_return_pct": 0.0,
                "risk_penalty_pct": 0.0,
                "liquidity_speed_days": 0,
                "notes": "Required to maintain 6-month operational survival floor."
            }
        ]

        # Calculate RAROC = (Gross Return - Risk Penalty)
        for opt in options:
            opt["raroc_score"] = opt["projected_gross_return_pct"] - opt["risk_penalty_pct"]

        ranked = sorted(options, key=lambda x: x["raroc_score"], reverse=True)

        recommendation = {
            "deployable_amount_inr": deployable_amount_inr,
            "top_priority": ranked[0]["use_case"],
            "rankings": ranked,
            "core_principle": "Reinvesting into high-margin customer acquisition and automation heavily outperforms passive external treasury instruments at early stages."
        }
        self.log_action("CAPITAL_ALLOCATION_RANKED", recommendation)
        return recommendation


capital_allocation_agent = CapitalAllocationAgent()
