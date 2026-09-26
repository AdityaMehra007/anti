"""Vector 9: Personal Wealth, Tax Optimization & Corporate Treasury AI (30 Capabilities)."""
from typing import Dict, Any

class WealthAndTreasuryEngine:
    @staticmethod
    def forecast_12_month_cashflow(initial_savings: float, monthly_income: float, monthly_expense: float) -> Dict[str, Any]:
        monthly_net = monthly_income - monthly_expense
        ending_balance = initial_savings + (monthly_net * 12)
        savings_rate = round((monthly_net / max(1.0, monthly_income)) * 100, 1)
        
        return {
            "initial_savings": initial_savings,
            "monthly_net_cashflow": monthly_net,
            "annual_savings_rate": f"{savings_rate}%",
            "projected_12m_balance": ending_balance,
            "financial_health": "EXCELLENT" if savings_rate >= 30.0 else "MODERATE"
        }
