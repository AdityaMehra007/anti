"""
AQUA Founder Operational War Room (ANTIGRAVITY Ω∞ Mode M / Mode F)
Unified Command & Control Interface for Venture Execution:
- Real-time North Star metrics & CRM telemetry
- 1-Touch Batch Pre-Shipment Risk Auditing
- Autonomous Pilot Term Sheet Generation & Indemnity Shield
- Multichannel Outreach & Follow-Up Sequence Dispatch
- Continuous Learning & Gazette Ingestion
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "GLOBAL-COMPANY-OS", "06_ENGINEERING")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "GLOBAL-COMPANY-OS", "12_LEGAL")))

from aqua.dashboard import FounderDashboard
from aqua.crm_tracker import PipelineCRM
from aqua.follow_up_engine import FollowUpEngine
from aqua.daemon import AquaDaemon
from aqua.learning_engine import ContinuousLearningEngine
from pilot_agreement_generator import PilotAgreementGenerator
from src.document_ingestion import DocumentIngestionPipeline


def safe_str(s: Any) -> str:
    if isinstance(s, str):
        return s.replace("\u20b9", "INR").replace("\u20ac", "EUR").encode("ascii", "replace").decode("ascii")
    return str(s)


class WarRoomCommander:
    def __init__(self, workspace_root: str = "e:/anti"):
        self.workspace_root = workspace_root
        self.dashboard = FounderDashboard(workspace_root=workspace_root)
        self.crm = PipelineCRM()
        self.follow_up = FollowUpEngine(self.crm)
        self.daemon = AquaDaemon(workspace_root=workspace_root)
        self.learning_engine = ContinuousLearningEngine()

    def get_war_room_summary(self) -> Dict[str, Any]:
        data = self.dashboard.generate_dashboard_data()
        crm_metrics = self.crm.calculate_pipeline_metrics()
        learning_stats = self.learning_engine.get_learning_stats()

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "north_star": data["north_star_metric"],
            "current_stage": data["current_stage"],
            "system_health": data["system_health"],
            "subsystems_online": data["subsystems_online"],
            "pipeline": {
                "total_accounts": crm_metrics["total_accounts"],
                "total_demurrage_exposure_usd": crm_metrics["total_demurrage_identified_usd"],
                "total_pipeline_mrr_inr": crm_metrics["potential_pipeline_mrr_inr"],
                "total_pipeline_arr_usd": crm_metrics["potential_pipeline_arr_usd"],
                "stage_counts": crm_metrics["stage_counts"]
            },
            "learning": {
                "rules_learned": learning_stats["total_rules_learned"],
                "total_hs_rules": learning_stats["total_catalog_rules"]
            },
            "top_priorities": data["top_priorities"],
            "leverage_actions": data["leverage_actions"]
        }

    def print_summary_terminal(self):
        summary = self.get_war_room_summary()
        p = summary["pipeline"]

        print("\n" + "=" * 78)
        print("  AQUA FOUNDER OPERATIONAL WAR ROOM - COMMAND TELEMETRY (ANTIGRAVITY OM-INF)")
        print("=" * 78)
        print(f"  Status: {safe_str(summary['system_health'])} | Subsystems Online: {summary['subsystems_online']} | Stage: {safe_str(summary['current_stage'])}")
        print(f"  North Star: {safe_str(summary['north_star'])}")
        print("-" * 78)
        print("  CRM PIPELINE & RISK EXPOSURE:")
        print(f"    - Target Enterprise Accounts: {p['total_accounts']}")
        print(f"    - Demurrage Exposure Found:   ${p['total_demurrage_exposure_usd']:,.2f} USD")
        print(f"    - Monthly Pipeline Revenue:   INR {p['total_pipeline_mrr_inr']:,.2f} / mo")
        print(f"    - Annual Pipeline Value (ARR): ${p['total_pipeline_arr_usd']:,.2f} USD")
        print(f"    - Pipeline Stages:            {p['stage_counts']}")
        print("-" * 78)
        print("  TOP STRATEGIC PRIORITIES:")
        for prio in summary["top_priorities"]:
            print(f"    * {safe_str(prio)}")
        print("-" * 78)
        print("  LEVERAGE ACTIONS (OMEGA ZERO-VIBE MANDATE):")
        for k, v in summary["leverage_actions"].items():
            print(f"    [{k.upper()}]: {safe_str(v)}")
        print("=" * 78 + "\n")

    def generate_pilot_agreement_for_company(
        self,
        company_name: str,
        signatory: str = "Authorized Signatory",
        title: str = "Director of International Trade",
        fee_inr: float = 35000.0,
        quota: int = 50
    ) -> Dict[str, Any]:
        """
        Creates bespoke pilot term sheet and indemnity contract.
        """
        contract = PilotAgreementGenerator.generate_pilot_agreement(
            company_name=company_name,
            authorized_signatory=signatory,
            signatory_title=title,
            registered_address="Industrial Area, Karnataka / Maharashtra, India",
            iec_code="0788001122",
            gstin="29AAACS0000A1Z1",
            monthly_fee_inr=fee_inr,
            consignments_quota=quota
        )

        out_dir = os.path.abspath(os.path.join(self.workspace_root, "GLOBAL-COMPANY-OS", "12_LEGAL", "contracts"))
        paths = PilotAgreementGenerator.save_agreements(out_dir, contract)
        return {
            "status": "GENERATED",
            "contract_id": contract["contract_id"],
            "company_name": company_name,
            "monthly_fee_inr": fee_inr,
            "paths": paths
        }

    def generate_follow_up_copy(self, company_name: str) -> Dict[str, Any]:
        """
        Generates 4-touch follow up sequence for an account.
        """
        return self.follow_up.generate_outreach_sequence(company_name)

    def test_sample_docket_ingestion(self) -> Dict[str, Any]:
        sample_docket = """
        COMMERCIAL EXPORT INVOICE
        Invoice No: EXP-WAR-ROOM-001
        Exporter: Sansera Engineering Limited
        IEC: 0788012345
        GSTIN: 29AAACS1234A1Z1
        Consignee: Continental Automotive GmbH
        Destination Country: Germany
        Port of Discharge: Hamburg Port (DEHAM)

        Item: Precision connecting rod forged steel
        Quantity: 500 NOS
        Price: 42.00

        ----------------------------------------
        PACKING LIST
        Packing List No: PK-WAR-ROOM-001
        Invoice Ref: EXP-WAR-ROOM-001
        Exporter: Sansera Engineering Limited
        Consignee: Continental Automotive GmbH
        Total Packages: 5
        Total Net Weight: 400.0 kg
        Total Gross Weight: 460.0 kg

        Package: PKG-01 Item: ITEM-1 Quantity: 500.0 Net: 400.0 Gross: 460.0
        """
        report = DocumentIngestionPipeline.process_composite_docket(sample_docket)
        return {
            "status": "AUDITED",
            "invoice_number": report.invoice_number,
            "composite_status": report.composite_status,
            "demurrage_exposure_usd": report.total_demurrage_exposure_usd,
            "master_seal": report.master_seal,
            "recommendations": report.recommendations
        }


def main():
    parser = argparse.ArgumentParser(description="AQUA Founder Operational War Room CLI")
    parser.add_argument("--summary", action="store_true", help="Print real-time command telemetry")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON format")
    parser.add_argument("--contract", type=str, help="Generate pilot agreement for specified company")
    parser.add_argument("--follow-up", type=str, help="Generate 4-touch follow-up sequence for company")
    parser.add_argument("--test-docket", action="store_true", help="Run composite docket ingestion test")
    parser.add_argument("--run-daemon", action="store_true", help="Execute background daemon heartbeat cycle")

    args = parser.parse_args()
    commander = WarRoomCommander()

    if args.contract:
        res = commander.generate_pilot_agreement_for_company(args.contract)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"\n[SUCCESS] Generated Pilot Agreement {res['contract_id']} for {res['company_name']}")
            print(f"  Monthly Pilot Fee: INR {res['monthly_fee_inr']:,}")
            print(f"  Markdown: {res['paths']['markdown_path']}")
            print(f"  HTML:     {res['paths']['html_path']}\n")
        return

    if args.follow_up:
        res = commander.generate_follow_up_copy(args.follow_up)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"\n[FOLLOW-UP SEQUENCE] {res['company_name']}")
            print(f"  Demurrage Exposure: ${res['demurrage_exposure_usd']:,.2f}")
            print(f"  Stage: {res['current_stage']}\n")
            for touch in res["touches"]:
                print(f"  [{touch['touch'].upper()}] (Day {touch['day_offset']}) - Subject: {touch['subject']}")
                print(f"  Body Preview: {touch['body'][:120]}...\n")
        return

    if args.test_docket:
        res = commander.test_sample_docket_ingestion()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"\n[DOCKET AUDIT TEST] Status: {res['composite_status']}")
            print(f"  Invoice: {res['invoice_number']} | Seal: {res['master_seal']}")
            print(f"  Demurrage Exposure: ${res['demurrage_exposure_usd']:,.2f}")
            print(f"  Recommendations Count: {len(res['recommendations'])}\n")
        return

    if args.run_daemon:
        state = commander.daemon.run_cycle()
        if args.json:
            print(json.dumps(state, indent=2))
        else:
            print(f"\n[DAEMON CYCLE COMPLETE] Health: {state['health_status']} | Accounts Checked: {state['pipeline']['accounts_count']} | Subsystems: {state['subsystems_online']}\n")
        return

    # Default to summary
    if args.json:
        print(json.dumps(commander.get_war_room_summary(), indent=2))
    else:
        commander.print_summary_terminal()


if __name__ == "__main__":
    main()
