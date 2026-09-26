"""Business Opportunity Agent — 13-Factor Business Viability Evaluator."""
from typing import Dict, Any

class BusinessAgent:
    @staticmethod
    def evaluate_opportunity(name: str, problem_severity: float, market_size: float,
                             competition: float, startup_cost: float, time_to_revenue_days: int,
                             gross_margin_pct: float, operational_complexity: float,
                             automation_potential: float, customer_acq_difficulty: float,
                             scalability: float, defensibility: float, founder_fit: float) -> Dict[str, Any]:
        # Weighted score (0 - 100)
        positive_factors = (problem_severity + market_size + (gross_margin_pct/10) + 
                            automation_potential + scalability + defensibility + founder_fit) / 7.0
        friction_factors = (competition + (startup_cost/10000) + (time_to_revenue_days/30) + 
                            operational_complexity + customer_acq_difficulty) / 5.0
        viability_score = round(max(0.0, min(100.0, (positive_factors * 12) - (friction_factors * 3))), 1)
        
        return {
            "business_name": name,
            "viability_score": viability_score,
            "recommendation": "PROCEED TO MVP" if viability_score >= 70 else "REJECT / PIVOT",
            "unit_economics": {"gross_margin": f"{gross_margin_pct}%", "time_to_revenue": f"{time_to_revenue_days} days"}
        }
