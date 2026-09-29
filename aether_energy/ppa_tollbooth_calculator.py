"""
Aether Energy-Compute: Power Purchase Agreement (PPA) & Token Tollbooth Calculator.
Evaluates the dual monetization of clean baseload electricity + collocated AI token throughput.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AetherEconomicProjection:
    year: int
    deployed_reactors: int
    total_gigawatts_gw: float
    power_revenue_b: float
    ai_compute_revenue_b: float
    total_revenue_b: float
    free_cash_flow_b: float
    implied_valuation_at_25x_b: float


class AetherVentureCalculator:
    """
    10-Year venture scaling engine for sovereign energy-compute infrastructure.
    """

    def __init__(
        self,
        base_power_price_per_mwh: float = 62.0,  # $62/MWh fixed sovereign PPA
        ai_token_monetization_multiplier: float = 3.8,  # Compute revenue upside per MW
    ):
        self.base_power_price = base_power_price_per_mwh
        self.ai_multiplier = ai_token_monetization_multiplier

    def project_10_year_trajectory(self) -> List[AetherEconomicProjection]:
        # Reactor deployment schedule: 2 -> 6 -> 18 -> 45 -> 100 -> 220 -> 450 -> 800 -> 1200 -> 1600
        reactor_schedule = [2, 6, 18, 45, 100, 220, 450, 800, 1200, 1600]
        results = []

        for idx, num_r in enumerate(reactor_schedule):
            y = idx + 1
            # 65 MWe per reactor
            total_gw = (num_r * 65.0) / 1000.0
            annual_mwh = total_gw * 1000.0 * 8760.0 * 0.95

            # Power revenue ($B)
            power_rev_b = (annual_mwh * self.base_power_price) / 1e9

            # Direct AI compute colocation tollbooth revenue ($B)
            ai_rev_b = power_rev_b * self.ai_multiplier

            total_rev_b = power_rev_b + ai_rev_b
            # Nuclear SMR + data center operates at ~48% FCF margin at scale
            fcf_b = total_rev_b * 0.48
            val_b = fcf_b * 25.0

            results.append(
                AetherEconomicProjection(
                    year=y,
                    deployed_reactors=num_r,
                    total_gigawatts_gw=round(total_gw, 2),
                    power_revenue_b=round(power_rev_b, 2),
                    ai_compute_revenue_b=round(ai_rev_b, 2),
                    total_revenue_b=round(total_rev_b, 2),
                    free_cash_flow_b=round(fcf_b, 2),
                    implied_valuation_at_25x_b=round(val_b, 2),
                )
            )

        return results
