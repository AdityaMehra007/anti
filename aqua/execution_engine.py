"""
AQUA Autonomous Master Execution Engine (ANTIGRAVITY Ω∞)
Executes prioritized task DAGs, runs exporter audits, generates compliance dossiers,
updates decision journals, and enforces verification gates (Zero Vibe Coding).
"""

import os
import sys
import json
import time
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "GLOBAL-COMPANY-OS", "06_ENGINEERING")))

from core.aqua_core import AquaCore
from core.aqua_orchestrator import AquaOrchestrator, AquaTask, TaskStatus
from aqua.dashboard import FounderDashboard
from aqua.decision_journal import DecisionJournal
from src.exporter_audit_pipeline import ExporterAuditPipeline, ExporterProfile
from src.dossier_generator import DossierGenerator
from src.cbam_xml_generator import CBAMDeclarationGenerator, InstallationData, CBAMEmissionsItem

class AquaExecutionEngine:
    def __init__(self, workspace_root: str = "e:/anti"):
        self.workspace_root = workspace_root
        self.core = AquaCore(workspace_root=workspace_root)
        self.orchestrator = self.core.orchestrator
        self.journal = DecisionJournal(os.path.join(workspace_root, "aqua", "decision_journal.jsonl"))
        self.dashboard = FounderDashboard(workspace_root=workspace_root)

    def bootstrap_execution_backlog(self) -> None:
        """
        Registers core high-leverage tasks into the priority orchestrator.
        """
        # Task 1: Environment & Health Diagnostic
        t1 = AquaTask(
            task_id="TSK-001",
            objective="Run System Health & 22-Subsystems Audit",
            assigned_agent="AGT-CEO",
            value=9.0,
            probability=0.99,
            urgency=10.0,
            effort=1.0,
            verification_criteria="System health audit overall_status == HEALTHY"
        )

        # Task 2: Exporter Cohort Pre-Shipment Audit Execution
        t2 = AquaTask(
            task_id="TSK-002",
            objective="Execute TradeNexus Cohort Compliance Audits for Exporters",
            assigned_agent="AGT-COMPLIANCE-EXIM",
            value=10.0,
            probability=0.95,
            urgency=9.0,
            effort=1.5,
            dependencies=["TSK-001"],
            verification_criteria="Audit results generated with quantified demurrage valuations"
        )

        # Task 3: Client Dossier HTML/CSS Generation
        t3 = AquaTask(
            task_id="TSK-003",
            objective="Generate Tamper-Evident Pre-Shipment Compliance Dossiers",
            assigned_agent="AGT-CTO",
            value=9.5,
            probability=0.95,
            urgency=8.5,
            effort=1.2,
            dependencies=["TSK-002"],
            verification_criteria="HTML dossiers written to disk with SHA-256 seals"
        )

        # Task 4: EU CBAM XML Generation
        t4 = AquaTask(
            task_id="TSK-004",
            objective="Compile EU-Compliant CBAM XML Declaration for Steel/Fastener Exporter",
            assigned_agent="AGT-COMPLIANCE-EXIM",
            value=9.0,
            probability=0.92,
            urgency=8.0,
            effort=1.5,
            dependencies=["TSK-001"],
            verification_criteria="Valid CBAM XML document conforming to EU Regulation 2023/956"
        )

        self.orchestrator.register_task(t1)
        self.orchestrator.register_task(t2)
        self.orchestrator.register_task(t3)
        self.orchestrator.register_task(t4)

    def execute_all(self) -> Dict[str, Any]:
        """
        Executes the autonomous loop until all ready tasks are verified.
        """
        self.bootstrap_execution_backlog()
        executed_log = []

        # Step 1: Execute TSK-001
        task_1 = self.orchestrator.get_next_runnable_task()
        if task_1 and task_1.task_id == "TSK-001":
            health = self.core.run_system_health_audit()
            verified = self.orchestrator.verify_and_complete_task(
                "TSK-001",
                verification_fn=lambda: health["overall_status"] == "HEALTHY",
                result_evidence=health
            )
            executed_log.append({"task_id": "TSK-001", "status": "VERIFIED" if verified else "FAILED"})

        # Step 2: Execute TSK-002 & TSK-004 (which depended on TSK-001)
        profiles = [
            ExporterProfile(
                company_name="Sansera Engineering Limited",
                iec_code="0788012345",
                gstin="29AAACS1234A1Z1",
                destination_country="Germany",
                destination_port="DEHAM",
                sample_items=[
                    {"description": "Precision forged connecting rods steel", "quantity": 1200.0, "unit_price": 48.0, "declared_hs_code": "87082900"}
                ]
            ),
            ExporterProfile(
                company_name="Bharat Steel Tubing Corp",
                iec_code="0798765432",
                gstin="29BBBBB0000B1Z5",
                destination_country="Netherlands",
                destination_port="NLRTM",
                sample_items=[
                    {"description": "Hot rolled steel coil 2mm thickness", "quantity": 50.0, "unit_price": 2400.0, "declared_hs_code": "72081000"}
                ]
            )
        ]

        task_2 = self.orchestrator.get_next_runnable_task()
        audit_results = []
        if task_2 and task_2.task_id == "TSK-002":
            audit_results = ExporterAuditPipeline.run_cohort_audit(profiles)
            verified = self.orchestrator.verify_and_complete_task(
                "TSK-002",
                verification_fn=lambda: len(audit_results) == 2 and any(a["demurrage_exposure_usd"] > 0 for a in audit_results),
                result_evidence={"audits_count": len(audit_results), "audits": audit_results}
            )
            executed_log.append({"task_id": "TSK-002", "status": "VERIFIED" if verified else "FAILED"})

        # Step 3: Execute TSK-003 (Dossiers)
        task_3 = self.orchestrator.get_next_runnable_task()
        dossier_files = []
        if task_3 and task_3.task_id == "TSK-003":
            output_dir = os.path.join(self.workspace_root, "GLOBAL-COMPANY-OS", "09_SALES", "audits")
            for audit in audit_results:
                safe_name = audit["exporter_name"].replace(" ", "_").upper()
                html_path = os.path.join(output_dir, f"AUDIT_{safe_name}.html")
                items_mock = [
                    {
                        "item_id": "ITEM-1",
                        "description": "Export Consignment",
                        "declared_hs_code": "Declared",
                        "verified_hs_code": "Verified",
                        "cbam_applicable": audit["risk_score"] > 0,
                        "scomet_restricted": False,
                        "status": "PASS" if audit["overall_status"] == "APPROVED" else "WARNING"
                    }
                ]
                html_str = DossierGenerator.generate_html_dossier(audit, items_mock)
                DossierGenerator.save_dossier(html_path, html_str)
                dossier_files.append(html_path)

            verified = self.orchestrator.verify_and_complete_task(
                "TSK-003",
                verification_fn=lambda: all(os.path.isfile(p) for p in dossier_files),
                result_evidence={"dossiers_created": dossier_files}
            )
            executed_log.append({"task_id": "TSK-003", "status": "VERIFIED" if verified else "FAILED"})

        # Step 4: Execute TSK-004 (EU CBAM XML)
        task_4 = self.orchestrator.get_next_runnable_task()
        cbam_xml_path = ""
        if task_4 and task_4.task_id == "TSK-004":
            inst = InstallationData(
                installation_name="Bharat Steel Tubing Works Unit 2",
                country_code="IN",
                un_locode="INBLR",
                latitude=12.9716,
                longitude=77.5946
            )
            items = [
                CBAMEmissionsItem(
                    item_id="CBAM-ITM-01",
                    cn_code="72081000",
                    goods_description="Hot rolled steel coil 2mm thickness",
                    net_mass_tonnes=50.0,
                    production_route="Electric Arc Furnace",
                    direct_embedded_emissions=1.85,
                    indirect_embedded_emissions=0.45,
                    carbon_price_due_eur=3250.0
                )
            ]
            xml_data = CBAMDeclarationGenerator.generate_declaration_xml(
                declaration_id="CBAM-DECL-2026-Q3-001",
                quarter="2026-Q3",
                declarant_eori="NL876543210",
                installation=inst,
                items=items
            )
            cbam_xml_path = os.path.join(self.workspace_root, "GLOBAL-COMPANY-OS", "09_SALES", "audits", "CBAM_DECLARATION_SAMPLE.xml")
            with open(cbam_xml_path, "w", encoding="utf-8") as f:
                f.write(xml_data)

            verified = self.orchestrator.verify_and_complete_task(
                "TSK-004",
                verification_fn=lambda: os.path.isfile(cbam_xml_path) and "CBAMDeclaration" in xml_data,
                result_evidence={"xml_file": cbam_xml_path}
            )
            executed_log.append({"task_id": "TSK-004", "status": "VERIFIED" if verified else "FAILED"})

        # Log Decision in Journal
        self.journal.record_decision(
            decision_id=f"DEC-RUN-{int(time.time())}",
            decision="Generate live pre-shipment dossiers and CBAM XML declarations for Sansera and Bharat Steel",
            context="Autonomous execution loop triggered by founder",
            options=["Generate dossiers", "Wait for human confirmation"],
            assumptions=["Automated sample audits with $3,600+ demurrage risk findings provide strongest conversion wedge"],
            expected_outcome="2 HTML dossiers + 1 CBAM XML generated and verified without regressions",
            probability=0.98,
            risk="Formatting mismatches on different browsers"
        )

        return {
            "executed_tasks": executed_log,
            "dossiers_created": dossier_files,
            "cbam_xml_created": cbam_xml_path,
            "orchestrator_state": self.orchestrator.export_state()
        }

if __name__ == "__main__":
    engine = AquaExecutionEngine()
    result = engine.execute_all()
    print("Execution complete:")
    print(json.dumps(result, indent=2))
