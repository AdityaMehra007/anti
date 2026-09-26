"""Career Intelligence Agent — Maximizes P(Interview) * P(Offer) * Comp * Leverage."""
from typing import Dict, Any

class CareerAgent:
    @staticmethod
    def calculate_opportunity_score(p_interview: float, p_offer: float, compensation_lpa: float, leverage_score: float) -> float:
        """Opportunity Score = P(Int) * P(Offer) * Comp (LPA) * Leverage (1-10)"""
        return round(p_interview * p_offer * compensation_lpa * leverage_score, 2)
