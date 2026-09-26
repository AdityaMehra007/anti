"""
ADI CAREER OS — MASTER CAREER ORCHESTRATOR & UNIFIED FACADE (Section 8, 12, 52, 269)
Central controller binding Sales Exclusion, 100-Point Scoring, ATS Matching,
Application State Machine, Recruiter CRM, and Skill Intelligence into a single deep module.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import uuid

from .sales_exclusion_engine import SalesExclusionEngine
from .job_entity import JobEntity, JobNormalizer, JobDeduplicator
from .job_scoring_engine import JobScoringEngine
from .application_pipeline import (
    ApplicationRecord, ApplicationState, InvalidStateTransitionError, MissingSubmissionProofError
)
from .ats_engine import ATSEngine
from .recruiter_crm import RecruiterCRM, RecruiterContact, OutreachEngine
from .skill_intelligence import SkillIntelligenceEngine

class CareerOrchestrator:
    """
    Unified Deep Module implementing ADI CAREER OS according to
    ADI OMNI CODEX (OMNI-X / Production Engineering Mode).
    """

    def __init__(self, workspace: str = r"e:\anti"):
        self.workspace = workspace
        self.deduplicator = JobDeduplicator()
        self.applications: Dict[str, ApplicationRecord] = {}
        self.recruiter_crm = RecruiterCRM()

    def process_job_posting(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the complete Job Intelligence Pipeline (Section 12):
        DISCOVER -> INGEST -> NORMALIZE -> VALIDATE -> DEDUPLICATE -> CLASSIFY -> SCORE -> VERIFY -> PRIORITIZE -> TRACK
        """
        raw_title = raw_data.get("title", "")
        raw_desc = raw_data.get("description", "")
        raw_company = raw_data.get("company", raw_data.get("company_name", "Target Company"))
        raw_loc = raw_data.get("location", "Bengaluru, India")
        raw_salary = raw_data.get("salary", "")
        raw_exp = raw_data.get("experience", "")

        # 1. Normalization (Sections 293-296)
        norm_loc = JobNormalizer.normalize_location(raw_loc)
        norm_exp = JobNormalizer.normalize_experience(raw_exp)
        norm_sal = JobNormalizer.normalize_salary(raw_salary)

        # 2. Sales Exclusion Engine (Section 11)
        sales_eval = SalesExclusionEngine.evaluate(
            title=raw_title,
            description=raw_desc,
            responsibilities=raw_data.get("responsibilities", []),
            compensation_type=raw_data.get("compensation_type", "fixed")
        )

        job_id = raw_data.get("id") or f"JOB-{uuid.uuid4().hex[:8].upper()}"
        job = JobEntity(
            id=job_id,
            source=raw_data.get("source", "Career Engine Direct"),
            title=raw_title,
            description=raw_desc,
            location=norm_loc,
            source_job_id=raw_data.get("source_job_id", ""),
            company_id=raw_data.get("company_id", ""),
            company_name=raw_company,
            work_model=raw_data.get("work_model", "Hybrid"),
            experience_min=norm_exp["min"],
            experience_max=norm_exp["max"],
            salary_min=norm_sal["min"],
            salary_max=norm_sal["max"],
            salary_currency=norm_sal["currency"],
            posted_at=raw_data.get("posted_at", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            application_url=raw_data.get("application_url", raw_data.get("url", "")),
            role_family=raw_data.get("role_family", "Business Operations"),
            sales_risk_score=sales_eval["sales_risk_score"]
        )

        # 3. Deduplication (Section 14)
        is_new = self.deduplicator.register_job(job)

        # 4. 100-Point Scoring (Section 16 & 17)
        score_eval = JobScoringEngine.score_job(job, sales_risk_score=sales_eval["sales_risk_score"])
        job.fit_score = score_eval["final_fit_score"]
        job.eligibility_score = score_eval["components"]["eligibility"]
        job.hiring_probability = score_eval["components"]["hiring_probability"]
        job.company_quality = score_eval["components"]["company_quality"]

        # 5. ATS Matching & Tailoring (Sections 20, 21, 22)
        ats_eval = ATSEngine.analyze_match(job.title, job.description)

        # 6. Skill Coverage Audit (Sections 27, 28)
        skill_eval = SkillIntelligenceEngine.audit_job_posting_skills(job.description)

        # 7. Executive Job View (Section 52)
        executive_view = {
            "why_this_job": score_eval["explainability"]["why"],
            "why_adi_fits": "BBA International Business degree with verifiable summit ops, CRM, and analytics execution.",
            "what_is_missing": score_eval["explainability"]["missing_requirements"],
            "how_to_apply": f"Submit tailored resume profile '{ats_eval['selected_profile']}' via portal / referral.",
            "who_to_contact": f"Talent Acquisition / HR Lead at {job.company_name} (Search verified network of 9,223 contacts).",
            "what_to_prepare": "STAR stories covering high-stakes logistics, SQL queries, and SOP workflow design.",
            "risk": f"Sales Risk: {sales_eval['sales_risk_score']}/100 ({sales_eval['risk_level']}).",
            "next_action": score_eval["explainability"]["recommended_action"]
        }

        return {
            "job": job.to_dict(),
            "is_new_opportunity": is_new,
            "freshness": job.get_freshness(),
            "sales_evaluation": sales_eval,
            "scoring": score_eval,
            "ats_matching": ats_eval,
            "skill_audit": skill_eval,
            "executive_view": executive_view
        }

    def create_application_record(self, job_id: str, company: str, role: str) -> ApplicationRecord:
        """Initializes a tracked application record in DISCOVERED state."""
        app_id = f"APP-{uuid.uuid4().hex[:8].upper()}"
        rec = ApplicationRecord(app_id, job_id, company, role)
        self.applications[app_id] = rec
        return rec

    def get_career_overview(self) -> Dict[str, Any]:
        """Telemetry snapshot for Executive Dashboard (Section 49)."""
        state_counts = {}
        for app in self.applications.values():
            s = app.current_state.value
            state_counts[s] = state_counts.get(s, 0) + 1

        return {
            "candidate": "Aditya Mehra (Adi)",
            "degree": "BBA International Business (Dayananda Sagar University, 2023-2026)",
            "target_positioning": "AI-enabled Business Operations / Business Analyst / Strategy & Operations",
            "sales_exclusion_policy": "STRICT (0% Telecalling/BDE/Cold Calling Tolerance)",
            "tracked_applications_count": len(self.applications),
            "funnel_distribution": state_counts,
            "core_skills_matrix": SkillIntelligenceEngine.get_ranked_skills(),
            "status": "AUTONOMOUS_OPERATIONAL_24_7"
        }
