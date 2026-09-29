"""
Test Suite for Sovereign Empire Orchestrator, Geopolitical Shield, Mega-Syndication & Antifragile Red-Team.
"""

import pytest
from sovereign_continuum.shield_agent import GeopoliticalShieldAgent
from sovereign_continuum.syndication_agent import AutonomousSyndicationAgent
from sovereign_continuum.red_team_agent import PlanetaryRedTeamAgent
from sovereign_continuum.empire_orchestrator import SovereignEmpireOrchestrator


def test_geopolitical_shield_assessment():
    agent = GeopoliticalShieldAgent()
    
    # Test high-risk / redlined jurisdiction
    chn_eval = agent.evaluate_deployment(country_code="CHN", smr_reactors=10, robots_deployed=5000)
    assert chn_eval.risk_level == "REDLINED"
    assert "air-gap" in chn_eval.mitigation_strategy.lower()
    assert chn_eval.regulatory_clearance_timeline_months >= 24

    # Test western restricted jurisdiction
    usa_eval = agent.evaluate_deployment(country_code="USA", smr_reactors=20, robots_deployed=20000)
    assert usa_eval.risk_level == "RESTRICTED"
    assert "FedRAMP" in usa_eval.mitigation_strategy or "Federal" in usa_eval.mitigation_strategy

    # Test open jurisdiction (UAE)
    are_eval = agent.evaluate_deployment(country_code="ARE", smr_reactors=15, robots_deployed=15000)
    assert are_eval.risk_level == "PERMITTED"
    assert are_eval.projected_effective_tax_rate <= 0.15


def test_autonomous_syndication_facility():
    agent = AutonomousSyndicationAgent()
    package = agent.structure_sovereign_facility(
        required_capex_usd=50_000_000_000.0,
        target_smr_count=100,
        target_robot_fleet=500_000,
    )

    assert package.total_facility_usd == 50_000_000_000.0
    assert package.blended_wacc_pct < 6.0  # WACC beat hurdle rate
    assert len(package.participating_tranches) == 4
    assert package.debt_to_equity_ratio == 3.0  # 75% debt / 25% equity
    assert package.quarterly_debt_service_usd > 0.0


def test_planetary_red_team_adversarial_suite():
    agent = PlanetaryRedTeamAgent()
    results = agent.run_full_adversarial_suite(nominal_mwe=8000.0)

    assert results["antifragility_status"] == "HARDENED_RESILIENT"
    assert results["probes_evaluated"] == 4
    assert results["all_probes_passed"] is True

    # Test specific probe bounds
    grid_probe = agent.probe_energy_grid_severance(nominal_mwe=8000.0)
    assert grid_probe.passed is True
    assert grid_probe.recovery_time_objective_sec <= 0.20

    wan_probe = agent.probe_byzantine_network_partition(global_latency_ms=900.0)
    assert wan_probe.passed is True


def test_sovereign_empire_orchestrator_execution():
    orchestrator = SovereignEmpireOrchestrator(sovereign_code="OMEGA_SUPREME")
    
    # Run Year 5, Quarter 20 cycle
    report = orchestrator.execute_planetary_cycle(year=5, quarter=20)
    
    assert report.calendar_year == 5
    assert report.quarter_index == 20
    assert report.consolidated_revenue_b > 10.0  # Multi-billion quarterly scale
    assert report.consolidated_free_cash_flow_b > 5.0
    assert report.consolidated_market_cap_t > 0.25  # Reaching intermediate trillion scale
    assert report.terra_kinetics_fleet > 100_000
    assert report.aether_nuclear_capacity_gw > 5.0
    assert report.m2m_transactions_cleared_count >= 1
    assert report.blended_financing_wacc_pct < 6.0
    assert report.shield_status == "PERMITTED"
    assert report.red_team_antifragility == "HARDENED_RESILIENT"
