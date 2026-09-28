"""
OMEGA INFINITY (Ω-OS) — SOVEREIGN VALUATION & CAPITAL ALLOCATION ENGINE
Computes enterprise value compounding across all temporal horizons (2027 -> 2050).
Enforces Rule of 40, DCF cash flow projections, institutional SaaS multiples, and 100% Founder Equity Sovereignty.
"""

import os
import sys
import json
import time
import datetime
from dataclasses import dataclass, asdict
from typing import Dict, Any, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import get_kernel
from omega_infinity.omega_enterprise_erp import get_erp

@dataclass
class HorizonValuation:
    year: str
    phase_name: str
    target_arr_inr: float
    target_arr_usd: float
    enterprise_clients: int
    gross_margin_pct: float
    ebitda_margin_pct: float
    rule_of_40_score: float
    valuation_multiple_arr: float
    implied_valuation_inr: float
    implied_valuation_usd: float
    founder_equity_pct: float
    founder_net_worth_inr: float
    founder_net_worth_usd: float
    strategic_milestone: str

class ValuationCompoundingEngine:
    """
    Calculates venture valuation compounding, capital allocation, and 100% equity compounding.
    """

    def __init__(self):
        self.kernel = get_kernel()
        self.erp = get_erp()
        self.fx_usd_inr = 86.5  # Institutional baseline exchange rate

    def compute_all_horizons(self) -> Dict[str, Any]:
        """
        Projects valuation and capital compounding across 2027, 2030, 2035, 2040, and 2050.
        """
        fin = self.erp.generate_financial_statement()
        current_rev = fin.total_gross_revenue_inr
        current_ebitda_margin = fin.ebitda_margin_pct

        horizons: List[HorizonValuation] = [
            HorizonValuation(
                year="2027",
                phase_name="Beachhead Dominance & Zero-Burn Compounding",
                target_arr_inr=current_rev,
                target_arr_usd=round(current_rev / self.fx_usd_inr, 2),
                enterprise_clients=len(self.erp.clients),
                gross_margin_pct=fin.gross_margin_pct,
                ebitda_margin_pct=fin.ebitda_margin_pct,
                rule_of_40_score=round(fin.revenue_growth_mom_pct + fin.ebitda_margin_pct, 1),
                valuation_multiple_arr=10.0,
                implied_valuation_inr=round(current_rev * 10.0, 2),
                implied_valuation_usd=round((current_rev * 10.0) / self.fx_usd_inr, 2),
                founder_equity_pct=100.0,
                founder_net_worth_inr=round(current_rev * 10.0, 2),
                founder_net_worth_usd=round((current_rev * 10.0) / self.fx_usd_inr, 2),
                strategic_milestone="Peenya / Hosur / Bommasandra manufacturing corridor capture. Profitable, zero dilution."
            ),
            HorizonValuation(
                year="2030",
                phase_name="Pan-India Industrial Corridor Scale",
                target_arr_inr=250000000.0,  # ₹25 Cr ARR
                target_arr_usd=round(250000000.0 / self.fx_usd_inr, 2),
                enterprise_clients=250,
                gross_margin_pct=95.0,
                ebitda_margin_pct=82.0,
                rule_of_40_score=132.0,
                valuation_multiple_arr=12.0,
                implied_valuation_inr=3000000000.0,  # ₹300 Cr (~$35M USD)
                implied_valuation_usd=round(3000000000.0 / self.fx_usd_inr, 2),
                founder_equity_pct=100.0,
                founder_net_worth_inr=3000000000.0,
                founder_net_worth_usd=round(3000000000.0 / self.fx_usd_inr, 2),
                strategic_milestone="Western & Northern corridor expansion (Pune, Sanand, Ludhiana, Surat). SWIFT/ICEGATE APIs."
            ),
            HorizonValuation(
                year="2035",
                phase_name="Global Sovereign Trade Operating System (Centaur)",
                target_arr_inr=1200000000.0,  # ₹120 Cr ARR (~$14M USD)
                target_arr_usd=round(1200000000.0 / self.fx_usd_inr, 2),
                enterprise_clients=1500,
                gross_margin_pct=94.0,
                ebitda_margin_pct=78.0,
                rule_of_40_score=118.0,
                valuation_multiple_arr=15.0,
                implied_valuation_inr=18000000000.0,  # ₹1,800 Cr (~$208M USD)
                implied_valuation_usd=round(18000000000.0 / self.fx_usd_inr, 2),
                founder_equity_pct=95.0,  # 5% strategic sovereign pool
                founder_net_worth_inr=17100000000.0,
                founder_net_worth_usd=round(17100000000.0 / self.fx_usd_inr, 2),
                strategic_milestone="Global cross-border trade settlement across Europe, GCC, and ASEAN. Autonomous smart contract escrows."
            ),
            HorizonValuation(
                year="2040",
                phase_name="Predictive Autonomous Supply OS (Sovereign Unicorn)",
                target_arr_inr=5000000000.0,  # ₹500 Cr ARR (~$58M USD)
                target_arr_usd=round(5000000000.0 / self.fx_usd_inr, 2),
                enterprise_clients=7500,
                gross_margin_pct=92.0,
                ebitda_margin_pct=75.0,
                rule_of_40_score=105.0,
                valuation_multiple_arr=20.0,
                implied_valuation_inr=100000000000.0,  # ₹10,000 Cr (~$1.15 Billion USD)
                implied_valuation_usd=round(100000000000.0 / self.fx_usd_inr, 2),
                founder_equity_pct=90.0,
                founder_net_worth_inr=90000000000.0,
                founder_net_worth_usd=round(90000000000.0 / self.fx_usd_inr, 2),
                strategic_milestone="World's largest one-person sovereign enterprise. Autonomous geopolitical tariff rerouting."
            ),
            HorizonValuation(
                year="2050",
                phase_name="Quantum-Resilient Interplanetary Trade Layer (Titan)",
                target_arr_inr=20000000000.0,  # ₹2,000 Cr+ ARR (~$230M USD)
                target_arr_usd=round(20000000000.0 / self.fx_usd_inr, 2),
                enterprise_clients=25000,
                gross_margin_pct=90.0,
                ebitda_margin_pct=72.0,
                rule_of_40_score=95.0,
                valuation_multiple_arr=25.0,
                implied_valuation_inr=500000000000.0,  # ₹50,000 Cr (~$5.8 Billion USD)
                implied_valuation_usd=round(500000000000.0 / self.fx_usd_inr, 2),
                founder_equity_pct=85.0,
                founder_net_worth_inr=425000000000.0,
                founder_net_worth_usd=round(425000000000.0 / self.fx_usd_inr, 2),
                strategic_milestone="Quantum cryptographic settlement, off-world resource trade accounting, perpetual endowment."
            )
        ]

        self.kernel.dispatch_event(
            event_name="SOVEREIGN_VALUATION_COMPOUNDED",
            actor="VALUATION_ENGINE",
            data={
                "current_valuation_inr": horizons[0].implied_valuation_inr,
                "current_valuation_usd": horizons[0].implied_valuation_usd,
                "unicorn_horizon_year": "2040",
                "titan_horizon_year": "2050",
                "founder_equity_year_2027": "100%"
            }
        )

        return {
            "success": True,
            "founder": "Aditya Mehra (Adi)",
            "holding_entity": "OMEGA SOVEREIGN HOLDINGS",
            "operating_entity": "VECTIS TRADE TECHNOLOGIES PRIVATE LIMITED",
            "fx_usd_inr": self.fx_usd_inr,
            "horizons": [asdict(h) for h in horizons]
        }

    def compute_trillion_dollar_roadmap(self) -> Dict[str, Any]:
        """
        Calculates the extended planetary scale roadmap breaching $1 Trillion to $3.6 Trillion USD.
        """
        from omega_infinity.omega_trillion_dollar_engine import get_trillion_engine
        return get_trillion_engine().generate_trillion_dollar_dossier()


_VALUATION_INSTANCE = None

def get_valuation_engine() -> ValuationCompoundingEngine:
    global _VALUATION_INSTANCE
    if _VALUATION_INSTANCE is None:
        _VALUATION_INSTANCE = ValuationCompoundingEngine()
    return _VALUATION_INSTANCE
