"""
Unit & Integration Tests for Windmill Autonomous Orchestrator Suite
===================================================================
Tests client initialization, worker telemetry, script execution, flow DAG execution,
human-in-the-loop approvals, typed resources, Hub catalog search, CLI commands,
and MCP server tool handlers.
"""

import os
import sys
import pytest
from windmill_orchestrator import (
    WindmillConfig,
    WindmillClient,
    WindmillOrchestrator,
    WindmillMockEngine
)
import windmill_cli
import windmill_mcp_server
from windmill.scripts import (
    cbam_carbon_audit,
    erp_invoice_recon,
    lead_intelligence_strike,
    customer_churn_risk_radar,
    sec_edgar_filing_recon,
    daily_cloud_snapshot_and_s3_vault
)


@pytest.fixture
def mock_client():
    config = WindmillConfig(mock_mode=True)
    return WindmillClient(config)


@pytest.fixture
def orchestrator(mock_client):
    return WindmillOrchestrator(mock_client)


def test_mock_engine_initial_state():
    engine = WindmillMockEngine()
    assert engine.version.startswith("1.")
    assert "nightly" in engine.rust_engine_version
    assert engine.active_workers_count == 16
    assert len(engine.workspaces) >= 3
    assert len(engine.scripts) >= 5
    assert len(engine.flows) >= 3
    assert len(engine.resources) >= 3
    assert len(engine.apps) >= 1
    assert len(engine.hub_catalog) >= 4


def test_client_telemetry(mock_client):
    telemetry = mock_client.get_telemetry()
    assert telemetry["status"] == "ok"
    assert telemetry["active_workers"] == 16
    assert telemetry["scripts_count"] >= 5
    assert telemetry["flows_count"] >= 3
    assert telemetry["mode"] == "SIMULATION"


def test_workspaces_listing(mock_client):
    workspaces = mock_client.list_workspaces()
    assert isinstance(workspaces, list)
    assert any(w["id"] == "omega" for w in workspaces)


def test_script_listing_and_execution(mock_client):
    scripts = mock_client.list_scripts()
    assert len(scripts) >= 5
    
    # Test CBAM script run
    cbam_res = mock_client.run_script("u/admin/cbam_carbon_audit", {"net_mass_kg": 24500.0})
    assert cbam_res["status"] == "COMPLETED"
    assert cbam_res["result"]["compliance_status"] == "PAYMENT_REQUIRED"
    assert cbam_res["result"]["net_mass_tonnes"] == 24.5
    assert cbam_res["duration_ms"] > 0
    assert "Rust Native Worker" in cbam_res["logs"]

    # Test ERP recon script run
    recon_res = mock_client.run_script("u/admin/erp_invoice_recon", {"tolerance_inr": 5.0})
    assert recon_res["status"] == "COMPLETED"
    assert recon_res["result"]["audit_verdict"] == "CLEAN"
    assert recon_res["result"]["reconciliation_rate_pct"] == 100.0


def test_flow_dag_execution_and_branch_suspension(mock_client):
    flows = mock_client.list_flows()
    assert len(flows) >= 3
    
    # High-value credit line (> 500k) should suspend for human approval
    flow_res = mock_client.execute_flow(
        "u/admin/enterprise_client_onboarding_dag",
        {"client_name": "Sansera Engineering Limited", "requested_credit_inr": 750000.0}
    )
    assert flow_res["status"] == "SUSPENDED"
    assert flow_res["result"]["suspended_step"] == "step_approval_gate"
    assert flow_res["result"]["slack_notification_dispatched"] is True
    
    # Low-value credit line (< 500k) should complete without suspension
    flow_auto = mock_client.execute_flow(
        "u/admin/enterprise_client_onboarding_dag",
        {"client_name": "Small Vendor", "requested_credit_inr": 300000.0}
    )
    assert flow_auto["status"] == "COMPLETED"
    assert flow_auto["result"]["suspended_step"] is None


def test_human_in_the_loop_approval_lifecycle(mock_client):
    # Execute flow that suspends
    flow_res = mock_client.execute_flow(
        "u/admin/enterprise_client_onboarding_dag",
        {"client_name": "Bharat Steel Tubing Corp", "requested_credit_inr": 900000.0}
    )
    job_id = flow_res["id"]
    assert flow_res["status"] == "SUSPENDED"

    # Executive approves the job
    approval_res = mock_client.approve_job(job_id, approved=True, notes="Approved by Aditya Mehra")
    assert approval_res["success"] is True
    assert approval_res["new_status"] == "COMPLETED"
    assert approval_res["job"]["result"]["approval_status"] == "APPROVED_BY_EXECUTIVE"
    assert "RESUMED" in approval_res["job"]["logs"]


