"""
orchestrator.py - OMEGA Master Career & Autonomous Job Conquest Orchestrator
============================================================================
Unifies all 7 specialized agents into an autonomous, closed-loop execution system:
  1. SentinelLearnerAgent: Web mining, live scraping, continuous company intelligence.
  2. TruthTailorAgent: Zero-hallucination ATS resume, cover letter & elevator pitches.
  3. NetworkStrikeAgent: 9,223 LinkedIn network recruiter matching & outreach cadences.
  4. AutoApplyDispatcherAgent: ATS autofill payload generation & Kanban tracking.
  5. InterviewMasterAgent: STAR interview simulation & curveball question defense.
  6. CompensationStrategistAgent: Market salary benchmarking & negotiation playbooks.
  7. CareerGrowthArchitectAgent: 30-60-90 day blueprints & 5-year hyper-growth ladders.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from apex_career_os.core.knowledge_learning_vault import KnowledgeLearningVault
from apex_career_os.agents.sentinel_learner import SentinelLearnerAgent
from apex_career_os.agents.truth_tailor import TruthTailorAgent
from apex_career_os.agents.network_strike import NetworkStrikeAgent
from apex_career_os.agents.auto_apply_dispatcher import AutoApplyDispatcherAgent
from apex_career_os.agents.interview_master import InterviewMasterAgent
from apex_career_os.agents.compensation_strategist import CompensationStrategistAgent
from apex_career_os.agents.career_growth_architect import CareerGrowthArchitectAgent

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
TELEMETRY_JSON = DATA_DIR / "apex_master_career_telemetry.json"

class ApexCareerOrchestrator:
    def __init__(self):
        self.vault = KnowledgeLearningVault()
        self.sentinel = SentinelLearnerAgent(vault=self.vault)
        self.tailor = TruthTailorAgent()
        self.network = NetworkStrikeAgent()
        self.dispatcher = AutoApplyDispatcherAgent()
        self.interview = InterviewMasterAgent(vault=self.vault)
        self.compensation = CompensationStrategistAgent()
        self.growth = CareerGrowthArchitectAgent()

    def run_full_autonomous_cycle(self, limit_jobs: int = 50) -> Dict[str, Any]:
        """Runs the complete multi-agent job discovery, tailoring, and intelligence cycle."""
        start_time = datetime.now()
        print("[Orchestrator] Launching SentinelLearnerAgent to harvest and learn...")
        harvest_result = self.sentinel.run_harvest_and_learn_cycle(limit=limit_jobs)
        raw_jobs = harvest_result.get("sample_jobs", [])

        processed_opportunities = []
        print(f"[Orchestrator] Evaluating ATS compatibility across {len(raw_jobs)} active opportunities...")

        for job in raw_jobs:
            # 1. ATS Match Evaluation
            match_res = self.tailor.evaluate_ats_match(job)
            match_score = match_res["match_score_percent"]

            # 2. Recruiter Intelligence
            recruiters = self.network.find_recruiters_for_company(job["company"], limit=3)
            primary_recruiter = recruiters[0] if recruiters else None
            outreach_pack = self.network.generate_outreach_dossier(job, contact=primary_recruiter)

            # 3. Resume & Cover Letter
            resume_md = self.tailor.generate_tailored_resume(job, output_format="markdown")
            cover_letter = self.tailor.generate_cover_letter(job)
            pitches = self.tailor.generate_elevator_pitches(job)

            # 4. ATS Autofill & Kanban Registration
            ats_payload = self.dispatcher.generate_ats_payload(job)
            self.dispatcher.register_application(job, initial_stage="TAILORED" if match_score >= 80 else "DISCOVERED")

            # 5. Interview Prep Pack
            interview_pack = self.interview.generate_interview_prep_pack(job["company"], job["title"])

            # 6. Compensation Benchmark
            comp_bench = self.compensation.benchmark_role_compensation(job["track"])

            # 7. 30-60-90 Day Blueprint
            onboarding = self.growth.generate_30_60_90_day_blueprint(job["company"], job["title"])

            opp_dossier = {
                "job": job,
                "ats_evaluation": match_res,
                "recruiters": recruiters,
                "outreach_pack": outreach_pack,
                "resume_preview": resume_md[:800] + "...",
                "cover_letter_preview": cover_letter[:600] + "...",
                "pitches": pitches,
                "interview_pack": interview_pack,
                "compensation_benchmark": comp_bench,
                "onboarding_blueprint": onboarding
            }
            processed_opportunities.append(opp_dossier)

        # Sort by match score descending
        processed_opportunities.sort(key=lambda x: x["ats_evaluation"]["match_score_percent"], reverse=True)

        telemetry = {
            "cycle_timestamp": datetime.now().isoformat(),
            "duration_seconds": round((datetime.now() - start_time).total_seconds(), 2),
            "total_jobs_evaluated": len(processed_opportunities),
            "top_tier_matches": len([x for x in processed_opportunities if x["ats_evaluation"]["match_score_percent"] >= 85]),
            "kanban_pipeline": self.dispatcher.get_pipeline_summary(),
            "trending_skills": self.vault.get_top_trending_keywords(limit=20),
            "five_year_trajectory": self.growth.generate_5_year_career_ladder(),
            "opportunities": processed_opportunities
        }

        # Save Telemetry
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(TELEMETRY_JSON, "w", encoding="utf-8") as f:
            json.dump(telemetry, f, indent=2)

        print(f"[Orchestrator] Cycle completed in {telemetry['duration_seconds']}s. Telemetry written to {TELEMETRY_JSON}")
        return telemetry

    def execute_instant_strike_for_custom_role(self, company: str, title: str, description: str, track: str = "Operations & BD") -> Dict[str, Any]:
        """Runs immediate all-agent strike for any user-provided job."""
        job = {
            "id": f"CUSTOM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "company": company,
            "title": title,
            "description": description,
            "location": "Bengaluru, India",
            "url": "https://www.linkedin.com/jobs",
            "track": track,
            "source": "Instant Custom Strike"
        }

        # Learn immediately from the custom role description
        self.vault.learn_from_job_posting(job)

        match_res = self.tailor.evaluate_ats_match(job)
        resume_md = self.tailor.generate_tailored_resume(job, output_format="markdown")
        resume_html = self.tailor.generate_tailored_resume(job, output_format="html")
        cover_letter = self.tailor.generate_cover_letter(job)
        pitches = self.tailor.generate_elevator_pitches(job)
        recruiters = self.network.find_recruiters_for_company(company, limit=3)
        outreach = self.network.generate_outreach_dossier(job, contact=recruiters[0] if recruiters else None)
        ats_payload = self.dispatcher.generate_ats_payload(job)
        interview_pack = self.interview.generate_interview_prep_pack(company, title)
        comp_benchmark = self.compensation.benchmark_role_compensation(track)
        onboarding = self.growth.generate_30_60_90_day_blueprint(company, title)

        return {
            "job": job,
            "ats_evaluation": match_res,
            "resume_markdown": resume_md,
            "resume_html": resume_html,
            "cover_letter": cover_letter,
            "pitches": pitches,
            "recruiters": recruiters,
            "outreach_pack": outreach,
            "ats_autofill_payload": ats_payload,
            "interview_pack": interview_pack,
            "compensation_benchmark": comp_benchmark,
            "onboarding_blueprint": onboarding
        }
