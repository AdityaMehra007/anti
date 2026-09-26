import os
import pytest
from omnimoney.omnimoney_engine import (
    OmniMoneyEngine,
    Opportunity,
    EconomicAction,
    calculate_opportunity_score,
)

def test_calculate_opportunity_score():
    # High demand (9), High margin (9), Fast speed (8), Low competition (4), High fit (9)
    score = calculate_opportunity_score(demand=9, margin=9, speed=8, competition=4, fit=9)
    assert 0 <= score <= 100
    assert score >= 80

def test_calculate_opportunity_score_bounds():
    low_score = calculate_opportunity_score(demand=1, margin=1, speed=1, competition=10, fit=1)
    assert 0 <= low_score <= 100
    assert low_score < 30

def test_engine_initialization():
    engine = OmniMoneyEngine()
    assert engine is not None
    assert len(engine.get_monetizable_services()) >= 10
    assert len(engine.get_bengaluru_customer_categories()) >= 20

def test_section_153_highest_probability_action():
    engine = OmniMoneyEngine()
    action = engine.get_highest_probability_action()
    assert isinstance(action, EconomicAction)
    assert action.opportunity is not None
    assert action.customer is not None
    assert action.problem is not None
    assert action.offer is not None
    assert action.price_inr > 0
    assert action.acquisition_channel is not None
    assert action.exact_next_action is not None

def test_top_ranked_opportunities():
    engine = OmniMoneyEngine()
    opps = engine.get_ranked_opportunities(limit=5)
    assert len(opps) == 5
    # Should be sorted descending by score
    scores = [o.score for o in opps]
    assert scores == sorted(scores, reverse=True)

def test_b2b_sales_engine():
    from omnimoney.b2b_sales_engine import B2BSalesEngine, LeadStatus
    sales = B2BSalesEngine()
    prospects = sales.get_prospects()
    assert len(prospects) >= 5

    # Test status update
    lead_id = prospects[0].id
    assert sales.update_status(lead_id, LeadStatus.AUDIT_SENT, "Demo sent") is True
    assert prospects[0].status == LeadStatus.AUDIT_SENT

    # Test pipeline summary
    summary = sales.get_pipeline_summary()
    assert summary["total_leads"] == len(prospects)
    assert summary["pipeline_value_inr"] > 0

    # Test script generation
    script = sales.generate_outreach_script("whatsapp_clinic_audit", "Dr. Rao", "Aura Clinic")
    assert "Dr. Rao" in script
    assert "WhatsApp" in script

def test_master_scoring_system():
    from omnimoney.scoring_system import compute_master_scorecard, generate_markdown_scorecard
    scorecard = compute_master_scorecard()
    assert scorecard["composite_score"] >= 90.0
    assert scorecard["grade"] in ["A", "A+"]
    assert len(scorecard["opportunities"]) == 5
    path = generate_markdown_scorecard("reports/SYSTEM_MASTER_SCORECARD.md")
    assert os.path.exists(path)


