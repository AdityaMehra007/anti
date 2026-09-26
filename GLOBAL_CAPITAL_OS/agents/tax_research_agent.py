"""Tax Research Agent - Statutory Reserve & Tax Planning Guardian.

Calculates GST, Advance Tax schedules, export exemptions (LUT),
and protects tax reserves from premature operational spending.
"""

from typing import Any
from datetime import datetime
from .base_agent import BaseFinancialAgent
from ..core.config import settings
from ..core.models import ActionTier
from ..core.database import db


class TaxResearchAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="TaxResearchAgent",
            role_description="Tax specialist calculating Advance Tax, GST export compliance, and statutory reserve requirements."
        )

    def calculate_tax_liability_estimate(self) -> dict[str, Any]:
        """Calculates estimated taxable income and statutory tax reserve requirements."""
        self.check_permission(ActionTier.ANALYZE)

        with db.get_connection() as conn:
            cur = conn.cursor()
            # YTD Gross Revenue
            cur.execute("""
                SELECT COALESCE(SUM(amount_inr), 0.0) FROM transactions
                WHERE category IN ('REVENUE_CUSTOMER', 'REVENUE_PILOT')
                AND status IN ('RECONCILED', 'APPROVED')
                AND timestamp >= strftime('%Y-04-01', 'now')  # Indian FY starts April 1
            """)
            ytd_revenue_inr = float(cur.fetchone()[0])

            # YTD Allowable Business Expenses
            cur.execute("""
                SELECT COALESCE(SUM(amount_inr), 0.0) FROM transactions
                WHERE category IN ('COST_AI', 'COST_INFRA', 'COST_SOFTWARE', 'COST_PAYMENT_FEE', 'COST_PROFESSIONAL')
                AND timestamp >= strftime('%Y-04-01', 'now')
            """)
            ytd_expenses_inr = float(cur.fetchone()[0])

        estimated_net_profit = max(0.0, ytd_revenue_inr - ytd_expenses_inr)
        # Conservative effective corporate/slab rate estimate: 25%
        estimated_income_tax = estimated_net_profit * 0.25

        # Advance Tax Schedule tracking (Indian Income Tax Act)
        # 15% by 15 June, 45% by 15 Sept, 75% by 15 Dec, 100% by 15 March
        now = datetime.utcnow()
        if now.month < 6 or (now.month == 6 and now.day <= 15):
            due_pct = 0.15
            quarter = "Q1 (June 15)"
        elif now.month < 9 or (now.month == 9 and now.day <= 15):
            due_pct = 0.45
            quarter = "Q2 (September 15)"
        elif now.month < 12 or (now.month == 12 and now.day <= 15):
            due_pct = 0.75
            quarter = "Q3 (December 15)"
        else:
            due_pct = 1.00
            quarter = "Q4 (March 15)"

        advance_tax_due = estimated_income_tax * due_pct

        tax_report = {
            "financial_year": f"{now.year}-{now.year + 1}" if now.month >= 4 else f"{now.year - 1}-{now.year}",
            "ytd_revenue_inr": ytd_revenue_inr,
            "ytd_deductible_expenses_inr": ytd_expenses_inr,
            "estimated_net_taxable_profit_inr": estimated_net_profit,
            "estimated_full_year_tax_inr": estimated_income_tax,
            "current_advance_tax_quarter": quarter,
            "cumulative_advance_tax_due_inr": advance_tax_due,
            "gst_treatment": "Export of services is zero-rated under Letter of Undertaking (LUT); Domestic B2B services subject to 18% GST.",
            "statutory_mandate": "NEVER use Tax Reserve balance in ACC-IN-TAX-01 for operational spending."
        }
        self.log_action("TAX_ESTIMATE_CALCULATED", tax_report)
        return tax_report


tax_research_agent = TaxResearchAgent()
