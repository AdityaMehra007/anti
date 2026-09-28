"""
OMEGA INFINITY (Ω-OS) — STARTUP & MNC MATRIX & POWERFUL AGENTS TEST SUITE
Enforces Section 101, Section 5, and Directive 110 of OMEGA_CONSTITUTION.md.

Tests:
  1. Startup & MNC Playbook Engine initialization and master catalog (14 playbooks).
  2. Individual playbook retrieval (Stripe, Flexport, Berkshire, ASML).
  3. Venture Blueprint synthesis combining startup velocity with MNC durability.
  4. Specialized execution missions across all 24 sovereign agents.
  5. Full fleet cycle aggregation and KPI verification.
"""

import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_startup_mnc_matrix import get_playbook_engine
from omega_infinity.omega_all_agents import get_fleet


class TestStartupMNCAndPowerfulAgents:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.playbook_engine = get_playbook_engine()
        self.fleet = get_fleet()

    def test_01_playbook_engine_catalog(self):
        """Verifies all 14 startup and MNC playbooks are present with complete specs."""
        playbooks = self.playbook_engine.get_all_playbooks()
        assert len(playbooks) >= 14

        expected_ids = [
            "stripe", "flexport", "palantir", "databricks", "shopify",
            "wise", "ramp", "veeva", "berkshire", "apple", "amazon",
            "maersk", "tata", "asml"
        ]
        available_ids = [p["id"] for p in playbooks]
        for eid in expected_ids:
            assert eid in available_ids, f"Expected playbook '{eid}' not found in matrix."

    def test_02_playbook_deep_inspection(self):
        """Verifies detailed attributes of specific startup and MNC models."""
        stripe = self.playbook_engine.get_playbook("stripe")
        assert stripe is not None
        assert stripe["entity_type"] == "STARTUP_UNICORN"
        assert "UCP 600" in stripe["autonomous_1person_adaptation"]
        assert len(stripe["tactical_rules"]) >= 3

        berkshire = self.playbook_engine.get_playbook("berkshire")
        assert berkshire is not None
        assert berkshire["entity_type"] == "GLOBAL_MNC"
        assert "Permanent capital" in berkshire["structural_moat"]
        assert "ceo" in berkshire["sovereign_agent_mapping"]

    def test_03_venture_blueprint_synthesis(self):
        """Verifies automated synthesis of custom venture blueprints for the founder."""
        bp = self.playbook_engine.synthesize_venture_blueprint(
            industry="Precision Metal Engineering",
            target_hub="Peenya Industrial Estate & Hosur Auto-Corridor",
            scale_goal="Top-1% Sovereign Cross-Border Trade OS"
        )
        assert bp["blueprint_id"].startswith("BLUEPRINT-")
        assert bp["target_industry"] == "Precision Metal Engineering"
        assert len(bp["architecture_blend"]) >= 5
        assert "starter_tier" in bp["recommended_pricing_tiers"]
        assert "phase_1_beachhead" in bp["execution_phases"]

    def test_04_all_24_agents_execute_specialized_missions(self):
        """Verifies each of the 24 sovereign agents executes its specialized mission cleanly."""
        agents = self.fleet.agents
        assert len(agents) == 24

        for agent_id in agents.keys():
            res = self.fleet.execute_specialized_mission(agent_id)
            assert res["success"] is True
            assert res["agent_id"] == agent_id
            assert len(res["capability"]) > 0
            assert isinstance(res["output"], dict)
            assert len(res["output"]) > 0

    def test_05_executive_agents_kpi_fidelity(self):
        """Verifies specific deep KPI outputs from Executive Council and Technical leads."""
        # CEO Aura
        ceo_res = self.fleet.execute_specialized_mission("ceo")
        assert ceo_res["output"]["founder_equity_pct"] == 100.0
        assert ceo_res["output"]["runway_months"] > 200.0

        # CTO Nexus
        cto_res = self.fleet.execute_specialized_mission("cto")
        assert cto_res["output"]["python_stdlib_purity"] == "100%"
        assert cto_res["output"]["external_runtime_dependencies"] == 0

        # Trade Vectis
        trade_res = self.fleet.execute_specialized_mission("trade")
        assert trade_res["output"]["checkpoints_verified"] == 39
        assert trade_res["output"]["zero_tolerance_accuracy"] == "100%"

        # CBAM Veritas
        cbam_res = self.fleet.execute_specialized_mission("cbam")
        assert cbam_res["output"]["eu_ets_benchmark_price_eur"] > 50.0

        # Risk Aegis
        risk_res = self.fleet.execute_specialized_mission("risk")
        assert risk_res["output"]["resilience_verdict"] == "SOVEREIGN ANTIFRAGILITY CONFIRMED"
        assert risk_res["output"]["average_survival_probability_pct"] >= 99.0

        # Evaluator
        eval_res = self.fleet.execute_specialized_mission("evaluator")
        assert eval_res["output"]["qa_verdict"] == "CERTIFIED_FOR_PRODUCTION"

    def test_06_full_fleet_cycle_aggregation(self):
        """Verifies full 24-agent fleet synchronization returns all 24 individual reports."""
        res = self.fleet.run_full_fleet_cycle()
        assert res["success"] is True
        assert res["agents_executed"] == 24
        assert len(res["agent_reports"]) == 24
        assert res["elapsed_seconds"] < 1.0  # Runs in under a second
