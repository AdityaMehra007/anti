"""
ANTIGRAVITY OMNIVERSE: CORE SYSTEM PRIMITIVES
=============================================
Defines the foundational data contracts, task representations, agent contracts,
and provenance envelopes.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import hashlib
import time

class AutonomyTier(Enum):
    LEVEL_0_OBSERVE = 0
    LEVEL_1_SUGGEST = 1
    LEVEL_2_PREPARE = 2
    LEVEL_3_LOCAL_EXEC = 3
    LEVEL_4_BOUNDED_EXEC = 4
    LEVEL_5_SUPERVISED_DAEMON = 5

class HumanControlTier(Enum):
    GREEN = "GREEN"     # Autonomous safe
    YELLOW = "YELLOW"   # Confirmation required
    RED = "RED"         # Mandatory hard gate

@dataclass
class ProvenanceEnvelope:
    source: str
    source_url: str
    source_date: str
    owner: str
    license: str
    confidence_score: float  # [0.0, 1.0]
    transformation_history: List[Dict[str, Any]] = field(default_factory=list)
    access_policy: str = "UNRESTRICTED_READ"
    last_verified: float = field(default_factory=time.time)
    sha256_hash: str = ""

    def compute_hash(self, content_bytes: bytes) -> str:
        self.sha256_hash = hashlib.sha256(content_bytes).hexdigest()
        return self.sha256_hash

@dataclass
class UniversalTaskObject:
    task_id: str
    goal: str
    description: str
    priority: float  # (Value * Probability * Urgency) / Effort
    owner: str
    agents: List[str]
    inputs: Dict[str, Any]
    tools: List[str]
    control_tier: HumanControlTier
    autonomy_tier: AutonomyTier
    dependencies: List[str] = field(default_factory=list)
    status: str = "PENDING"
    cost_usd: float = 0.0
    evidence: List[str] = field(default_factory=list)
    result: Optional[Dict[str, Any]] = None

@dataclass
class UniversalAgentContract:
    agent_id: str
    name: str
    mission: str
    autonomy_tier: AutonomyTier
    tools: List[str]
    limits: Dict[str, Any]
    failure_policy: str
    verification_method: str
    cost_budget_usd: float = 0.50
