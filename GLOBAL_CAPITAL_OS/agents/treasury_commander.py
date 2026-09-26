"""Treasury Commander - Liquidity & Multi-Currency Treasury Lead.

Responsible for the legitimate bank account map, multi-currency balances,
statutory tax buffer segregation, and capital liquidity enforcement.
"""

from typing import Any
from datetime import datetime
from .base_agent import BaseFinancialAgent
from ..core.config import settings
from ..core.models import ActionTier, CurrencyCode
from ..core.database import db


class TreasuryCommander(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="TreasuryCommander",
            role_description="Treasury manager maintaining liquidity buffers, multi-currency accounts, and statutory tax segregation."
        )

    def get_treasury_map(self) -> dict[str, Any]:
        """Returns the full balances and health of all legitimate bank accounts."""
        self.check_permission(ActionTier.READ)

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, institution, account_name, account_number_masked,
                       currency, category, balance, balance_inr, purpose
                FROM bank_accounts WHERE is_active = 1
                ORDER BY category ASC
            """)
            accounts = [dict(r) for r in cur.fetchall()]

        total_inr_value = sum(a["balance_inr"] for a in accounts)
        by_category = {}
        for a in accounts:
            cat = a["category"]
            by_category[cat] = by_category.get(cat, 0.0) + a["balance_inr"]

        treasury_state = {
            "total_treasury_inr": total_inr_value,
            "category_breakdown_inr": by_category,
            "accounts": accounts,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.log_action("TREASURY_MAP_RETRIEVED", treasury_state)
        return treasury_state

    def verify_tax_reserves(self) -> dict[str, Any]:
        """Audits tax reserves to ensure tax money is never mixed with operating or growth cash."""
        self.check_permission(ActionTier.ANALYZE)

        with db.get_connection() as conn:
            cur = conn.cursor()
            # Calculate total cumulative revenue in INR
            cur.execute("""
                SELECT COALESCE(SUM(amount_inr), 0.0) FROM transactions
                WHERE category IN ('REVENUE_CUSTOMER', 'REVENUE_PILOT') AND status = 'RECONCILED'
            """)
            total_rev_inr = float(cur.fetchone()[0])
            expected_tax_reserve = total_rev_inr * settings.DEFAULT_TAX_RESERVE_PCT

            # Actual balance in Tax Reserve account
            cur.execute("SELECT balance_inr FROM bank_accounts WHERE id = 'ACC-IN-TAX-01'")
            row = cur.fetchone()
            actual_tax_reserve = float(row[0]) if row else 0.0

        is_adequately_funded = actual_tax_reserve >= expected_tax_reserve
        report = {
            "total_revenue_inr": total_rev_inr,
            "expected_tax_reserve_inr": expected_tax_reserve,
            "actual_tax_reserve_inr": actual_tax_reserve,
            "is_adequately_funded": is_adequately_funded,
            "variance_inr": actual_tax_reserve - expected_tax_reserve,
            "recommendation": "TAX RESERVE HEALTHY" if is_adequately_funded else "ACTION REQUIRED: Transfer variance into ACC-IN-TAX-01."
        }
        self.log_action("TAX_RESERVES_VERIFIED", report)
        return report


treasury_commander = TreasuryCommander()
