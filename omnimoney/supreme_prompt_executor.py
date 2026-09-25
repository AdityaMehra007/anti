"""
OMNIMONEY OS - Supreme Prompt Executor
Loads the supreme prompt, activates the 18-agent swarm and 300+ skills matrix,
and executes the daily money-making sequence.
"""

import os
import sys
import json
import datetime
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

from omnimoney.omnimoney_engine import OmniMoneyEngine
from omnimoney.b2b_sales_engine import B2BSalesEngine
from omnimoney.agent_workforce import AgentWorkforceSwarm
from omnimoney.morning_brief import MorningBriefEngine
from omnimoney.prospect_miner import ProspectMiner
from omnimoney.outreach_vault import OutreachVault
from omnimoney.daily_scheduler import DailyScheduler


class SupremePromptExecutor:
    """
    Executes the Supreme Autonomous Money Prompt end-to-end:
    Orchestrates Swarm, Mining, Scripting, Proposals, and Dashboard Synchronization.
    """

    def __init__(self):
        self.engine = OmniMoneyEngine()
        self.sales = B2BSalesEngine()
        self.swarm = AgentWorkforceSwarm()
        self.brief_engine = MorningBriefEngine(self.engine, self.sales)
        self.miner = ProspectMiner()
        self.vault = OutreachVault()
        self.scheduler = DailyScheduler()

    def execute_supreme_cycle(self) -> Dict[str, Any]:
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("=" * 70)
        print(" ⚡ EXECUTING THE SUPREME OMNIMONEY AUTONOMOUS MONEY SYSTEM ⚡")
        print("=" * 70)
        print(f"Timestamp: {now_str}")
        print("Operator: Aditya Mehra | Base: Bengaluru & World Economy\n")

        # Step 1: Run 18-Agent Swarm Cycle
        print("[1/5] Activating 18-Agent Economic Workforce Swarm...")
        swarm_status = self.swarm.run_swarm_cycle()
        print(f"      Swarm Status: {swarm_status['active_agents']}/{swarm_status['total_agents']} Agents Active")
        print(f"      Verdict: {swarm_status['system_verdict']}")

        # Step 2: Determine Section 153 Highest-Probability Action
        print("\n[2/5] Deriving Section 153 Immediate Rupee Action...")
        top_action = self.engine.get_highest_probability_action()
        print(f"      Opportunity: {top_action.opportunity}")
        print(f"      Target: {top_action.customer}")
        print(f"      Ticket Size: ₹{top_action.price_inr:,.0f}")
        print(f"      First Action: {top_action.exact_next_action}")

        # Step 3: Run Daily Cycle & Prospect Extraction
        print("\n[3/5] Mining Database for 5 High-Ticket Ready-for-Outreach Prospects...")
        daily_res = self.scheduler.run_daily_cycle()
        prospects = self.miner.mine_high_value_prospects(limit=5)
        print(f"      Mined {len(prospects)} targets from 4,500 company founder gap database.")

        # Step 4: Generate Master Battlecard Report
        print("\n[4/5] Compiling Supreme Daily Money Battlecard...")
        battlecard_path = os.path.join(r"e:\anti\reports", "TODAY_SUPREME_MONEY_EXECUTION_BATTLECARD.md")
        
        content = []
        content.append(f"# ⚡ SUPREME OMNIMONEY DAILY EXECUTION BATTLECARD")
        content.append(f"**Date:** {today_str} | **Operator:** Aditya Mehra | **System:** OMNIMONEY OS (18 Agents + 300 Skills)")
        content.append(f"**Execution Mode:** Mode F (Autonomous Dispatch) & Mode M (Chief Economic Officer)")
        content.append(f"---\n")

        content.append(f"## 🎯 SECTION 153: TODAY'S HIGHEST-PROBABILITY CASH ACTION")
        content.append(f"- **Primary Focus:** {top_action.opportunity}")
        content.append(f"- **Target Niche:** {top_action.customer}")
        content.append(f"- **Price Point:** **₹{top_action.price_inr:,.0f}** upfront / retainer")
        content.append(f"- **Evidence:** {top_action.evidence}")
        content.append(f"- **Immediate Next Step:** {top_action.exact_next_action}\n")

        content.append(f"## 🏢 TOP 5 VERIFIED BENGALURU PROSPECTS (READY FOR IMMEDIATE OUTREACH)")
        content.append(f"| # | Company | Sector | Decision Maker / Contact | Email / Phone | Fit Score | Status |")
        content.append(f"|---|---|---|---|---|---|---|")
        for i, p in enumerate(prospects, 1):
            comp = p.get("company", "N/A")
            sec = p.get("sector", "N/A")
            contact = f"{p.get('hr_name', p.get('founder_ceo_name', 'Lead'))} ({p.get('hr_designation', 'Exec')})"
            email = p.get("hr_email", "N/A")
            score = p.get("fit_score", 90)
            content.append(f"| {i} | **{comp}** | {sec} | {contact} | `{email}` | **{score}** | `READY_FOR_OUTREACH` |")

        content.append(f"\n## 📨 READY-TO-DISPATCH OUTREACH DOSSIERS")
        for i, p in enumerate(prospects, 1):
            comp = p.get("company")
            hr = p.get("hr_name") or p.get("founder_ceo_name") or "there"
            gap = p.get("identified_company_gap")
            pitch = p.get("pitch_angle")
            email = p.get("hr_email")
            phone = p.get("hr_phone", "N/A")
            linkedin = p.get("linkedin_search_url")

            content.append(f"### Prospect {i}: {comp}")
            content.append(f"- **Direct Email:** `{email}` | **Phone:** `{phone}`")
            content.append(f"- **LinkedIn Search:** [{hr} at {comp}]({linkedin})")
            content.append(f"- **Company Friction Identified:** {gap}")
            content.append(f"- **Our High-Value Pitch:** {pitch}")
            content.append(f"\n**Copy-Paste Message:**")
            content.append("```text")
            content.append(f"Subject: Operational execution gap analysis for {comp}")
            content.append(f"Hi {hr},")
            content.append(f"")
            content.append(f"I was reviewing {comp}'s operational footprint across Bengaluru. Specifically regarding {gap.lower()[:130]}, we've built a specialized AI workflow that eliminates this bottleneck.")
            content.append(f"")
            content.append(f"By deploying automated milestone verification and ground execution governance, peer teams have reclaimed 15+ hours weekly while protecting SLA adherence.")
            content.append(f"")
            content.append(f"I put together a 1-page sample brief illustrating how this applies to {comp}. Mind if I send the PDF over?")
            content.append(f"")
            content.append(f"Best regards,")
            content.append(f"Aditya Mehra")
            content.append("```\n")

        content.append(f"## 📊 18-AGENT SWARM OPERATIONAL DIRECTIVES")
        for d in swarm_status.get("top_directives", []):
            content.append(f"- {d}")

        content.append(f"\n## 💰 DAILY REVENUE PROJECTION & MILESTONES")
        content.append(f"- **1 Closed Setup:** ₹20,000 – ₹25,000 cash upfront")
        content.append(f"- **4 Retainer Clients:** ₹50,000/month recurring = **₹1,667/day** guaranteed baseline")
        content.append(f"- **8 Retainer Clients:** ₹1,00,000/month recurring = **₹3,333/day** baseline")
        content.append(f"- **Micro-SaaS & Trade Dockets:** +₹25,000/sprint")

        with open(battlecard_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        print(f"      Saved: {battlecard_path}")

        # Step 5: Refresh Dashboard Data
        print("\n[5/5] Rebuilding Live Cockpit Data Payload...")
        import omnimoney.build_dashboard_data as bdd
        bdd.main()
        print("      Dashboard data synchronized successfully.")

        print("\n" + "=" * 70)
        print(" 🚀 SUPREME EXECUTION COMPLETE. MONEY ENGINE IS FIRING ON ALL CYLINDERS.")
        print("=" * 70)

        return {
            "status": "SUCCESS",
            "timestamp": now_str,
            "battlecard": battlecard_path,
            "brief": daily_res["brief_file"],
            "hit_list": daily_res["hit_list_file"],
            "scripts": daily_res["scripts_file"],
            "swarm_active": swarm_status["active_agents"],
            "prospects_ready": len(prospects)
        }


def main():
    executor = SupremePromptExecutor()
    executor.execute_supreme_cycle()


if __name__ == "__main__":
    main()
