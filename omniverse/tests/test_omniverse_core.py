"""
ANTIGRAVITY OMNIVERSE: CORE TEST SUITE
======================================
Verifies system primitives, truth engine cryptographic integrity, 7-tier memory,
executive council debate, quality index scoring, and the Universal Execution Loop.
"""
import pytest
import os
import sys

# Ensure root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from omniverse.core.primitives import ProvenanceEnvelope, HumanControlTier, AutonomyTier
from omniverse.core.truth_engine import TruthEngine
from omniverse.memory.memory_manager import OmniverseMemoryEngine
from omniverse.agents.executive_council import ExecutiveCouncil
from omniverse.evaluation.quality_scorer import QualityScorer
from omniverse.orchestrator.master_orchestrator import OmniverseMasterOrchestrator

def test_primitives_and_provenance_envelope():
    env = ProvenanceEnvelope(
        source="Test Source",
        source_url="https://example.com/data",
        source_date="2026-09-16",
        owner="Test Owner",
        license="MIT",
        confidence_score=0.95
    )
    h = env.compute_hash(b"test data payload")
    assert len(h) == 64
    assert env.sha256_hash == h
    assert env.confidence_score == 0.95

def test_truth_engine_recording_and_verification():
    te = TruthEngine()
    rec = te.record_claim(
        claim_text="TSMC 3nm foundry capacity is at 98% utilization",
        source="SIA Industry Report",
        source_date="2026-Q2",
        evidence="Quarterly Foundry Allocation Filing",
        confidence=0.97
    )
    assert rec["claim_id"].startswith("CLM-")
    assert te.verify_claim(rec["claim_id"]) is True
    assert te.verify_claim("NON-EXISTENT-ID") is False

def test_memory_engine_working_and_persistent_tiers(tmp_path):
    db_file = str(tmp_path / "test_mem.db")
    mem = OmniverseMemoryEngine(db_file)
    
    # Working memory
    mem.set_working("current_focus", "Semiconductor Architecture")
    assert mem.get_working("current_focus") == "Semiconductor Architecture"
    
    # Persistent memory
    mem.persist("DECISION", "DEC-001", {"action": "APPROVE_CHIPFLOW"}, {"domain": "SEMI"})
    res = mem.query("DECISION", "DEC-001")
    assert len(res) == 1
    assert res[0]["value"]["action"] == "APPROVE_CHIPFLOW"

def test_executive_council_roster_and_debate():
    council = ExecutiveCouncil()
    cto = council.get_agent("AGT-CTO")
    assert cto is not None
    assert cto.name == "Chief Technology Agent"
    assert cto.autonomy_tier == AutonomyTier.LEVEL_3_LOCAL_EXEC

    debate = council.convene_debate("Deploy Edge Silicon ASIC", "Scale to 50k units")
    assert debate["consensus_verdict"] == "APPROVED_STAGE_1_MVP"
    assert len(debate["proponent_arguments"]) > 0
    assert len(debate["counter_arguments"]) > 0

def test_quality_scorer_and_readiness_gates():
    scores = {
        "reliability": 100.0,
        "accuracy": 100.0,
        "latency": 90.0,
        "cost_efficiency": 95.0,
        "security": 100.0,
        "scalability": 90.0,
        "maintainability": 95.0,
        "usability": 95.0,
        "automation": 95.0,
        "observability": 95.0
    }
    oqi = QualityScorer.compute_oqi(scores)
    assert oqi >= 90.0

    gates = {
        "technical": True,
        "security": True,
        "data": True,
        "operational": True,
        "financial": True,
        "compliance": True,
        "user": True,
        "recovery": True
    }
    readiness = QualityScorer.evaluate_readiness(gates)
    assert readiness["production_ready"] is True
    assert readiness["readiness_percentage"] == 100.0

def test_master_orchestrator_execution_loop(tmp_path):
    db_file = str(tmp_path / "test_orch.db")
    orch = OmniverseMasterOrchestrator(db_file)
    
    # Green tier execution
    res = orch.execute_universal_loop("Analyze Edge AI Silicon", "SEMI", HumanControlTier.GREEN)
    assert res["status"] == "COMPLETED"
    assert res["mission_id"].startswith("MSN-")
    assert res["oqi_score"] >= 90.0
    assert "truth_claim_id" in res

    # Red tier hard gate blocking
    red_res = orch.execute_universal_loop("Transfer $500k to Fab", "FINANCE", HumanControlTier.RED)
    assert red_res["status"] == "BLOCKED_AWAITING_HUMAN_APPROVAL"
