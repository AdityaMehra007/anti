"""Founder Chief of Staff - Executive Decision Synthesizer.

Compresses intelligence from all 16 specialized agents into:
1. Daily CEO/CFO Brief
2. Top 3 High-Leverage Strategic Actions
3. Founder Approval Queue (Consequential Action Decision Cards)
Enforces: The founder handles judgment, relationships, and approvals;
the system handles monitoring, calculation, simulation, and preparation.
"""

from typing import Any, Optional
from datetime import datetime
from .base_agent import BaseFinancialAgent
from ..core.config import settings
from ..core.models import ActionTier, ApprovalStatus
from ..core.database import db
from .capital_commander import capital_commander
from .revenue_commander import revenue_commander
from .treasury_commander import treasury_commander
from .risk_agent import risk_agent
from .audit_agent import audit_agent


class FounderChiefOfStaff(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            agent_name="FounderChiefOfStaff",
            role_description="Executive gatekeeper synthesizing multi-agent intelligence into clear, concise founder decisions."
        )

    def generate_daily_brief(self) -> dict[str, Any]:
        """Synthesizes the complete Daily CEO/CFO Morning Brief."""
        self.check_permission(ActionTier.READ)

        posture = capital_commander.get_master_financial_posture()
        pipeline = revenue_commander.get_pipeline_summary()
        treasury = treasury_commander.get_treasury_map()
        risk_summary = risk_agent.run_stress_scenarios()
        audit_res = audit_agent.reconcile_ledger_and_bank()

        top_3_actions = [
            "1. Dispatch Experiment #1 outbound campaign to 10 priority US/UK B2B leads (Elevate/Upwork proof points).",
            "2. Review and confirm GST LUT (Letter of Undertaking) filing status for FY26-27 to maintain 0% IGST export.",
            "3. Verify and safeguard the ₹9,018.00 statutory tax reserve in ACC-IN-TAX-01 against operating spend."
        ]

        brief = {
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "founder": settings.FOUNDER_NAME,
            "system_codename": settings.CODENAME,
            "financial_summary": {
                "total_cash_inr": posture["total_cash_inr"],
                "liquid_investments_inr": posture["liquid_assets_inr"],
                "monthly_burn_inr": posture["monthly_burn_inr"],
                "runway_months": posture["runway_months"],
                "total_debt_inr": posture["total_debt_inr"],
                "revenue_mtd_inr": posture["revenue_mtd_inr"],
                "profit_mtd_inr": posture["profit_mtd_inr"],
            },
            "sales_pipeline": {
                "active_pipeline_value_inr": posture["pipeline_value_inr"],
                "new_leads_ready": pipeline["new_leads_uncontacted"],
                "active_deals_count": posture["active_deals_count"]
            },
            "risk_and_solvency": {
                "liquidity_score": risk_summary["liquidity_score"],
                "solvency_score": risk_summary["solvency_score"],
                "emergency_reserve_met": posture["emergency_reserve_met"]
            },
            "reconciliation_status": audit_res["reconciliation_status"],
            "pending_approvals_count": posture["pending_approvals_count"],
            "top_3_actions": top_3_actions,
            "core_directive": "WHAT IS THE HIGHEST EXPECTED-RISK-ADJUSTED-VALUE ACTION WE CAN TAKE TODAY?"
        }
        self.log_action("DAILY_BRIEF_GENERATED", brief)
        return brief

    def get_pending_approvals(self) -> list[dict[str, Any]]:
        """Returns all decision-ready Money Approval Cards pending human Founder action."""
        self.check_permission(ActionTier.READ)

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, requester_agent, action_type, amount, currency, amount_inr,
                       source_account, destination, purpose, expected_benefit, worst_case_loss,
                       legal_status, tax_considerations, risk_level, recommendation, alternatives,
                       status, created_at
                FROM approvals
                WHERE status = 'PENDING'
                ORDER BY created_at ASC
            """)
            approvals = [dict(r) for r in cur.fetchall()]

        return approvals

    def resolve_approval(self, approval_id: str, decision: str, notes: Optional[str] = None) -> dict[str, Any]:
        """Records Founder decision on a Money Approval Card (APPROVE, REJECT, SIMULATE, DELAY)."""
        valid_decisions = ["APPROVE", "REJECT", "SIMULATE", "DELAY", "RESEARCH_MORE"]
        if decision.upper() not in valid_decisions:
            raise ValueError(f"Decision '{decision}' is not recognized. Must be one of {valid_decisions}.")

        new_status = "APPROVED" if decision.upper() == "APPROVE" else "REJECTED"

        with db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM approvals WHERE id = ?", (approval_id,))
            approval = cur.fetchone()
            if not approval:
                raise ValueError(f"Approval Card '{approval_id}' not found.")

            cur.execute("""
                UPDATE approvals
                SET status = ?, decision_notes = ?, resolved_at = datetime('now')
                WHERE id = ?
            """, (new_status, notes or f"Decided by {settings.FOUNDER_NAME}: {decision}", approval_id))
            conn.commit()

        event = {
            "approval_id": approval_id,
            "decision": decision.upper(),
            "status": new_status,
            "resolved_by": settings.FOUNDER_NAME,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.log_action("APPROVAL_RESOLVED_BY_FOUNDER", event)
        return event


founder_chief_of_staff = FounderChiefOfStaff()
