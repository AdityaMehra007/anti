"""
Sovereign Continuum: Autonomous Sovereign Wealth & Mega-Financing Syndication Agent.

Structures multi-billion dollar capital syndications across Sovereign Wealth Funds (SWFs),
export credit agencies, green infrastructure bonds, and off-take capacity forward contracts.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class CapitalTranche:
    tranche_name: str
    source_type: str  # SWF_EQUITY, GREEN_BOND, EXIM_DEBT, INFRASTRUCTURE_DEBT, RaaS_OFFTAKE_FORWARD
    amount_usd: float
    cost_of_capital_pct: float
    covenants: str


@dataclass
class SyndicationPackage:
    total_facility_usd: float
    blended_wacc_pct: float
    participating_tranches: List[CapitalTranche]
    debt_to_equity_ratio: float
    quarterly_debt_service_usd: float


class AutonomousSyndicationAgent:
    """
    Autonomous investment banker structuring multi-billion dollar planetary infrastructure tranches.
    """

    def structure_sovereign_facility(
        self,
        required_capex_usd: float,
        target_smr_count: int,
        target_robot_fleet: int,
        tenor_years: int = 15,
    ) -> SyndicationPackage:
        """
        Structures an optimized financing syndication minimizing WACC and dilution.
        """
        # Tranche 1: Sovereign Wealth Fund Equity (Anchor, strategic patient capital) - 25%
        swf_amount = required_capex_usd * 0.25
        swf_cost = 9.5  # 9.5% required return

        # Tranche 2: Green Infrastructure Bonds (Tax-exempt / concessionary for Nuclear SMRs) - 35%
        green_amount = required_capex_usd * 0.35
        green_cost = 4.2  # 4.2% coupon

        # Tranche 3: Exim Bank Export Credit Financing (for heavy robotics hardware) - 20%
        exim_amount = required_capex_usd * 0.20
        exim_cost = 4.8  # 4.8% fixed rate

        # Tranche 4: RaaS Forward Off-take Prepayments (BMW, DHL, Siemens pre-funding capacity) - 20%
        offtake_amount = required_capex_usd * 0.20
        offtake_cost = 3.0  # 3.0% synthetic implied cost via capacity discount

        tranches = [
            CapitalTranche(
                tranche_name="Anchor_SWF_Consortium",
                source_type="SWF_EQUITY",
                amount_usd=swf_amount,
                cost_of_capital_pct=swf_cost,
                covenants="1 Board seat, right of first refusal on regional SMR deployments.",
            ),
            CapitalTranche(
                tranche_name="Global_Green_Nuclear_Bonds",
                source_type="GREEN_BOND",
                amount_usd=green_amount,
                cost_of_capital_pct=green_cost,
                covenants="100% nuclear zero-carbon audit certification every 12 months.",
            ),
            CapitalTranche(
                tranche_name="Exim_Credit_Facility",
                source_type="EXIM_DEBT",
                amount_usd=exim_amount,
                cost_of_capital_pct=exim_cost,
                covenants="Hardware assembly in certified allied jurisdiction facilities.",
            ),
            CapitalTranche(
                tranche_name="Enterprise_Forward_Offtake_Tranche",
                source_type="RaaS_OFFTAKE_FORWARD",
                amount_usd=offtake_amount,
                cost_of_capital_pct=offtake_cost,
                covenants="Guaranteed 99.8% uptime SLA at fixed $9.50/hr task metering rate.",
            ),
        ]

        total_facility = sum(t.amount_usd for t in tranches)
        blended_wacc = sum(t.amount_usd * t.cost_of_capital_pct for t in tranches) / total_facility

        total_debt = green_amount + exim_amount + offtake_amount
        total_equity = swf_amount
        debt_to_equity = total_debt / total_equity

        # Approximate quarterly debt service (simple amortizing principal + interest)
        annual_interest = (green_amount * 0.042) + (exim_amount * 0.048) + (offtake_amount * 0.030)
        annual_principal = total_debt / tenor_years
        quarterly_debt_service = (annual_interest + annual_principal) / 4.0

        return SyndicationPackage(
            total_facility_usd=total_facility,
            blended_wacc_pct=round(blended_wacc, 3),
            participating_tranches=tranches,
            debt_to_equity_ratio=round(debt_to_equity, 2),
            quarterly_debt_service_usd=round(quarterly_debt_service, 2),
        )
