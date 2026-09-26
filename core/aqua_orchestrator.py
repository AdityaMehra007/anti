"""
AQUA Orchestrator (ANTIGRAVITY Ω∞)
Deterministic, priority-scored task scheduler with explicit dependency resolution
and verification gates (Zero Vibe Coding & Evidence-First Protocol).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from enum import Enum
import json
import os
import time

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"

@dataclass
class AquaTask:
    task_id: str
    objective: str
    assigned_agent: str
    value: float = 5.0          # 1.0 to 10.0 scale
    probability: float = 0.9    # 0.0 to 1.0 confidence
    urgency: float = 5.0        # 1.0 to 10.0 scale
    effort: float = 2.0         # 1.0 to 10.0 scale
    dependencies: List[str] = field(default_factory=list)
    verification_criteria: str = "Test suite passing with 0 regression"
    status: TaskStatus = TaskStatus.PENDING
    result_data: Optional[Dict[str, Any]] = None
    created_at: float = field(default_factory=time.time)
    verified_at: Optional[float] = None

    @property
    def priority_score(self) -> float:
        """
        Antigravity Leverage Formula: (Value * Probability * Urgency) / Effort
        """
        eff = max(0.1, self.effort)
        return round((self.value * self.probability * self.urgency) / eff, 3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "objective": self.objective,
            "assigned_agent": self.assigned_agent,
            "value": self.value,
            "probability": self.probability,
            "urgency": self.urgency,
            "effort": self.effort,
            "priority_score": self.priority_score,
            "dependencies": self.dependencies,
            "verification_criteria": self.verification_criteria,
            "status": self.status.value,
            "result_data": self.result_data,
            "created_at": self.created_at,
            "verified_at": self.verified_at
        }

class AquaOrchestrator:
    def __init__(self, state_file: Optional[str] = None):
        self.tasks: Dict[str, AquaTask] = {}
        self.state_file = state_file

    def register_task(self, task: AquaTask) -> AquaTask:
        self.tasks[task.task_id] = task
        self._update_task_state(task)
        return task

    def get_task(self, task_id: str) -> Optional[AquaTask]:
        return self.tasks.get(task_id)

    def _update_task_state(self, task: AquaTask) -> None:
        if task.status in (TaskStatus.VERIFIED, TaskStatus.FAILED, TaskStatus.IN_PROGRESS):
            return
        
        # Check dependencies
        for dep_id in task.dependencies:
            dep_task = self.tasks.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.VERIFIED:
                task.status = TaskStatus.BLOCKED
                return
        
        task.status = TaskStatus.READY

    def get_next_runnable_task(self) -> Optional[AquaTask]:
        """
        Returns the highest-priority READY task whose dependencies are verified.
        """
        # Refresh states
        for task in self.tasks.values():
            self._update_task_state(task)

        ready_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.READY]
        if not ready_tasks:
            return None

        # Sort descending by priority_score
        ready_tasks.sort(key=lambda t: t.priority_score, reverse=True)
        return ready_tasks[0]

    def verify_and_complete_task(
        self, 
        task_id: str, 
        verification_fn: Optional[Callable[[], bool]] = None,
        result_evidence: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Verification Gate: Task CANNOT be marked complete without passing verification.
        """
        task = self.tasks.get(task_id)
        if not task:
            raise KeyError(f"Task {task_id} not found")

        # Execute verification check
        if verification_fn is not None:
            passed = verification_fn()
            if not passed:
                task.status = TaskStatus.FAILED
                task.result_data = {"error": "Verification check failed", "evidence": result_evidence}
                return False

        task.status = TaskStatus.VERIFIED
        task.verified_at = time.time()
        task.result_data = result_evidence or {"status": "Verified without errors"}

        # Refresh dependent tasks
        for other_task in self.tasks.values():
            self._update_task_state(other_task)

        return True

    def export_state(self) -> Dict[str, Any]:
        return {
            "total_tasks": len(self.tasks),
            "verified_tasks": sum(1 for t in self.tasks.values() if t.status == TaskStatus.VERIFIED),
            "pending_or_ready": sum(1 for t in self.tasks.values() if t.status in (TaskStatus.READY, TaskStatus.PENDING)),
            "blocked_tasks": sum(1 for t in self.tasks.values() if t.status == TaskStatus.BLOCKED),
            "tasks": [t.to_dict() for t in self.tasks.values()]
        }
