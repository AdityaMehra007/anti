"""
MODEL ROUTING MEMORY (HARDENED)
Tracks empirical performance across tasks, models, quality, speed, and cost.
Learns ONLY from real verified live executions. Never learns from simulations.
"""
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class RouteMemoryRecord:
    task_category: str
    chosen_model: str
    provider: str
    latency_ms: float
    cost_usd: float
    success: bool
    verified: bool
    execution_mode: str  # LIVE, SANDBOX, SIMULATION
    fallback_used: bool = False
    quality_achieved: float = 1.0
    human_evaluation: Optional[float] = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class RoutingMemory:
    def __init__(self):
        self._history: List[RouteMemoryRecord] = []

    def record_run(self, record: RouteMemoryRecord):
        # Strict Learning Rule: Only learn from real verified LIVE executions
        if record.execution_mode != "LIVE" or not record.verified:
            return
        self._history.append(record)

    def get_best_model_for_task(self, task_category: str) -> str:
        matching = [r for r in self._history if r.task_category == task_category and r.success]
        if not matching:
            return "claude-3-7-sonnet-20250219" if task_category == "HARD" else "gemini-2.5-flash"
        matching.sort(key=lambda r: (r.quality_achieved / (r.cost_usd + 0.001)), reverse=True)
        return matching[0].chosen_model
