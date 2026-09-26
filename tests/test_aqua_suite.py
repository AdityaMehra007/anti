import pytest
import os
import sys

# Ensure root and GLOBAL-COMPANY-OS/06_ENGINEERING are in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "GLOBAL-COMPANY-OS", "06_ENGINEERING")))

from core.aqua_orchestrator import AquaOrchestrator, AquaTask, TaskStatus
from core.aqua_core import AquaCore

def test_aqua_task_priority_formula():
    # Value = 10, Probability = 0.95, Urgency = 8, Effort = 2
    # Priority = (10 * 0.95 * 8) / 2 = 76 / 2 = 38.0
    task = AquaTask(
        task_id="TSK-001",
        objective="Ship TradeNexus Pre-Shipment Audit",
        assigned_agent="AGT-CTO",
        value=10.0,
        probability=0.95,
        urgency=8.0,
        effort=2.0
    )
    assert task.priority_score == 38.0
    assert task.status == TaskStatus.PENDING

def test_aqua_orchestrator_dependency_resolution():
    orch = AquaOrchestrator()

    task_a = AquaTask(
        task_id="TSK-A",
        objective="Build Exporter Database",
        assigned_agent="AGT-CIO",
        value=8.0,
        probability=0.9,
        urgency=7.0,
        effort=2.0
    )

    task_b = AquaTask(
        task_id="TSK-B",
        objective="Run Automated Audits on Exporter Cohort",
        assigned_agent="AGT-COMPLIANCE-EXIM",
        value=10.0,
        probability=0.9,
        urgency=9.0,
        effort=1.5,
        dependencies=["TSK-A"]
    )

    orch.register_task(task_a)
    orch.register_task(task_b)

    # Task A is ready; Task B is blocked by Task A
    assert task_a.status == TaskStatus.READY
    assert task_b.status == TaskStatus.BLOCKED

    # Next runnable task should be Task A
    next_task = orch.get_next_runnable_task()
    assert next_task is not None
    assert next_task.task_id == "TSK-A"

    # Failing verification keeps Task A failed and Task B blocked
    passed = orch.verify_and_complete_task("TSK-A", verification_fn=lambda: False)
    assert passed is False
    assert task_a.status == TaskStatus.FAILED
    assert task_b.status == TaskStatus.BLOCKED

    # Passing verification marks Task A verified and unblocks Task B
    passed_retry = orch.verify_and_complete_task("TSK-A", verification_fn=lambda: True)
    assert passed_retry is True
    assert task_a.status == TaskStatus.VERIFIED
    assert task_b.status == TaskStatus.READY

    # Now Task B is the next runnable task
    next_task_after = orch.get_next_runnable_task()
    assert next_task_after is not None
    assert next_task_after.task_id == "TSK-B"

def test_aqua_core_initialization_and_registry():
    core = AquaCore(workspace_root="e:/anti")
    assert core.VERSION == "1.0.0-OMEGA-INFINITY"

    # Check 22 subsystems registered
    sub1 = core.get_subsystem("AQUA-SUB-01")
    assert sub1 is not None
    assert sub1["name"] == "AQUA CORE"

    sub22 = core.get_subsystem("AQUA-SUB-22")
    assert sub22 is not None
    assert sub22["name"] == "AQUA EXECUTIVE COMMAND"

    # Check Executive Agent
    ceo = core.get_agent("AGT-CEO")
    assert ceo is not None
    assert ceo["tier"] == 4

def test_aqua_core_trillion_dollar_ladder():
    core = AquaCore(workspace_root="e:/anti")

    # Day 0 Beachhead: $0 ARR -> Stage 1 target
    ladder_0 = core.evaluate_trillion_dollar_ladder(0.0)
    assert ladder_0["active_stage"]["tier"] == "Stage 1"
    assert ladder_0["active_stage"]["label"] == "$1M ARR"
    assert ladder_0["next_target_stage"]["label"] == "$10M ARR"

    # Scale to $50M ARR -> Stage 2 passed, currently Stage 2 active, targeting Stage 3 ($100M ARR)
    ladder_scale = core.evaluate_trillion_dollar_ladder(50_000_000.0)
    assert ladder_scale["active_stage"]["tier"] == "Stage 2"
    assert ladder_scale["next_target_stage"]["label"] == "$100M ARR"

def test_aqua_core_system_health():
    core = AquaCore(workspace_root="e:/anti")
    health = core.run_system_health_audit()

    assert health["overall_status"] == "HEALTHY"
    assert health["checks"]["all_22_subsystems_present"] is True
    assert health["checks"]["global_company_os_present"] is True
    assert health["checks"]["tradenexus_mvp_present"] is True

def test_aqua_executive_briefing():
    core = AquaCore(workspace_root="e:/anti")
    briefing = core.generate_executive_briefing()

    assert briefing["engine"] == "ANTIGRAVITY Ω∞ / AQUA CORE"
    assert briefing["status"] == "HEALTHY"
    assert briefing["subsystems_online"] == 22
    assert "active_growth_vector" in briefing

