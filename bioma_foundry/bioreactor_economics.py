"""
Bioma Foundry: Precision Fermentation Unit Economics & Tollbooth Model.
Calculates cost-per-kilogram parity against petrochemical cracking and projects 10-year enterprise scale.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class BiomaEconomicProjection:
    year: int
    fermentation_capacity_liters_m: float  # in millions of liters
    annual_metric_tons_produced: float
    avg_price_per_kg_usd: float
    gross_revenue_b: float
    gross_margin_pct: float
    free_cash_flow_b: float
    implied_valuation_at_25x_b: float


class BiomaEconomicEngine:
    """
    Precision cellular biomanufacturing economics simulator.
    """

    def __init__(self, avg_titer_g_per_l: float = 85.0, batch_turnover_days: float = 4.5):
        self.titer_g_l = avg_titer_g_per_l
        self.batch_turnaround = batch_turnover_days

    def project_10_year_trajectory(self) -> List[BiomaEconomicProjection]:
        # Capacity in Millions of Liters: 0.5 -> 2.0 -> 8.0 -> 30 -> 100 -> 350 -> 1000 -> 2500 -> 6000 -> 12000
        capacity_schedule_m_l = [0.5, 2.0, 8.0, 30.0, 100.0, 350.0, 1000.0, 2500.0, 6000.0, 12000.0]
        results = []

        batches_per_year = 365.0 / self.batch_turnaround

        for idx, cap_m in enumerate(capacity_schedule_m_l):
            y = idx + 1
            # Total grams produced per year
            total_kg = cap_m * 1e6 * (self.titer_g_l / 1000.0) * batches_per_year
            metric_tons = total_kg / 1000.0

            # Price per kg decays from high-value pharma/specialty ($250/kg) to commodity materials ($18/kg)
            price_per_kg = max(18.0, 250.0 * (0.75 ** (y - 1)))

            gross_rev_b = (total_kg * price_per_kg) / 1e9

            # Feedstock (sugar/methanol/CO2) COGS
            cogs_rate = min(0.35, 0.15 + (0.02 * (y - 1)))
            gross_margin_pct = (1.0 - cogs_rate) * 100.0

            # FCF margin ~40% at scale
            fcf_b = gross_rev_b * 0.40
            val_b = fcf_b * 25.0

            results.append(
                BiomaEconomicProjection(
                    year=y,
                    fermentation_capacity_liters_m=cap_m,
                    annual_metric_tons_produced=round(metric_tons, 1),
                    avg_price_per_kg_usd=round(price_per_kg, 2),
                    gross_revenue_b=round(gross_rev_b, 2),
                    gross_margin_pct=round(gross_margin_pct, 1),
                    free_cash_flow_b=round(fcf_b, 2),
                    implied_valuation_at_25x_b=round(val_b, 2),
                )
            )

        return results
