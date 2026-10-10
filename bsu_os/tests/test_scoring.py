"""Unit tests for BSU OS Multi-Factor Mathematical Scoring Engine."""

import pytest
from bsu_os.scoring_engine import (
    compute_power_score,
    compute_career_score,
    compute_momentum_score,
    compute_risk_score,
    compute_future_potential_score,
    score_startup
)


@pytest.fixture
def sample_startup():
    return {
        "name": "OmniGen Bangalore",
        "sector": "AI / ML",
        "sub_sector": "Foundational LLMs",
        "stage": "Series A",
        "total_funding_usd": 40_000_000.0,
        "headcount": 80,
        "hiring_status": True,
        "tech_stack": ["PyTorch", "CUDA", "Triton", "Ray", "vLLM", "C++"],
        "founders": [
            {
                "name": "Test Founder",
                "prior_exits": True,
                "educational_background": "PhD Computer Science, IIT Bombay"
            }
        ],
        "funding_rounds": [
            {
                "round_name": "Series A",
                "amount_usd": 40_000_000.0,
                "round_date": "2024-05-10"
            }
        ]
    }


def test_power_score_bounds(sample_startup):
    """Ensures Power Score stays strictly between 0.0 and 100.0."""
    score = compute_power_score(sample_startup)
    assert 0.0 <= score <= 100.0
    assert score > 75.0, "High-pedigree Series A AI startup should score high on power."


def test_career_score_bounds(sample_startup):
    """Ensures Career Score behaves appropriately with salary tiers."""
    job = {"max_salary_lpa": 90.0}
    score = compute_career_score(sample_startup, job)
    assert 0.0 <= score <= 100.0
    assert score >= 80.0


def test_risk_score_bounds(sample_startup):
    """Ensures Risk Score is calibrated."""
    score = compute_risk_score(sample_startup)
    assert 0.0 <= score <= 100.0


def test_score_startup_dict(sample_startup):
    """Ensures all 5 scores are generated."""
    scores = score_startup(sample_startup)
    required_keys = ["power_score", "career_score", "momentum_score", "risk_score", "future_potential_score"]
    for k in required_keys:
        assert k in scores
        assert isinstance(scores[k], float)
        assert 0.0 <= scores[k] <= 100.0
