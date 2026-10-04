"""
tests/test_transcendence_engine.py
==================================
Tests for OMEGA Transcendence Engine and OMEGA_TRANSCENDENCE_X_SUPREME_PROMPT.
"""

from pathlib import Path
import pytest
from omega.orchestration.transcendence_engine import TranscendenceEngine

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_transcendence_prompt_exists_and_integrity():
    engine = TranscendenceEngine()
    audit = engine.run_self_audit()

    assert audit["ground_truth_verified"] is True
    assert audit["all_modules_present"] is True
    assert len(audit["prompt_sha256"]) == 64
    assert audit["ground_truth_details"]["candidate_name"] is True
    assert audit["ground_truth_details"]["education"] is True
    assert audit["ground_truth_details"]["flagship_leadership"] is True
    assert audit["ground_truth_details"]["ai_ops_precision"] is True
    assert audit["ground_truth_details"]["salary_floor_enforced"] is True


def test_transcendence_execution_cycle_deterministic():
    engine = TranscendenceEngine()
    res = engine.execute_transcendence_cycle()

    assert res["status"] == "TRANSCENDENT_TRIUMPH_VERIFIED"
    assert res["test_success"] is True
    assert res["elapsed_seconds"] > 0
    assert "TRANSCENDENCE-CYCLE-" in res["cycle_id"]
    assert "DO-EVERYTHING-" in res["hyper_manifest_id"]
