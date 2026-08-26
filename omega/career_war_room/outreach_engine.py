"""
RECRUITER OUTREACH ENGINE
Drafts highly tailored, non-spam recruiter & hiring manager InMails and emails.
State Tracking: DRAFT, APPROVED, SENT, DELIVERED, REPLIED.
External sending strictly requires explicit human approval.
"""
import time
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
from .database import war_room_db

class OutreachStatus(str, Enum):
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    REPLIED = "REPLIED"

class OutreachEngine:
    def __init__(self):
        self.db = war_room_db
        self._seed_drafts()

    def _seed_drafts(self):
        drafts = [
            {
                "outreach_id": "OUT-AMZN-01",
                "application_id": "APP-JOB-AMZN-001",
                "company_name": "Amazon Global Operations",
                "target_person": "Senior Talent Acquisition Specialist - Operations & Compliance",
                "channel": "LINKEDIN",
                "subject": "Inquiry: Global Trade Compliance Analyst Requisition (Bengaluru Hub)",
                "body_text": "Hi [Name], I noticed Amazon's expanding Global Trade Compliance operations in Bengaluru. With a BBA in International Business and hands-on expertise in HS tariff classification, Incoterms 2020, and cross-border trade modeling, I have tailored my background to support Amazon's transportation compliance workflows. I would welcome 5 minutes to share how my international trade background directly aligns with your team's current goals. Best regards, Aditya Mehra."
            },
            {
                "outreach_id": "OUT-MAERSK-02",
                "application_id": "APP-JOB-MAERSK-002",
                "company_name": "A.P. Moller - Maersk",
                "target_person": "Talent Acquisition Lead - Ocean & Logistics Hub",
                "channel": "LINKEDIN",
                "subject": "Connecting regarding International Logistics Operations at RMZ EcoWorld",
                "body_text": "Hi [Name], I have been following Maersk's integrated logistics expansion in Bengaluru. Having focused my BBA thesis on cross-border multimodal freight optimization and customs documentation workflows, I admire Maersk's customer-centric supply chain vision. I've prepared a comprehensive analysis on export-import logistics efficiency and would value the opportunity to connect. Regards, Aditya Mehra."
            },
            {
                "outreach_id": "OUT-TGT-03",
                "application_id": "APP-JOB-TGT-004",
                "company_name": "Target in India",
                "target_person": "Lead Recruiter - Supply Chain & Inventory GCC",
                "channel": "EMAIL",
                "subject": "Aditya Mehra - BBA International Business | Inventory Operations & Global Trade",
                "body_text": "Dear [Name], Target in India's inventory planning excellence at Manyata Tech Park is a benchmark for global retail supply chains. Bringing formal BBA International Business training and analytical grounding in vendor logistics and supply chain optimization, I have assembled a tailored STAR portfolio demonstrating rapid operational execution. I would appreciate the opportunity to discuss early-career opportunities on your team. Sincerely, Aditya Mehra."
            }
        ]

        with self.db.get_connection() as conn:
            cur = conn.cursor()
            for d in drafts:
                cur.execute("""
                INSERT OR REPLACE INTO outreach (
                    outreach_id, application_id, contact_id, company_name, target_person,
                    channel, subject, body_text, status, dispatch_authorized,
                    approved_by, sent_at, reply_received_at, source, verification_status,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    d["outreach_id"], d["application_id"], None, d["company_name"], d["target_person"],
                    d["channel"], d["subject"], d["body_text"], OutreachStatus.DRAFT.value, 0,
                    None, None, None, "OMEGA Recruiter Engine", "VERIFIED",
                    time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                ))
            conn.commit()

    def list_outreach(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            if status:
                cur.execute("SELECT * FROM outreach WHERE status = ?", (status,))
            else:
                cur.execute("SELECT * FROM outreach")
            return [dict(r) for r in cur.fetchall()]

    def approve_outreach(self, outreach_id: str, approver: str = "User") -> Dict[str, Any]:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
            UPDATE outreach SET
                status = 'APPROVED',
                dispatch_authorized = 1,
                approved_by = ?,
                updated_at = ?
            WHERE outreach_id = ?
            """, (approver, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), outreach_id))
            conn.commit()
        return {"success": True, "outreach_id": outreach_id, "status": "APPROVED"}

outreach_engine = OutreachEngine()
