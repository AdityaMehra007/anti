"""
TASK CLASSIFIER
Classifies prompts/tasks into:
- SIMPLE: Extraction, formatting, deduplication -> Fast / Low Cost model
- MEDIUM: Research synthesis, application analysis -> Balanced model
- HARD: Architecture, complex strategy, executive reasoning, high-stakes negotiations -> Frontier model
- SENSITIVE: Private keys, credentials, confidential PII -> Local Private model
"""
import re
from enum import Enum
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

class TaskTier(str, Enum):
    SIMPLE = "SIMPLE"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    SENSITIVE = "SENSITIVE"

@dataclass
class TaskProfile:
    tier: TaskTier
    confidence: float
    recommended_category: str
    detected_keywords: List[str]
    is_sensitive: bool

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["tier"] = self.tier.value
        return d

class TaskClassifier:
    SENSITIVE_PATTERNS = [
        r"private\s+key", r"password", r"ssn", r"salary\s+negotiation\s+secret",
        r"confidential", r"internal\s+secret", r"credentials", r"private"
    ]
    HARD_PATTERNS = [
        r"architecture", r"strategy", r"executive", r"system\s+design", r"negotiation\s+strategy",
        r"high-stakes", r"multi-model\s+debate", r"executive\s+dossier", r"complex", r"blueprint"
    ]
    MEDIUM_PATTERNS = [
        r"research", r"synthesis", r"company\s+analysis", r"tailored\s+resume",
        r"interview\s+prep", r"cover\s+letter", r"skill\s+gap", r"analysis"
    ]

    @classmethod
    def classify(cls, task_text: str, context: Dict[str, Any] = None) -> TaskProfile:
        ctx = context or {}
        lower = (task_text + " " + str(ctx)).lower()

        # Check Sensitive first
        for p in cls.SENSITIVE_PATTERNS:
            if re.search(p, lower):
                return TaskProfile(TaskTier.SENSITIVE, 0.98, "LOCAL", [p], True)

        # Check Hard
        hard_matches = [p for p in cls.HARD_PATTERNS if re.search(p, lower)]
        if hard_matches or ctx.get("difficulty") == "HARD":
            return TaskProfile(TaskTier.HARD, 0.95, "FRONTIER_QUALITY", hard_matches, False)

        # Check Medium
        med_matches = [p for p in cls.MEDIUM_PATTERNS if re.search(p, lower)]
        if med_matches or ctx.get("difficulty") == "MEDIUM":
            return TaskProfile(TaskTier.MEDIUM, 0.90, "FAST", med_matches, False)

        # Default Simple
        return TaskProfile(TaskTier.SIMPLE, 0.85, "LOW_COST_FREE", ["routine_operation"], False)
