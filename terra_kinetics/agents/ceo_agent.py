"""
Terra Kinetics: Autonomous CEO Agent.
Governs capital allocation, financial runway, enterprise valuation targets, and corporate rulings.
Adheres strictly to OMEGA Constitution Mode M (CEO & Capital Allocation).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time


@dataclass
class CorporateRuling:
    ruling_id: str
    decision: str
    rationale: str
    capital_impact_usd: float
    timestamp_ns: int


@dataclass
class CapitalRunwayReport:
    cash_balance_usd: float
    monthly_burn_usd: float
    runway_months: float
    arr_run_rate_usd: float
    implied_valuation_usd: float
    health_status: str


class AutonomousCeoAgent:
    """
    Autonomous corporate decision engine monitoring solvency, growth, and capital strategy.
    """

    def __init__(self, initial_treasury_usd: float = 35_000_000.0):
        self.treasury_usd = initial_treasury_usd
        self.decision_ledger: List[CorporateRuling] = []

    def evaluate_financial_health(self, active_fleet: int, monthly_burn_usd: float) -> CapitalRunwayReport:
        # Each robot generates ~ $1.25/hr * 16 hrs * 30 days = $600/month
        monthly_revenue = active_fleet * 600.0
        arr = monthly_revenue * 12.0
        net_burn = max(0.0, monthly_burn_usd - monthly_revenue)
        runway = (self.treasury_usd / net_burn) if net_burn > 0 else 999.0

        # Valuation rule: 25x ARR or 20x gross margin
        valuation = max(175_000_000.0, arr * 22.0)
        status = "EXPANSION_MODE" if monthly_revenue >= monthly_burn_usd else "CONTROLLED_BURN"

        return CapitalRunwayReport(
            cash_balance_usd=self.treasury_usd,
            monthly_burn_usd=monthly_burn_usd,
            runway_months=round(runway, 1),
            arr_run_rate_usd=round(arr, 2),
            implied_valuation_usd=round(valuation, 2),
            health_status=status,
        )

    def record_executive_ruling(self, decision: str, why: str, cost: float) -> CorporateRuling:
        ruling = CorporateRuling(
            ruling_id=f"ruling_{time.time_ns()}",
            decision=decision,
            rationale=why,
            capital_impact_usd=cost,
            timestamp_ns=time.time_ns(),
        )
        self.treasury_usd -= cost
        self.decision_ledger.append(ruling)
        return ruling
