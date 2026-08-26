"""
APEX Multi-Queue Engine (Priority, Scheduled, Approval, Retry, Dead-Letter)
"""
import heapq
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

@dataclass(order=True)
class QueuedTask:
    priority: int
    task_id: str = field(compare=False)
    name: str = field(compare=False)
    payload: Dict[str, Any] = field(compare=False, default_factory=dict)
    retries: int = field(compare=False, default=0)
    max_retries: int = field(compare=False, default=3)
    created_at: float = field(compare=False, default_factory=time.time)
    scheduled_at: float = field(compare=False, default=0.0)
    status: str = field(compare=False, default="QUEUED")  # QUEUED, RUNNING, APPROVAL_PENDING, COMPLETED, FAILED, DEAD_LETTER

class ApexQueueEngine:
    def __init__(self):
        self.priority_queue: List[QueuedTask] = []
        self.scheduled_queue: List[QueuedTask] = []
        self.approval_queue: Dict[str, QueuedTask] = {}
        self.dead_letter_queue: List[QueuedTask] = []
        self.completed_tasks: Dict[str, QueuedTask] = {}

    def enqueue(self, task_id: str, name: str, payload: Dict[str, Any] = None, priority: int = 5, delay_seconds: float = 0.0) -> QueuedTask:
        scheduled_time = time.time() + delay_seconds if delay_seconds > 0 else 0.0
        task = QueuedTask(
            priority=priority,
            task_id=task_id,
            name=name,
            payload=payload or {},
            scheduled_at=scheduled_time
        )
        if delay_seconds > 0:
            self.scheduled_queue.append(task)
        else:
            heapq.heappush(self.priority_queue, task)
        return task

    def pop_next_task(self) -> Optional[QueuedTask]:
        now = time.time()
        ready_scheduled = [t for t in self.scheduled_queue if t.scheduled_at <= now]
        for t in ready_scheduled:
            self.scheduled_queue.remove(t)
            heapq.heappush(self.priority_queue, t)

        if self.priority_queue:
            task = heapq.heappop(self.priority_queue)
            task.status = "RUNNING"
            return task
        return None

    def mark_completed(self, task: QueuedTask):
        task.status = "COMPLETED"
        self.completed_tasks[task.task_id] = task

    def mark_failed(self, task: QueuedTask, error: str):
        task.retries += 1
        if task.retries <= task.max_retries:
            task.status = "RETRYING"
            task.payload["last_error"] = error
            task.scheduled_at = time.time() + (2 ** task.retries)
            self.scheduled_queue.append(task)
        else:
            task.status = "DEAD_LETTER"
            task.payload["fatal_error"] = error
            self.dead_letter_queue.append(task)

    def route_for_approval(self, task: QueuedTask, reason: str):
        task.status = "APPROVAL_PENDING"
        task.payload["approval_reason"] = reason
        self.approval_queue[task.task_id] = task

    def approve_task(self, task_id: str) -> Optional[QueuedTask]:
        if task_id in self.approval_queue:
            task = self.approval_queue.pop(task_id)
            task.status = "APPROVED"
            heapq.heappush(self.priority_queue, task)
            return task
        return None

    def get_stats(self) -> Dict[str, int]:
        return {
            "priority_queue_depth": len(self.priority_queue),
            "scheduled_queue_depth": len(self.scheduled_queue),
            "approval_queue_depth": len(self.approval_queue),
            "dead_letter_queue_depth": len(self.dead_letter_queue),
            "completed_total": len(self.completed_tasks)
        }
