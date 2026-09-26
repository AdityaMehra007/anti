"""Vector 4: Predictive Compensation, Offer Negotiation & Equity Modeling (30 Capabilities)."""
from typing import Dict, Any

class CompensationNegotiationEngine:
    @staticmethod
    def calculate_counter_offer(offered_ctc_lpa: float, target_ctc_lpa: float, competing_offers: int = 1) -> Dict[str, Any]:
        leverage_multiplier = 1.0 + (competing_offers * 0.05)
        recommended_counter = round(max(target_ctc_lpa, offered_ctc_lpa * 1.15) * leverage_multiplier, 2)
        take_home_monthly = round((offered_ctc_lpa * 100000 * 0.85) / 12, 2)
        
        return {
            "offered_ctc_lpa": offered_ctc_lpa,
            "recommended_counter_lpa": recommended_counter,
            "estimated_take_home_monthly": take_home_monthly,
            "strategy": "Leverage multi-offer competition and proven frontline proof points"
        }
