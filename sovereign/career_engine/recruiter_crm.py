"""
ADI CAREER OS — RECRUITER CRM & OUTREACH ENGINE (Sections 23, 24)
Manages recruiter relations, prevents duplicate outreach, and generates concise, truthful messages.
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

@dataclass
class RecruiterContact:
    contact_id: str
    full_name: str
    company: str
    title: str
    channel: str = "LinkedIn InMail"   # LinkedIn InMail, Email, Warm Referral
    relationship: str = "1st Connection" # 1st Connection, 2nd Connection, Alumni, Cold
    email: Optional[str] = None
    profile_url: Optional[str] = None
    is_decision_maker: bool = False
    referral_potential: str = "HIGH"    # HIGH, MEDIUM, LOW
    last_contact_date: Optional[str] = None
    next_action_due: Optional[str] = None
    status: str = "UNCONTACTED"        # UNCONTACTED, CONTACTED, REPLIED, SCHEDULED, DORMANT
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RecruiterCRM:
    """Tracks outreach and guarantees zero duplicate spam (Section 23)."""

    def __init__(self, cooldown_days: int = 14):
        self.contacts: Dict[str, RecruiterContact] = {}
        self.cooldown_days = cooldown_days

    def add_contact(self, contact: RecruiterContact) -> None:
        self.contacts[contact.contact_id] = contact

    def can_contact(self, contact_id: str) -> Dict[str, Any]:
        """Verifies cooldown window to avoid spamming the same individual."""
        contact = self.contacts.get(contact_id)
        if not contact:
            return {"can_contact": True, "reason": "New contact"}
        if not contact.last_contact_date:
            return {"can_contact": True, "reason": "No previous contact recorded"}

        try:
            last_date = datetime.strptime(contact.last_contact_date[:10], "%Y-%m-%d")
            elapsed = (datetime.now() - last_date).days
            if elapsed < self.cooldown_days:
                return {
                    "can_contact": False,
                    "reason": f"Active cooldown: Contacted {elapsed} days ago. Must wait {self.cooldown_days - elapsed} more days."
                }
        except Exception:
            pass
        return {"can_contact": True, "reason": "Cooldown period satisfied"}

    def record_outreach(self, contact_id: str, message_type: str, actor: str = "Adi") -> None:
        contact = self.contacts.get(contact_id)
        if not contact:
            return
        now_str = datetime.now(timezone.utc).isoformat()
        contact.last_contact_date = now_str
        contact.status = "CONTACTED"
        contact.next_action_due = (datetime.now(timezone.utc) + timedelta(days=5)).strftime("%Y-%m-%d")
        contact.notes.append(f"[{now_str[:10]}] Dispatched {message_type} via {contact.channel} by {actor}.")


class OutreachEngine:
    """Generates short, professional, contextual, and truthful outreach messages (Section 24)."""

    @staticmethod
    def generate_recruiter_inmail(candidate_name: str, target_company: str, target_role: str,
                                  recruiter_name: str) -> str:
        """Concise InMail for talent acquisition / recruiters."""
        first_name = recruiter_name.split()[0] if recruiter_name else "there"
        return (
            f"Hi {first_name},\n\n"
            f"I came across the {target_role} opening at {target_company} and wanted to reach out directly. "
            f"I have a background in International Business (BBA) from Bengaluru, with hands-on experience in "
            f"process operations, workflow automation, and analytics (Excel, SQL).\n\n"
            f"Given {target_company}'s operational scale, I would welcome the opportunity to discuss how my execution "
            f"background aligns with the team's requirements. Are you open to a brief conversation this week?\n\n"
            f"Best regards,\n"
            f"{candidate_name}"
        )

    @staticmethod
    def generate_referral_request(candidate_name: str, target_company: str, target_role: str,
                                  referrer_name: str, job_id: str = "") -> str:
        """Professional referral request for alumni or 1st-degree connections."""
        first_name = referrer_name.split()[0] if referrer_name else "there"
        req_ref = f" (Req: {job_id})" if job_id else ""
        return (
            f"Hi {first_name},\n\n"
            f"Hope you are doing well! I noticed an opening for {target_role}{req_ref} on the {target_company} career portal. "
            f"My background is in International Business and business operations, focusing on process standardization "
            f"and data analysis.\n\n"
            f"If you feel comfortable, would you be open to submitting an internal referral on my behalf? "
            f"I have my resume tailored and ready for review. Either way, appreciate your time and insights into the team!\n\n"
            f"Warm regards,\n"
            f"{candidate_name}"
        )

    @staticmethod
    def generate_followup_message(candidate_name: str, contact_name: str, company: str,
                                  role: str) -> str:
        """Polite follow-up after 5 business days."""
        first_name = contact_name.split()[0] if contact_name else "there"
        return (
            f"Hi {first_name},\n\n"
            f"Following up briefly regarding my earlier note about the {role} position at {company}. "
            f"I remain very interested in supporting your team's operational goals and would appreciate 5 minutes "
            f"to share how my background fits your current priorities.\n\n"
            f"Thanks again for your consideration,\n"
            f"{candidate_name}"
        )
