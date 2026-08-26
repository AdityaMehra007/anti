"""
APEX V2 Kernel - Task Data Model & Lifecycle State Machine
"""
import time
import uuid
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

class TaskState(str, Enum):
    PLANNED = "PLANNED"
    SCAFFOLDED = "SCAFFOLDED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    APPROVAL_PENDING = "APPROVAL_PENDING"

class VerificationState(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    QA_PASSED = "QA_PASSED"
    QA_FAILED = "QA_FAILED"
    FULLY_VERIFIED = "FULLY_VERIFIED"
    REJECTED = "REJECTED"

@dataclass
class KernelTask:
    task_id: str = field(default_factory=lambda: f"TASK-{str(uuid.uuid4())[:8]}")
    name: str = ""
    goal: str = ""
    parent_task_id: Optional[str] = None
    project_id: str = "DEFAULT_PROJECT"
    assigned_agent: Optional[str] = None
    assigned_tool: Optional[str] = None
    state: TaskState = TaskState.PLANNED
    verification_state: VerificationState = VerificationState.UNVERIFIED
    
    # Inputs & Outputs
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    artifacts_created: List[str] = field(default_factory=list)
    
    # Tracking & Correlation
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    causation_id: Optional[str] = None
    priority: int = 5
    retries: int = 0
    max_retries: int = 3
    
    # Telemetry
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    duration_ms: float = 0.0

    def start(self):
        self.state = TaskState.RUNNING
        self.started_at = time.time()

    def complete(self, outputs: Dict[str, Any], artifacts: List[str] = None):
        self.state = TaskState.COMPLETED
        self.completed_at = time.time()
        self.outputs = outputs or {}
        if artifacts:
            self.artifacts_created.extend(artifacts)
        if self.started_at:
            self.duration_ms = round((self.completed_at - self.started_at) * 1000, 2)

    def fail(self, error_msg: str):
        self.errors.append(error_msg)
        self.retries += 1
        if self.retries > self.max_retries:
            self.state = TaskState.FAILED
        else:
            self.state = TaskState.PLANNED  # Ready for retry
        if self.started_at:
            self.duration_ms = round((time.time() - self.started_at) * 1000, 2)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["state"] = self.state.value
        d["verification_state"] = self.verification_state.value
        return d
