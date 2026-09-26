"""
Sovereign Core — Task Engine & State Machine
Tracks task progression through formal states:
DISCOVERED -> PLANNED -> READY -> RUNNING -> REVIEW -> VERIFIED -> COMPLETE
"""

import time
import json
import uuid
from typing import Dict, List, Any, Optional

class TaskState:
    DISCOVERED = "DISCOVERED"
    PLANNED = "PLANNED"
    READY = "READY"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    REVIEW = "REVIEW"
    VERIFIED = "VERIFIED"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    ESCALATED = "ESCALATED"
    CANCELLED = "CANCELLED"

class Task:
    def __init__(self, objective: str, owner: str, priority_score: float = 5.0, 
                 dependencies: Optional[List[str]] = None, inputs: Optional[Dict[str, Any]] = None,
                 risk_level: str = "LOW", autonomy_level: int = 2):
        self.id = f"TSK-{uuid.uuid4().hex[:8].upper()}"
        self.objective = objective
        self.owner = owner
        self.priority_score = priority_score
        self.dependencies = dependencies or []
        self.inputs = inputs or {}
        self.outputs = {}
        self.status = TaskState.DISCOVERED
        self.risk_level = risk_level
        self.autonomy_level = autonomy_level
        self.verification_proof = None
        self.created_at = time.time()
        self.updated_at = time.time()
        self.execution_log = []

    def transition(self, new_state: str, message: str = ""):
        self.execution_log.append({
            "timestamp": time.time(),
            "from_state": self.status,
            "to_state": new_state,
            "message": message
        })
        self.status = new_state
        self.updated_at = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "objective": self.objective,
            "owner": self.owner,
            "priority_score": self.priority_score,
            "dependencies": self.dependencies,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "status": self.status,
            "risk_level": self.risk_level,
            "autonomy_level": self.autonomy_level,
            "verification_proof": self.verification_proof,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "execution_log": self.execution_log
        }

class TaskEngine:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def create_task(self, objective: str, owner: str, priority: float = 5.0,
                    dependencies: Optional[List[str]] = None, inputs: Optional[Dict[str, Any]] = None,
                    risk_level: str = "LOW", autonomy_level: int = 2) -> Task:
        task = Task(objective, owner, priority, dependencies, inputs, risk_level, autonomy_level)
        self.tasks[task.id] = task
        task.transition(TaskState.PLANNED, "Task planned by Sovereign Core")
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        if status:
            return [t for t in self.tasks.values() if t.status == status]
        return list(self.tasks.values())
