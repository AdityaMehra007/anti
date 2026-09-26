"""FX Agent - Currency Risk & Global Conversion Specialist.

Monitors foreign exchange exposure, conversion costs, and multi-currency balances.
Enforces strictly non-speculative FX policies.
"""

from typing import Any
from .base_agent import BaseFinancialAgent
from ..core.config import settings
from ..core.models import ActionTier
from ..core.database import db


class FXAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="FXAgent",
            role_description="Multi-currency FX specialist managing trade conversion costs and exposure hedging without speculation."
        )

    def get_fx_exposure(self) -> dict[str, Any]:
        """Calculates foreign currency exposure and INR equivalence across all accounts."""
        self.check_permission(ActionTier.READ)

        rates = settings.DEFAULT_FX_RATES
        exposures = {}
        total_foreign_inr = 0.0

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT currency, SUM(balance) as total_bal, SUM(balance_inr) as total_inr
                FROM bank_accounts
                WHERE is_active = 1 AND currency != 'INR'
                GROUP BY currency
            """)
            for row in cur.fetchall():
                curr = row["currency"]
                bal = row["total_bal"]
                inr_val = row["total_inr"]
                exposures[curr] = {
                    "balance": bal,
                    "inr_value": inr_val,
                    "spot_rate": rates.get(curr, 1.0),
                    "estimated_conversion_spread_pct": 0.45,  # Typical competitive rate on Wise
                    "net_realizable_inr": inr_val * (1.0 - 0.0045)
                }
                total_foreign_inr += inr_val

        summary = {
            "total_foreign_exposure_inr": total_foreign_inr,
            "currency_breakdown": exposures,
            "speculation_guard": "STRICTLY NON-SPECULATIVE: FX held solely for trade settlement and export earnings.",
            "recommendation": "OPTIMAL CONVERSION: Keep USD/EUR earnings in export vault until required, then convert via Authorized Dealer / Wise with e-FIRC."
        }
        self.log_action("FX_EXPOSURE_EVALUATED", summary)
        return summary


fx_agent = FXAgent()