def test_rejection_of_suspended_job(mock_client):
    flow_res = mock_client.execute_flow(
        "u/admin/enterprise_client_onboarding_dag",
        {"client_name": "High Risk Client", "requested_credit_inr": 800000.0}
    )
    job_id = flow_res["id"]
    rejection_res = mock_client.approve_job(job_id, approved=False, notes="KYC discrepancy")
    assert rejection_res["success"] is True
    assert rejection_res["new_status"] == "REJECTED"


def test_resource_management(mock_client):
    resources = mock_client.list_resources()
    assert len(resources) >= 3
    assert any(r["resource_type"] == "postgresql" for r in resources)

    # Provision custom resource
    new_res = mock_client.create_resource(
        path="u/admin/redis_cache",
        resource_type="redis",
        value={"host": "localhost", "port": 6379},
        description="Redis Cache Cluster"
    )
    assert new_res["path"] == "u/admin/redis_cache"
    assert mock_client.mock_engine.get_resource("u/admin/redis_cache") is not None


def test_hub_catalog_and_import(mock_client):
    items = mock_client.search_hub(query="slack")
    assert len(items) >= 1
    assert "slack" in items[0]["id"]

    import_res = mock_client.import_from_hub("hub/scripts/slack_post_message")
    assert import_res["success"] is True
    assert import_res["local_path"] == "u/admin/slack_post_message"
    assert mock_client.get_script("u/admin/slack_post_message") is not None


def test_orchestrator_high_level_pipelines(orchestrator):
    overview = orchestrator.get_platform_overview()
    assert overview["engine_status"] == "READY"
    assert overview["total_scripts"] >= 8
    assert overview["total_flows"] >= 5
    assert overview["total_schedules"] >= 4
    assert overview["total_variables"] >= 3

    # Run CBAM pipeline
    cbam_pipe = orchestrator.run_cbam_pipeline("DKT-2026-TEST", 18500.0)
    assert cbam_pipe["status"] == "COMPLETED"

    # Run Reconciliation pipeline
    recon_pipe = orchestrator.run_reconciliation("BATCH-TEST-001")
    assert recon_pipe["status"] == "COMPLETED"

    # Run Churn radar & SEC Edgar scripts
    churn_run = orchestrator.run_churn_radar("ACC-TEST-001", 2400000.0)
    assert churn_run["status"] == "COMPLETED"
    assert "mrr_at_risk_inr" in churn_run["result"]

    sec_run = orchestrator.run_sec_edgar_recon("NVDA", "10-Q")
    assert sec_run["status"] == "COMPLETED"
    assert sec_run["result"]["verdict"] == "HEALTHY_SOLVENT"

    # Run SaaS Recovery & Security Incident Response flows
    saas_pipe = orchestrator.run_saas_recovery_pipeline("CUST-901", "INV-11", 6000.0)
    assert saas_pipe["status"] == "COMPLETED"

    secops_pipe = orchestrator.run_security_incident_response("203.0.113.1", "DDoS", "HIGH")
    assert secops_pipe["status"] == "COMPLETED"

    # Run complete do_everything cycle
    manifest = orchestrator.do_everything()
    assert manifest["status"] == "SOVEREIGN WORKFLOW ENGINE FULL POWERS VERIFIED"
    assert manifest["total_phases_executed"] == 12
    assert len(manifest["phases"]) == 12
    assert os.path.exists(os.path.join(os.path.dirname(__file__), "..", "omega", "data", "windmill_do_everything_manifest.json"))


def test_schedules_and_cron_triggers(mock_client):
    schedules = mock_client.list_schedules()
    assert len(schedules) >= 4
    assert any("hourly" in s["path"] for s in schedules)

    # Trigger hourly schedule
    res = mock_client.trigger_schedule("u/admin/hourly_carbon_audit_schedule")
    assert res["success"] is True
    assert res["job"]["status"] == "COMPLETED"


