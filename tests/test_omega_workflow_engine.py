"""
Unit and Integration Tests for OMEGA INFINITY Autonomous Workflow Engine.
Enforces Section 27 and Section 28 of OMEGA_CONSTITUTION.md.
"""

import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_workflow_engine import (
    OmegaWorkflowEngine,
    get_workflow_engine,
    WorkflowDefinition,
    WorkflowExecutionRecord
)


class TestWorkflowEngine:

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.engine = get_workflow_engine()

    def test_01_workflow_catalog_integrity(self):
        """Verifies that all 10 canonical enterprise workflows are defined with complete 8-point specs."""
        workflows = self.engine.list_workflows()
        assert len(workflows) == 10

        required_ids = [f"WF-{i:02d}" for i in range(1, 11)]
        existing_ids = [w["workflow_id"] for w in workflows]
        for req in required_ids:
            assert req in existing_ids, f"Workflow {req} must exist in catalog."

        for w in workflows:
            assert w["name"]
            assert w["domain"]
            assert w["maturity"] in ["MANUAL", "AI-ASSISTED", "SEMI-AUTOMATED", "AUTOMATED", "AUTONOMOUS"]
            assert w["governing_directive"]
            assert w["description"]
            spec = w["spec"]
            assert spec["trigger"]
            assert spec["input_desc"]
            assert spec["process_desc"]
            assert spec["decision_rule"]
            assert spec["output_desc"]
            assert spec["verification_check"]
            assert spec["log_destination"]
            assert spec["escalation_path"]

    def test_02_individual_workflow_run_wf01_trade(self):
        """Tests WF-01 Autonomous Trade Clearance execution through all 8 canonical points."""
        rec: WorkflowExecutionRecord = self.engine.run_workflow("WF-01")
        assert rec.workflow_id == "WF-01"
        assert rec.status == "COMPLETED"
        assert rec.verification_passed is True
        assert len(rec.verification_seal) == 64
        assert len(rec.steps_executed) == 8

        point_names = [s.point_name for s in rec.steps_executed]
        assert point_names == [
            "TRIGGER", "INPUT", "PROCESS", "DECISION", "OUTPUT", "VERIFICATION", "LOG", "ESCALATION"
        ]
        for step in rec.steps_executed:
            assert step.status == "PASSED"
            assert step.latency_ms >= 0.0

    def test_03_individual_workflow_run_wf02_cbam(self):
        """Tests WF-02 EU CBAM carbon emissions notarization and XML generation."""
        rec = self.engine.run_workflow("WF-02")
        assert rec.workflow_id == "WF-02"
        assert rec.status == "COMPLETED"
        assert rec.verification_passed is True
        assert "declaration_xml" in rec.outputs
        assert "<CBAMDeclaration>" in rec.outputs["declaration_xml"]

    def test_04_individual_workflow_run_wf04_erp(self):
        """Tests WF-04 Double-Entry ERP Accrual and Balance Sheet verification."""
        rec = self.engine.run_workflow("WF-04")
        assert rec.workflow_id == "WF-04"
        assert rec.status == "COMPLETED"
        assert rec.verification_passed is True
        fin = rec.outputs.get("financial_statement", {})
        assets = fin.get("total_assets_inr", 0.0)
        liab_equity = fin.get("accounts_payable_inr", 0.0) + fin.get("total_equity_inr", 0.0)
        assert abs(assets - liab_equity) < 1.0

    def test_05_all_10_workflows_batch_execution(self):
        """Executes all 10 workflows in sequence and confirms 100% sovereign verification."""
        batch = self.engine.run_all_workflows()
        assert batch["workflows_executed"] == 10
        assert batch["all_passed"] is True
        assert batch["status"] == "ALL_WORKFLOWS_SOVEREIGN_VERIFIED"
        assert batch["total_elapsed_seconds"] < 5.0
        assert len(batch["results"]) == 10
        for r in batch["results"]:
            assert r["status"] == "COMPLETED"
            assert r["verification_passed"] is True
            assert len(r["seal"]) == 64

    def test_06_state_persistence_and_history(self):
        """Verifies workflow history is stored and loaded accurately."""
        history = self.engine.execution_history
        assert len(history) > 0
        last_rec = history[-1]
        assert "execution_id" in last_rec
        assert "workflow_id" in last_rec
        assert "seal" in last_rec

    def test_07_invalid_workflow_raises_error(self):
        """Verifies appropriate exception handling for non-existent workflows."""
        with pytest.raises(ValueError):
            self.engine.run_workflow("WF-99")
