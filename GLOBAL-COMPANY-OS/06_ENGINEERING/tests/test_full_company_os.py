import os
import sys
import pytest

OS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, OS_ROOT)
sys.path.insert(0, os.path.join(OS_ROOT, "06_ENGINEERING"))

def test_financial_engine_milestones():
    import importlib.util
    fe_path = os.path.join(OS_ROOT, "11_FINANCE", "financial_engine.py")
    spec = importlib.util.spec_from_file_location("financial_engine", fe_path)
    fe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fe)
    
    milestones = fe.FinancialEngine.calculate_scale_ladder()
    assert len(milestones) == 9
    assert milestones[0]["tier"] == "₹1"
    assert milestones[-1]["tier"] == "₹1,000 Crore"
    for m in milestones:
        assert m["gross_margin"] >= 0.80, f"Margin dipped below 80% in {m['tier']}"

    scenarios = fe.FinancialEngine.project_scenarios()
    assert "Survival" in scenarios
    assert "Base" in scenarios
    assert "Breakout" in scenarios
    assert scenarios["Base"]["cash_flow_positive"] is True

def test_autonomous_daemon_subsystem_health():
    import importlib.util
    daemon_path = os.path.join(OS_ROOT, "25_AUTOMATIONS", "autonomous_company_daemon.py")
    spec = importlib.util.spec_from_file_location("autonomous_company_daemon", daemon_path)
    daemon_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(daemon_mod)

    daemon = daemon_mod.AutonomousDaemon()
    report = daemon.run_single_cycle()
    assert report["system_health"] == "OPTIMAL"
    assert report["subsystems_online"] == report["subsystems_checked"]
    assert report["active_alerts"] == 0
    assert len(report["monitors"]) == 4

def test_executive_health_cli_vitals():
    import importlib.util
    cli_path = os.path.join(OS_ROOT, "24_DASHBOARDS", "executive_health_cli.py")
    spec = importlib.util.spec_from_file_location("executive_health_cli", cli_path)
    cli_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli_mod)

    vitals = cli_mod.ExecutiveHealthCLI.get_system_vitals()
    assert vitals["status"] == "HEALTHY"
    assert vitals["operating_entity"] == "TradeNexus AI"
    assert vitals["gross_margin_pct"] >= 90.0
    assert vitals["total_opportunities_indexed"] >= 100
    assert vitals["total_problems_indexed"] >= 100
    assert vitals["total_automations_indexed"] >= 100

def test_all_operational_documents_present():
    required_docs = [
        ("10_MARKETING", "BRAND_GUIDELINES.md"),
        ("10_MARKETING", "CONTENT_ENGINE.md"),
        ("10_MARKETING", "DISTRIBUTION_CHANNELS.md"),
        ("14_SECURITY", "SECURITY_ARCHITECTURE.md"),
        ("14_SECURITY", "INCIDENT_RESPONSE_PLAN.md"),
        ("15_OPERATIONS", "STANDARD_OPERATING_PROCEDURES.md"),
        ("15_OPERATIONS", "FOUNDER_COGNITIVE_PROTECTION.md"),
        ("16_HIRING", "ORG_DESIGN_1_TO_50.md"),
        ("16_HIRING", "ROLE_SCORECARDS.md"),
        ("18_PARTNERSHIPS", "PARTNERSHIP_STRATEGY.md"),
        ("18_PARTNERSHIPS", "CHANNEL_AGREEMENT_TEMPLATE.md"),
        ("21_RISK", "MASTER_RISK_REGISTER.md"),
        ("21_RISK", "BLACK_SWAN_PREMORTEMS.md"),
        ("22_EXPERIMENTS", "EXPERIMENTATION_LEDGER.md"),
        ("24_DASHBOARDS", "EXECUTIVE_DASHBOARD_SPECS.md"),
    ]
    for folder, doc in required_docs:
        p = os.path.join(OS_ROOT, folder, doc)
        assert os.path.isfile(p), f"Missing operational document: {folder}/{doc}"
        assert os.path.getsize(p) > 200, f"Operational document too short: {folder}/{doc}"
