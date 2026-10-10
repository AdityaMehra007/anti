"""Unit tests for BSU OS Multi-Agent Copilot & Section 197 Contract."""

import pytest
from bsu_os.copilot_engine import CopilotEngine
from bsu_os.seed_data import seed_database


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_database()


def test_copilot_routing():
    copilot = CopilotEngine()
    assert copilot.route_agent("What is the salary for CUDA engineers?") == "career"
    assert copilot.route_agent("Which startups should a VC invest in?") == "investor"
    assert copilot.route_agent("Is Koramangala better than Whitefield for an office?") == "geo"
    assert copilot.route_agent("How did Zerodha build their moat?") == "founder"


def test_copilot_output_contract():
    copilot = CopilotEngine()
    response = copilot.query("Show me high paying AI roles in Bengaluru")

    # Verify Section 197 Output Contract fields
    assert "verdict" in response
    assert "evidence" in response
    assert isinstance(response["evidence"], list)
    assert len(response["evidence"]) >= 1
    assert "why_it_matters" in response
    assert "fit_score" in response
    assert 0.0 <= response["fit_score"] <= 100.0
    assert "recommended_action" in response
    assert "risk_factors" in response
    assert isinstance(response["risk_factors"], list)
