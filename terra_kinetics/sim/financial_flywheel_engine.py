"""
Terra Kinetics: Venture Economics & Fleet Scale Simulation Engine (10-Year Tollbooth Model)

Mathematically models the progression to a $1 Trillion Enterprise Valuation:
Calculates Fleet Size, Labor-as-a-Service (LaaS) Tollbooth ARR, Cloud COGS,
Operating Margins, Free Cash Flow (FCF), and Implied Enterprise Value.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class YearMetrics:
    year: int
    active_robots: int
    annual_operating_hours_b: float
    gross_revenue_b: float
    gross_margin_pct: float
    cogs_b: float
    rd_opex_b: float
    operating_income_b: float
    free_cash_flow_b: float
    implied_valuation_at_25x_b: float


class FleetVentureSimulator:
    """
    Simulates the 10-year growth trajectory of Terra Kinetics.
    """

    def __init__(
        self,
        initial_fleet: int = 1_500,
        fleet_cagr: float = 2.45,
        avg_daily_operating_hours: float = 16.0,
        avg_hourly_toll_rate: float = 1.25,  # Blend across logistics & industrial
        inference_cost_per_hour: float = 0.22,
        r_and_d_base_b: float = 0.15,
    ):
        self.initial_fleet = initial_fleet
        self.fleet_cagr = fleet_cagr
        self.avg_daily_operating_hours = avg_daily_operating_hours
        self.avg_hourly_toll_rate = avg_hourly_toll_rate
        self.inference_cost_per_hour = inference_cost_per_hour
        self.r_and_d_base_b = r_and_d_base_b

    def run_projection(self, years: int = 10) -> List[YearMetrics]:
        results: List[YearMetrics] = []
        fleet = float(self.initial_fleet)

        # Calibrated global adoption curve matching multi-OEM platform inflection:
        # Y1-Y3: High-value industrial beachheads & logistics (5k -> 100k)
        # Y4-Y6: Tier-1 automotive, manufacturing & hazardous operations (400k -> 3.5M)
        # Y7-Y8: Commercial facility maintenance, hospitality, healthcare (8M -> 16M)
        # Y9-Y10: Global universal physical labor substrate (22M -> 28M+)
        fleet_trajectory = [
            5_000,        # Y1
            25_000,       # Y2
            100_000,      # Y3
            450_000,      # Y4
            1_500_000,    # Y5
            4_000_000,    # Y6
            9_500_000,    # Y7
            16_000_000,   # Y8
            22_500_000,   # Y9
            28_000_000,   # Y10
        ]

        for y in range(1, min(years + 1, len(fleet_trajectory) + 1)):
            active_robots_int = fleet_trajectory[y - 1]
            annual_hours = (active_robots_int * self.avg_daily_operating_hours * 365) / 1e9  # in billions

            # Dynamic toll rate: Early early adopters pay slightly less, specialized skill marketplace adds take rate
            effective_toll = self.avg_hourly_toll_rate * (1.0 + min(0.4, (y - 1) * 0.05))

            # Revenue in $ Billions
            gross_rev_b = annual_hours * effective_toll

            # COGS: Cloud inference, edge telemetry bandwidth, shadow tele-op reserves
            # Unit inference cost decreases with custom silicon and model quantization
            unit_cogs = max(0.08, self.inference_cost_per_hour * (0.88 ** (y - 1)))
            cogs_b = annual_hours * unit_cogs
            gross_margin_pct = ((gross_rev_b - cogs_b) / gross_rev_b) * 100.0 if gross_rev_b > 0 else 0.0

            # OPEX: World model training clusters, robotic fleet gyms, enterprise GTM
            rd_opex_b = self.r_and_d_base_b * (1.6 ** (y - 1))
            # Cap realistic corporate OPEX at scale
            if rd_opex_b > 35.0:
                rd_opex_b = 35.0 + (gross_rev_b * 0.05)

            operating_income_b = gross_rev_b - cogs_b - rd_opex_b

            # Tax rate of 21% + normalized Capex
            taxes_b = max(0.0, operating_income_b * 0.21)
            capex_b = gross_rev_b * 0.04
            free_cash_flow_b = operating_income_b - taxes_b - capex_b

            # Valuation at mature multiple (25x FCF for >20% growth)
            valuation_b = max(0.0, free_cash_flow_b * 25.0)

            results.append(
                YearMetrics(
                    year=y,
                    active_robots=active_robots_int,
                    annual_operating_hours_b=round(annual_hours, 2),
                    gross_revenue_b=round(gross_rev_b, 2),
                    gross_margin_pct=round(gross_margin_pct, 1),
                    cogs_b=round(cogs_b, 2),
                    rd_opex_b=round(rd_opex_b, 2),
                    operating_income_b=round(operating_income_b, 2),
                    free_cash_flow_b=round(free_cash_flow_b, 2),
                    implied_valuation_at_25x_b=round(valuation_b, 2),
                )
            )

        return results

    def format_summary_table(self, metrics: List[YearMetrics]) -> str:
        headers = [
            "Year",
            "Active Robots",
            "Oper Hours (B)",
            "Revenue ($B)",
            "Gross Margin",
            "FCF ($B)",
            "Valuation ($B)",
        ]
        rows = [headers]
        for m in metrics:
            rows.append([
                f"Y{m.year}",
                f"{m.active_robots:,}",
                f"{m.annual_operating_hours_b:.1f}B",
                f"${m.gross_revenue_b:.2f}B",
                f"{m.gross_margin_pct:.1f}%",
                f"${m.free_cash_flow_b:.2f}B",
                f"${m.implied_valuation_at_25x_b:,.0f}B",
            ])

        col_widths = [max(len(str(row[i])) for row in rows) for i in range(len(headers))]
        table_lines = []
        # Header
        table_lines.append(" | ".join(rows[0][i].ljust(col_widths[i]) for i in range(len(headers))))
        table_lines.append("-+-".join("-" * col_widths[i] for i in range(len(headers))))
        for row in rows[1:]:
            table_lines.append(" | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(headers))))

        return "\n".join(table_lines)


if __name__ == "__main__":
    sim = FleetVentureSimulator()
    projection = sim.run_projection(10)
    print(sim.format_summary_table(projection))
