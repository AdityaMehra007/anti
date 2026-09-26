import os, time
from datetime import datetime
from database import SovereignDB

class SovereignObservability:
    '''Telemetry, Metrics, Token & Cost Estimation Engine.'''
    def __init__(self, db=None):
        if isinstance(db, str):
            self.log_file = db
            self.db = SovereignDB()
        else:
            self.db = db or SovereignDB()

    def record_telemetry(self, task_id, agent_id, duration, estimated_tokens=100, cost_per_1k_tokens=0.0015):
        cost = (estimated_tokens / 1000.0) * cost_per_1k_tokens
        now = datetime.now().isoformat()

        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO telemetry (task_id, agent_id, duration_seconds, tokens_estimated, cost_estimated_usd, timestamp) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (task_id, agent_id, duration, estimated_tokens, cost, now)
            )
            conn.commit()

    def log_event(self, agent_id, task_id, action, status, duration_ms=0, metadata=None):
        duration_sec = (duration_ms / 1000.0) if duration_ms > 10 else duration_ms
        self.record_telemetry(task_id, agent_id, duration_sec)

    def get_summary_metrics(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            task_stats = cursor.execute("SELECT status, count(*) as count FROM tasks GROUP BY status").fetchall()
            agent_count = cursor.execute("SELECT count(*) FROM agents").fetchone()[0]
            memory_count = cursor.execute("SELECT count(*) FROM memories").fetchone()[0]
            total_cost = cursor.execute("SELECT sum(cost_estimated_usd) FROM telemetry").fetchone()[0] or 0.0
            
            return {
                "tasks_by_status": {dict(r)['status']: dict(r)['count'] for r in task_stats},
                "total_agents": agent_count,
                "total_memories": memory_count,
                "total_cost_usd": round(total_cost, 4)
            }

ObservabilityHub = SovereignObservability
