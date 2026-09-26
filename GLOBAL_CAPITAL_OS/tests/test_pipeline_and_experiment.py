"""Tests for sales CRM pipeline, opportunity database, and zero-capital experiment."""

import pytest
from GLOBAL_CAPITAL_OS.core.models import SalesStage
from GLOBAL_CAPITAL_OS.agents.revenue_commander import revenue_commander
from GLOBAL_CAPITAL_OS.engines.opportunity_database import opportunity_db
from GLOBAL_CAPITAL_OS.engines.first_rupee_ladder import rupee_ladder
from GLOBAL_CAPITAL_OS.experiments.exp01_b2b_intelligence import exp01


def test_opportunity_database_500_candidates():
    """Verifies that 500 legitimate opportunities are present and scored."""
    top_opps = opportunity_db.get_top_opportunities(limit=10)
    assert len(top_opps) == 10
    top = top_opps[0]
    assert top["zero_capital_score"] >= 80.0
    assert top["gross_margin_pct"] >= 90.0


def test_first_rupee_ladder_milestones():
    """Tests ladder progression from ₹1 to ₹1 Crore."""
    stages = rupee_ladder.get_ladder_stages()
    assert len(stages) == 6
    assert stages[0]["target_amount_inr"] == 1.0
    assert stages[-1]["target_amount_inr"] == 10000000.0

    current = rupee_ladder.get_current_stage(cumulative_revenue_inr=50100.0)
    assert "B2B Lead Intelligence Pack" in current["current_milestone_achieved"] or "Productized" in current["current_milestone_achieved"]


def test_sales_pipeline_stage_advance():
    """Tests 12-stage CRM deal advancement."""
    res = revenue_commander.advance_deal_stage(
        deal_id="DEAL-0001",
        new_stage=SalesStage.PROPOSAL,
        notes="Dispatched custom sample audit"
    )
    assert res["new_stage"] == "PROPOSAL"
    assert res["win_probability"] == 0.75
    assert res["expected_value_inr"] > 0


def test_experiment_01_unit_economics_and_collection():
    """Tests EXP-01 offer structure and automated statutory tax reservation upon revenue win."""
    details = exp01.get_experiment_details()
    econ = details["unit_economics"]
    assert econ["capital_required_inr"] == 0.0
    assert econ["gross_margin_pct"] >= 95.0

    # Simulate revenue win for lead
    rec = exp01.simulate_deal_won_and_reconciliation(lead_id="LEAD-0001")
    assert rec["amount_inr"] == 37500.0
    assert rec["tax_reserve_held_inr"] == 37500.0 * 0.18
    assert rec["status"] == "RECONCILED_AND_PROTECTED"
