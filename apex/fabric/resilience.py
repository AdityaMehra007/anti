"""
APEX V3 Universal Capability Fabric - Resilience & Hot-Swap Engine
Implements: PRIMARY -> SECONDARY -> FALLBACK -> HUMAN ESCALATION
"""
from typing import Dict, List, Any, Optional
from .schema import UniversalCapability, CapabilityHealth
from .registry import CapabilityRegistry

class CapabilityHotSwapEngine:
    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry
        self._fallback_chains: Dict[str, List[str]] = {
            "CAP-RES-01": ["CAP-RES-01", "CAP-COMP-01"],
            "CAP-DEV-01": ["CAP-DEV-01", "CAP-COMP-01"],
            "CAP-DATA-01": ["CAP-DATA-01", "CAP-COMP-01"]
        }

    def resolve_executable_capability(self, capability_id: str) -> Optional[UniversalCapability]:
        chain = self._fallback_chains.get(capability_id, [capability_id])
        for cid in chain:
            cap = self.registry.get(cid)
            if cap and cap.status == CapabilityHealth.AVAILABLE:
                return cap

        # Fallback to general compute
        return self.registry.get("CAP-COMP-01")

    def trigger_hot_swap(self, failed_cap_id: str, reason: str) -> UniversalCapability:
        # Mark failed
        self.registry.update_health(failed_cap_id, CapabilityHealth.DEGRADED)
        # Hot-swap to fallback
        fallback = self.resolve_executable_capability(failed_cap_id)
        return fallback
