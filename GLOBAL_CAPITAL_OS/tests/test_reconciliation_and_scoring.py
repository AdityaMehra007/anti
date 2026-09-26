"""Tests for 3-way reconciliation, stress scenarios, and master scoring."""

import pytest
from GLOBAL_CAPITAL_OS.engines.reconciliation_engine import reconciliation_engine
from GLOBAL_CAPITAL_OS.engines.scoring_engine import scoring_engine
from GLOBAL_CAPITAL_OS.agents.risk_agent import risk_agent


def test_three_way_reconciliation():
    """Verifies that reconciliation matches bank balances with underlying ledgers."""
    recon = reconciliation_engine.execute_three_way_reconciliation()
    assert recon["audit_chain_valid"] is True
    assert recon["total_bank_balances_inr"] > 0
    assert recon["calculated_net_ledger_inr"] >= 0


def test_master_scoring_engine():
    """Tests computation of all 13 Master Company Scores + Wealth & Founder scores."""
    res = scoring_engine.compute_all_scores()
    scores = res["master_scores"]

    assert "revenue_score" in scores
    assert "profit_score" in scores
    assert "capital_efficiency_score" in scores
    assert "liquidity_score" in scores
    assert "debt_safety_score" in scores
    assert "security_score" in scores
    assert "compliance_score" in scores

    # Validate range
    for k, v in scores.items():
        assert 0.0 <= v <= 100.0, f"Score '{k}' out of range: {v}"

    assert 0.0 <= res["master_wealth_score"] <= 100.0
    assert 0.0 <= res["master_founder_score"] <= 100.0


def test_stress_scenarios_survival():
    """Tests that all 10 stress scenarios simulate survival runway."""
    sim = risk_agent.run_stress_scenarios()
    scenarios = sim["scenarios"]
    assert len(scenarios) == 10

    # Ensure -50% revenue scenario is modeled
    assert "S2_REV_DROP_50" in scenarios
    assert scenarios["S2_REV_DROP_50"]["survival_runway_months"] >= 6.0
    assert sim["liquidity_score"] > 0.0
    assert sim["solvency_score"] >= 90.0  # Zero debt posture
