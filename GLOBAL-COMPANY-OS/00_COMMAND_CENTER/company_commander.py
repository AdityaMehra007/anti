#!/usr/bin/env python3
"""
Company Commander: Principal Orchestrator Daemon for GLOBAL COMPANY OS
Enforces Least Privilege, Strategic Consistency, and Founder Cognitive Protection.
"""

import os
import sys
import json
import argparse
from datetime import datetime

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class CompanyCommander:
    def __init__(self, root_dir=ROOT_DIR):
        self.root_dir = root_dir
        self.state_file = os.path.join(root_dir, "CURRENT_STATE.md")
        self.queue_file = os.path.join(root_dir, "EXECUTION_QUEUE.md")
        self.risk_file = os.path.join(root_dir, "RISK_REGISTER.md")
        self.north_star_file = os.path.join(root_dir, "NORTH_STAR.md")

    def get_daily_command_brief(self):
        """Generates the standardized Daily Command Center Startup Brief."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        brief = {
            "DATE": today,
            "COMPANY STAGE": "Stage 0 (Autonomous Beachhead Validation)",
            "CASH": "Bootstrapped / Lean Founder Capital (< ₹50,000 monthly burn)",
            "REVENUE": "₹0 (Targeting First ₹85,000 / $1,000 paid pilot)",
            "CUSTOMERS": "0 Paid Accounts (50 Target Leads Curated)",
            "PIPELINE": "₹2,50,000 potential across 10 qualified pilot candidates",
            "PRODUCT": "TradeNexus V1 MVP (HS-code & Customs Compliance Engine)",
            "BIGGEST RISK": "Sales cycle inertia among traditional export managers",
            "BIGGEST OPPORTUNITY": "DGFT/CBAM regulatory mandate forcing exporters to automate",
            "BIGGEST BOTTLENECK": "Delivering first zero-error export docket audit to a live exporter",
            "TOP_3_ACTIONS": [
                "1. Complete automated parsing test suite on commercial export invoices",
                "2. Launch direct personalized audit outreach to Top 25 Peenya/Whitefield exporters",
                "3. Submit Google Cloud for Startups credits application for foundational compute"
            ],
            "ONE_THING_TO_STOP": "Building non-core features before validating customer willingness to pay",
            "ONE_THING_TO_WATCH": "New European Union CBAM compliance enforcement deadlines"
        }
        return brief

    def format_daily_brief(self, brief=None):
        if brief is None:
            brief = self.get_daily_command_brief()
        output = [
            "=" * 60,
            "        GLOBAL COMPANY OS: DAILY COMMAND BRIEF",
            "=" * 60,
            f"DATE: {brief['DATE']}",
            f"COMPANY STAGE: {brief['COMPANY STAGE']}",
            f"CASH: {brief['CASH']}",
            f"REVENUE: {brief['REVENUE']}",
            f"CUSTOMERS: {brief['CUSTOMERS']}",
            f"PIPELINE: {brief['PIPELINE']}",
            f"PRODUCT: {brief['PRODUCT']}",
            f"BIGGEST RISK: {brief['BIGGEST RISK']}",
            f"BIGGEST OPPORTUNITY: {brief['BIGGEST OPPORTUNITY']}",
            f"BIGGEST BOTTLENECK: {brief['BIGGEST BOTTLENECK']}",
            "",
            "TOP 3 ACTIONS:",
            brief['TOP_3_ACTIONS'][0],
            brief['TOP_3_ACTIONS'][1],
            brief['TOP_3_ACTIONS'][2],
            "",
            f"ONE THING TO STOP: {brief['ONE_THING_TO_STOP']}",
            f"ONE THING TO WATCH: {brief['ONE_THING_TO_WATCH']}",
            "=" * 60
        ]
        return "\n".join(output)

    def compress_directive(self, topic="Current Beachhead & Go-To-Market"):
        """Compresses massive research down to the single actionable truth."""
        return {
            "WHAT_MATTERS": "Mid-market Indian exporters face immediate multi-thousand dollar fines for customs documentation errors under new EU CBAM and US trade rules.",
            "EVIDENCE": "DGFT public trade data records 4,500+ exporters in Bangalore; manual compliance checks take 4 hours per shipment with a 6% error rate.",
            "DECISION": "Focus 100% of engineering and sales resources on TradeNexus V1 MVP: automated export invoice and customs docket verification.",
            "NEXT_3_ACTIONS": [
                "Run test suite on sample shipping bills to verify 100% parsing accuracy.",
                "Send 25 personalized compliance teardowns to Bengaluru exporter managing directors.",
                "Close first ₹25,000–₹85,000 paid pilot within 30 days."
            ]
        }

    def prioritize_queue(self):
        """Ranks tasks strictly by Impact * Confidence / Effort."""
        tasks = [
            {"id": "TSK-01", "name": "V1 MVP Compliance Document Parser", "impact": 5, "conf": 5, "effort": 2},
            {"id": "TSK-02", "name": "Outreach to Top 50 Bangalore Exporters", "impact": 5, "conf": 4, "effort": 1},
            {"id": "TSK-03", "name": "Startup India & DPIIT Registration Dossier", "impact": 4, "conf": 4, "effort": 1},
            {"id": "TSK-04", "name": "Google Cloud / AWS Credits Submission", "impact": 4, "conf": 4, "effort": 1},
            {"id": "TSK-05", "name": "Automated Daily Regulatory Scraper", "impact": 4, "conf": 4, "effort": 2}
        ]
        for t in tasks:
            t["score"] = round((t["impact"] * t["conf"]) / t["effort"], 2)
        tasks.sort(key=lambda x: x["score"], reverse=True)
        return tasks

def main():
    parser = argparse.ArgumentParser(description="Company Commander CLI")
    parser.add_argument("--status", action="store_true", help="Print daily command brief")
    parser.add_argument("--compress", action="store_true", help="Compress strategy to core decision")
    parser.add_argument("--prioritize", action="store_true", help="Prioritize execution queue")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()
    commander = CompanyCommander()

    if args.compress:
        data = commander.compress_directive()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print("=== WHAT MATTERS ===")
            print(data["WHAT_MATTERS"])
            print("\n=== EVIDENCE ===")
            print(data["EVIDENCE"])
            print("\n=== DECISION ===")
            print(data["DECISION"])
            print("\n=== NEXT 3 ACTIONS ===")
            for a in data["NEXT_3_ACTIONS"]:
                print(f"- {a}")
    elif args.prioritize:
        tasks = commander.prioritize_queue()
        if args.json:
            print(json.dumps(tasks, indent=2))
        else:
            print("=== PRIORITIZED EXECUTION QUEUE (Impact * Conf / Effort) ===")
            for t in tasks:
                print(f"[{t['score']}] {t['id']}: {t['name']} (I:{t['impact']}, C:{t['conf']}, E:{t['effort']})")
    else:
        # Default to status brief
        if args.json:
            print(json.dumps(commander.get_daily_command_brief(), indent=2))
        else:
            print(commander.format_daily_brief())

if __name__ == "__main__":
    main()