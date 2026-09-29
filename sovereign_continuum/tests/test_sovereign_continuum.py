"""
Test Suite for Sovereign Continuum Substrate and Macro Money Flows.
"""

import pytest
from sovereign_continuum.macro_money_flows import GlobalMoneyFlowEngine, GlobalMacroLiquidityStack
from sovereign_continuum.continuum_core import SovereignContinuumCore, ContinuumNode


def test_macro_money_flow_siphon_mechanics():
    engine = GlobalMoneyFlowEngine()
    metrics = engine.simulate_continuum_capture(
        labor_penetration_pct=0.03,    # 3% of global physical labor
        energy_penetration_pct=0.05,   # 5% of global industrial electrons
        compute_market_share_pct=0.40, # 40% of global AI compute
        m2m_fx_take_rate_bps=3.0,
    )
    assert metrics.labor_displacement_capture_b > 300.0  # > $300B revenue from labor tollbooth
    assert metrics.energy_capture_b > 300.0              # > $300B revenue from nuclear baseload
    assert metrics.compute_token_toll_b > 350.0          # > $350B revenue from AI tokens
    assert metrics.total_annual_revenue_b > 1000.0       # > $1.0 Trillion in gross revenue
    assert metrics.total_free_cash_flow_b > 500.0        # > $500 Billion annual FCF
    assert metrics.implied_market_cap_t > 12.0           # > $12 Trillion Enterprise Valuation


def test_continuum_core_node_registration_and_m2m_settlement():
    core = SovereignContinuumCore(sovereign_id="OMEGA_CONTINUUM_01")
    node = ContinuumNode(
        node_id="node_us_east_virginia",
        location_lat_long=(38.9072, -77.0369),
        smr_power_capacity_mwe=650.0,  # 10 SMR units
        gpu_exaflops_capacity=14.5,
        active_robot_swarm_size=50_000,
        settlement_channel_id="chan_m2m_va_01",
    )
    core.register_planetary_node(node)

    capacity = core.audit_continuum_capacity()
    assert capacity["total_connected_nodes"] == 1
    assert capacity["continuous_nuclear_baseload_mwe"] == 650.0
    assert capacity["aggregate_ai_compute_exaflops"] == 14.5
    assert capacity["deployed_physical_robot_fleet"] == 50_000

    # Execute M2M settlement
    tx = core.settle_m2m_transaction(
        sender_id="robot_unitree_h1_092",
        receiver_id="aether_charging_substation_04",
        amount_ecu=12.45,
    )
    assert tx.sender_robot_id == "robot_unitree_h1_092"
    assert tx.amount_units == 12.45
    assert len(tx.cryptographic_signature) == 64
    assert len(core.ledger) == 1
