"""
Sovereign Continuum: Global Macroeconomic Money Flow Simulation Engine.

Simulates the planetary capital stack across:
1. Global Debt & Sovereign Treasuries (~$315 Trillion)
2. Global Real Estate & Infrastructure (~$380 Trillion)
3. Global Derivatives & Eurodollar Shadow Banking (~$650 Trillion Notional)
4. Global Annual Physical & Cognitive Labor Wages (~$52 Trillion)
5. Global Energy Baseload & Petro/Electron Settlement (~$14 Trillion)
6. Global Gross Domestic Product (~$105 Trillion)

Models how a supra-planetary substrate siphons fractional velocity from each macro artery.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class GlobalMacroLiquidityStack:
    global_gdp_annual_t: float = 105.0
    global_physical_labor_wages_t: float = 46.0
    global_energy_settlement_t: float = 14.5
    global_compute_ai_capex_t: float = 1.2
    global_debt_and_sovereign_bonds_t: float = 315.0
    global_derivatives_notional_t: float = 650.0
    daily_fx_settlement_turnover_t: float = 7.5


@dataclass
class SiphonCaptureMetrics:
    energy_capture_b: float
    labor_displacement_capture_b: float
    compute_token_toll_b: float
    m2m_settlement_arbitrage_b: float
    total_annual_revenue_b: float
    total_free_cash_flow_b: float
    implied_market_cap_t: float


class GlobalMoneyFlowEngine:
    """
    Mathematical simulator analyzing historical, present, and future capital migration.
    """

    HISTORICAL_MONOPOLIES = {
        "Dutch East India Company (VOC - 1637)": {
            "peak_adjusted_market_cap_t": 7.9,
            "core_chokehold": "Spice Trade Monopoly + Sovereign Naval State Violence + Floating Equity Rails",
            "margin_profile": "75% gross margin on spice/silk freight",
            "demise": "Bureaucratic bloat, sovereign corruption, Fourth Anglo-Dutch War",
        },
        "Standard Oil (1911)": {
            "peak_adjusted_market_cap_t": 1.2,
            "core_chokehold": "91% of US Oil Refining Capacity + Railroad Secret Rebate Cartels",
            "margin_profile": "Vertical scale economies squeezing producers & consumers",
            "demise": "Sherman Antitrust Act Section 2 breakup into 34 separate entities",
        },
        "Apple / Microsoft / Nvidia (Present 2024-2026)": {
            "peak_adjusted_market_cap_t": 3.6,
            "core_chokehold": "Mobile OS 30% App Store tollbooth / Wintel Enterprise lock-in / CUDA Parallel Compute",
            "margin_profile": "70-85% software/IP gross margins",
            "demise": "Antitrust scrutiny, compute commoditization, demographic labor cliff",
        },
    }

    def __init__(self, liquidity_stack: GlobalMacroLiquidityStack = None):
        self.stack = liquidity_stack or GlobalMacroLiquidityStack()

    def simulate_continuum_capture(
        self,
        labor_penetration_pct: float = 0.025,    # 2.5% of global physical labor
        energy_penetration_pct: float = 0.040,   # 4.0% of global industrial electrons
        compute_market_share_pct: float = 0.35,  # 35% of global frontier inference
        m2m_fx_take_rate_bps: float = 2.5,       # 2.5 basis points on machine-to-machine trade
    ) -> SiphonCaptureMetrics:
        """
        Calculates annual cash generation from direct arterial money flows.
        """
        # 1. Labor Capture: Take 20% of the cost savings when replacing human labor
        # If human labor is $46T, 2.5% = $1.15T. Terra captures 25% of that in software tolls
        labor_rev_b = (self.stack.global_physical_labor_wages_t * 1000.0) * labor_penetration_pct * 0.25

        # 2. Energy Capture: SMR electrons sold at high baseload margins ($65/MWh)
        energy_rev_b = (self.stack.global_energy_settlement_t * 1000.0) * energy_penetration_pct * 0.45

        # 3. Compute Token Capture: Frontier inference tokens
        compute_rev_b = (self.stack.global_compute_ai_capex_t * 1000.0) * compute_market_share_pct * 0.85

        # 4. M2M Settlement Rails: Autonomous machines paying each other via sub-second micro-settlement
        # Assuming $5T in autonomous M2M transaction volume per year at 2.5 bps
        annual_m2m_volume_b = 5_000.0
        m2m_rev_b = annual_m2m_volume_b * (m2m_fx_take_rate_bps / 10000.0)

        total_rev_b = labor_rev_b + energy_rev_b + compute_rev_b + m2m_rev_b
        # Average blended Free Cash Flow margin across software, power, and tollbooth = 52%
        fcf_b = total_rev_b * 0.52
        market_cap_t = (fcf_b * 25.0) / 1000.0

        return SiphonCaptureMetrics(
            energy_capture_b=round(energy_rev_b, 2),
            labor_displacement_capture_b=round(labor_rev_b, 2),
            compute_token_toll_b=round(compute_rev_b, 2),
            m2m_settlement_arbitrage_b=round(m2m_rev_b, 2),
            total_annual_revenue_b=round(total_rev_b, 2),
            total_free_cash_flow_b=round(fcf_b, 2),
            implied_market_cap_t=round(market_cap_t, 2),
        )
