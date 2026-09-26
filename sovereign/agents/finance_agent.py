"""Finance Agent — Personal Cash Flow, 12-Month Forecast, and Runway Stress-Testing."""
from typing import Dict, Any

class FinanceAgent:
    @staticmethod
    def calculate_runway(current_savings: float, monthly_income: float, monthly_burn: float) -> Dict[str, Any]:
        net_cash_flow = monthly_income - monthly_burn
        runway_months = "INFINITE (Cash Flow Positive)" if net_cash_flow >= 0 else round(current_savings / abs(net_cash_flow), 1)
        return {
            "monthly_income": monthly_income,
            "monthly_burn": monthly_burn,
            "net_cash_flow": net_cash_flow,
            "runway_months": runway_months,
            "status": "HEALTHY & SUSTAINABLE" if net_cash_flow >= 0 else "DEFICIT"
        }
