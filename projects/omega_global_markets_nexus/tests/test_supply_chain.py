"""
Unit Tests for Maritime Supply Chain & Chokepoint Logistics Optimizer
"""
import pytest
from projects.omega_global_markets_nexus.core.supply_chain_optimizer import (
    MaritimeSupplyChainOptimizer, Chokepoint
)


def test_corridor_catalog_and_transit_days():
    catalog = MaritimeSupplyChainOptimizer.get_corridor_catalog()
    assert "ASIA_EUROPE_SUEZ" in catalog
    assert "ASIA_EUROPE_CAPE" in catalog
    suez = catalog["ASIA_EUROPE_SUEZ"]
    cape = catalog["ASIA_EUROPE_CAPE"]

    assert suez.transit_days < cape.transit_days
    assert suez.total_bunker_fuel_cost_usd > 0
    assert suez.total_voyage_cost_usd > 0


def test_chokepoint_blockade_simulation():
    res = MaritimeSupplyChainOptimizer.simulate_chokepoint_blockade(Chokepoint.SUEZ_CANAL)
    assert res["status"] == "DISRUPTED_REROUTING_REQUIRED"
    assert res["additional_transit_days"] > 5.0
    assert res["additional_nautical_miles"] > 2_000.0
    assert res["freight_rate_spike_indicator_pct"] > 0


def test_demurrage_and_detention_calculations():
    # 0 demurrage when within free days
    clean = MaritimeSupplyChainOptimizer.compute_demurrage_and_detention(
        teu_containers=50,
        port_delay_days=4,
        free_days_allowed=5
    )
    assert clean["chargeable_days"] == 0
    assert clean["total_demurrage_usd"] == 0.0

    # Delayed 10 days with 5 free days -> 5 chargeable days (Tier 1: 5 * 150 = 750/TEU)
    delayed = MaritimeSupplyChainOptimizer.compute_demurrage_and_detention(
        teu_containers=100,
        port_delay_days=10,
        free_days_allowed=5
    )
    assert delayed["chargeable_days"] == 5
    assert delayed["charge_per_teu_usd"] == 750.0
    assert delayed["total_demurrage_usd"] == 75_000.0
