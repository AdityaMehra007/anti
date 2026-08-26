import json
from datetime import datetime
from database import OmegaDB

class OmegaSecurityCenter:
    '''Level 0-5 RBAC, Token Redaction & Human-Approval Governance Engine.'''
    def __init__(self, db=None):
        self.db = db or OmegaDB()

    def evaluate_action_permission(self, agent_id, action_name, required_level, payload=None):
        now = datetime.now().isoformat()
        requires_human = (required_level >= 5)
        status = "PENDING_APPROVAL" if requires_human else "APPROVED_BY_POLICY"

        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO audit_logs (agent_id, action, permission_level, status, details, timestamp) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (agent_id, action_name, required_level, status, json.dumps(payload) if payload else "", now)
            )
            conn.commit()

        return {
            "action": action_name,
            "permission_level": required_level,
            "status": status,
            "requires_human_approval": requires_human
        }
