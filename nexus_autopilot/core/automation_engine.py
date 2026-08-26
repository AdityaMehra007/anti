"""
NEXUS AUTOPILOT - No-Code Workflow Automation Engine
Executes automated business triggers (Invoice Created, Payment Received, Overdue, Document Uploaded)
with conditional logic (IF, THEN, ELSE, WAIT, ESCALATE, APPROVE).
"""
import time
import json
from typing import Dict, Any, List, Optional

class AutomationEngine:
    def __init__(self):
        self.active_rules = [
            {
                "rule_id": "RULE-COL-001",
                "name": "Auto-Draft Collections on Overdue Invoices",
                "trigger": "INVOICE_OVERDUE",
                "condition": {"days_overdue_gte": 5, "min_amount_inr": 25000.0},
                "action": "DRAFT_WHATSAPP_REMINDER",
                "requires_approval": True,
                "approval_level": 2
            },
            {
                "rule_id": "RULE-PAY-002",
                "name": "Instant WhatsApp Thank You & Receipt on Payment",
                "trigger": "PAYMENT_RECEIVED",
                "condition": {"status": "SUCCESS"},
                "action": "SEND_WHATSAPP_RECEIPT",
                "requires_approval": False,
                "approval_level": 1
            },
            {
                "rule_id": "RULE-RISK-003",
                "name": "CEO Cash Risk Alert on Stress Scenario",
                "trigger": "CASH_FORECAST_DIP",
                "condition": {"projected_runway_days_lt": 20},
                "action": "ESCALATE_TO_FOUNDER",
                "requires_approval": False,
                "approval_level": 1
            }
        ]

    def evaluate_trigger(self, trigger_event: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        executed_actions = []
        for rule in self.active_rules:
            if rule["trigger"] == trigger_event:
                # Condition matching
                matched = True
                for cond_key, cond_val in rule["condition"].items():
                    if cond_key == "days_overdue_gte":
                        if payload.get("days_overdue", 0) < cond_val:
                            matched = False
                    elif cond_key == "min_amount_inr":
                        if payload.get("amount", 0.0) < cond_val:
                            matched = False
                    elif cond_key == "status":
                        if payload.get("status") != cond_val:
                            matched = False
                
                if matched:
                    executed_actions.append({
                        "rule_id": rule["rule_id"],
                        "rule_name": rule["name"],
                        "action": rule["action"],
                        "requires_approval": rule["requires_approval"],
                        "approval_level": rule["approval_level"],
                        "status": "AWAITING_OWNER_APPROVAL" if rule["requires_approval"] else "AUTO_EXECUTED",
                        "timestamp": time.time()
                    })
        return executed_actions

if __name__ == "__main__":
    auto = AutomationEngine()
    test_res = auto.evaluate_trigger("INVOICE_OVERDUE", {"days_overdue": 10, "amount": 140000.0})
    print("[AUTOMATION TEST]:", json.dumps(test_res, indent=2))
