"""
ANTIGRAVITY OMNIVERSE: DIGITAL TWIN & "WHAT IF?" SIMULATION ENGINE
==================================================================
Simulates business models, supply chains, customer funnels, and pricing dynamics
under macro stress, competitor moves, and cost shocks.
"""
from typing import Dict, Any, List, Optional
import math

class DigitalTwinSimulator:
    """Quantitative scenario and sensitivity engine."""

    @classmethod
    def simulate_business_what_if(
        cls,
        baseline_revenue: float,
        baseline_cogs: float,
        baseline_opex: float,
        price_change_percent: float = 0.0,
        demand_change_percent: float = 0.0,
        tariff_shock_percent: float = 0.0,
        model_cost_change_percent: float = 0.0,
        competitor_churn_percent: float = 0.0
    ) -> Dict[str, Any]:
        """
        Evaluates second-order impacts of multiple simultaneous or individual shocks.
        Elasticity assumption: Price elasticity of demand = -0.75 for B2B mission-critical tech.
        """
        price_multiplier = 1.0 + (price_change_percent / 100.0)
        
        # Price change induces demand elasticity
        elasticity_demand_effect = (price_change_percent * -0.75)
        total_demand_percent = demand_change_percent + elasticity_demand_effect - competitor_churn_percent
        volume_multiplier = max(0.1, 1.0 + (total_demand_percent / 100.0))

        # Adjusted revenue
        projected_revenue = baseline_revenue * price_multiplier * volume_multiplier

        # Adjusted COGS (Impacted by tariffs on imported chips/packaging + volume)
        tariff_multiplier = 1.0 + (tariff_shock_percent / 100.0)
        projected_cogs = baseline_cogs * volume_multiplier * tariff_multiplier

        # Adjusted OpEx (Impacted by model inference cost reductions)
        # Assume AI compute is ~25% of baseline OpEx
        ai_compute_portion = baseline_opex * 0.25
        fixed_opex_portion = baseline_opex * 0.75
        new_ai_compute = ai_compute_portion * (1.0 + (model_cost_change_percent / 100.0))
        projected_opex = fixed_opex_portion + new_ai_compute

        # Baseline vs Projected
        baseline_gross_profit = baseline_revenue - baseline_cogs
        baseline_net_income = baseline_gross_profit - baseline_opex

        projected_gross_profit = projected_revenue - projected_cogs
        projected_net_income = projected_gross_profit - projected_opex

        net_income_delta = projected_net_income - baseline_net_income
        net_income_pct_change = (net_income_delta / max(1.0, abs(baseline_net_income))) * 100.0

        risks = []
        if projected_net_income < 0:
            risks.append("CRITICAL: Operation dips into negative operating cash flow.")
        if projected_cogs / max(1.0, projected_revenue) > 0.40:
            risks.append("WARNING: Gross margin compressed below 60% threshold.")
        if competitor_churn_percent > 15.0:
            risks.append("WARNING: Severe churn indicates vulnerability to commoditization.")

        return {
            "baseline": {
                "revenue_usd": round(baseline_revenue, 2),
                "cogs_usd": round(baseline_cogs, 2),
                "opex_usd": round(baseline_opex, 2),
                "gross_margin_percent": round((baseline_gross_profit / max(1.0, baseline_revenue)) * 100, 2),
                "net_income_usd": round(baseline_net_income, 2)
            },
            "projected": {
                "revenue_usd": round(projected_revenue, 2),
                "cogs_usd": round(projected_cogs, 2),
                "opex_usd": round(projected_opex, 2),
                "gross_margin_percent": round((projected_gross_profit / max(1.0, projected_revenue)) * 100, 2),
                "net_income_usd": round(projected_net_income, 2)
            },
            "variance": {
                "revenue_delta_usd": round(projected_revenue - baseline_revenue, 2),
                "net_income_delta_usd": round(net_income_delta, 2),
                "net_income_percent_change": round(net_income_pct_change, 2)
            },
            "sensitivity_risks": risks or ["Scenario within sustainable resilience bounds."]
        }
