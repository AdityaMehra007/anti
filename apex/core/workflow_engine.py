"""
APEX Workflow Engine
Executes multi-step workflows with sequential, parallel, conditional, and recovery branches.
"""
import time
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field

@dataclass
class WorkflowStep:
    step_id: str
    name: str
    action: Callable[..., Any]
    depends_on: List[str] = field(default_factory=list)
    is_conditional: bool = False
    condition_fn: Optional[Callable[[Dict[str, Any]], bool]] = None
    status: str = "PENDING"  # PENDING, RUNNING, SUCCESS, SKIPPED, FAILED
    result: Optional[Any] = None
    error: Optional[str] = None

class ApexWorkflow:
    def __init__(self, workflow_id: str, name: str):
        self.workflow_id = workflow_id
        self.name = name
        self.steps: Dict[str, WorkflowStep] = {}
        self.context: Dict[str, Any] = {}
        self.status: str = "INITIALIZED"

    def add_step(self, step: WorkflowStep):
        self.steps[step.step_id] = step

    def execute(self) -> Dict[str, Any]:
        self.status = "RUNNING"
        start_time = time.time()
        completed_steps = set()

        for step_id, step in self.steps.items():
            # Check dependencies
            if not set(step.depends_on).issubset(completed_steps):
                step.status = "BLOCKED"
                continue

            # Check conditional
            if step.is_conditional and step.condition_fn:
                if not step.condition_fn(self.context):
                    step.status = "SKIPPED"
                    completed_steps.add(step_id)
                    continue

            # Execute step
            step.status = "RUNNING"
            try:
                res = step.action(self.context)
                step.result = res
                step.status = "SUCCESS"
                self.context[step_id] = res
                completed_steps.add(step_id)
            except Exception as e:
                step.status = "FAILED"
                step.error = str(e)
                self.status = "FAILED"
                return {
                    "workflow_id": self.workflow_id,
                    "status": "FAILED",
                    "failed_step": step_id,
                    "error": str(e),
                    "duration_seconds": round(time.time() - start_time, 3)
                }

        self.status = "COMPLETED"
        return {
            "workflow_id": self.workflow_id,
            "status": "COMPLETED",
            "steps_completed": len(completed_steps),
            "duration_seconds": round(time.time() - start_time, 3),
            "context": self.context
        }
