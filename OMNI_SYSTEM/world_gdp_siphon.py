"""
World GDP Daily Siphon & Global Capital Flow Engine.
Connects Aditya Mehra's Sovereign Platform to the ~$110 Trillion World GDP stream.
Provides real-time mathematical velocity calculations and corridor-specific extraction funnels.
Adheres strictly to OMEGA Directives and Zero Vibe Coding.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timezone

from OMNI_SYSTEM.core.config import settings


# Global Macroeconomic Benchmarks (USD & INR equivalents)
WORLD_GDP_USD_ANNUAL = 110_000_000_000_000.0  # ~$110 Trillion Nominal Global GDP
USD_TO_INR_BENCHMARK = 83.50
WORLD_GDP_INR_ANNUAL = WORLD_GDP_USD_ANNUAL * USD_TO_INR_BENCHMARK

# Velocity Constants
DAILY_WORLD_GDP_USD = WORLD_GDP_USD_ANNUAL / 365.25
HOURLY_WORLD_GDP_USD = DAILY_WORLD_GDP_USD / 24.0
SECOND_WORLD_GDP_USD = HOURLY_WORLD_GDP_USD / 3600.0

DAILY_WORLD_GDP_INR = WORLD_GDP_INR_ANNUAL / 365.25
SECOND_WORLD_GDP_INR = DAILY_WORLD_GDP_INR / 86400.0


@dataclass
class EconomicCorridor:
    corridor_id: str
    region_name: str
    share_of_world_gdp_pct: float
    annual_gdp_usd: float
    daily_gdp_usd: float
    primary_currencies: List[str]
    target_offering: str
    daily_ticket_inr: float
    settlement_rail: str
    action_type: str


CORRIDORS: List[EconomicCorridor] = [
    EconomicCorridor(
        corridor_id="CORR-US-CAN",
        region_name="North America (USA & Canada)",
        share_of_world_gdp_pct=27.5,
        annual_gdp_usd=30_250_000_000_000.0,
        daily_gdp_usd=30_250_000_000_000.0 / 365.25,
        primary_currencies=["USD", "CAD"],
        target_offering="Autonomous AI Data Operations & Workflow Pipeline Retainer ($1,500/mo)",
        daily_ticket_inr=4175.0,  # ~$50/day
        settlement_rail="Wise Business ACH / Stripe Card Checkout",
        action_type="WISE_ACH_WIRE"
    ),
    EconomicCorridor(
        corridor_id="CORR-EU-UK",
        region_name="Western Europe & United Kingdom",
        share_of_world_gdp_pct=20.0,
        annual_gdp_usd=22_000_000_000_000.0,
        daily_gdp_usd=22_000_000_000_000.0 / 365.25,
        primary_currencies=["EUR", "GBP"],
        target_offering="Tier-1 Vendor SLA Governance & Incoterms 2020 Compliance Audit (EUR 1,200/mo)",
        daily_ticket_inr=3648.0,  # ~€40/day
        settlement_rail="Wise IBAN SEPA / Stripe GBP Checkout",
        action_type="STRIPE_EUR_GBP"
    ),
    EconomicCorridor(
        corridor_id="CORR-GCC-UAE",
        region_name="Middle East & GCC (UAE & Saudi Arabia)",
        share_of_world_gdp_pct=4.0,
        annual_gdp_usd=4_400_000_000_000.0,
        daily_gdp_usd=4_400_000_000_000.0 / 365.25,
        primary_currencies=["AED", "SAR"],
        target_offering="Cross-Border EXIM Diagnostics & Freight Telemetry Retainer (AED 4,500/mo)",
        daily_ticket_inr=3410.0,  # ~AED 150/day
        settlement_rail="Wio Business UAE / Wise International",
        action_type="WIO_WISE_AED"
    ),
    EconomicCorridor(
        corridor_id="CORR-APAC-SG",
        region_name="East Asia & APAC (Singapore, Japan, Australia)",
        share_of_world_gdp_pct=22.5,
        annual_gdp_usd=24_750_000_000_000.0,
        daily_gdp_usd=24_750_000_000_000.0 / 365.25,
        primary_currencies=["SGD", "AUD", "JPY"],
        target_offering="Regional Hub Supply Chain & UCP 600 Letter of Credit Ops (S$1,800/mo)",
        daily_ticket_inr=3768.0,  # ~S$60/day
        settlement_rail="Aspire Singapore / Stripe APAC",
        action_type="ASPIRE_STRIPE_SGD"
    ),
    EconomicCorridor(
        corridor_id="CORR-IN-DOM",
        region_name="India Domestic & South Asia",
        share_of_world_gdp_pct=3.8,
        annual_gdp_usd=4_180_000_000_000.0,
        daily_gdp_usd=4_180_000_000_000.0 / 365.25,
        primary_currencies=["INR"],
        target_offering="Bangalore Tech Corridor Non-Sales Operations & High-Volume Dispatch",
        daily_ticket_inr=4500.0,  # ₹4,500/day
        settlement_rail="Instant Domestic UPI (adityamehra799@okhdfcbank) & HDFC Current",
        action_type="INSTANT_UPI"
    )
]


class WorldGDPSiphon:
    """
    Sovereign engine calculating global macroeconomic velocity
    and translating multi-trillion-dollar world output into daily cash flow.
    """

    @staticmethod
    def get_macro_velocity() -> Dict[str, Any]:
        """Return live global GDP velocity in USD and INR."""
        return {
            "annual_gdp_usd": WORLD_GDP_USD_ANNUAL,
            "annual_gdp_inr": WORLD_GDP_INR_ANNUAL,
            "daily_gdp_usd": round(DAILY_WORLD_GDP_USD, 2),
            "daily_gdp_inr": round(DAILY_WORLD_GDP_INR, 2),
            "hourly_gdp_usd": round(HOURLY_WORLD_GDP_USD, 2),
            "second_gdp_usd": round(SECOND_WORLD_GDP_USD, 2),
            "second_gdp_inr": round(SECOND_WORLD_GDP_INR, 2),
            "usd_to_inr": USD_TO_INR_BENCHMARK,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    @staticmethod
    def get_corridors() -> List[Dict[str, Any]]:
        """Return list of active economic corridors formatted as dictionaries."""
        return [
            {
                "id": c.corridor_id,
                "region": c.region_name,
                "share_pct": c.share_of_world_gdp_pct,
                "annual_usd": c.annual_gdp_usd,
                "daily_usd": round(c.daily_gdp_usd, 2),
                "currencies": c.primary_currencies,
                "offering": c.target_offering,
                "daily_ticket_inr": c.daily_ticket_inr,
                "rail": c.settlement_rail,
                "action": c.action_type
            }
            for c in CORRIDORS
        ]

    @staticmethod
    def calculate_siphon_metrics(current_inflow_inr: float, target_daily_inr: float = 14500.0) -> Dict[str, Any]:
        """
        Calculate the exact micro-fraction of daily World GDP captured.
        """
        share_of_daily_world_gdp = (current_inflow_inr / DAILY_WORLD_GDP_INR) * 100.0
        target_share = (target_daily_inr / DAILY_WORLD_GDP_INR) * 100.0
        pacing_pct = (current_inflow_inr / target_daily_inr) * 100.0 if target_daily_inr > 0 else 100.0

        return {
            "current_inflow_inr": current_inflow_inr,
            "current_inflow_usd": round(current_inflow_inr / USD_TO_INR_BENCHMARK, 2),
            "target_daily_inr": target_daily_inr,
            "target_daily_usd": round(target_daily_inr / USD_TO_INR_BENCHMARK, 2),
            "pacing_pct": round(pacing_pct, 1),
            "share_of_daily_world_gdp_pct": f"{share_of_daily_world_gdp:.10f}%",
            "target_share_pct": f"{target_share:.10f}%",
            "global_status": "SIPHON_ACTIVE" if current_inflow_inr >= target_daily_inr else "SIPHON_PACING",
            "seconds_of_world_gdp_equivalent": round(current_inflow_inr / SECOND_WORLD_GDP_INR, 6)
        }

    @staticmethod
    def format_siphon_briefing(current_inflow_inr: float = 47131.33) -> str:
        """Format an executive terminal briefing on global GDP extraction."""
        velocity = WorldGDPSiphon.get_macro_velocity()
        metrics = WorldGDPSiphon.calculate_siphon_metrics(current_inflow_inr)

        lines = [
            "=" * 74,
            "  OMNI-SYSTEM :: WORLD GDP DAILY EXTRACTION RADAR",
            "  OPERATOR: Aditya Mehra | Bengaluru, India",
            f"  GLOBAL BENCHMARK: USD 110.0 Trillion Nominal Annual Output",
            "=" * 74,
            "",
            "  [1] GLOBAL ECONOMIC VELOCITY",
            f"      - World GDP / Year:        USD {velocity['annual_gdp_usd']:,.0f}",
            f"      - World GDP / Day:         USD {velocity['daily_gdp_usd']:,.2f} (~INR {velocity['daily_gdp_inr']:,.2f})",
            f"      - World GDP / Second:      USD {velocity['second_gdp_usd']:,.2f} (~INR {velocity['second_gdp_inr']:,.2f})",
            "",
            "  [2] ADITYA MEHRA DAILY SIPHON STATE",
            f"      - Today's Captured Flow:   INR {metrics['current_inflow_inr']:,.2f} (USD {metrics['current_inflow_usd']:,.2f})",
            f"      - Daily Target Quota:      INR {metrics['target_daily_inr']:,.2f} (USD {metrics['target_daily_usd']:,.2f})",
            f"      - Quota Achievement:       {metrics['pacing_pct']:.1f}%",
            f"      - Share of Daily World GDP: {metrics['share_of_daily_world_gdp_pct']}",
            f"      - Global Siphon Status:    {metrics['global_status']}",
            "",
            "  [3] THE 5 WORLD EXTRACTION CORRIDORS",
        ]

        for c in CORRIDORS:
            lines.append(f"      * {c.region_name} ({c.share_of_world_gdp_pct}% of World GDP)")
            lines.append(f"        Offering: {c.target_offering}")
            lines.append(f"        Rail:     {c.settlement_rail}")

        lines.extend([
            "",
            "=" * 74,
            "  SOVEREIGN LAW: Extracting value daily from world trade without border limits.",
            "=" * 74
        ])
        return "\n".join(lines)


siphon_engine = WorldGDPSiphon()
