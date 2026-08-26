"""
APEX Security Policy Engine & Autonomy Governance (A0 to A5)
A0: Observe | A1: Recommend | A2: Reversible Local | A3: Approved Workflows | A4: Supervised External | A5: High-Impact
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

AUTONOMY_LEVELS = {
    "A0": {"rank": 0, "desc": "Observe only, no state modifications"},
    "A1": {"rank": 1, "desc": "Recommend actions, generate proposals"},
    "A2": {"rank": 2, "desc": "Execute reversible local actions (read files, run tests)"},
    "A3": {"rank": 3, "desc": "Execute approved automated multi-step workflows"},
    "A4": {"rank": 4, "desc": "Supervised external interactions (API calls, web queries)"},
    "A5": {"rank": 5, "desc": "Restricted high-impact actions (financial, infrastructure changes)"}
}

class ApexSecurityPolicy:
    def __init__(self, default_autonomy: str = "A3"):
        self.default_autonomy = default_autonomy
        self.blocked_patterns = [
            "rm -rf /", "DROP DATABASE", "format c:", "del /f /s /q c:\\",
            "curl -X DELETE", "shutdown /s"
        ]
        self.sensitive_tools = {"financial_transfer", "delete_production_db", "modify_iam_root"}

    def is_action_permitted(self, agent_autonomy: str, required_autonomy: str, action_command: str = "") -> Dict[str, Any]:
        agent_rank = AUTONOMY_LEVELS.get(agent_autonomy, {"rank": 2})["rank"]
        required_rank = AUTONOMY_LEVELS.get(required_autonomy, {"rank": 3})["rank"]

        # Check dangerous patterns
        for bad in self.blocked_patterns:
            if bad in action_command:
                return {
                    "permitted": False,
                    "reason": f"Action contains strictly forbidden destructive pattern: '{bad}'",
                    "severity": "CRITICAL"
                }

        # Check autonomy sufficiency
        if agent_rank < required_rank:
            return {
                "permitted": False,
                "reason": f"Agent autonomy '{agent_autonomy}' is lower than required '{required_autonomy}'. Approval required.",
                "severity": "WARNING",
                "requires_approval": True
            }

        return {"permitted": True, "reason": "Policy check passed.", "severity": "INFO"}
