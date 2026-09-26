import os, json
from datetime import datetime
from database import SovereignDB

class PermissionGuard:
    '''Security Engine Enforcing Permission Levels 0 through 5.'''
    LEVELS = {
        0: "READ_ONLY",
        1: "LOCAL_WORKSPACE_READ_WRITE",
        2: "PROJECT_MODIFICATION",
        3: "TEST_AND_BUILD_EXECUTION",
        4: "STAGING_DEPLOYMENT",
        5: "PRODUCTION_AND_EXTERNAL_CONSEQUENTIAL"
    }

    def __init__(self, db=None):
        self.db = db or SovereignDB()

    def check_and_audit(self, agent_id, action_name, required_level, details=None):
        now = datetime.now().isoformat()
        details_str = json.dumps(details) if details else ""

        # Check if Level 5 requires human approval
        if required_level >= 5:
            status = "PENDING_APPROVAL"
        else:
            status = "APPROVED_BY_POLICY"

        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO audit_logs (agent_id, action, permission_level, status, details, timestamp) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (agent_id, action_name, required_level, status, details_str, now)
            )
            conn.commit()

        return {
            "action": action_name,
            "required_level": required_level,
            "status": status,
            "requires_human_approval": (required_level >= 5)
        }
