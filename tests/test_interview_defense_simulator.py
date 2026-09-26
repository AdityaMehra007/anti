import os
import sys
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from interview_defense_simulator import InterviewDefenseSimulator, DefenseEvaluation

def test_load_scenarios():
    sim = InterviewDefenseSimulator()
    scenarios = sim.load_scenarios()
    assert len(scenarios) >= 4
    assert scenarios[0]["scenario_id"] == "SCEN-001-AERO-INDIA-RUN-OF-SHOW"

def test_evaluate_candidate_answer_high_score():
    sim = InterviewDefenseSimulator()
    sample_answer = """
    At Aero India 2025, when the AV vendor was stalled at Gate 4, my task was to ensure 100% booth readiness by 07:30 AM.
    I immediately deployed our liaison officer with the master manifest to the gate while directing the crew to use backup gear.
    We completed setup at 07:22 AM with 100% on-time readiness and zero inventory shrinkage across 100k+ attendees.
    """
    eval_result = sim.evaluate_response("SCEN-001-AERO-INDIA-RUN-OF-SHOW", sample_answer)
    assert eval_result.overall_score >= 80.0
    assert eval_result.metrics_cited >= 2
    assert "READY" in eval_result.readiness_status

def test_evaluate_candidate_answer_low_score():
    sim = InterviewDefenseSimulator()
    weak_answer = "I just asked the vendor to hurry up and waited for them."
    eval_result = sim.evaluate_response("SCEN-001-AERO-INDIA-RUN-OF-SHOW", weak_answer)
    assert eval_result.overall_score < 60.0
    assert "NEEDS_REHEARSAL" in eval_result.readiness_status
