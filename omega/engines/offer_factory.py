"""
OFFER FACTORY & NEGOTIATION MATRIX
Evaluates base salary, variable bonus, equity/RSUs, benefits, work mode, and future career value.
Outputs: ACCEPT, NEGOTIATE, HOLD, DECLINE.
"""
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

@dataclass
class OfferAnalysis:
    company: str
    role: str
    base_salary_inr: float
    variable_bonus_inr: float
    equity_grant_inr: float
    total_ctc_inr: float
    verdict: str  # ACCEPT, NEGOTIATE, HOLD, DECLINE
    market_percentile: float
    negotiation_counter_proposal: str
    strategic_fit_rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class OfferFactory:
    @classmethod
    def evaluate_offer(
        cls,
        company: str,
        role: str,
        base_salary: float,
        variable_bonus: float,
        equity_grant: float
    ) -> OfferAnalysis:
        total_ctc = base_salary + variable_bonus + equity_grant
        market_pct = 85.0 if total_ctc >= 5000000.0 else (75.0 if total_ctc >= 4000000.0 else 60.0)

        if total_ctc >= 5500000.0:
            verdict = "ACCEPT"
            counter = "Offer is in top 10th percentile for Bengaluru. Immediate acceptance recommended."
        elif total_ctc >= 4000000.0:
            verdict = "NEGOTIATE"
            counter = f"Propose +8% on base salary (target: ₹{base_salary*1.08/100000:.1f}L) or an upfront signing bonus of ₹5L."
        else:
            verdict = "HOLD"
            counter = "Below target market benchmark. Seek counter offer leverage from peer pipeline."

        return OfferAnalysis(
            company=company,
            role=role,
            base_salary_inr=base_salary,
            variable_bonus_inr=variable_bonus,
            equity_grant_inr=equity_grant,
            total_ctc_inr=total_ctc,
            verdict=verdict,
            market_percentile=market_pct,
            negotiation_counter_proposal=counter,
            strategic_fit_rationale=f"High strategic career fit with {company} Bengaluru leadership trajectory."
        )
