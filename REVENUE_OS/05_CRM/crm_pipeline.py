"""
12-Stage Sales Funnel & CRM Pipeline for REVENUE OS
Adheres strictly to Directives 20, 21, 91, 92.

Funnel Stages:
LEAD -> CONTACT -> RESPONSE -> DISCOVERY -> QUALIFIED -> DEMO ->
PROPOSAL -> NEGOTIATION -> WON -> ONBOARDING -> RETENTION -> EXPANSION
"""

from typing import Any, Dict, List, Optional
import uuid
from REVENUE_OS.database.db import DatabaseManager, get_db

class CRMPipeline:
    """
    Manages deal progression through the 12 funnel stages with probability weightings.
    """
    
    STAGE_PROBABILITIES: Dict[str, float] = {
        "LEAD": 0.05,
        "CONTACT": 0.10,
        "RESPONSE": 0.15,
        "DISCOVERY": 0.25,
        "QUALIFIED": 0.40,
        "DEMO": 0.50,
        "PROPOSAL": 0.60,
        "NEGOTIATION": 0.80,
        "WON": 1.00,
        "ONBOARDING": 1.00,
        "RETENTION": 1.00,
        "EXPANSION": 0.75,
        "LOST": 0.00
    }

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or get_db()

    def create_deal(
        self,
        lead_id: str,
        deal_name: str,
        deal_value_inr: float,
        stage: str = "LEAD",
        currency: str = "INR"
    ) -> str:
        stage = stage.upper()
        if stage not in self.STAGE_PROBABILITIES:
            raise ValueError(f"Invalid stage: {stage}")
            
        prob = self.STAGE_PROBABILITIES[stage]
        expected_rev = deal_value_inr * prob
        deal_id = f"DEAL-{uuid.uuid4().hex[:8].upper()}"

        with self.db.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO deals (
                    id, lead_id, deal_name, stage, deal_value_inr,
                    currency, win_probability, expected_revenue_inr,
                    owner_agent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'SalesAssistant')
                """,
                (deal_id, lead_id, deal_name, stage, deal_value_inr, currency, prob, expected_rev)
            )

        self.db.log_audit(
            agent_name="SalesAssistant",
            action_tier="DRAFT",
            action_name="create_deal",
            details={"deal_id": deal_id, "deal_name": deal_name, "value": deal_value_inr, "stage": stage}
        )
        return deal_id

    def advance_stage(self, deal_id: str, new_stage: str, loss_reason: Optional[str] = None):
        new_stage = new_stage.upper()
        if new_stage not in self.STAGE_PROBABILITIES:
            raise ValueError(f"Invalid stage: {new_stage}")
            
        prob = self.STAGE_PROBABILITIES[new_stage]
        
        with self.db.get_cursor() as cur:
            # Fetch current deal value
            cur.execute("SELECT deal_value_inr FROM deals WHERE id = ?", (deal_id,))
            row = cur.fetchone()
            if not row:
                raise KeyError(f"Deal {deal_id} not found.")
            val = float(row[0])
            expected_rev = val * prob

            cur.execute(
                """
                UPDATE deals
                SET stage = ?, win_probability = ?, expected_revenue_inr = ?,
                    loss_reason = ?, updated_at = datetime('now')
                WHERE id = ?
                """,
                (new_stage, prob, expected_rev, loss_reason, deal_id)
            )

        self.db.log_audit(
            agent_name="SalesAssistant",
            action_tier="DRAFT",
            action_name="advance_stage",
            details={"deal_id": deal_id, "new_stage": new_stage, "win_prob": prob}
        )

    def get_deal(self, deal_id: str) -> Optional[Dict[str, Any]]:
        with self.db.get_cursor() as cur:
            cur.execute("SELECT * FROM deals WHERE id = ?", (deal_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_all_deals(self) -> List[Dict[str, Any]]:
        with self.db.get_cursor() as cur:
            cur.execute("SELECT * FROM deals ORDER BY expected_revenue_inr DESC")
            return [dict(row) for row in cur.fetchall()]

    def get_pipeline_summary(self) -> Dict[str, Any]:
        """
        Directive 21: Sales Dashboard & Pipeline aggregation.
        """
        with self.db.get_cursor() as cur:
            cur.execute(
                """
                SELECT
                    COUNT(*) as total_deals,
                    COALESCE(SUM(deal_value_inr), 0.0) as total_pipeline_value,
                    COALESCE(SUM(expected_revenue_inr), 0.0) as weighted_pipeline_value,
                    COALESCE(SUM(CASE WHEN stage = 'WON' THEN deal_value_inr ELSE 0 END), 0.0) as won_revenue,
                    COALESCE(SUM(CASE WHEN stage = 'WON' THEN 1 ELSE 0 END), 0) as won_count,
                    COALESCE(SUM(CASE WHEN stage = 'LOST' THEN 1 ELSE 0 END), 0) as lost_count
                FROM deals
                """
            )
            row = dict(cur.fetchone())
            
            won = row["won_count"]
            lost = row["lost_count"]
            closed = won + lost
            conversion_rate = round((won / closed * 100.0), 1) if closed > 0 else 0.0

            return {
                "total_deals": row["total_deals"],
                "total_pipeline_value_inr": row["total_pipeline_value"],
                "weighted_pipeline_value_inr": row["weighted_pipeline_value"],
                "won_revenue_inr": row["won_revenue"],
                "won_count": won,
                "lost_count": lost,
                "win_conversion_rate_pct": conversion_rate
            }
