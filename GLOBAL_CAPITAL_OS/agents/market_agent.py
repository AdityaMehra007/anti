"""Market Agent - Demand Signal & Industry Intelligence Monitor.

Tracks executive hiring surges, Series A/B funding rounds, technology migrations,
and B2B buyer intent triggers to fuel the sales outreach pipeline.
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.models import ActionTier
from ..core.database import db


class MarketAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="MarketAgent",
            role_description="Market intelligence monitor scanning buying triggers, competitor shifts, and commercial demand trends."
        )

    def scan_buying_triggers(self) -> dict[str, Any]:
        """Identifies high-propensity buying signals from enriched leads database."""
        self.check_permission(ActionTier.READ)

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT company_name, contact_name, contact_title, location, buying_trigger, lead_score
                FROM leads
                WHERE lead_score = 'Hot'
                ORDER BY created_at DESC LIMIT 5
            """)
            hot_leads = [dict(r) for r in cur.fetchall()]

        signals = {
            "active_buying_signals_count": len(hot_leads),
            "priority_targets": hot_leads,
            "macro_theme": "Mid-market B2B SaaS and agency founders actively seeking qualified SDR pipeline and outbound intelligence without hiring high-overhead in-house headcount."
        }
        self.log_action("MARKET_SIGNALS_SCANNED", signals)
        return signals


market_agent = MarketAgent()
