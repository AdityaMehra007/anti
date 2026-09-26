#!/usr/bin/env python3
"""
========================================================================================
THE ULTIMATE AI-POWERED JOB ACQUISITION OPERATING SYSTEM
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Unified Master Orchestrator, CLI Engine, and 57-Directive Architecture:
  1. Candidate Profile & Ground Truth Evidence Ledger
  2. 100-Point Job Matching & Commute Friction Engine
  3. ATS Optimization & Keyword Analysis (ATS Score / 100)
  4. 12 Specialized 1-Page Harvard ATS Resume Variants
  5. 30-Question Mock Interview & STAR Story Compendium
  6. Green / Yellow / Red Skill Gap Roadmaps (7/30/90 Days)
  7. Living Daily Operating System (Morning Brief & Evening Retro)
  8. AI Career Copilot & "WHAT SHOULD I DO NEXT?" One-Click Trigger
  9. Emergency Mode (Fast Hire) & Premium Mode (MNC/GCC Compounding)
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import sqlite3
import argparse
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
CORE_DIR = ROOT_DIR / "core"
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(CORE_DIR))

from core.job_matching_100pt import JobMatching100Engine
from core.ats_optimizer import ATSOptimizer
from core.skill_gap_engine import SkillGapEngine
from core.interview_engine_30q import InterviewEngine30Q
from core.resume_vault import ResumeVault
from core.daily_cadence import DailyCadenceEngine
from core.career_copilot import CareerCopilot

APPROVALS_DB = DATA_DIR / "omega_approvals.db"
PROFILE_JSON = DATA_DIR / "verified_profile.json"

class UltimateCareerOS:
    """The unified master orchestrator for all 57 job acquisition subsystems."""

    def __init__(self):
        self.profile = self._load_profile()
        self.top_jobs = self._load_top_jobs()

    def _load_profile(self) -> Dict[str, Any]:
        if PROFILE_JSON.exists():
            with open(PROFILE_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"candidate": {"full_name": "Aditya Mehra"}}

    def _load_top_jobs(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "BLR-JOB-001",
                "company": "Accenture India",
                "title": "Global Business Operations & BD Analyst",
                "location": "Bengaluru (Bellandur / Ecospace)",
                "experience": "Fresher / 0-2 Yrs",
                "skills": "Business Operations, Process Mapping, Vendor SLAs, Excel Modeling",
                "url": "https://www.accenture.com/in-en/careers"
            },
            {
                "id": "BLR-JOB-002",
                "company": "Deloitte US-India",
                "title": "Risk & Business Operations Advisory Analyst",
                "location": "Bengaluru (Prestige Tech Park)",
                "experience": "Entry Level / 0-2 Yrs",
                "skills": "Trade Compliance, Incoterms 2020, Risk Governance, SOP Management",
                "url": "https://www2.deloitte.com/ui/en/careers/careers.html"
            },
            {
                "id": "BLR-JOB-003",
                "company": "EY (Ernst & Young GDS)",
                "title": "Business Analyst - Global Advisory",
                "location": "Bengaluru (RMZ Infinity / ORR)",
                "experience": "Fresher / 0-2 Yrs",
                "skills": "Cross-Border Trade Advisory, Operations Consulting, Stakeholder Management",
                "url": "https://www.ey.com/en_in/careers"
            },
            {
                "id": "BLR-JOB-004",
                "company": "Amazon Bangalore",
                "title": "Operations & Vendor Management Executive",
                "location": "Bengaluru (Bagmane Tech Park)",
                "experience": "0-2 Yrs",
                "skills": "Inbound/Outbound Logistics, Fulfillment SLAs, Vendor Reconciliation",
                "url": "https://www.amazon.jobs/en/locations/bangalore-india"
            },
            {
                "id": "BLR-JOB-005",
                "company": "Goldman Sachs",
                "title": "Global Markets Operations Analyst",
                "location": "Bengaluru (Prestige Falcon / Bellandur)",
                "experience": "Campus / Fresher",
                "skills": "Trade Settlements, Cross-Border Payments, Regulatory Compliance",
                "url": "https://www.goldmansachs.com/careers/"
            },
            {
                "id": "BLR-JOB-008",
                "company": "AERO India / Salt in My Coca",
                "title": "Exhibition & Event Operations Lead",
                "location": "Bengaluru (Yelahanka / CBD)",
                "experience": "Lead / Associate",
                "skills": "High-Security VIP Protocol, Crowd Logistics, Venue Staging, Crisis Management",
                "url": "https://aeroindia.gov.in/"
            },
            {
                "id": "BLR-JOB-010",
                "company": "Flipkart Bangalore",
                "title": "Operations Specialist - Supply Chain & Logistics",
                "location": "Bengaluru (Electronic City HQ)",
                "experience": "0-2 Yrs",
                "skills": "Supply Chain Network Design, Warehouse Operations, Vendor SLA Governance",
                "url": "https://www.flipkartcareers.com/"
            },
            {
                "id": "BLR-JOB-011",
                "company": "Puma India (Bangalore HQ)",
                "title": "Retail Operations & Brand Experience Coordinator",
                "location": "Bengaluru (Indiranagar HQ)",
                "experience": "0-2 Yrs",
                "skills": "Store Operations, Brand Activations, Inventory Intake, POS Tracking",
                "url": "https://about.puma.com/en/careers"
            }
        ]

    def get_morning_brief(self) -> Dict[str, Any]:
        scored_jobs = []
        for j in self.top_jobs:
            score_data = JobMatching100Engine.compute_match_score(j)
            ats_data = ATSOptimizer.optimize_for_job(j, self.profile)
            scored_jobs.append({**j, "scores": score_data, "ats": ats_data})
        return DailyCadenceEngine.generate_morning_brief(scored_jobs, {"health_score": 96})

    def get_what_should_i_do_next(self) -> Dict[str, Any]:
        return CareerCopilot.what_should_i_do_next()

    def get_full_dashboard_payload(self) -> Dict[str, Any]:
        """Returns the complete aggregated JSON payload powering the web dashboard."""
        scored_jobs = []
        for j in self.top_jobs:
            score_data = JobMatching100Engine.compute_match_score(j)
            ats_data = ATSOptimizer.optimize_for_job(j, self.profile)
            scored_jobs.append({**j, "scores": score_data, "ats": ats_data})

        agencies_file = DATA_DIR / "bangalore_job_agencies.json"
        agencies = []
        if agencies_file.exists():
            with open(agencies_file, "r", encoding="utf-8") as af:
                agencies = json.load(af)

        funded_file = DATA_DIR / "bangalore_funded_startups_and_global_mncs.json"
        funded_companies = []
        if funded_file.exists():
            with open(funded_file, "r", encoding="utf-8") as ff:
                funded_companies = json.load(ff)

        return {
            "candidate": self.profile.get("candidate", {}),
            "evidence_chains": self.profile.get("skill_evidence_chains", []),
            "health_score": 96,
            "funnel": {
                "discovered": 4500,
                "qualified": 300,
                "packaged": 61,
                "dispatched": 49,
                "screenings": 3,
                "interviews": 0,
                "offers": 0
            },
            "what_to_do_next": CareerCopilot.what_should_i_do_next(),
            "top_openings": scored_jobs,
            "resume_variants": ResumeVault.list_variants(),
            "skill_gap_audit": SkillGapEngine.audit_profile_against_role("Global Business Operations Analyst"),
            "interview_compendium": InterviewEngine30Q.get_compendium(),
            "bangalore_agencies": agencies,
            "funded_startups_and_global_mncs": funded_companies,
            "modes": {
                "emergency_mode": {
                    "focus": "Time-to-Offer Acceleration (7-14 Days)",
                    "priority_targets": ["Puma India Retail Ops", "Salt in My Coca Event Ops", "Swiggy City Ops"],
                    "strategy": "Leverage verified direct ground operations and immediate joining status."
                },
                "premium_mode": {
                    "focus": "MNC Brand Capital & International Compounding (3-Year Horizon)",
                    "priority_targets": ["Accenture India GCC", "Deloitte US-India Advisory", "Goldman Sachs Global Markets"],
                    "strategy": "Leverage DSU International Business degree, trade compliance, and enterprise analytics."
                }
            }
        }

    def launch_dashboard(self):
        dash_path = ROOT_DIR / "apps" / "get_me_hired_dashboard" / "index.html"
        data_path = ROOT_DIR / "apps" / "get_me_hired_dashboard" / "data.json"
        try:
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(self.get_full_dashboard_payload(), f, indent=2)
        except Exception as e:
            print(f"[!] Warning updating data.json: {e}")
            
        print("=" * 80)
        print("  LAUNCHING 'GET ME HIRED' MASTER CONTROL DASHBOARD")
        print(f"  Path: {dash_path}")
        print("=" * 80)
        webbrowser.open(dash_path.as_uri())

def main():
    parser = argparse.ArgumentParser(description="Ultimate AI-Powered Job Acquisition OS")
    parser.add_argument("--brief", action="store_true", help="Print Morning Job Briefing")
    parser.add_argument("--next-action", action="store_true", help="Print single highest-ROI action right now")
    parser.add_argument("--copilot", type=str, help="Ask the AI Career Copilot a question")
    parser.add_argument("--dashboard", action="store_true", help="Open the full 'GET ME HIRED' web dashboard")
    parser.add_argument("--export-json", action="store_true", help="Export aggregated telemetry payload to JSON")
    parser.add_argument("--global-directory", action="store_true", help="Print Bangalore Funded Startups & Global MNCs summary")
    
    args = parser.parse_args()
    os_engine = UltimateCareerOS()

    if args.global_directory:
        from scripts.compile_funded_startups_and_global_mncs import print_status
        print_status()
        return

    if args.export_json:
        data_path = ROOT_DIR / "apps" / "get_me_hired_dashboard" / "data.json"
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(os_engine.get_full_dashboard_payload(), f, indent=2)
        print(f"[*] Dashboard payload exported to {data_path}")
        return
    
    if args.brief:
        brief = os_engine.get_morning_brief()
        print("\n" + "=" * 80)
        print(f"  {brief['briefing_type']} — {brief['date']}")
        print("=" * 80)
        print(f"[*] Job Hunt Health Score : {brief['job_hunt_health_score']}/100")
        print("\n[!] TODAY'S TOP 3 MUST-DO ACTIONS:")
        for idx, act in enumerate(brief['top_3_must_do_actions'], 1):
            print(f"  {idx}. {act}")
        print(f"\n[*] Strategic Insight: {brief['strategic_insight']}")
        print("=" * 80)
        return
        
    if args.next_action:
        act = os_engine.get_what_should_i_do_next()
        print("\n" + "=" * 80)
        print("  SINGLE HIGHEST-ROI ACTION RIGHT NOW")
        print("=" * 80)
        print(f"[*] Action Title : {act['action_title']}")
        print(f"[*] ROI Formula  : {act['roi_formula']}")
        print(f"[*] Step 1       : {act['step_1']}")
        print(f"[*] Step 2       : {act['step_2']}")
        print(f"[*] Step 3       : {act['step_3']}")
        print(f"[*] Urgency      : {act['urgency']}")
        print("=" * 80)
        return
        
    if args.copilot:
        ans = CareerCopilot.answer_query(args.copilot)
        print("\n" + "=" * 80)
        print(f"  AI CAREER COPILOT: '{args.copilot}'")
        print("=" * 80)
        for k, v in ans.items():
            print(f"[*] {k.replace('_', ' ').title()}: {v}")
        print("=" * 80)
        return
        
    if args.dashboard or len(sys.argv) == 1:
        os_engine.launch_dashboard()

if __name__ == "__main__":
    main()
