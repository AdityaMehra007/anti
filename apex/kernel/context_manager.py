"""
APEX V2 Kernel - Context Fabric & Scoped Memory Manager
Provides isolated context for Task, Project, and Agent levels, avoiding whole-project context dumping.
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

@dataclass
class ScopedContext:
    project_id: str
    task_id: str
    agent_id: str
    task_inputs: Dict[str, Any] = field(default_factory=dict)
    relevant_knowledge: List[str] = field(default_factory=list)
    available_tools: List[str] = field(default_factory=list)
    scoped_files: List[str] = field(default_factory=list)

class ApexContextManager:
    def __init__(self):
        self._project_contexts: Dict[str, Dict[str, Any]] = {}
        self._agent_memories: Dict[str, List[Dict[str, Any]]] = {}

    def set_project_context(self, project_id: str, context_data: Dict[str, Any]):
        self._project_contexts[project_id] = context_data

    def get_project_context(self, project_id: str) -> Dict[str, Any]:
        return self._project_contexts.get(project_id, {})

    def record_agent_memory(self, agent_id: str, event_type: str, data: Any):
        if agent_id not in self._agent_memories:
            self._agent_memories[agent_id] = []
        self._agent_memories[agent_id].append({
            "event": event_type,
            "data": data
        })

    def assemble_task_context(self, project_id: str, task_id: str, agent_id: str, inputs: Dict[str, Any], tools: List[str]) -> ScopedContext:
        proj_ctx = self.get_project_context(project_id)
        # Select only relevant knowledge & files matching inputs
        scoped_files = inputs.get("target_files", [])
        knowledge_snippets = [f"Project Objective: {proj_ctx.get('objective', 'Standard Task')}"]
        if "topic" in inputs:
            knowledge_snippets.append(f"Domain Focus: {inputs['topic']}")

        return ScopedContext(
            project_id=project_id,
            task_id=task_id,
            agent_id=agent_id,
            task_inputs=inputs,
            relevant_knowledge=knowledge_snippets,
            available_tools=tools,
            scoped_files=scoped_files
        )
