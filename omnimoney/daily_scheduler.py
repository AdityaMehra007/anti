"""
OMNIMONEY OS - Daily Automation & Scheduling System
Runs morning briefing, mines high-probability prospects, generates custom outreach scripts,
and archives daily money-making battle cards.
"""

import os
import sys
import datetime
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

from omnimoney.omnimoney_engine import OmniMoneyEngine
from omnimoney.b2b_sales_engine import B2BSalesEngine
from omnimoney.morning_brief import MorningBriefEngine
from omnimoney.prospect_miner import ProspectMiner
from omnimoney.outreach_vault import OutreachVault


class DailyScheduler:
    def __init__(self, reports_dir: str = r"e:\anti\reports\daily"):
        self.reports_dir = reports_dir
        self.engine = OmniMoneyEngine()
        self.sales = B2BSalesEngine()
        self.brief_engine = MorningBriefEngine(self.engine, self.sales)
        self.miner = ProspectMiner()
        self.vault = OutreachVault()

        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir, exist_ok=True)

    def run_daily_cycle(self) -> Dict[str, Any]:
        date_str = datetime.date.today().strftime("%Y-%m-%d")

        # 1. Generate Morning CEO Brief
        brief_data = self.brief_engine.generate_brief()
        brief_path = os.path.join(self.reports_dir, f"MORNING_BRIEF_{date_str}.md")
        with open(brief_path, "w", encoding="utf-8") as f:
            f.write(brief_data.get("markdown_brief", "# Morning Brief"))

        # 2. Mine Top 5 High-Value Prospects from Database
        prospects = self.miner.mine_high_value_prospects(limit=5)

        # Write Prospect Hit List
        hit_list_path = os.path.join(self.reports_dir, f"PROSPECT_HIT_LIST_{date_str}.md")
        with open(hit_list_path, "w", encoding="utf-8") as f:
            f.write(f"# 🎯 OMNIMONEY PROSPECT HIT LIST - {date_str}\n\n")
            f.write(f"**Target Objective:** Reach out to 5 verified high-fit prospects today to secure discovery calls.\n\n")
            f.write("| # | Company | Sector | Contact / Title | Email | Fit Score | Strategic Pitch Angle |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            for i, p in enumerate(prospects, 1):
                company = p.get("company", "Unknown")
                sector = p.get("sector", "Tech")
                contact = f"{p.get('hr_name', p.get('founder_ceo_name', 'Lead'))} ({p.get('hr_designation', p.get('founder_ceo_title', 'Exec'))})"
                email = p.get("hr_email", p.get("careers_email", "N/A"))
                score = p.get("fit_score", 90)
                pitch = p.get("pitch_angle", "Operational optimization")
                f.write(f"| {i} | **{company}** | {sector} | {contact} | `{email}` | **{score}** | {pitch} |\n")

            f.write("\n\n## Specific Company Action Briefs\n\n")
            for i, p in enumerate(prospects, 1):
                f.write(f"### {i}. {p.get('company')} ({p.get('sector')})\n")
                f.write(f"- **Decision Maker:** {p.get('founder_ceo_name')} - {p.get('founder_ceo_title')}\n")
                f.write(f"- **HR / Talent Lead:** {p.get('hr_name')} ({p.get('hr_designation')})\n")
                f.write(f"- **Direct Email:** `{p.get('hr_email')}` | Phone: `{p.get('hr_phone', 'N/A')}`\n")
                f.write(f"- **Identified Gap:** {p.get('identified_company_gap')}\n")
                f.write(f"- **Candidate Solution:** {p.get('candidate_solution')}\n")
                f.write(f"- **Pitch Angle:** {p.get('pitch_angle')}\n")
                f.write(f"- **LinkedIn Profile:** [{p.get('hr_name')} on LinkedIn]({p.get('linkedin_search_url')})\n\n")

        # 3. Generate Outreach Scripts for the 5 prospects
        scripts_path = os.path.join(self.reports_dir, f"OUTREACH_SCRIPTS_{date_str}.md")
        with open(scripts_path, "w", encoding="utf-8") as f:
            f.write(f"# 📨 READY-TO-SEND OUTREACH SCRIPTS - {date_str}\n\n")
            f.write(f"Copy and paste directly into LinkedIn InMail or Email.\n\n")
            for i, p in enumerate(prospects, 1):
                company = p.get("company", "your firm")
                contact = p.get("hr_name") or p.get("founder_ceo_name") or "there"
                gap = p.get("identified_company_gap", "scaling operations efficiently")
                pitch = p.get("pitch_angle", "streamlining operational execution with AI systems")
                
                f.write(f"## Script {i}: {company} (To: {contact})\n\n")
                f.write("```text\n")
                f.write(f"Hi {contact},\n\n")
                f.write(f"Noticed {company}'s ongoing expansion across the Bengaluru corridor. In analyzing GCC and tech operational workflows, {gap.lower()[:120]} often creates unnecessary friction.\n\n")
                f.write(f"We've built an autonomous execution framework focused on {pitch.lower()[:120]}.\n\n")
                f.write(f"I've put together a brief 1-page operational brief specifically for {company}. Would you be open to reviewing it this week?\n\n")
                f.write(f"Best regards,\nAditya Mehra\n")
                f.write("```\n\n---\n\n")

        return {
            "date": date_str,
            "brief_file": brief_path,
            "hit_list_file": hit_list_path,
            "scripts_file": scripts_path,
            "prospects_mined": len(prospects),
            "status": "SUCCESS"
        }


if __name__ == "__main__":
    scheduler = DailyScheduler()
    res = scheduler.run_daily_cycle()
    print("Daily cycle executed successfully:")
    for k, v in res.items():
        print(f"  {k}: {v}")
