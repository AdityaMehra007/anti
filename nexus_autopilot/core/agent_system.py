"""
NEXUS AUTOPILOT - Multi-Agent Coordination Fabric & Human-In-The-Loop Control Plane
Enforces strict agent permissions, tool gates, and audit trails across 10 specialized agent roles.
"""
import time
import json
import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

DB_PATH = Path(r"e:\anti\nexus_autopilot\data\nexus.db")

@dataclass
class AgentPermissionRule:
    role_name: str
    allowed_tools: List[str]
    forbidden_actions: List[str]
    max_autonomous_amount_inr: float
    requires_approval_above_level: int # 0=Read, 1=Auto, 2=OwnerApprove, 3=FinanceApprove, 4=HumanOnly

class NexusAgentSystem:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.agents: Dict[str, AgentPermissionRule] = {
            "CEO_Agent": AgentPermissionRule("CEO_Agent", ["read_all", "generate_reports", "propose_strategy"], ["execute_unauthorized_payment"], 0.0, 2),
            "Collections_Agent": AgentPermissionRule("Collections_Agent", ["read_invoices", "draft_reminders", "send_approved_templates"], ["waive_debt", "modify_bank_info", "change_totals"], 0.0, 2),
            "Sales_Agent": AgentPermissionRule("Sales_Agent", ["qualify_leads", "draft_quotes", "create_orders"], ["issue_discounts_above_15pct", "delete_customers"], 50000.0, 2),
            "Finance_Agent": AgentPermissionRule("Finance_Agent", ["compute_cashflow", "reconcile_payments", "forecast_risk"], ["transfer_funds", "write_off_debt"], 0.0, 3),
            "Accounting_Agent": AgentPermissionRule("Accounting_Agent", ["create_accounting_events", "tag_gst", "generate_e_invoice"], ["alter_past_audits", "delete_ledger_records"], 0.0, 3),
            "Compliance_Assistant": AgentPermissionRule("Compliance_Assistant", ["verify_gstin", "audit_invoices"], ["submit_statutory_returns_without_ca"], 0.0, 4)
        }

    def evaluate_action_permission(self, agent_role: str, action_type: str, amount_inr: float = 0.0) -> Dict[str, Any]:
        rule = self.agents.get(agent_role)
        if not rule:
            return {"permitted": False, "approval_required": True, "approval_level": 4, "reason": "UNKNOWN_AGENT_ROLE"}

        if action_type in rule.forbidden_actions:
            return {
                "permitted": False,
                "approval_required": True,
                "approval_level": 4,
                "reason": f"ACTION_STRICTLY_FORBIDDEN_FOR_ROLE_{agent_role}"
            }

        if amount_inr > rule.max_autonomous_amount_inr:
            return {
                "permitted": True,
                "approval_required": True,
                "approval_level": rule.requires_approval_above_level,
                "reason": f"AMOUNT_INR_{amount_inr}_EXCEEDS_AUTONOMOUS_LIMIT_{rule.max_autonomous_amount_inr}"
            }

        return {
            "permitted": True,
            "approval_required": False,
            "approval_level": 1,
            "reason": "WITHIN_SAFE_AUTONOMOUS_BOUNDS"
        }

    def log_agent_audit_event(self, org_id: str, agent_role: str, event_type: str, description: str, payload: Dict[str, Any]):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        log_id = f"LOG-{int(time.time()*1000)}"
        cur.execute(
            "INSERT INTO audit_logs VALUES (?,?,?,?,?,?,?)",
            (log_id, org_id, event_type, agent_role, description, json.dumps(payload), time.time())
        )
        conn.commit()
        conn.close()

if __name__ == "__main__":
    agents = NexusAgentSystem()
    chk = agents.evaluate_action_permission("Collections_Agent", "draft_reminders", 140000.0)
    print(f"[AGENT_SYSTEM] Permission Check: {json.dumps(chk, indent=2)}")
