"""
tests/test_future_plans_orchestrator.py
=======================================
Verification suite for the 2026-2060 Sovereign Future Master Plan and Orchestrator.
"""

from pathlib import Path
import pytest
from omega.orchestration.future_plans_orchestrator import FuturePlansOrchestrator, HORIZON_PROJECTIONS

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_future_plan_document_and_invariants_verified():
    orchestrator = FuturePlansOrchestrator()
    verification = orchestrator.verify_plan_invariants()

    assert verification["all_verified"] is True
    assert verification["doc_invariants"]["candidate_name"] is True
    assert verification["doc_invariants"]["education"] is True
    assert verification["doc_invariants"]["aero_india"] is True
    assert verification["doc_invariants"]["instawork_qa"] is True
    assert verification["doc_invariants"]["compensation_floor"] is True
    assert verification["doc_invariants"]["horizon_1_present"] is True
    assert verification["doc_invariants"]["horizon_5_present"] is True


def test_future_plan_projection_simulation_and_persistence():
    orchestrator = FuturePlansOrchestrator()
    dossier = orchestrator.generate_projection_dossier()

    assert dossier["verification_status"] == "VERIFIED"
    assert len(dossier["horizons"]) == 5
    assert dossier["principal"] == "Aditya Mehra"

    json_file = REPO_ROOT / "omega" / "data" / "future_plans_projection.json"
    assert json_file.exists()


def test_terminal_horizon_quadrillion_grid_metrics():
    h5 = HORIZON_PROJECTIONS[-1]
    assert h5["horizon_id"] == "H5_2060_BANK_OF_CONTINUUM"
    assert "$3,600,000,000,000" in h5["implied_valuation_usd"]
    assert "36.00 bps of World GDP" in h5["key_metrics"]
