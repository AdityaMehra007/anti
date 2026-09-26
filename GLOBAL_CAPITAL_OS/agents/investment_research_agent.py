"""Investment Research Agent - Treasury & Capital Preservation Researcher.

Enforces:
1. Liquidity -> Safety -> Return hierarchy.
2. Operating business is the primary wealth engine; external investments are secondary.
3. Strictly NO autonomous speculative trading (no crypto, options, futures, or leveraged gambling).
4. Operates strictly in Research + Simulation + Recommendation mode.
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.models import ActionTier


class InvestmentResearchAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="InvestmentResearchAgent",
            role_description="Prudential investment researcher focusing on cash-equivalents, capital preservation, and risk-adjusted compounding."
        )

    def formulate_treasury_investment_thesis(
        self,
        instrument_name: str,
        instrument_type: str,
        expected_annual_yield_pct: float,
        duration_days: int,
        downside_risk_summary: str,
        liquidity_terms: str
    ) -> dict[str, Any]:
        """Formulates a disciplined, thesis-driven treasury allocation proposal."""
        self.check_permission(ActionTier.SIMULATE)

        # Enforce non-speculative guidelines
        prohibited_types = ["CRYPTO", "DERIVATIVES", "FUTURES", "OPTIONS", "LEVERAGED_FOREX", "MEME_STOCKS"]
        if instrument_type.upper() in prohibited_types:
            raise ValueError(
                f"Speculative asset class '{instrument_type}' is strictly prohibited under Global Capital OS Charter Rule 47."
            )

        thesis = {
            "instrument": instrument_name,
            "type": instrument_type,
            "expected_annual_yield_pct": expected_annual_yield_pct,
            "horizon_days": duration_days,
            "liquidity": liquidity_terms,
            "downside_risk": downside_risk_summary,
            "kill_condition": f"Exit immediately if yield drops below 5.0% or credit rating downgrades below AAA/A1+.",
            "mode": "PAPER_SIMULATION_ONLY",
            "regulatory_note": "Requires Board / Founder authorization under Section 186 of Companies Act 2013."
        }
        self.log_action("TREASURY_THESIS_FORMULATED", thesis)
        return thesis


investment_research_agent = InvestmentResearchAgent()
