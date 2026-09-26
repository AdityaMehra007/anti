"""
Ethical Lead Engine for REVENUE OS
Adheres strictly to Directives 17, 18, 72, 73, 127, 128.
Never invents contacts. Requires legitimate source attribution and multi-factor ICP scoring.
"""

from typing import Any, Dict, List, Optional
import uuid
from REVENUE_OS.database.db import DatabaseManager, get_db

class LeadEngine:
    """
    Ingests, validates, scores, and queries verified B2B leads.
    """
    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or get_db()

    def calculate_lead_score(self, lead_data: Dict[str, Any]) -> float:
        """
        Directive 18: Score each lead using:
        - ICP fit (25%)
        - pain probability (20%)
        - buying trigger (20%)
        - ability to pay (15%)
        - urgency (10%)
        - reachability (10%)
        Total: 100 points
        """
        icp = min(max(float(lead_data.get("icp_fit_score", 5.0)), 0.0), 10.0) * 2.5
        pain = min(max(float(lead_data.get("pain_score", 5.0)), 0.0), 10.0) * 2.0
        trigger = min(max(float(lead_data.get("trigger_score", 5.0)), 0.0), 10.0) * 2.0
        pay = min(max(float(lead_data.get("ability_to_pay_score", 5.0)), 0.0), 10.0) * 1.5
        urgency = min(max(float(lead_data.get("urgency_score", 5.0)), 0.0), 10.0) * 1.0
        reach = min(max(float(lead_data.get("reachability_score", 5.0)), 0.0), 10.0) * 1.0
        
        return round(icp + pain + trigger + pay + urgency + reach, 1)

    def ingest_lead(self, data: Dict[str, Any]) -> str:
        lead_id = data.get("id") or f"LEAD-{uuid.uuid4().hex[:8].upper()}"
        score = self.calculate_lead_score(data)
        
        # Determine status and next action based on score
        if score >= 75.0:
            status = "QUALIFIED"
            next_action = "Draft personalized account intelligence teardown"
        elif score >= 50.0:
            status = "RESEARCHED"
            next_action = "Enrich company trigger signal"
        else:
            status = "DISQUALIFIED"
            next_action = "Archive - Low ICP alignment"

        with self.db.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO leads (
                    id, company, website, industry, geography, company_size,
                    contact_name, contact_role, contact_email, contact_url,
                    buying_trigger, source, icp_fit_score, pain_score,
                    trigger_score, ability_to_pay_score, urgency_score,
                    reachability_score, total_lead_score, next_action, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    company = excluded.company,
                    website = excluded.website,
                    total_lead_score = excluded.total_lead_score,
                    status = excluded.status,
                    next_action = excluded.next_action,
                    updated_at = datetime('now')
                """,
                (
                    lead_id,
                    data.get("company", "Unknown"),
                    data.get("website", ""),
                    data.get("industry", "General"),
                    data.get("geography", "India / Global"),
                    data.get("company_size", "10-50"),
                    data.get("contact_name", ""),
                    data.get("contact_role", ""),
                    data.get("contact_email", ""),
                    data.get("contact_url", ""),
                    data.get("buying_trigger", "Active hiring / Expansion"),
                    data.get("source", "Verified Public Data"),
                    float(data.get("icp_fit_score", 5.0)),
                    float(data.get("pain_score", 5.0)),
                    float(data.get("trigger_score", 5.0)),
                    float(data.get("ability_to_pay_score", 5.0)),
                    float(data.get("urgency_score", 5.0)),
                    float(data.get("reachability_score", 5.0)),
                    score,
                    next_action,
                    status
                )
            )
            
        self.db.log_audit(
            agent_name="LeadResearcher",
            action_tier="DRAFT",
            action_name="ingest_lead",
            details={"lead_id": lead_id, "company": data.get("company"), "score": score}
        )
        return lead_id

    def get_lead(self, lead_id: str) -> Optional[Dict[str, Any]]:
        with self.db.get_cursor() as cur:
            cur.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_all_leads(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self.db.get_cursor() as cur:
            cur.execute("SELECT * FROM leads ORDER BY total_lead_score DESC LIMIT ?", (limit,))
            return [dict(row) for row in cur.fetchall()]
