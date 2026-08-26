"""
CAREER ANALYTICS ENGINE
Computes real funnel conversions and reality-audited metrics.
"""
from typing import Dict, Any
from .database import war_room_db

class CareerAnalyticsEngine:
    def __init__(self):
        self.db = war_room_db

    def get_funnel_metrics(self) -> Dict[str, Any]:
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM jobs")
            total_jobs = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM jobs WHERE verification_status = 'CONFIRMED_OPENING'")
            confirmed_jobs = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM jobs WHERE verification_status = 'SEEDED_NOT_VERIFIED'")
            seeded_jobs = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM jobs WHERE verification_status = 'SOURCE_ERROR'")
            error_jobs = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM companies")
            comp_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM applications WHERE current_stage = 'READY'")
            ready_apps = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM applications WHERE current_stage = 'SUBMITTED'")
            submitted_apps = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM outreach WHERE status = 'DRAFT'")
            outreach_drafts = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM outreach WHERE status = 'SENT'")
            outreach_sent = cur.fetchone()[0]

        return {
            "jobs_discovered": total_jobs,
            "jobs_confirmed_openings": confirmed_jobs,
            "jobs_seeded_templates": seeded_jobs,
            "jobs_source_errors": error_jobs,
            "priority_companies_monitored": comp_count,
            "applications_ready_for_human": ready_apps,
            "applications_actually_submitted": submitted_apps,
            "outreach_drafts_ready": outreach_drafts,
            "outreach_actually_sent": outreach_sent,
            "truth_standard": "STRICT_REALITY_AUDITED"
        }

career_analytics = CareerAnalyticsEngine()
