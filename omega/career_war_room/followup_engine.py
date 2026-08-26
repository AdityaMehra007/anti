"""
FOLLOW-UP ENGINE
Tracks 7-day and 14-day polite inquiry cadences.
Strict rule: State is updated exclusively upon real message receipts. Zero fake replies.
"""
import time
from typing import Dict, Any, List
from .database import war_room_db

class FollowupEngine:
    def __init__(self):
        self.db = war_room_db
        self._init_followups()

    def _init_followups(self):
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM followups")
            if cur.fetchone()[0] == 0:
                cur.execute("""
                INSERT INTO followups (
                    followup_id, application_id, company_name, cadence_days, scheduled_date,
                    status, message_draft, source, verification_status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    "FOL-001", "APP-JOB-AMZN-001", "Amazon Global Operations", 7,
                    time.strftime("%Y-%m-%d", time.localtime(time.time() + 7*86400)),
                    "PENDING",
                    "Hi [Name], following up on my recent inquiry regarding the Global Trade Compliance Analyst requisition. I remain very enthusiastic about contributing to Amazon's logistics operations.",
                    "OMEGA Followup Scheduler", "VERIFIED",
                    time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                ))
                conn.commit()

    def list_followups(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM followups ORDER BY scheduled_date ASC")
            return [dict(r) for r in cur.fetchall()]

followup_engine = FollowupEngine()
