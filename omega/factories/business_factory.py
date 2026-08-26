import json
from datetime import datetime

class OmegaBusinessFactory:
    '''Business Operations, Unit Economics, Invoicing & Pricing Sensitivity Engine.'''
    def __init__(self):
        pass

    def model_unit_economics(self, product_name, price_inr, marginal_cost_inr, target_customers=50):
        revenue = price_inr * target_customers
        cost = marginal_cost_inr * target_customers
        gross_profit = revenue - cost
        margin_pct = (gross_profit / max(1, revenue)) * 100

        return {
            "product": product_name,
            "price_per_unit_inr": price_inr,
            "target_customers": target_customers,
            "projected_revenue_inr": revenue,
            "projected_gross_profit_inr": gross_profit,
            "gross_margin_percentage": round(margin_pct, 2),
            "economic_viability": "HIGHLY_VIABLE" if margin_pct >= 60 else "MODERATE",
            "modeled_at": datetime.now().isoformat()
        }
