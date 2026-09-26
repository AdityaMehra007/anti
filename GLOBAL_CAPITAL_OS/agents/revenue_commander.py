"""Revenue Commander - Revenue Engine Lead for GLOBAL CAPITAL OS.

Responsible for the 500-opportunity funnel, ethical B2B lead intelligence,
12-stage sales CRM progression, pricing strategies, and collecting revenue.
"""

from typing import Any, Optional
from datetime import datetime
from .base_agent import BaseFinancialAgent
from ..core.config import settings
from ..core.models import ActionTier, SalesStage, CurrencyCode, TransactionCategory
from ..core.database import db


class RevenueCommander(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="RevenueCommander",
            role_description="Revenue growth orchestrator overseeing opportunity qualification, outbound sales pipeline, and customer collections."
        )

    def get_pipeline_summary(self) -> dict[str, Any]:
        """Summarizes all active deals across the 12-stage CRM pipeline."""
        self.check_permission(ActionTier.READ)

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT stage, COUNT(*) as count, SUM(deal_value_inr) as total_value, SUM(expected_value_inr) as expected_value
                FROM deals
                GROUP BY stage
            """)
            stages = {r["stage"]: {
                "count": r["count"],
                "total_value_inr": r["total_value"],
                "expected_value_inr": r["expected_value"]
            } for r in cur.fetchall()}

            cur.execute("SELECT COUNT(*) FROM leads WHERE status = 'NEW'")
            new_leads = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*), SUM(amount_inr) FROM transactions
                WHERE category IN ('REVENUE_CUSTOMER', 'REVENUE_PILOT') AND status = 'RECONCILED'
            """)
            won_row = cur.fetchone()
            won_deals_count = won_row[0] or 0
            total_collected_inr = won_row[1] or 0.0

        summary = {
            "new_leads_uncontacted": new_leads,
            "pipeline_stages": stages,
            "won_deals_count": won_deals_count,
            "total_collected_revenue_inr": total_collected_inr,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.log_action("PIPELINE_SUMMARY_GENERATED", summary)
        return summary

    def advance_deal_stage(self, deal_id: str, new_stage: SalesStage, notes: Optional[str] = None) -> dict[str, Any]:
        """Progresses a deal across the 12-stage CRM pipeline and adjusts win probabilities."""
        self.check_permission(ActionTier.RECOMMEND)

        stage_probabilities = {
            SalesStage.LEAD: 0.05,
            SalesStage.CONTACT: 0.10,
            SalesStage.RESPONSE: 0.20,
            SalesStage.DISCOVERY: 0.30,
            SalesStage.QUALIFIED: 0.45,
            SalesStage.DEMO: 0.60,
            SalesStage.PROPOSAL: 0.75,
            SalesStage.NEGOTIATION: 0.85,
            SalesStage.WON: 1.00,
            SalesStage.ONBOARDING: 1.00,
            SalesStage.RETENTION: 1.00,
            SalesStage.EXPANSION: 0.90,
        }
        prob = stage_probabilities.get(new_stage, 0.1)

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT deal_value_inr, deal_name FROM deals WHERE id = ?", (deal_id,))
            deal = cur.fetchone()
            if not deal:
                raise ValueError(f"Deal '{deal_id}' not found.")

            val_inr = deal["deal_value_inr"]
            new_expected = val_inr * prob

            cur.execute("""
                UPDATE deals
                SET stage = ?, win_probability = ?, expected_value_inr = ?, updated_at = datetime('now')
                WHERE id = ?
            """, (new_stage.value, prob, new_expected, deal_id))
            conn.commit()

        event_data = {
            "deal_id": deal_id,
            "deal_name": deal["deal_name"],
            "new_stage": new_stage.value,
            "win_probability": prob,
            "expected_value_inr": new_expected,
            "notes": notes
        }
        self.log_action("DEAL_STAGE_ADVANCED", event_data)
        return event_data

    def record_collected_revenue(
        self,
        client_name: str,
        amount_usd: float,
        amount_inr: float,
        service_description: str,
        source_account_id: str = "ACC-GL-WISE-01"
    ) -> dict[str, Any]:
        """Records a collected customer payment, automatically sweeps tax reserves, and logs audit."""
        self.check_permission(ActionTier.RECOMMEND, amount_inr)

        tax_reserve = amount_inr * settings.DEFAULT_TAX_RESERVE_PCT
        tx_id = f"TX-REV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        with db.get_connection() as conn:
            cur = conn.cursor()
            # 1. Insert transaction
            cur.execute("""
                INSERT INTO transactions (
                    id, timestamp, source_account_id, destination_account_id,
                    counterparty_name, amount, currency, amount_inr, category,
                    description, tax_reserve_amount_inr, status
                ) VALUES (?, datetime('now'), ?, 'ACC-IN-OPS-01', ?, ?, ?, ?, 'REVENUE_CUSTOMER', ?, ?, 'RECONCILED')
            """, (
                tx_id, source_account_id, client_name,
                amount_usd if amount_usd > 0 else amount_inr,
                "USD" if amount_usd > 0 else "INR",
                amount_inr, service_description, tax_reserve
            ))

            # 2. Update Operating Account balance
            cur.execute("UPDATE bank_accounts SET balance = balance + ?, balance_inr = balance_inr + ? WHERE id = 'ACC-IN-OPS-01'", (amount_inr, amount_inr))
            # 3. Update Tax Reserve Account
            cur.execute("UPDATE bank_accounts SET balance = balance + ?, balance_inr = balance_inr + ? WHERE id = 'ACC-IN-TAX-01'", (tax_reserve, tax_reserve))
            conn.commit()

        record = {
            "transaction_id": tx_id,
            "client": client_name,
            "amount_inr": amount_inr,
            "amount_usd": amount_usd,
            "tax_reserve_held_inr": tax_reserve,
            "status": "RECONCILED_AND_PROTECTED"
        }
        self.log_action("REVENUE_COLLECTED_AND_TAX_RESERVED", record)
        return record


revenue_commander = RevenueCommander()
