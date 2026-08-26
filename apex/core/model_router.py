"""
APEX Model Router & Dynamic Token Budgeting
Routes tasks to optimal models (fast/flash, balanced, reasoning/pro, coding, multimodal) with fallback paths.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ModelRoute:
    model_name: str
    tier: str  # FLASH, BALANCED, PRO, CODING, MULTIMODAL
    max_tokens: int
    temperature: float
    fallback_model: Optional[str] = None
    estimated_cost_per_1k: float = 0.001

class ApexModelRouter:
    def __init__(self):
        self.routes = {
            "FLASH": ModelRoute("gemini-2.5-flash", "FLASH", 8192, 0.2, "gemini-2.5-flash-lite", 0.0005),
            "BALANCED": ModelRoute("gemini-2.5-pro", "BALANCED", 16384, 0.3, "gemini-2.5-flash", 0.002),
            "PRO": ModelRoute("gemini-3.7-pro", "PRO", 32768, 0.4, "gemini-2.5-pro", 0.005),
            "CODING": ModelRoute("gemini-3.7-flash", "CODING", 32768, 0.1, "gemini-2.5-pro", 0.003),
            "MULTIMODAL": ModelRoute("gemini-2.5-flash", "MULTIMODAL", 16384, 0.2, "gemini-2.5-pro", 0.002)
        }

    def route(self, task_type: str, complexity: str = "NORMAL", has_media: bool = False) -> ModelRoute:
        task_type_upper = task_type.upper()
        if has_media:
            return self.routes["MULTIMODAL"]
        if "CODE" in task_type_upper or "REFACTOR" in task_type_upper or "DEBUG" in task_type_upper or "TEST" in task_type_upper:
            return self.routes["CODING"]
        if complexity == "HIGH" or "RESEARCH" in task_type_upper or "ARCHITECT" in task_type_upper or "SYNTHESIZE" in task_type_upper:
            return self.routes["PRO"]
        if complexity == "LOW" or "CLASSIFY" in task_type_upper or "EXTRACT" in task_type_upper:
            return self.routes["FLASH"]
        return self.routes["BALANCED"]

    def estimate_cost(self, route: ModelRoute, prompt_tokens: int, completion_tokens: int) -> float:
        total_tokens = prompt_tokens + completion_tokens
        return (total_tokens / 1000.0) * route.estimated_cost_per_1k
