"""
tests/test_omega_hub.py — Unit tests for OMEGA Executive Control Plane CLI
"""

import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.omega_hub import get_system_status

def test_system_status_structure():
    status = get_system_status()
    assert "repo_root" in status
    assert "database_ready" in status
    assert "tests_passed" in status
    assert "portfolio_exists" in status
    assert status["portfolio_exists"] is True
    assert status["manifesto_exists"] is True

def test_prospect_miner_integration():
    from omnimoney.prospect_miner import ProspectMiner
    miner = ProspectMiner()
    prospects = miner.mine_high_value_prospects(limit=3)
    assert len(prospects) > 0
    assert "company" in prospects[0]
    assert "fit_score" in prospects[0]

def test_interview_cockpit_dossier_generation(tmp_path):
    from scripts.interview_cockpit import InterviewCockpit
    res = InterviewCockpit.generate_prep_dossier("Target Corp", "Operations Specialist", "ROUND_1_HR_SCREEN")
    assert "filepath" in res
    assert Path(res["filepath"]).exists()
    content = Path(res["filepath"]).read_text(encoding="utf-8")
    assert "Target Corp" in content
    assert "Aditya Mehra" in content

def test_offer_negotiator_evaluation():
    from scripts.offer_negotiator import OfferNegotiator
    evaluation = OfferNegotiator.evaluate_offer(7.5)
    assert "suggested_counter_ctc_lpa" in evaluation
    assert evaluation["suggested_counter_ctc_lpa"] > 7.5
