import os, json
from datetime import datetime
from database import OmegaDB

class OmegaControlPlane:
    '''Central Brain & Single Source of Truth for Omega System State.'''
    def __init__(self, db=None):
        self.db = db or OmegaDB()

    def get_system_state(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            missions_count = cursor.execute("SELECT count(*) FROM missions").fetchone()[0]
            tasks_by_status = cursor.execute("SELECT status, count(*) FROM tasks GROUP BY status").fetchall()
            agent_count = cursor.execute("SELECT count(*) FROM agents").fetchone()[0]
            memory_count = cursor.execute("SELECT count(*) FROM memories").fetchone()[0]
            pending_approvals = cursor.execute("SELECT count(*) FROM audit_logs WHERE status = 'PENDING_APPROVAL'").fetchone()[0]

            return {
                "system_status": "ONLINE & OPERATIONAL",
                "missions_total": missions_count,
                "tasks_by_status": {r[0]: r[1] for r in tasks_by_status},
                "registered_agents": agent_count,
                "total_memories": memory_count,
                "pending_human_approvals": pending_approvals,
                "timestamp": datetime.now().isoformat()
            }
