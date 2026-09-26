"""
ANTIGRAVITY OMNIVERSE: SEMICONDUCTOR VENTURE TEST SUITE
=======================================================
Verifies the complete first autonomous vertical slice:
Research intelligence, 5-business ranking, financial models,
and the ChipFlow AI yield engine prototype.
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from omniverse.research.semiconductor_intelligence import SemiconductorIntelligence
from omniverse.business.semiconductor_venture_studio import SemiconductorVentureStudio
from omniverse.business.chipflow_prototype import ChipFlowYieldEngine

def test_semiconductor_intelligence_provenance():
    market = SemiconductorIntelligence.get_market_overview()
    assert market["global_market_size_usd_billions"] == 680.0
    assert market["provenance"]["confidence"] >= 0.95
    assert market["provenance"]["verified"] is True

    bottlenecks = SemiconductorIntelligence.get_bottleneck_analysis()
    assert len(bottlenecks) >= 3
    assert any(b["bottleneck_id"] == "BN-01-PACKAGING" for b in bottlenecks)

def test_five_businesses_evaluation_and_ranking():
    ventures = SemiconductorVentureStudio.evaluate_five_businesses()
    assert len(ventures) == 5
    
    # Verify sorted ranking
    ranks = [v["rank"] for v in ventures]
    assert ranks == [1, 2, 3, 4, 5]
    
    # Verify winner
    winner = ventures[0]
    assert winner["name"] == "ChipFlow AI"
    assert winner["viability_score"] > 90.0
    assert winner["gross_margin_percent"] > 80.0

def test_winner_financial_model_unit_economics():
    model = SemiconductorVentureStudio.get_winner_financial_model()
    assert model["venture"] == "ChipFlow AI"
    ue = model["unit_economics"]
    assert ue["ltv_to_cac_ratio"] > 15.0
    assert ue["months_to_recover_cac"] < 3.0
    
    pnl = model["projections_3_year"]
    assert pnl["year_1"]["net_profit_usd"] > 0.0
    assert pnl["year_3"]["total_revenue_usd"] > 10000000.0

def test_chipflow_yield_engine_dpw_calculation():
    # 300mm wafer, 48 mm2 die
    dpw = ChipFlowYieldEngine.calculate_die_per_wafer(300.0, 48.0)
    assert dpw > 1100
    assert dpw < 1500

def test_chipflow_yield_engine_defect_model():
    # 48 mm2 die (0.48 cm2), 0.08 defects/cm2
    s_yield = ChipFlowYieldEngine.calculate_defect_yield(48.0, 0.08)
    assert 0.90 <= s_yield <= 0.99

def test_chipflow_yield_engine_packaging_loss():
    assert ChipFlowYieldEngine.calculate_packaging_yield("FLIP_CHIP_BGA") == 0.965
    assert ChipFlowYieldEngine.calculate_packaging_yield("2.5D_INTERPOSER_COWOS") == 0.910
    assert ChipFlowYieldEngine.calculate_packaging_yield("UNKNOWN") == 0.950

def test_chipflow_wafer_batch_arbitrage_and_hash_seal():
    batch = ChipFlowYieldEngine.evaluate_wafer_batch(
        batch_id="LOT-2026-X88",
        chip_name="EdgeNPU-Tiny",
        wafer_diameter_mm=300.0,
        die_area_mm2=48.0,
        wafer_cost_usd=6500.0,
        packaging_tech="FLIP_CHIP_BGA",
        packaging_cost_per_die_usd=0.85,
        wafer_count=25
    )
    assert batch["final_good_packaged_chips"] > 20000
    assert batch["cost_per_good_chip_usd"] > 0.0
    assert batch["arbitrage_savings_usd"] > 10000.0
    assert len(batch["audit_checksum_sha256"]) == 64

def test_chipflow_landing_page_exists():
    lp_path = os.path.join(os.path.dirname(__file__), "..", "ui", "chipflow_landing_page.html")
    assert os.path.isfile(lp_path)
    with open(lp_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert "ChipFlow AI" in html
    assert "Autonomous Silicon Packaging" in html
