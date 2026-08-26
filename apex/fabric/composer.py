"""
APEX V3 Universal Capability Fabric - Capability Composer
Composes multiple atomic capabilities into validated composite pipelines.
Example: WEB_SEARCH + DATA_EXTRACTION + SOURCE_VERIFICATION + REPORT_GENERATION = MARKET_INTELLIGENCE
"""
from typing import List, Dict, Any, Optional
import uuid
import time
from .schema import UniversalCapability, CapabilityCategory, CapabilityHealth, CapabilityScore
from .registry import CapabilityRegistry

class CapabilityComposer:
    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry

    def compose_composite(self, name: str, category: CapabilityCategory, sub_capability_ids: List[str], purpose: str) -> UniversalCapability:
        collected_tools = []
        collected_agents = []
        collected_skills = []
        total_cost = 0.0
        max_latency = 0.0
        
        for cid in sub_capability_ids:
            cap = self.registry.get(cid)
            if cap:
                collected_tools.extend(cap.tools)
                collected_agents.extend(cap.agents)
                collected_skills.extend(cap.skills)
                total_cost += cap.estimated_cost_usd
                max_latency += cap.avg_latency_ms

        composite_id = f"CAP-COMPOSITE-{str(uuid.uuid4())[:6].upper()}"
        composite_cap = UniversalCapability(
            capability_id=composite_id,
            name=name,
            category=category,
            purpose=purpose,
            agents=list(set(collected_agents)),
            tools=list(set(collected_tools)),
            skills=list(set(collected_skills)),
            dependencies=sub_capability_ids,
            estimated_cost_usd=round(total_cost, 4),
            avg_latency_ms=round(max_latency, 2),
            documentation=f"Composite capability constructed from: {', '.join(sub_capability_ids)}."
        )

        self.registry.register(composite_cap)
        return composite_cap
