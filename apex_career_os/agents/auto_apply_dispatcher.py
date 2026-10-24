"""
auto_apply_dispatcher.py - Agent 4: Autonomous Application & Dispatch Orchestrator
==================================================================================
Assembles ATS autofill JSON payloads (Greenhouse, Lever, Workday, SmartRecruiters, Taleo),
generates deterministic screening question answers, and manages the complete lifecycle
of active job applications across Kanban pipeline stages.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from apex_career_os.core.truth_layer import get_candidate_profile

DATA_DIR = Path(r"e:\anti\data")
PIPELINE_STORE_JSON = DATA_DIR / "apex_application_pipeline.json"

class AutoApplyDispatcherAgent:
    def __init__(self):
        self.candidate = get_candidate_profile()
        self.pipeline_file = PIPELINE_STORE_JSON
        self._init_pipeline()

    def _init_pipeline(self):
        if not self.pipeline_file.exists():
            initial_data = {
                "created_at": datetime.now().isoformat(),
                "total_applications": 0,
                "stages": {
                    "DISCOVERED": [],
                    "TAILORED": [],
                    "OUTREACH_SENT": [],
                    "APPLIED": [],
                    "INTERVIEW_SCHEDULED": [],
                    "OFFER_RECEIVED": []
                }
            }
            with open(self.pipeline_file, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

    def generate_ats_payload(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Generates machine-readable autofill payload for ATS form submissions."""
        company = job.get("company", "")
        title = job.get("title", "")
        
        return {
            "candidate_info": {
                "first_name": "Aditya",
                "last_name": "Mehra",
                "email": self.candidate.email,
                "phone": self.candidate.phone,
                "location": self.candidate.location,
                "linkedin": self.candidate.linkedin_url,
                "github_portfolio": "https://github.com/adityamehra07",
                "work_authorization": "Yes, Indian Citizen (Authorized to work in India)",
                "requires_sponsorship": "No",
                "notice_period": "0 Days (Immediate Joiner)",
                "willingness_to_relocate": "Yes (Bangalore Primary, Open to travel)"
            },
            "education": {
                "institution": self.candidate.institution,
                "degree": self.candidate.degree,
                "graduation_year": self.candidate.graduation_year,
                "gpa_status": "Graduated / First Class Standing"
            },
            "screening_responses": self.generate_screening_answers(company, title),
            "job_metadata": {
                "job_id": job.get("id"),
                "company": company,
                "title": title,
                "url": job.get("url"),
                "track": job.get("track")
            }
        }

    def generate_screening_answers(self, company: str, title: str) -> Dict[str, str]:
        """Provides verified, bullet-proof responses to common ATS screening questions."""
        return {
            "notice_period": "0 Days (Immediate Joiner)",
            "current_ctc": "Fresher / Early Career Candidate (Standard Corporate Scale)",
            "expected_ctc": "INR 6.5 LPA - 9.0 LPA (Flexible based on role scope and growth trajectory)",
            "authorized_in_india": "Yes",
            "sponsorship_required": "No",
            "why_this_company": (
                f"I admire {company}'s market leadership and relentless execution velocity. My background managing "
                f"high-stakes operations for 100,000+ attendees at Aero India 2025 and negotiating 15% recurring cost savings "
                f"directly mirrors the ownership culture at {company}. I am eager to apply this operational rigor to the {title} team."
            ),
            "relevant_experience": (
                "Over 8 years of accumulated real-world business exposure including frontline family business retail operations "
                "starting at age 17, 300+ event and brand activation deployments (Aero India 2025, Tata Comms, Puma), B2B sales pipeline "
                "management closing INR 1.5L+ at Pencil Mark, and 99%+ accuracy in AI data operations at Instawork AI."
            ),
            "handling_deadlines": (
                "At Aero India 2025, operating under military security constraints, I enforced 24-hour advance protocol badge verification "
                "and proactive inventory replenishment batches, ensuring 100% on-time morning gate openings with 0 breaches and 0% shrinkage."
            )
        }

    def register_application(self, job: Dict[str, Any], initial_stage: str = "TAILORED") -> Dict[str, Any]:
        """Registers a job into the active tracking Kanban pipeline."""
        with open(self.pipeline_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        app_record = {
            "job_id": job.get("id"),
            "company": job.get("company"),
            "title": job.get("title"),
            "track": job.get("track"),
            "url": job.get("url"),
            "stage": initial_stage,
            "updated_at": datetime.now().isoformat()
        }

        # Check if already present
        existing_stage = None
        for stage, items in data["stages"].items():
            for idx, item in enumerate(items):
                if item.get("job_id") == job.get("id"):
                    existing_stage = stage
                    items.pop(idx)
                    break

        if initial_stage not in data["stages"]:
            initial_stage = "TAILORED"

        data["stages"][initial_stage].append(app_record)
        
        # Recount total
        total = sum(len(v) for v in data["stages"].values())
        data["total_applications"] = total
        data["last_updated"] = datetime.now().isoformat()

        with open(self.pipeline_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return {
            "status": "UPDATED",
            "job_id": job.get("id"),
            "stage": initial_stage,
            "total_active_pipeline": total
        }

    def get_pipeline_summary(self) -> Dict[str, Any]:
        """Returns the current breakdown of applications across all Kanban stages."""
        with open(self.pipeline_file, "r", encoding="utf-8") as f:
            return json.load(f)
