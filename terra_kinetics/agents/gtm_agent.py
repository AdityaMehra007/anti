"""
Terra Kinetics: Autonomous GTM & Commercial Enterprise Pipeline Agent.
Identifies prospective manufacturing/logistics facilities, models labor cost arbitrage,
and generates customized enterprise Labor-as-a-Service proposals.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import time


@dataclass
class EnterpriseLead:
    company_name: str
    facility_type: str  # "automotive", "ecommerce_3pl", "aerospace"
    location: str
    annual_workforce_headcount: int
    avg_hourly_wage_usd: float
    annual_shifts: int = 3
    hours_per_day: float = 24.0


@dataclass
class CommercialProposal:
    proposal_id: str
    company_name: str
    recommended_fleet_size: int
    annual_human_labor_cost_usd: float
    annual_terra_labor_cost_usd: float
    annual_net_savings_usd: float
    roi_percentage: float
    payback_period_months: float
    executive_pitch: str


class AutonomousGtmAgent:
    """
    Evaluates enterprise leads and generates deterministic economic proposals.
    """

    def __init__(self, target_hourly_laas_rate: float = 7.50):
        self.laas_hourly_rate = target_hourly_laas_rate
        self.pipeline: List[EnterpriseLead] = []
        self.proposals_sent: List[CommercialProposal] = []

    def qualify_and_generate_proposal(self, lead: EnterpriseLead) -> CommercialProposal:
        # A robot cell replaces ~0.75 human worker equivalent per shift across 3 shifts (24/7 uptime)
        # So 1 robot cell can replace ~2.25 human FTE shifts
        recommended_robots = max(10, int(lead.annual_workforce_headcount * 0.45))

        annual_human_cost = (
            lead.annual_workforce_headcount * lead.avg_hourly_wage_usd * 2080.0
        )

        annual_operating_hours = recommended_robots * 365.0 * 20.0  # 20 operating hrs/day
        annual_terra_cost = annual_operating_hours * self.laas_hourly_rate

        net_savings = annual_human_cost - annual_terra_cost
        roi_pct = (net_savings / annual_terra_cost) * 100.0 if annual_terra_cost > 0 else 0.0
        payback_months = round(max(1.0, (annual_terra_cost / max(1.0, annual_human_cost)) * 12.0), 1)

        pitch = (
            f"Deployment of {recommended_robots} Terra-powered cells at {lead.company_name} ({lead.location}) "
            f"reduces direct operational labor expenditures from ${annual_human_cost:,.0f} to "
            f"${annual_terra_cost:,.0f}/year, unlocking ${net_savings:,.0f} in recurring annual savings "
            f"with a payback period of {payback_months} months."
        )

        proposal = CommercialProposal(
            proposal_id=f"prop_{time.time_ns()}",
            company_name=lead.company_name,
            recommended_fleet_size=recommended_robots,
            annual_human_labor_cost_usd=round(annual_human_cost, 2),
            annual_terra_labor_cost_usd=round(annual_terra_cost, 2),
            annual_net_savings_usd=round(net_savings, 2),
            roi_percentage=round(roi_pct, 1),
            payback_period_months=payback_months,
            executive_pitch=pitch,
        )

        self.pipeline.append(lead)
        self.proposals_sent.append(proposal)
        return proposal
