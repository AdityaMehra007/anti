"""
Sales Assistant for REVENUE OS
Adheres strictly to Directives 19, 20, 22, 23, 72, 127.
Generates relevant, concise, personalized, useful outbound communications.
Never generates deceptive claims, spam blasts, or fake urgency.
"""

from typing import Any, Dict, Optional
from REVENUE_OS.database.db import DatabaseManager, get_db
from REVENUE_OS.compliance.charter import EthicalCharter

class SalesAssistant:
    """
    Drafts tailored outbound messages and prepares proposal artifacts.
    """
    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or get_db()
        self.charter = EthicalCharter()

    def draft_personalized_outreach(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        contact_name = lead_data.get("contact_name") or "Founder"
        company = lead_data.get("company", "your team")
        trigger = lead_data.get("buying_trigger", "recent growth and hiring initiatives")
        industry = lead_data.get("industry", "B2B")

        subject = f"Pipeline acceleration for {company} / {industry}"
        
        body = (
            f"Hi {contact_name},\n\n"
            f"Noticed {company}'s momentum around {trigger}. Congratulations on the trajectory.\n\n"
            f"As your team scales, manual outbound prospecting often burns 15-20 hours a week of senior leadership "
            f"time or results in generic SDR spam that damages domain deliverability.\n\n"
            f"We built an autonomous B2B sales intelligence engine that continuously detects high-intent buying signals, "
            f"verifies decision-maker data, and prepares highly tailored, value-first pipeline for your team to review in 10 minutes a day.\n\n"
            f"Would it be helpful if I shared a 3-account sample dossier tailored specifically for {company}'s ideal customer profile?\n\n"
            f"Best regards,\n"
            f"Aditya Mehra\n"
            f"Founder, REVENUE OS (Bengaluru, India)\n\n"
            f"---\n"
            f"Opt out / Unsubscribe: Reply 'unsubscribe' to stop receiving updates."
        )

        # Ensure compliance
        self.charter.check_outreach_compliance(
            recipient_email=lead_data.get("contact_email", ""),
            content=body
        )

        draft = {
            "lead_id": lead_data.get("id"),
            "recipient_name": contact_name,
            "recipient_company": company,
            "subject": subject,
            "body": body,
            "requires_approval": False, # Drafting is autonomous
            "status": "DRAFTED"
        }

        self.db.log_audit(
            agent_name="SalesAssistant",
            action_tier="DRAFT",
            action_name="draft_outreach",
            details={"company": company, "subject": subject}
        )

        return draft
