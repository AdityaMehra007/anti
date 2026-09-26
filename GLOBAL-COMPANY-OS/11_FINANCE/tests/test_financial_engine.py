import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from financial_engine import FinancialEngine

def test_scale_ladder():
    ladder = FinancialEngine.calculate_scale_ladder()
    assert len(ladder) == 9
    assert ladder[0]["tier"] == "₹1"
    assert ladder[-1]["tier"] == "₹1,000 Crore"
    assert ladder[3]["arr_inr"] == 1200000

def test_project_scenarios():
    scenarios = FinancialEngine.project_scenarios(12)
    assert "Survival" in scenarios
    assert "Base" in scenarios
    assert "Breakout" in scenarios
    assert scenarios["Base"]["cash_flow_positive"] is True
