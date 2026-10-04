"""
Tests for OMEGA INFINITY — Hyper-Orchestrator, Red Team Engine, and Sovereign Valuation Compounding.
Enforces Constitution Section 101 ("DO EVERYTHING" Protocol) and Section 14 (12 Adversarial Probes).
"""

import os
import sys
import json
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import get_kernel
from omega_infinity.omega_red_team_engine import get_red_team, RedTeamEngine
from omega_infinity.omega_valuation_compounding import get_valuation_engine, ValuationCompoundingEngine
from omega_infinity.omega_hyper_orchestrator import get_orchestrator, HyperOrchestrator


class TestHyperOrchestratorAndCapabilities:

    @pytest.fixture(autouse=True)
    def setup_engines(self):
        self.kernel = get_kernel()
        self.red_team = get_red_team()
        self.valuation = get_valuation_engine()
        self.orchestrator = get_orchestrator()

    def test_red_team_12_canonical_probes(self):
        res = self.red_team.run_all_12_probes()
        assert res["success"] is True
        assert res["total_probes"] == 12, "Must execute all 12 canonical Section 14 probes"
        assert res["average_survival_probability_pct"] >= 95.0, "Antifragile survival probability must exceed 95%"
        assert res["overall_resilience_verdict"] == "SOVEREIGN ANTIFRAGILITY CONFIRMED"

        # Verify probe IDs and properties
        probe_ids = [p["probe_id"] for p in res["probes"]]
        for i in range(1, 13):
            expected_id = f"PROBE-{i:02d}"
            assert expected_id in probe_ids, f"Missing {expected_id}"

        # Verify resilience ratings
        for p in res["probes"]:
            assert p["resilience_rating"] in ["ANTIFRAGILE", "ROBUST"]
            assert len(p["mitigation_mechanism"]) > 20

    def test_sovereign_valuation_compounding_horizons(self):
        res = self.valuation.compute_all_horizons()
        assert res["success"] is True
        assert res["founder"] == "Aditya Mehra (Adi)"
        assert len(res["horizons"]) == 5, "Must project 2027, 2030, 2035, 2040, 2050 horizons"

        years = [h["year"] for h in res["horizons"]]
        assert years == ["2027", "2030", "2035", "2040", "2050"]

        # Check 2027 Beachhead
        h2027 = res["horizons"][0]
        assert h2027["valuation_multiple_arr"] == 10.0
        assert h2027["implied_valuation_inr"] > 0
        assert h2027["founder_equity_pct"] == 100.0

        # Check 2040 Sovereign Unicorn
        h2040 = res["horizons"][3]
        assert h2040["implied_valuation_inr"] >= 100000000000.0  # ₹10,000 Cr (~$1.15B USD)
        assert h2040["implied_valuation_usd"] >= 1000000000.0

        # Check Rule of 40 across horizons
        for h in res["horizons"]:
            assert h["rule_of_40_score"] >= 40.0, f"Rule of 40 failed in {h['year']}: {h['rule_of_40_score']}"

    def test_do_everything_full_powers_execution(self):
        initial_blocks = len(self.kernel.ledger.blocks)
        manifest = self.orchestrator.do_everything()

        assert manifest["overall_status"] == "SOVEREIGN TRIUMPH — FULL POWERS EXECUTED"
        assert manifest["total_modes_executed"] == 13, "Must execute all 13 Constitutional Modes (A through M)"
        assert manifest["total_elapsed_seconds"] < 8.0, "Execution must be fast and minimal"

        # Verify all 13 modes present
        executed_codes = [m["mode_code"] for m in manifest["modes"]]
        expected_codes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
        assert executed_codes == expected_codes

        for m in manifest["modes"]:
            assert m["status"] == "COMPLETED"
            assert len(m["actions_taken"]) >= 2

        # Verify Manifest file on disk
        manifest_path = os.path.join(REPO_ROOT, "omega", "data", "do_everything_execution_manifest.json")
        assert os.path.exists(manifest_path)

        with open(manifest_path, "r", encoding="utf-8") as f:
            disk_manifest = json.load(f)
            assert disk_manifest["execution_id"] == manifest["execution_id"]

        # Verify ledger chained new event blocks
        assert len(self.kernel.ledger.blocks) > initial_blocks
        verification = self.kernel.ledger.verify_integrity()
        assert verification["valid"] is True, f"Ledger broken: {verification.get('reason')}"