def test_aqua_founder_dashboard():
    from aqua.dashboard import FounderDashboard
    dashboard = FounderDashboard(workspace_root="e:/anti")
    data = dashboard.generate_dashboard_data()
    assert data["mission"] is not None
    assert data["system_health"] == "HEALTHY"
    assert data["subsystems_online"] == 22
    cli_str = dashboard.render_cli()
    assert "ANTIGRAVITY OMEGA" in cli_str
    assert "TOP 3 PRIORITIES" in cli_str

def test_aqua_decision_journal(tmp_path):
    from aqua.decision_journal import DecisionJournal
    journal_file = str(tmp_path / "test_decision_journal.jsonl")
    journal = DecisionJournal(storage_path=journal_file)

    rec = journal.record_decision(
        decision_id="DEC-001",
        decision="Select TradeNexus as beachhead",
        context="Evaluation of 500 opportunities",
        options=["TradeNexus", "CBAM Verifier", "LC Auditor"],
        assumptions=["Mid-market exporters face urgent demurrage pain"],
        expected_outcome="Close Customer #1 within 30 days",
        probability=0.85,
        risk="Customer inertia"
    )
    assert rec["decision_id"] == "DEC-001"

    decisions = journal.list_decisions()
    assert len(decisions) == 1
    assert decisions[0]["decision_id"] == "DEC-001"

    updated = journal.update_outcome(
        decision_id="DEC-001",
        actual_outcome="Pilot onboarded successfully",
        accuracy_score=0.95,
        lesson="Quantifying demurrage exposure in initial outreach accelerated deal close"
    )
    assert updated is True

    stats = journal.calculate_calibration_stats()
    assert stats["reviewed_decisions"] == 1
    assert stats["mean_accuracy"] == 0.95

def test_cbam_xml_generation():
    from src.cbam_xml_generator import CBAMDeclarationGenerator, InstallationData, CBAMEmissionsItem
    inst = InstallationData(
        installation_name="Test Bangalore Forging Mill",
        country_code="IN",
        un_locode="INBLR",
        latitude=12.97,
        longitude=77.59
    )
    items = [
        CBAMEmissionsItem(
            item_id="ITM-01",
            cn_code="72081000",
            goods_description="Hot rolled coil",
            net_mass_tonnes=10.0,
            production_route="Electric Arc Furnace",
            direct_embedded_emissions=1.8,
            indirect_embedded_emissions=0.4,
            carbon_price_due_eur=500.0
        )
    ]
    xml_str = CBAMDeclarationGenerator.generate_declaration_xml(
        declaration_id="DECL-001",
        quarter="2026-Q3",
        declarant_eori="DE123456789",
        installation=inst,
        items=items
    )
    assert "CBAMDeclaration" in xml_str
    assert "DECL-001" in xml_str
    assert "CBAM-SEAL-" in xml_str

def test_dossier_html_generation(tmp_path):
    from src.dossier_generator import DossierGenerator
    audit_data = {
        "exporter_name": "Test Engineering Ltd",
        "iec_code": "0711122233",
        "destination": "DEHAM, Germany",
        "overall_status": "REQUIRES_REVIEW",
        "risk_score": 25.0,
        "demurrage_exposure_usd": 3600.0,
        "certificate_seal": "TN-SEAL-TEST1234",
        "recommendations": ["Reconcile tariff classification"]
    }
    items = [
        {
            "item_id": "ITEM-1",
            "description": "Transmission Shaft",
            "declared_hs_code": "84831099",
            "verified_hs_code": "84831099",
            "cbam_applicable": True,
            "scomet_restricted": False,
            "status": "WARNING"
        }
    ]
    html = DossierGenerator.generate_html_dossier(audit_data, items)
    assert "Test Engineering Ltd" in html
    assert "$3,600" in html
    assert "TN-SEAL-TEST1234" in html

    out_file = str(tmp_path / "test_dossier.html")
    saved = DossierGenerator.save_dossier(out_file, html)
    assert os.path.isfile(saved)

def test_aqua_execution_engine():
    from aqua.execution_engine import AquaExecutionEngine
    engine = AquaExecutionEngine(workspace_root="e:/anti")
    res = engine.execute_all()
    assert len(res["executed_tasks"]) == 4
    assert all(t["status"] == "VERIFIED" for t in res["executed_tasks"])
    assert len(res["dossiers_created"]) == 2
    assert os.path.isfile(res["cbam_xml_created"])

