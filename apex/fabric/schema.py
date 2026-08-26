"""
APEX V3 Universal Capability Fabric - Schema Definitions
"""
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
import time

class CapabilityCategory(str, Enum):
    COMPUTE = "COMPUTE"
    DATA = "DATA"
    RESEARCH = "RESEARCH"
    AI = "AI"
    BROWSER = "BROWSER"
    DEVELOPMENT = "DEVELOPMENT"
    BUSINESS = "BUSINESS"
    DESIGN = "DESIGN"
    SECURITY = "SECURITY"
    CLOUD = "CLOUD"
    COMMUNICATION = "COMMUNICATION"
    KNOWLEDGE = "KNOWLEDGE"
    AUTOMATION = "AUTOMATION"

class CapabilityHealth(str, Enum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    DISABLED = "DISABLED"
    BLOCKED = "BLOCKED"
    DEPRECATED = "DEPRECATED"

@dataclass
class CapabilityScore:
    utility: float = 1.0        # 0.0 - 1.0
    reliability: float = 1.0    # 0.0 - 1.0
    security: float = 1.0       # 0.0 - 1.0
    reusability: float = 1.0    # 0.0 - 1.0
    cost_efficiency: float = 1.0 # 0.0 - 1.0
    latency_score: float = 1.0  # 0.0 - 1.0
    maintainability: float = 1.0 # 0.0 - 1.0

    @property
    def overall_composite(self) -> float:
        weights = [0.20, 0.20, 0.20, 0.15, 0.10, 0.05, 0.10]
        scores = [self.utility, self.reliability, self.security, self.reusability, self.cost_efficiency, self.latency_score, self.maintainability]
        return round(sum(w * s for w, s in zip(weights, scores)), 3)

@dataclass
class UniversalCapability:
    capability_id: str
    name: str
    category: CapabilityCategory
    version: str = "1.0.0"
    purpose: str = ""
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    agents: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    mcp_servers: List[str] = field(default_factory=list)
    api_endpoints: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    permissions: Dict[str, Any] = field(default_factory=lambda: {
        "filesystem": "scoped",
        "network": "restricted",
        "autonomy_level": "A3"
    })
    risk_level: str = "LOW"
    estimated_cost_usd: float = 0.001
    avg_latency_ms: float = 5.0
    reliability_rate: float = 0.99
    tests: List[str] = field(default_factory=list)
    owner: str = "APEX_CORE"
    status: CapabilityHealth = CapabilityHealth.AVAILABLE
    documentation: str = ""
    created_at: float = field(default_factory=time.time)
    score: CapabilityScore = field(default_factory=CapabilityScore)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["category"] = self.category.value
        d["status"] = self.status.value
        d["overall_score"] = self.score.overall_composite
        return d
