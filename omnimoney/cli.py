"""
OMNIMONEY OS - Terminal Command Center CLI
Compliant with ANTIGRAVITY OMNIMONEY OS Master Specification (Sections 116 & 117).
"""

import sys
import argparse
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from omnimoney.omnimoney_engine import OmniMoneyEngine
from omnimoney.b2b_sales_engine import B2BSalesEngine
from omnimoney.agent_workforce import AgentWorkforceSwarm
from omnimoney.morning_brief import MorningBriefEngine
from omnimoney.business_generator import BusinessGenerator
from omnimoney.build_dashboard_data import build_data

def main():
    parser = argparse.ArgumentParser(description="OMNIMONEY OS Command Center")
    parser.add_argument("command", choices=["today", "brief", "pipeline", "swarm", "generate", "export"],
                        help="Action to execute")
    parser.add_argument("--vertical", type=str, default="Aesthetic Clinics",
                        help="Target vertical for business generation")

    args = parser.parse_args()

    engine = OmniMoneyEngine()
    sales = B2BSalesEngine()
    swarm = AgentWorkforceSwarm()
    brief_engine = MorningBriefEngine(engine, sales)
    biz_gen = BusinessGenerator()

    if args.command == "today":
        action = engine.get_highest_probability_action()
        print("\n=======================================================")
        print("⚡ OMNIMONEY OS: SECTION 153 PRIORITY ACTION TODAY")
        print("=======================================================")
        print(f"OPPORTUNITY : {action.opportunity}")
        print(f"TARGET      : {action.customer}")
        print(f"PROBLEM     : {action.problem}")
        print(f"OFFER       : {action.offer}")
        print(f"PRICE       : ₹{action.price_inr:,.2f}")
        print(f"CHANNEL     : {action.acquisition_channel}")
        print(f"NEXT ACTION : {action.exact_next_action}")
        print("=======================================================\n")

    elif args.command == "brief":
        brief = brief_engine.generate_brief()
        print(brief["markdown_brief"])

    elif args.command == "pipeline":
        summary = sales.get_pipeline_summary()
        print("\n=======================================================")
        print("📊 B2B SALES CRM & DEAL FLOW")
        print("=======================================================")
        print(f"Total Leads    : {summary['total_leads']}")
        print(f"Pipeline Value : ₹{summary['pipeline_value_inr']:,}")
        print(f"Won Revenue    : ₹{summary['won_revenue_inr']:,}")
        print("\nStages Breakdown:")
        for stage, count in summary["stages"].items():
            print(f"  - {stage:15s}: {count}")
        print("\nActive Prospects:")
        for p in sales.get_prospects():
            print(f"  [{p.status:14s}] {p.business_name} (₹{p.deal_value_inr:,}) - {p.contact_person}")
        print("=======================================================\n")

    elif args.command == "swarm":
        cycle = swarm.run_swarm_cycle()
        print("\n=======================================================")
        print("🤖 18-AGENT AUTONOMOUS WORKFORCE SWARM STATUS")
        print("=======================================================")
        print(f"Total Agents   : {cycle['total_agents']}")
        print(f"Active Agents  : {cycle['active_agents']}")
        print(f"Verdict        : {cycle['system_verdict']}")
        print("\nActive Directives:")
        for d in cycle["top_directives"]:
            print(f"  • {d}")
        print("=======================================================\n")

    elif args.command == "generate":
        bp = biz_gen.generate_blueprint(args.vertical)
        print("\n=======================================================")
        print(f"🚀 INSTANT BUSINESS BLUEPRINT: {bp.vertical_name.upper()}")
        print("=======================================================")
        print(f"ICP Target: {bp.icp_description}\n")
        print("Offer Stack:")
        for tier, desc in bp.offer_stack.items():
            print(f"  • {tier}: {desc}")
        print("\nMonthly P&L Projection:")
        for k, v in bp.monthly_pl_projection.items():
            print(f"  - {k.replace('_', ' ').title()}: {v}")
        print("=======================================================\n")

    elif args.command == "export":
        build_data()
        print("Successfully synchronized omnimoney_data.js with database and CRM state!")

if __name__ == "__main__":
    main()
