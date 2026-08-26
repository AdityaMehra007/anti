"""
CAREER BRAIN & SCORING ENGINE
Matches candidate profile against job records and recalculates scores on job change events.
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from ..engines.job_extractor import CanonicalJobRecord

@dataclass
class CandidateProfile:
    name: str = "Alex Mehr"
    target_roles: List[str] = None
    target_skills: List[str] = None
    preferred_locations: List[str] = None
    min_salary_inr: float = 3000000.0

    def __post_init__(self):
        if self.target_roles is None:
            self.target_roles = [
                "Principal Operations Strategist", "Lead Systems Architect",
                "Supply Chain AI Architect", "Director of Operations", "VP Operations"
            ]
        if self.target_skills is None:
            self.target_skills = [
                "Python", "Operations Strategy", "Supply Chain Analytics",
                "Process Optimization", "Agentic AI", "Distributed Systems", "SQL"
            ]
        if self.preferred_locations is None:
            self.preferred_locations = ["Bengaluru", "Bangalore", "Remote", "Hybrid"]

@dataclass
class JobMatchScore:
    job_id: str
    company: str
    role: str
    overall_score: float
    fit_rationale: str
    skill_match_pct: float
    tier_bonus: float
    next_recommended_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class CareerBrain:
    def __init__(self, profile: Optional[CandidateProfile] = None):
        self.profile = profile or CandidateProfile()

    def score_job(self, job: CanonicalJobRecord) -> JobMatchScore:
        score = 60.0
        rationale_items = []

        # 1. Location match
        loc = job.location.lower()
        if any(p.lower() in loc for p in self.profile.preferred_locations):
            score += 15.0
            rationale_items.append("Prime Bengaluru location match")

        # 2. Role keyword alignment
        role_lower = job.role.lower()
        if any(r.lower() in role_lower for r in ["operations", "supply chain", "strategist", "architect", "lead"]):
            score += 15.0
            rationale_items.append("Direct operational & tech leadership alignment")

        # 3. Skill match
        reqs = [r.lower() for r in (job.requirements + job.preferred_skills)]
        matched_skills = [s for s in self.profile.target_skills if any(s.lower() in r for r in reqs)]
        skill_pct = (len(matched_skills) / max(1, len(self.profile.target_skills))) * 100.0
        score += min(10.0, (skill_pct / 10.0))

        # 4. S-Tier company boost
        if any(c in job.company for c in ["Walmart", "Target", "JPMorgan", "Swiggy", "Zepto", "Google", "Amazon"]):
            score += 5.0
            rationale_items.append("S-Tier Top Tier Employer")

        overall = min(99.0, round(score, 1))
        job.strategic_score = overall

        next_action = "PREPARE_APPLICATION" if overall >= 85.0 else ("SAVE_FOR_MONITORING" if overall >= 75.0 else "LOG_ARCHIVE")

        return JobMatchScore(
            job_id=job.requisition_id,
            company=job.company,
            role=job.role,
            overall_score=overall,
            fit_rationale="; ".join(rationale_items) or "Strong baseline career alignment",
            skill_match_pct=round(skill_pct, 1),
            tier_bonus=5.0,
            next_recommended_action=next_action
        )
