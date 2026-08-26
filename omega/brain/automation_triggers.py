"""
AUTOMATION TRIGGERS & APPLICATION MISSIONS
Triggers Priority Alerts and creates Application Preparation Missions.
Strictly requires authorization policy (no uncontrolled auto-submissions).
"""
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from ..engines.job_extractor import CanonicalJobRecord

@dataclass
class PriorityAlert:
    alert_id: str
    company: str
    role: str
    score: float
    deadline: Optional[str]
    contact_path: str
    source_url: str
    next_action: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ApplicationPreparationMission:
    mission_id: str
    job_id: str
    company: str
    role: str
    strategic_score: float
    target_deadline: str
    dossier_ready: bool
    tailored_resume_ready: bool
    cover_letter_ready: bool
    submission_policy: str = "REQUIRES_USER_EXPLICIT_APPROVAL"
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class AutomationTriggerEngine:
    def __init__(self, score_threshold: float = 85.0):
        self.score_threshold = score_threshold
        self.alerts: List[PriorityAlert] = []
        self.missions: List[ApplicationPreparationMission] = []

    def evaluate_job(self, job: CanonicalJobRecord, score: float) -> Optional[ApplicationPreparationMission]:
        now_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # Create Priority Alert for S-tier high scorers
        if score >= self.score_threshold:
            alert = PriorityAlert(
                alert_id=f"ALT-{len(self.alerts)+1:04d}",
                company=job.company,
                role=job.role,
                score=score,
                deadline=job.deadline or "Rolling",
                contact_path=job.public_recruiter or f"careers@{job.company.lower().replace(' ', '')}.com",
                source_url=job.source_url,
                next_action="PREPARE_APPLICATION_DOSSIER",
                created_at=now_ts
            )
            self.alerts.append(alert)

            mission = ApplicationPreparationMission(
                mission_id=f"MSN-APP-{len(self.missions)+1:04d}",
                job_id=job.requisition_id,
                company=job.company,
                role=job.role,
                strategic_score=score,
                target_deadline=job.deadline or "2026-09-30",
                dossier_ready=True,
                tailored_resume_ready=True,
                cover_letter_ready=True,
                submission_policy="REQUIRES_USER_EXPLICIT_APPROVAL",
                created_at=now_ts
            )
            self.missions.append(mission)
            return mission
        return None
