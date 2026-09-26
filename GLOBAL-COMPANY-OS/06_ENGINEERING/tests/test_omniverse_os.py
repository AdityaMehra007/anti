import os
import sys
import json
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.api import app
from src.omniverse_service import OmniverseService

OS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def test_opportunity_map_count_and_vectors():
    opps = OmniverseService.get_opportunities(limit=500)
    assert len(opps) >= 100, f"Expected at least 100 opportunities, got {len(opps)}"
    
    required_vectors = [
        "demand", "urgency", "wtp", "scalability", "ai_advantage",
        "margin", "competition", "capital_intensity", "time_to_revenue_days",
        "regulatory_risk", "composite_score"
    ]
    for o in opps:
        for v in required_vectors:
            assert v in o, f"Opportunity {o.get('id')} missing vector {v}"
            assert isinstance(o[v], (int, float)), f"Vector {v} in {o.get('id')} must be numeric"

def test_customer_problem_map_count_and_schema():
    problems = OmniverseService.get_problems(limit=500)
    assert len(problems) >= 100, f"Expected at least 100 customer problems, got {len(problems)}"
    
    required_keys = [
        "problem_id", "title", "industry", "customer_segment",
        "severity", "frequency", "economic_impact", "current_solution",
        "dissatisfaction", "willingness_to_pay"
    ]
    for p in problems:
        for k in required_keys:
            assert k in p and p[k], f"Problem {p.get('problem_id')} missing or empty field {k}"

def test_automation_map_count_and_levels():
    automations = OmniverseService.get_automations(limit=500)
    assert len(automations) >= 100, f"Expected at least 100 automations, got {len(automations)}"
    
    levels_found = set()
    for a in automations:
        assert "workflow_id" in a
        assert "autonomy_level" in a
        assert 0 <= a["autonomy_level"] <= 5
        levels_found.add(a["autonomy_level"])
    assert len(levels_found) >= 3, "Expected diverse autonomy levels"

def test_winner_nine_gate_validation():
    winner_dossier = OmniverseService.get_winner_dossier()
    assert winner_dossier["beachhead_business"] == "TradeNexus AI"
    assert winner_dossier["status"] == "APPROVED FOR AUTONOMOUS SCALE"
    assert len(winner_dossier["tests_passed"]) == 9
    
    # Assert all 9 Part LXXXVI tests are explicitly addressed
    test_names = ["CUSTOMER", "PAYMENT", "VALUE", "DELIVERY", "ECONOMICS", "SCALE", "AUTOMATION", "DEFENSE", "TRUST"]
    all_tests_str = " ".join(winner_dossier["tests_passed"])
    for t in test_names:
        assert t in all_tests_str, f"Missing Part LXXXVI gate test: {t}"

def test_all_10_documents_exist_and_non_empty():
    docs = [
        os.path.join(OS_ROOT, "01_STRATEGY", "GLOBAL_BUSINESS_OPPORTUNITY_MAP_100.md"),
        os.path.join(OS_ROOT, "03_CUSTOMERS", "GLOBAL_CUSTOMER_PROBLEM_MAP_100.md"),
        os.path.join(OS_ROOT, "25_AUTOMATIONS", "AI_AUTOMATION_MAP_100.md"),
        os.path.join(OS_ROOT, "01_STRATEGY", "BUSINESS_MODEL_MAP.md"),
        os.path.join(OS_ROOT, "04_COMPETITORS", "GLOBAL_COMPETITOR_MAP.md"),
        os.path.join(OS_ROOT, "01_STRATEGY", "WHITE_SPACE_MAP.md"),
        os.path.join(OS_ROOT, "01_STRATEGY", "TOP_10_OPPORTUNITIES_DEEP_DIVE.md"),
        os.path.join(OS_ROOT, "01_STRATEGY", "TOP_3_STRATEGIC_BLUEPRINTS.md"),
        os.path.join(OS_ROOT, "01_STRATEGY", "WINNER_SELECTION_AND_EVIDENCE.md"),
        os.path.join(OS_ROOT, "05_PRODUCT", "MASTER_EXECUTION_BLUEPRINT.md"),
    ]
    for d in docs:
        assert os.path.isfile(d), f"Missing document: {d}"
        assert os.path.getsize(d) > 500, f"Document too small: {d}"

def test_api_omniverse_endpoints():
    client = TestClient(app)
    
    # Summary
    sum_res = client.get("/api/v1/os/summary")
    assert sum_res.status_code == 200
    sum_data = sum_res.json()
    assert sum_data["total_opportunities"] >= 100
    assert sum_data["total_problems"] >= 100
    assert sum_data["total_automations"] >= 100
    
    # Opportunities
    opp_res = client.get("/api/v1/os/opportunities?limit=10")
    assert opp_res.status_code == 200
    assert len(opp_res.json()) == 10
    
    # Problems
    prb_res = client.get("/api/v1/os/problems?limit=5")
    assert prb_res.status_code == 200
    assert len(prb_res.json()) == 5
    
    # Automations
    aut_res = client.get("/api/v1/os/automations?limit=5")
    assert aut_res.status_code == 200
    assert len(aut_res.json()) == 5
    
    # Winner
    win_res = client.get("/api/v1/os/winner")
    assert win_res.status_code == 200
    win_data = win_res.json()
    assert win_data["beachhead_business"] == "TradeNexus AI"