def test_pipeline_crm(tmp_path):
    from aqua.crm_tracker import PipelineCRM
    db_file = str(tmp_path / "test_crm.db")
    crm = PipelineCRM(db_path=db_file)

    crm.upsert_account({
        "account_id": "TGT-TEST-01",
        "company_name": "Test Forgings Ltd",
        "hub_location": "Peenya, Bengaluru",
        "contact_title": "VP Exports",
        "key_products": "Precision Forgings",
        "destination": "Germany",
        "declared_hs": "87082900",
        "demurrage_exposure_usd": 5000.0,
        "target_monthly_inr": 35000.0,
        "stage": "OUTREACH_READY",
        "audit_seal": "TN-SEAL-TEST-01",
        "dossier_html_path": "/tmp/test.html",
        "notes": "Test account"
    })

    acc = crm.get_account("TGT-TEST-01")
    assert acc is not None
    assert acc["company_name"] == "Test Forgings Ltd"
    assert acc["stage"] == "OUTREACH_READY"

    # Move stage
    updated = crm.update_stage("TGT-TEST-01", "DEMO_COMPLETED", "Showed interactive ICEGATE and CBAM demo")
    assert updated is True
    acc_updated = crm.get_account("TGT-TEST-01")
    assert acc_updated["stage"] == "DEMO_COMPLETED"
    assert acc_updated["probability"] == 0.70

    metrics = crm.calculate_pipeline_metrics()
    assert metrics["total_accounts"] == 1
    assert metrics["total_demurrage_identified_usd"] == 5000.0
    assert metrics["stage_counts"]["DEMO_COMPLETED"] == 1

def test_aqua_daemon(tmp_path):
    from aqua.daemon import AquaDaemon
    state_file = str(tmp_path / "daemon_test_state.json")
    daemon = AquaDaemon(workspace_root="e:/anti", state_file=state_file)
    state = daemon.run_cycle()

    assert state["status"] == "OPERATIONAL"
    assert state["health_status"] == "HEALTHY"
    assert state["subsystems_online"] == 22
    assert state["pipeline"]["accounts_count"] >= 20
    assert os.path.isfile(state_file)

def test_unit_economics_engine():
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "GLOBAL-COMPANY-OS", "11_FINANCE")))
    from unit_economics_engine import UnitEconomicsEngine
    
    ue = UnitEconomicsEngine.calculate_unit_economics(monthly_arpu_inr=35000.0, cac_inr=45000.0)
    assert ue["gross_margin_percent"] == 89.0
    assert ue["ltv_to_cac_ratio"] > 10.0
    assert ue["payback_period_months"] < 2.0
    assert ue["acv_inr"] == 420000.0

    ladder = UnitEconomicsEngine.project_arr_ladder()
    assert len(ladder) == 4
    assert ladder[0]["paid_exporters"] == 25
    assert ladder[1]["paid_exporters"] == 250

def test_follow_up_engine():
    from aqua.follow_up_engine import FollowUpEngine
    from aqua.crm_tracker import PipelineCRM
    
    crm = PipelineCRM()
    engine = FollowUpEngine(crm=crm)
    
    # Step 2
    step2 = engine.generate_followup_message("TGT-01", step=2)
    assert "CBAM" in step2["subject"] or "ICEGATE" in step2["subject"]
    assert "Sansera" in step2["company_name"]
    assert "45 seconds" in step2["body"]

    # Step 3
    step3 = engine.generate_followup_message("TGT-01", step=3)
    assert "demurrage" in step3["subject"].lower()
    assert "Indemnity" in step3["body"]

    # Step 4
    step4 = engine.generate_followup_message("TGT-01", step=4)
    assert "Closing the audit file" in step4["subject"]

def test_continuous_learning_engine(tmp_path):
    from aqua.learning_engine import ContinuousLearningEngine
    from src.hs_engine import HSCatalog

    store_file = str(tmp_path / "test_knowledge.json")
    learner = ContinuousLearningEngine(store_path=store_file)

    res = learner.ingest_gazette_notification(
        source="CBIC Notification No. 88/2026-Customs",
        hs_code="81089090",
        keywords=["titanium fasteners", "aerospace grade titanium bolts"],
        tariff=5.0,
        cbam=True,
        scomet=True,
        legal_basis="DGFT Public Notice Reclassification for Aerospace Alloys"
    )

    assert res["status"] == "LEARNED"
    assert res["hs_code"] == "81089090"

    # Verify classification immediately detects the learned rule
    classification = HSCatalog.classify("aerospace grade titanium bolts")
    assert classification["hs_code"] == "81089090"
    assert classification["cbam_applicable"] is True
    assert classification["scomet_restricted"] is True

    stats = learner.get_learning_stats()
    assert stats["total_rules_learned"] >= 1
    assert os.path.isfile(store_file)

def test_war_room_commander():
    from aqua.war_room import WarRoomCommander

    commander = WarRoomCommander(workspace_root="e:/anti")
    summary = commander.get_war_room_summary()

    assert summary["system_health"] == "HEALTHY"
    assert summary["pipeline"]["total_accounts"] == 30
    assert summary["pipeline"]["total_demurrage_exposure_usd"] == 194700.0

    # Follow up sequence test
    seq = commander.generate_follow_up_copy("Sansera Engineering Limited")
    assert seq["company_name"] == "Sansera Engineering Limited"
    assert len(seq["touches"]) == 3

    # Ingestion test
    docket_res = commander.test_sample_docket_ingestion()
    assert docket_res["status"] == "AUDITED"
    assert "TN-DOCKET-" in docket_res["master_seal"]






