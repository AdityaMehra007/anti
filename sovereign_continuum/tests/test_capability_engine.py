"""
Test Suite for CIVILIZATION Ω∞∞ Autonomous Capability Generation Engine.

Verifies:
- Universal Problem Graph & Root Cause Resolution
- Failed Solution Memory & Zero Regression Enforcement
- The Unknown Engine Epistemic Audit
- Second-Order Effect Causal Ripple Simulator
- Recursive Capability Generator & Specification Synthesis
- Sovereign Empire Orchestrator Integration
- FastAPI Capability Gateway Endpoints
"""

import pytest
from fastapi.testclient import TestClient

from sovereign_continuum.capability_engine import (
    CivilizationCapabilityGenerator,
    UniversalProblemGraph,
    FailedSolutionMemory,
    UnknownEngine,
    SecondOrderEffectSimulator,
    ProblemNode,
    ProblemScale,
    ProblemStatus,
    FailedSolutionRecord,
)
from sovereign_continuum.empire_orchestrator import SovereignEmpireOrchestrator
from sovereign_continuum.api.gateway import app


def test_problem_graph_topology_and_root_causes():
    graph = UniversalProblemGraph()

    # Upstream root problem
    root_prob = ProblemNode(
        problem_id="PROB-ROOT-001",
        scale=ProblemScale.CIVILIZATIONAL,
        domain="Epistemics",
        title="Unverified Information Propagation",
        description="False claims and hallucinations spread faster than empirical verification.",
        root_causes=["Lack of cryptographic provenance", "Engagement-maximizing feed algorithms"],
    )
    graph.register_problem(root_prob)

    # Downstream enterprise problem
    downstream_prob = ProblemNode(
        problem_id="PROB-DOWN-001",
        scale=ProblemScale.ENTERPRISE,
        domain="Corporate Governance",
        title="Hallucinated Candidate Credentials",
        description="Firms hire candidates with fabricated CV credentials.",
        root_causes=["Unverified resume claims"],
    )
    graph.register_problem(downstream_prob)

    # Link upstream to downstream
    linked = graph.link_problems("PROB-ROOT-001", "PROB-DOWN-001")
    assert linked is True

    # Check root cause resolution
    discovered_roots = graph.resolve_root_causes("PROB-DOWN-001")
    assert len(discovered_roots) == 1
    assert discovered_roots[0].problem_id == "PROB-ROOT-001"

    # Check open problems
    open_probs = graph.get_open_problems()
    assert len(open_probs) == 2


def test_failed_solution_memory_zero_regression():
    memory = FailedSolutionMemory()

    record = FailedSolutionRecord(
        record_id="FAIL-TEST-001",
        solution_id="SOL-NAIVE-RL",
        problem_id="PROB-ROBOTICS-001",
        hypothesis="Train humanoid locomotion purely in sim without domain randomization or latency injection",
        failure_mode="Sim-to-real reality gap collapse; robot hardware motors violently vibrated and tripped breakers",
        root_cause_analysis="Real-world actuators have non-linear compliance, sensor latency, and gear backlash absent in naive physics sim.",
        conditions_under_which_it_failed={"environment": "physical_concrete", "motor_temp_c": 45.0},
        lessons_learned=[
            "Always apply heavy domain randomization to torque limits",
            "Inject artificial 5-15ms sensor latency into training environment",
        ],
    )
    memory.record_failure(record)
    assert memory.total_count() == 1

    # Check query and match
    match = memory.has_failed_previously(
        hypothesis="Train humanoid locomotion purely in sim without domain randomization",
        problem_id="PROB-ROBOTICS-001",
    )
    assert match is not None
    assert match.record_id == "FAIL-TEST-001"

    # Novel hypothesis should NOT match
    novel = memory.has_failed_previously(
        hypothesis="Apply sim-to-real transfer with 200 Hz edge kernel and domain randomization",
        problem_id="PROB-ROBOTICS-001",
    )
    assert novel is None


def test_unknown_engine_blind_spot_audit():
    engine = UnknownEngine()

    audit = engine.audit_blind_spots(
        initiative_name="Instantaneous Global M2M Invoicing",
        domain="Financial Infrastructure",
        assumptions=["zero-cost transactions", "instant global settlement across all jurisdictions"],
    )

    assert "missing_prerequisites" in audit
    assert "unstated_assumptions" in audit
    assert len(audit["missing_prerequisites"]) >= 2
    assert audit["audit_verdict"] == "PROCEED_WITH_CONTROLS"
    assert "why_hasnt_this_been_done" in audit


