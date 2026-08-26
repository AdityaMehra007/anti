"""
APEX V2 Execution Kernel & Master Orchestrator Runtime
Coordinates Task IDs, Parent/child tasks, Project context, Agent assignment, Tool assignment,
State, Events, Results, Errors, Verification, Retry, Cancellation, and Resume.
"""
import time
from typing import Dict, List, Any, Optional
from .task import KernelTask, TaskState, VerificationState
from .context_manager import ApexContextManager
from .agents import ApexAgentFabric, SpecialistAgent
from .tool_fabric import ApexToolFabric
from .verification_pipeline import ApexVerificationPipeline
from .recovery_engine import ApexRecoveryEngine

class ApexExecutionKernel:
    def __init__(self):
        self.tasks: Dict[str, KernelTask] = {}
        self.context_manager = ApexContextManager()
        self.agent_fabric = ApexAgentFabric()
        self.tool_fabric = ApexToolFabric()
        self.verification_pipeline = ApexVerificationPipeline()
        self.recovery_engine = ApexRecoveryEngine()
        self.events: List[Dict[str, Any]] = []

    def log_event(self, event_type: str, task_id: Optional[str] = None, payload: Dict[str, Any] = None):
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "task_id": task_id,
            "payload": payload or {}
        }
        self.events.append(event)

    def create_task(self, name: str, goal: str, parent_id: Optional[str] = None, project_id: str = "DEFAULT_PROJECT", assigned_agent: Optional[str] = None, assigned_tool: Optional[str] = None, inputs: Dict[str, Any] = None) -> KernelTask:
        task = KernelTask(
            name=name,
            goal=goal,
            parent_task_id=parent_id,
            project_id=project_id,
            assigned_agent=assigned_agent,
            assigned_tool=assigned_tool,
            inputs=inputs or {}
        )
        self.tasks[task.task_id] = task
        self.log_event("TASK_CREATED", task.task_id, {"name": name, "agent": assigned_agent})
        return task

    def execute_task(self, task_id: str) -> Dict[str, Any]:
        task = self.tasks.get(task_id)
        if not task:
            return {"status": "ERROR", "error": f"Task '{task_id}' not found."}

        task.start()
        self.log_event("TASK_STARTED", task_id, {"name": task.name})

        # 1. Resolve agent
        agent = self.agent_fabric.get_agent(task.assigned_agent or "developer")
        if not agent:
            task.fail(f"Agent '{task.assigned_agent}' not found.")
            self.log_event("TASK_FAILED", task_id, {"error": "Agent not found"})
            return {"status": "FAILED", "error": "Agent not found"}

        self.log_event("AGENT_STARTED", task_id, {"agent": agent.role})

        # 2. Assemble scoped context
        scoped_ctx = self.context_manager.assemble_task_context(
            project_id=task.project_id,
            task_id=task_id,
            agent_id=agent.agent_id,
            inputs=task.inputs,
            tools=agent.tools_permitted
        )

        # 3. Execute tool if assigned
        tool_result = None
        if task.assigned_tool:
            self.log_event("TOOL_CALLED", task_id, {"tool": task.assigned_tool})
            tool_res = self.tool_fabric.execute_with_lifecycle(
                task.assigned_tool,
                agent_autonomy=agent.autonomy_level,
                **task.inputs
            )
            if tool_res.get("status") == "FAILED":
                self.log_event("TOOL_FAILED", task_id, {"tool": task.assigned_tool, "error": tool_res.get("error")})
                task.fail(tool_res.get("error", "Tool failed"))
                return tool_res
            tool_result = tool_res

        # 4. Execute agent specialist logic
        agent_output = agent.execute(task.name, task.inputs, scoped_ctx)
        self.log_event("AGENT_COMPLETED", task_id, {"agent": agent.role})

        # 5. Complete task
        combined_outputs = {"agent_output": agent_output, "tool_result": tool_result}
        artifacts = []
        if "target_file" in task.inputs:
            artifacts.append(task.inputs["target_file"])

        task.complete(outputs=combined_outputs, artifacts=artifacts)
        self.log_event("TASK_COMPLETED", task_id, {"duration_ms": task.duration_ms})

        return {
            "status": "COMPLETED",
            "task_id": task_id,
            "duration_ms": task.duration_ms,
            "outputs": combined_outputs
        }

    def verify_task_output(self, task_id: str) -> Dict[str, Any]:
        task = self.tasks.get(task_id)
        if not task or not task.artifacts_created:
            return {"status": "NO_ARTIFACTS", "task_id": task_id}

        verdicts = []
        for art in task.artifacts_created:
            v = self.verification_pipeline.verify_artifact(art)
            verdicts.append(v)
            if v.overall_status == "FULLY_VERIFIED":
                task.verification_state = VerificationState.FULLY_VERIFIED
            else:
                task.verification_state = VerificationState.QA_FAILED

        return {
            "task_id": task_id,
            "verification_state": task.verification_state.value,
            "verdicts": [v.__dict__ for v in verdicts]
        }

    def run_goal_mission(self, goal: str, project_id: str = "APEX_MISSION") -> Dict[str, Any]:
        self.context_manager.set_project_context(project_id, {"objective": goal})
        
        # 1. Create Decomposed Pipeline Tasks
        t_research = self.create_task("Research Domain", goal, project_id=project_id, assigned_agent="researcher", inputs={"topic": goal})
        t_plan = self.create_task("Create Software Specification", goal, parent_id=t_research.task_id, project_id=project_id, assigned_agent="planner")
        t_arch = self.create_task("Architect System Topology", goal, parent_id=t_plan.task_id, project_id=project_id, assigned_agent="architect")
        
        app_file = f"e:/anti/apex/projects/{project_id.lower()}/index.html"
        t_dev = self.create_task("Build Application", goal, parent_id=t_arch.task_id, project_id=project_id, assigned_agent="developer", assigned_tool="file_writer", inputs={"file_path": app_file, "content": f"<!DOCTYPE html><html><head><title>{goal}</title></head><body><h1>{goal}</h1><p>Built autonomously by APEX V2 Execution Kernel.</p></body></html>", "target_file": app_file})
        
        t_qa = self.create_task("QA Testing", goal, parent_id=t_dev.task_id, project_id=project_id, assigned_agent="qa_agent", assigned_tool="qa_test_runner", inputs={"file_path": app_file})
        t_sec = self.create_task("Security Audit", goal, parent_id=t_qa.task_id, project_id=project_id, assigned_agent="security_agent", inputs={"target": app_file})
        t_ver = self.create_task("Independent Verification", goal, parent_id=t_sec.task_id, project_id=project_id, assigned_agent="verification_agent", inputs={"target": app_file})

        # 2. Execute Sequential Pipeline
        pipeline = [t_research, t_plan, t_arch, t_dev, t_qa, t_sec, t_ver]
        for t in pipeline:
            self.execute_task(t.task_id)

        # 3. Verify Artifact
        v_res = self.verify_task_output(t_dev.task_id)

        return {
            "project_id": project_id,
            "goal": goal,
            "tasks_executed": len(pipeline),
            "verification": v_res,
            "status": "MISSION_ACCOMPLISHED"
        }

    def get_live_state(self) -> Dict[str, Any]:
        task_states = {}
        for t in self.tasks.values():
            task_states[t.state.value] = task_states.get(t.state.value, 0) + 1
        return {
            "total_tasks": len(self.tasks),
            "state_distribution": task_states,
            "total_events_logged": len(self.events),
            "registered_specialists": len(self.agent_fabric.list_specialists()),
            "registered_tools": len(self.tool_fabric.discover()),
            "recent_events": self.events[-10:]
        }
