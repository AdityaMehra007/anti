"""
ANTIGRAVITY OMNIVERSE: FULL-SUITE INTEGRATION TESTS
===================================================
Verifies Connector Bus, Aladdin Risk Engine, Knowledge Graph, Digital Twin Simulator,
Pilot Outreach Engine, and Dashboard UI.
"""
import pytest
import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from omniverse.connectors.mcp_bus import OmniverseConnectorBus
from omniverse.finance.aladdin_risk import AladdinRiskEngine
from omniverse.knowledge.knowledge_graph import UniversalKnowledgeGraph
from omniverse.simulation.digital_twin import DigitalTwinSimulator
from omniverse.business.chipflow_pilot_outreach import ChipFlowPilotOutreach

def test_connector_bus_registry_and_tools_300():
    bus = OmniverseConnectorBus()
    conns = bus.list_connectors()
    assert len(conns) >= 6
    
    fs = bus.get_connector("CONN-FS-01")
    assert fs is not None
    assert "read_file" in fs["capabilities"]
    
    # Tool 300 invocation
    res = bus.execute_tool_300(tool_id=1, params={"test": True})
    assert res["status"] in ["SUCCESS", "FALLBACK_SUCCESS"]

def test_aladdin_risk_var_and_cvar():
    # $10M portfolio, 1.8% daily vol, 95% confidence
    risk = AladdinRiskEngine.calculate_parametric_var(10000000.0, 0.018, 0.95, 1)
    assert risk["var_usd"] > 0.0
    assert risk["cvar_usd"] > risk["var_usd"]  # Expected shortfall always exceeds VaR
    assert 2.0 <= risk["var_percent"] <= 4.0

def test_aladdin_risk_scenario_stress_testing():
    portfolio = {
        "equities": 5000000.0,
        "bonds": 3000000.0,
        "venture": 1000000.0,
        "cash": 1000000.0
    }
    scenarios = AladdinRiskEngine.run_scenario_stress_test(portfolio)
    assert len(scenarios) == 3
    
    # 2008 shock must cause negative net PnL
    gfc = scenarios[0]
    assert gfc["scenario"] == "2008 Liquidity & Banking Shock"
    assert gfc["net_pnl_usd"] < 0.0
    assert gfc["drawdown_percent"] < -10.0

def test_knowledge_graph_node_and_edge_traversal(tmp_path):
    db_file = str(tmp_path / "test_kg.db")
    kg = UniversalKnowledgeGraph(db_file)
    
    # Add nodes
    kg.add_node("COMP-TSMC", "Company", "TSMC", {"country": "Taiwan"})
    kg.add_node("COMP-APPLE", "Company", "Apple Inc", {"country": "USA"})
    kg.add_node("TECH-3NM", "Technology", "3nm N3E Process", {"node": "3nm"})
    
    # Add edges
    kg.add_edge("COMP-APPLE", "USES", "TECH-3NM", confidence=0.99)
    kg.add_edge("COMP-TSMC", "BUILDS", "TECH-3NM", confidence=1.0)
    
    counts = kg.count_nodes_and_edges()
    assert counts["nodes"] == 3
    assert counts["edges"] == 2
    
    # Neighbors
    neighbors = kg.get_neighbors("COMP-APPLE")
    assert len(neighbors) == 1
    assert neighbors[0]["target_name"] == "3nm N3E Process"

def test_digital_twin_business_simulation():
    res = DigitalTwinSimulator.simulate_business_what_if(
        baseline_revenue=1000000.0,
        baseline_cogs=200000.0,
        baseline_opex=500000.0,
        price_change_percent=10.0,
        demand_change_percent=-5.0,
        tariff_shock_percent=25.0
    )
    assert res["projected"]["revenue_usd"] > 0.0
    assert res["projected"]["cogs_usd"] > res["baseline"]["cogs_usd"]  # Tariffs inflate COGS
    assert "sensitivity_risks" in res

def test_chipflow_pilot_outreach_manifest_and_touches():
    manifest = ChipFlowPilotOutreach.generate_pilot_manifest(limit=250)
    assert len(manifest) == 250
    assert manifest[0]["target_id"] == "TGT-FABLESS-001"
    assert manifest[0]["tier"] == "TIER_1_PILOT"
    assert manifest[-1]["tier"] == "TIER_2_EXPANSION"
    
    touches = ChipFlowPilotOutreach.get_three_touch_sequence()
    assert "touch_1" in touches
    assert "touch_2" in touches
    assert "touch_3" in touches
    assert "CPGD" in touches["touch_1"]["body"]

def test_dashboard_html_structure():
    dashboard_path = os.path.join(os.path.dirname(__file__), "..", "ui", "dashboard.html")
    assert os.path.isfile(dashboard_path)
    with open(dashboard_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert "Civilization OS" in html
    assert "MSN-SEMI-001" in html
    assert "ChipFlow AI" in html
