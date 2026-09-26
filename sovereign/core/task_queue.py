import os, uuid, json
from datetime import datetime
from database import SovereignDB

class TaskQueue:
    '''DAG-Based Task Decomposition, Priority & Execution Queue.'''
    def __init__(self, db=None):
        self.db = db or SovereignDB()

    def create_task(self, project_id, title, assigned_agent=None, priority="MEDIUM", parent_task_id=None, input_data=None):
        task_id = f"TSK-{uuid.uuid4().hex[:8]}"
        now = datetime.now().isoformat()
        inp_str = json.dumps(input_data) if input_data else None

        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO tasks (id, project_id, parent_task_id, title, assigned_agent, priority, status, input_data, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, 'PENDING', ?, ?)",
                (task_id, project_id, parent_task_id, title, assigned_agent, priority, inp_str, now)
            )
            conn.commit()
        return task_id

    def update_status(self, task_id, status, output_data=None, error=None):
        now = datetime.now().isoformat()
        out_str = json.dumps(output_data) if output_data else None

        with self.db.get_connection() as conn:
            conn.execute(
                "UPDATE tasks SET status = ?, output_data = ?, error = ?, completed_at = ? WHERE id = ?",
                (status, out_str, error, now if status in ['COMPLETED', 'FAILED'] else None, task_id)
            )
            conn.commit()

    def get_pending_tasks(self, limit=10):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM tasks WHERE status = 'PENDING' ORDER BY created_at ASC LIMIT ?", (limit,)).fetchall()
            return [dict(r) for r in rows]