def test_second_order_effect_simulation():
    sim = SecondOrderEffectSimulator()

    results = sim.simulate_effects(
        action_name="Deploy Autonomous 500k Humanoid Robot Swarm",
        target_sector="Manufacturing",
        magnitude_scale=3.0,
    )

    assert results["cascading_risk_score"] > 3.0
    assert len(results["first_order_direct"]) >= 1
    assert len(results["second_order_counterparty_reactions"]) >= 2
    assert len(results["third_order_systemic_equilibrium"]) >= 1
    assert len(results["circuit_breakers"]) >= 2


def test_capability_generator_synthesis_and_regression_rejection():
    generator = CivilizationCapabilityGenerator()

    # 1. Propose hypothesis that matches seeded failure (FAIL-001)
    failing_attempt = generator.synthesize_capability(
        problem_id="PROB-ENERGY-001",
        proposed_hypothesis="Power 24/7 500MW AI hub using solar panels without nuclear baseload or battery buffers",
        domain="Energy & Infrastructure",
    )
    assert failing_attempt["success"] is False
    assert failing_attempt["status"] == "REJECTED_BY_FAILED_SOLUTION_MEMORY"
    assert "Directive 123" in failing_attempt["directive"]

    # 2. Propose sound hypothesis with SMR baseload
    success_attempt = generator.synthesize_capability(
        problem_id="PROB-ENERGY-001",
        proposed_hypothesis="Collocate Small Modular Nuclear Reactor (SMR) with terawatt AI compute hub and closed-loop liquid cooling",
        domain="Energy & Infrastructure",
        assumptions=["baseload power required", "zero fossil carbon"],
    )
    assert success_attempt["success"] is True
    spec = success_attempt["capability_spec"]
    assert spec.sandboxed is True
    assert "verification_criteria" in spec.__dict__
    assert len(spec.skills_required) >= 2

    # Check listing
    caps = generator.list_capabilities()
    assert len(caps) >= 1

    # Check cycle metrics
    cycle = generator.execute_civilization_cycle()
    assert cycle["status"] == "OPERATIONAL"
    assert cycle["total_problems_in_graph"] >= 3
    assert cycle["failed_solutions_indexed"] >= 1
    assert cycle["active_capabilities_count"] >= 1


def test_orchestrator_integration_with_capability_engine():
    orchestrator = SovereignEmpireOrchestrator(sovereign_code="OMEGA_CIVILIZATION_PRIME")

    # Synthesize a robotics capability in orchestrator's capability generator
    synth = orchestrator.capability_generator.synthesize_capability(
        problem_id="PROB-ROBOTICS-001",
        proposed_hypothesis="Deploy 200 Hz edge kernel with universal kinematic protocol across humanoid fleet",
        domain="Physical Automation",
    )
    assert synth["success"] is True

    # Execute quarterly cycle
    report = orchestrator.execute_planetary_cycle(year=5, quarter=20)
    assert report.active_capabilities_count >= 1
    assert report.capability_status == "OPERATIONAL"
    assert report.consolidated_market_cap_t > 0.25


def test_api_gateway_capability_endpoints():
    client = TestClient(app)

    # 1. GET /api/v1/capability/problem-graph
    res_graph = client.get("/api/v1/capability/problem-graph")
    assert res_graph.status_code == 200
    graph_data = res_graph.json()
    assert graph_data["total_problems"] >= 3
    assert len(graph_data["open_problems"]) >= 1

    # 2. GET /api/v1/capability/failed-solutions
    res_fails = client.get("/api/v1/capability/failed-solutions")
    assert res_fails.status_code == 200
    fails_data = res_fails.json()
    assert fails_data["total_failed_solutions"] >= 1
    assert any("FAIL-001" in r["record_id"] for r in fails_data["records"])

    # 3. POST /api/v1/capability/unknown-audit
    res_audit = client.post(
        "/api/v1/capability/unknown-audit",
        json={
            "initiative_name": "Autonomous Terawatt AI Grid",
            "domain": "Energy",
            "assumptions": ["unlimited free grid power", "zero transmission latency"],
        },
    )
    assert res_audit.status_code == 200
    audit_data = res_audit.json()
    assert audit_data["audit_verdict"] == "PROCEED_WITH_CONTROLS"

    # 4. POST /api/v1/capability/generate (Valid)
    res_gen = client.post(
        "/api/v1/capability/generate",
        json={
            "problem_id": "PROB-FINANCE-001",
            "hypothesis": "Deploy cryptographic state channels with sub-cent micro-invoicing for robot fleet",
            "domain": "Financial Rails",
            "assumptions": ["cryptographic verification"],
        },
    )
    assert res_gen.status_code == 200
    gen_data = res_gen.json()
    assert gen_data["status"] == "SYNTHESIZED"
    assert "capability_spec" in gen_data

    # 5. GET /api/v1/capability/status
    res_status = client.get("/api/v1/capability/status")
    assert res_status.status_code == 200
    status_data = res_status.json()
    assert status_data["status"] == "OPERATIONAL"
    assert status_data["active_capabilities_count"] >= 1