def test_variables_crud_and_secrets(mock_client):
    vars_list = mock_client.list_variables()
    assert len(vars_list) >= 3

    # Set new variable
    set_res = mock_client.set_variable("u/admin/test_var", "secret_val_123", is_secret=True, description="Test key")
    assert set_res["path"] == "u/admin/test_var"
    assert set_res["is_secret"] is True

    # Get variable
    get_res = mock_client.get_variable("u/admin/test_var")
    assert get_res is not None
    assert get_res["value"] == "secret_val_123"

    # Delete variable
    assert mock_client.mock_engine.delete_variable("u/admin/test_var") is True
    assert mock_client.get_variable("u/admin/test_var") is None


def test_webhook_ingress(mock_client):
    # Test billing webhook
    res_bill = mock_client.trigger_webhook("stripe-billing", {"amount_usd": 8500.0, "invoice_id": "INV-WH-01"})
    assert res_bill["success"] is True
    assert res_bill["job"]["status"] == "COMPLETED"

    # Test security webhook
    res_sec = mock_client.trigger_webhook("security-alert", {"source_ip": "198.51.100.99", "severity": "CRITICAL"})
    assert res_sec["success"] is True
    assert res_sec["job"]["status"] == "COMPLETED"


def test_mcp_server_tools():
    info = windmill_mcp_server.handle_tool_call("windmill_get_system_info", {})
    assert info["status"] == "ok"

    scripts = windmill_mcp_server.handle_tool_call("windmill_list_scripts", {})
    assert len(scripts) >= 8

    flows = windmill_mcp_server.handle_tool_call("windmill_list_flows", {})
    assert len(flows) >= 5

    schedules = windmill_mcp_server.handle_tool_call("windmill_list_schedules", {})
    assert len(schedules) >= 4

    vars_list = windmill_mcp_server.handle_tool_call("windmill_list_variables", {})
    assert len(vars_list) >= 3

    run_res = windmill_mcp_server.handle_tool_call(
        "windmill_run_script",
        {"script_path": "u/admin/cbam_carbon_audit", "args": {"net_mass_kg": 20000.0}}
    )
    assert run_res["status"] == "COMPLETED"

    trig_res = windmill_mcp_server.handle_tool_call(
        "windmill_trigger_schedule",
        {"path": "u/admin/hourly_carbon_audit_schedule"}
    )
    assert trig_res["success"] is True

    do_res = windmill_mcp_server.handle_tool_call("windmill_do_everything", {})
    assert do_res["total_phases_executed"] == 12


def test_standalone_python_scripts_direct_execution():
    # Test cbam_carbon_audit.main() directly
    cbam_out = cbam_carbon_audit.main(docket_id="DKT-UNIT-01", net_mass_kg=10000.0)
    assert cbam_out["compliance_status"] == "PAYMENT_REQUIRED"
    assert cbam_out["net_mass_tonnes"] == 10.0
    assert cbam_out["net_payable_eur"] > 0

    # Test erp_invoice_recon.main() directly
    recon_out = erp_invoice_recon.main(batch_reference="BATCH-UNIT-01")
    assert recon_out["reconciliation_rate_pct"] == 100.0
    assert recon_out["total_invoices_audited"] == 4

    # Test lead_intelligence_strike.main() directly
    lead_out = lead_intelligence_strike.main(company_name="Google India")
    assert lead_out["enrichment_status"] == "ENRICHED_HIGH_CONFIDENCE"
    assert "Google India" in lead_out["custom_inmail_body"]

    # Test customer_churn_risk_radar.main() directly
    churn_out = customer_churn_risk_radar.main(company_name="Acme Corp", annual_contract_value_inr=1200000.0)
    assert churn_out["status"] == "EVALUATION_COMPLETE"
    assert "risk_evaluation" in churn_out
    assert churn_out["monthly_recurring_revenue_inr"] == 100000.0

    # Test sec_edgar_filing_recon.main() directly
    sec_out = sec_edgar_filing_recon.main(ticker="MSFT", revenue_usd=60000000000.0)
    assert sec_out["filing_status"] == "OFFICIALLY_VERIFIED"
    assert "audit_metrics" in sec_out
    assert sec_out["audit_metrics"]["covenants"]["all_covenants_satisfied"] is True

    # Test daily_cloud_snapshot_and_s3_vault.main() directly
    backup_out = daily_cloud_snapshot_and_s3_vault.main(database_name="windmill_test_db")
    assert backup_out["status"] == "VAULTED_IMMUTABLE"
    assert "sha256_checksum" in backup_out["backup_details"]
