"""Global Economics Agent - Macro & Cross-Border Sovereign Monitor.

Monitors benchmark interest rates (RBI, Fed, ECB, BoE), sovereign stability,
and cross-border trade conditions across operational and customer jurisdictions.
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.models import ActionTier


class GlobalEconomicsAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="GlobalEconomicsAgent",
            role_description="Macroeconomist monitoring global rate cycles, inflation trends, and sovereign risk across key client jurisdictions."
        )

    def get_macro_environment(self) -> dict[str, Any]:
        """Provides an updated cross-border macroeconomic summary."""
        self.check_permission(ActionTier.READ)

        macro_data = {
            "benchmark_rates": {
                "India (RBI Repo Rate)": "6.50%",
                "United States (Fed Funds)": "5.25% - 5.50%",
                "United Kingdom (BoE Base Rate)": "5.00%",
                "European Union (ECB Refinancing Rate)": "3.75%"
            },
            "jurisdiction_ratings": {
                "India": {"risk": "LOW", "growth_outlook": "HIGH (7.0%+ GDP)", "currency_trend": "Controlled depreciation, strong FX reserves"},
                "United States": {"risk": "LOW", "growth_outlook": "MODERATE", "currency_trend": "High yield baseline, strong corporate B2B spending"},
                "United Kingdom": {"risk": "MODERATE", "growth_outlook": "STABLE", "currency_trend": "Resilient services sector"},
                "UAE": {"risk": "LOW", "growth_outlook": "HIGH", "currency_trend": "USD pegged, emerging global fintech and capital hub"},
                "Singapore": {"risk": "VERY_LOW", "growth_outlook": "STABLE", "currency_trend": "AAA rated regional financial treasury center"}
            },
            "strategic_implication": "US and UK mid-market tech companies retain high willingness to pay in USD/GBP for high-velocity intelligence, delivering superior margin realization for an India-based capital engine."
        }
        self.log_action("MACRO_ENVIRONMENT_ASSESSED", macro_data)
        return macro_data


global_economics_agent = GlobalEconomicsAgent()
