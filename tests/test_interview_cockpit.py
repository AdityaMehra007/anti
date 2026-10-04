#!/usr/bin/env python3
"""
tests/test_interview_cockpit.py — Verification of Interview Cockpit & Offer Negotiator
======================================================================================
Tests:
  1. Recruiter round classification accuracy.
  2. Interview prep briefing pack generation and STAR metric integrity.
  3. Offer evaluation logic across Bangalore GCC salary brackets.
  4. Counter-offer letter generation and target CTC constraints.
"""

import pytest
from pathlib import Path
from scripts.interview_cockpit import InterviewCockpit, CANDIDATE_PROFILE
from scripts.offer_negotiator import OfferNegotiator, GCC_BENCHMARKS

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_interview_round_classification():
    # Test HR screen
    text_hr = "Hi Aditya, we would love to schedule a quick 15-minute introductory call to understand your availability."
    assert InterviewCockpit.classify_round(text_hr) == "ROUND_1_HR_SCREEN"

    # Test Operations domain
    text_ops = "In the next round, our Operations Director will assess your process workflow and logistics experience from AERO India."
    assert InterviewCockpit.classify_round(text_ops) == "ROUND_2_OPERATIONS_DOMAIN"

    # Test AI data ops case
    text_ai = "Please be prepared to walk through your computer vision dataset QA methodology and Instawork experience."
    assert InterviewCockpit.classify_round(text_ai) == "ROUND_3_AI_OPS_CASE"

    # Test Executive bar-raiser
    text_exec = "You will be meeting our VP and Executive Leadership team for the strategic bar raiser."
    assert InterviewCockpit.classify_round(text_exec) == "ROUND_4_EXECUTIVE_BAR_RAISER"

    # Test Offer CTC round
    text_offer = "We are pleased to discuss the formal offer and CTC compensation breakdown."
    assert InterviewCockpit.classify_round(text_offer) == "ROUND_5_OFFER_CTC"

def test_interview_prep_dossier_synthesis(tmp_path):
    res = InterviewCockpit.generate_prep_dossier(
        company_name="Amazon India",
        role_title="Operations Specialist",
        round_type="ROUND_2_OPERATIONS_DOMAIN"
    )

    assert res["company"] == "Amazon India"
    assert res["round_type"] == "ROUND_2_OPERATIONS_DOMAIN"
    assert res["talking_points_count"] >= 3

    path = Path(res["filepath"])
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "AERO India 2025" in content
    assert "Aditya Mehra" in content
    assert "Instawork" in content
    assert "STAR Story" in content

def test_offer_negotiator_evaluation():
    # Sub-market offer
    sub = OfferNegotiator.evaluate_offer(550000)
    assert sub["rating"] == "BELOW_MARKET"
    assert sub["recommended_counter"] == GCC_BENCHMARKS["market_median_base"]
    assert sub["stance"] == "FIRM_UPWARD_REVISION"

    # Entry market offer
    entry = OfferNegotiator.evaluate_offer(750000)
    assert entry["rating"] == "FAIR_ENTRY"
    assert entry["recommended_counter"] == GCC_BENCHMARKS["top_quartile_target"]
    assert entry["stance"] == "STANDARD_TOP_TIER_COUNTER"

    # High target offer
    high = OfferNegotiator.evaluate_offer(950000)
    assert high["rating"] == "STRONG_TARGET"
    assert high["recommended_counter"] == GCC_BENCHMARKS["elite_stretch_ceiling"]

def test_counter_offer_letter_generation():
    res = OfferNegotiator.generate_counter_letter("Walmart Global Tech", "Business Operations Analyst", 750000)
    assert res["company"] == "Walmart Global Tech"
    assert res["evaluation"]["recommended_counter"] == 950000

    path = Path(res["letter_path"])
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Aditya Mehra" in text
    assert "AERO India 2025" in text
    assert "Instawork" in text
    assert "950,000" in text
