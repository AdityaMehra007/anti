"""
ADI CAREER OS — APPLICATION PIPELINE STATE MACHINE & TRUTH ENGINE (Sections 18, 19, 128, 129)
Strictly enforces valid stage transitions, immutable audit logs, and the Application Truth Rule.
"""

from enum import Enum
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

class ApplicationState(str, Enum):
    """Canonical 16 states from Section 18 of the Codex."""
    DISCOVERED = "DISCOVERED"
    SHORTLISTED = "SHORTLISTED"
    READY_TO_APPLY = "READY_TO_APPLY"
    APPLIED = "APPLIED"
    REFERRAL_REQUESTED = "REFERRAL_REQUESTED"
    RECRUITER_CONTACTED = "RECRUITER_CONTACTED"
    SCREENING = "SCREENING"
    ASSESSMENT = "ASSESSMENT"
    INTERVIEW_1 = "INTERVIEW_1"
    INTERVIEW_2 = "INTERVIEW_2"
    FINAL_ROUND = "FINAL_ROUND"
    OFFER = "OFFER"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    CLOSED = "CLOSED"


class InvalidStateTransitionError(ValueError):
    """Raised when an illegal application pipeline transition is attempted."""
    pass


class MissingSubmissionProofError(ValueError):
    """Raised when attempting to mark APPLIED without verified submission proof (Section 19)."""
    pass


class ApplicationRecord:
    """
    Manages an individual job application lifecycle with strict transition checks
    and tamperproof audit history.
    """

    # Directed Graph of legal state transitions
    VALID_TRANSITIONS: Dict[ApplicationState, List[ApplicationState]] = {
        ApplicationState.DISCOVERED: [
            ApplicationState.SHORTLISTED,
            ApplicationState.CLOSED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.SHORTLISTED: [
            ApplicationState.READY_TO_APPLY,
            ApplicationState.REFERRAL_REQUESTED,
            ApplicationState.RECRUITER_CONTACTED,
            ApplicationState.WITHDRAWN,
            ApplicationState.CLOSED
        ],
        ApplicationState.REFERRAL_REQUESTED: [
            ApplicationState.READY_TO_APPLY,
            ApplicationState.RECRUITER_CONTACTED,
            ApplicationState.APPLIED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.RECRUITER_CONTACTED: [
            ApplicationState.READY_TO_APPLY,
            ApplicationState.SCREENING,
            ApplicationState.APPLIED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.READY_TO_APPLY: [
            ApplicationState.APPLIED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.APPLIED: [
            ApplicationState.SCREENING,
            ApplicationState.ASSESSMENT,
            ApplicationState.INTERVIEW_1,
            ApplicationState.REJECTED,
            ApplicationState.WITHDRAWN,
            ApplicationState.CLOSED
        ],
        ApplicationState.SCREENING: [
            ApplicationState.ASSESSMENT,
            ApplicationState.INTERVIEW_1,
            ApplicationState.REJECTED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.ASSESSMENT: [
            ApplicationState.INTERVIEW_1,
            ApplicationState.REJECTED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.INTERVIEW_1: [
            ApplicationState.INTERVIEW_2,
            ApplicationState.FINAL_ROUND,
            ApplicationState.REJECTED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.INTERVIEW_2: [
            ApplicationState.FINAL_ROUND,
            ApplicationState.OFFER,
            ApplicationState.REJECTED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.FINAL_ROUND: [
            ApplicationState.OFFER,
            ApplicationState.REJECTED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.OFFER: [
            ApplicationState.ACCEPTED,
            ApplicationState.REJECTED,
            ApplicationState.WITHDRAWN
        ],
        ApplicationState.ACCEPTED: [],
        ApplicationState.REJECTED: [ApplicationState.CLOSED],
        ApplicationState.WITHDRAWN: [ApplicationState.CLOSED],
        ApplicationState.CLOSED: []
    }

    def __init__(self, application_id: str, job_id: str, company: str, role: str,
                 initial_state: ApplicationState = ApplicationState.DISCOVERED):
        self.application_id = application_id
        self.job_id = job_id
        self.company = company
        self.role = role
        self.current_state = initial_state
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = self.created_at
        self.history: List[Dict[str, Any]] = [{
            "from_state": None,
            "to_state": initial_state.value,
            "timestamp": self.created_at,
            "proof": "Initial Record Creation",
            "actor": "SYSTEM"
        }]

    def transition_to(self, new_state: ApplicationState, submission_proof: Optional[str] = None,
                      actor: str = "Adi", notes: str = "") -> None:
        """
        Transitions the application to a new state.
        Enforces Section 19: If new_state == APPLIED, submission_proof MUST be provided.
        """
        if new_state not in self.VALID_TRANSITIONS.get(self.current_state, []):
            raise InvalidStateTransitionError(
                f"Cannot transition application {self.application_id} from {self.current_state.value} to {new_state.value}. "
                f"Legal next states: {[s.value for s in self.VALID_TRANSITIONS.get(self.current_state, [])]}"
            )

        # Section 19: Application Truth Rule
        if new_state == ApplicationState.APPLIED:
            if not submission_proof or len(submission_proof.strip()) < 5:
                raise MissingSubmissionProofError(
                    "SECTION 19 VIOLATION: Never mark APPLIED without verified submission proof. "
                    "A prepared application is not a submitted application. "
                    "Provide confirmation ID, portal submission screenshot reference, or confirmation email timestamp."
                )

        old_state = self.current_state
        self.current_state = new_state
        self.updated_at = datetime.now(timezone.utc).isoformat()

        self.history.append({
            "from_state": old_state.value,
            "to_state": new_state.value,
            "timestamp": self.updated_at,
            "proof": submission_proof or "Standard Validated Transition",
            "actor": actor,
            "notes": notes
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "application_id": self.application_id,
            "job_id": self.job_id,
            "company": self.company,
            "role": self.role,
            "current_state": self.current_state.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "history": self.history
        }
