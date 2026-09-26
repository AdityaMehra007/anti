"""
Revenue Health Score Calculator
Adheres strictly to Directive 95:
Calculates REVENUE HEALTH SCORE /100 based on:
- growth
- retention
- margins
- pipeline
- customer concentration
- CAC
- cash
"""

from typing import Any, Dict

class RevenueHealthCalculator:
    """
    Computes holistic 0-100 health score for the business.
    """
    def calculate_health_score(
        self,
        monthly_growth_rate_pct: float,
        gross_margin_pct: float,
        retention_rate_pct: float,
        pipeline_coverage_ratio: float,
        top_customer_revenue_pct: float,
        cac_payback_months: float,
        runway_months: float
    ) -> Dict[str, Any]:
        # 1. Growth score (15 pts max) - 15% monthly growth = 15 pts
        growth_score = min(max(monthly_growth_rate_pct, 0.0), 15.0)
        
        # 2. Gross Margin score (20 pts max) - 85%+ is optimal
        margin_score = (min(max(gross_margin_pct, 0.0), 100.0) / 100.0) * 20.0
        
        # 3. Retention score (20 pts max) - 90%+ retention = 20 pts
        retention_score = (min(max(retention_rate_pct, 0.0), 100.0) / 100.0) * 20.0
        
        # 4. Pipeline coverage (15 pts max) - 3x coverage = 15 pts
        pipeline_score = min(max(pipeline_coverage_ratio / 3.0, 0.0), 1.0) * 15.0
        
        # 5. Concentration risk (10 pts max) - less than 25% for top customer is optimal
        if top_customer_revenue_pct <= 20.0:
            conc_score = 10.0
        elif top_customer_revenue_pct <= 40.0:
            conc_score = 7.0
        elif top_customer_revenue_pct <= 60.0:
            conc_score = 4.0
        else:
            conc_score = 1.0
            
        # 6. CAC Payback (10 pts max) - <= 3 months = 10 pts, <= 6 months = 7 pts
        if cac_payback_months <= 2.0:
            cac_score = 10.0
        elif cac_payback_months <= 4.0:
            cac_score = 7.5
        elif cac_payback_months <= 6.0:
            cac_score = 5.0
        else:
            cac_score = 2.0
            
        # 7. Cash Runway (10 pts max) - >= 12 months = 10 pts
        runway_score = min(max(runway_months / 12.0, 0.0), 1.0) * 10.0
        
        total_score = round(growth_score + margin_score + retention_score + pipeline_score + conc_score + cac_score + runway_score, 1)
        total_score = min(max(total_score, 0.0), 100.0)
        
        if total_score >= 85.0:
            rating = "EXCELLENT"
        elif total_score >= 70.0:
            rating = "HEALTHY"
        elif total_score >= 50.0:
            rating = "MODERATE_RISK"
        else:
            rating = "CRITICAL_ATTENTION_NEEDED"
            
        return {
            "total_score": total_score,
            "rating": rating,
            "breakdown": {
                "growth": round(growth_score, 1),
                "margin": round(margin_score, 1),
                "retention": round(retention_score, 1),
                "pipeline": round(pipeline_score, 1),
                "concentration": round(conc_score, 1),
                "cac_payback": round(cac_score, 1),
                "runway": round(runway_score, 1)
            }
        }
