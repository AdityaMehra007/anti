"""
APEX Project Graph & DAG Execution Engine
Decomposes goals into Program -> Project -> Epic -> Task -> Subtask graphs, detects cycles, and calculates parallel execution waves.
"""
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
import uuid

@dataclass
class GraphNode:
    node_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    node_type: str = "TASK"  # GOAL, PROGRAM, PROJECT, EPIC, TASK, SUBTASK
    status: str = "PLANNED"   # PLANNED, SCAFFOLDED, IMPLEMENTED, EXECUTING, VERIFIED, FAILED, BLOCKED
    dependencies: Set[str] = field(default_factory=set)
    assigned_agent: Optional[str] = None
    assigned_tool: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None

class ApexProjectGraph:
    def __init__(self, name: str = "APEX_MASTER_GRAPH"):
        self.name = name
        self.nodes: Dict[str, GraphNode] = {}

    def add_node(self, node: GraphNode) -> str:
        self.nodes[node.node_id] = node
        return node.node_id

    def add_dependency(self, node_id: str, depends_on_id: str):
        if node_id in self.nodes and depends_on_id in self.nodes:
            self.nodes[node_id].dependencies.add(depends_on_id)

    def has_cycle(self) -> bool:
        visited = set()
        rec_stack = set()

        def _dfs(v: str) -> bool:
            visited.add(v)
            rec_stack.add(v)
            for dep in self.nodes[v].dependencies:
                if dep not in visited:
                    if _dfs(dep):
                        return True
                elif dep in rec_stack:
                    return True
            rec_stack.remove(v)
            return False

        for node_id in self.nodes:
            if node_id not in visited:
                if _dfs(node_id):
                    return True
        return False

    def get_execution_waves(self) -> List[List[str]]:
        """
        Calculates topological layers / parallel execution waves.
        Wave 0: Nodes with no dependencies.
        Wave 1: Nodes depending only on Wave 0, etc.
        """
        if self.has_cycle():
            raise ValueError("Dependency cycle detected in Project Graph!")

        in_degree = {nid: len(node.dependencies) for nid, node in self.nodes.items()}
        completed = set()
        waves = []

        while len(completed) < len(self.nodes):
            current_wave = []
            for nid, node in self.nodes.items():
                if nid not in completed and node.dependencies.issubset(completed):
                    current_wave.append(nid)

            if not current_wave:
                break  # Cycle or unreachable node
            
            waves.append(current_wave)
            completed.update(current_wave)

        return waves

    def get_stats(self) -> Dict[str, Any]:
        statuses = {}
        for n in self.nodes.values():
            statuses[n.status] = statuses.get(n.status, 0) + 1
        return {
            "total_nodes": len(self.nodes),
            "status_breakdown": statuses,
            "waves_count": len(self.get_execution_waves()) if not self.has_cycle() else -1
        }
