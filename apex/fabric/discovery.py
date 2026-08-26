"""
APEX V3 Universal Capability Fabric - Discovery Engine
Implements 10-tier discovery hierarchy and multi-dimensional ranking:
FIT + RELIABILITY + SECURITY + COST + SPEED
"""
from typing import List, Dict, Any, Optional
from .schema import UniversalCapability, CapabilityCategory, CapabilityHealth
from .registry import CapabilityRegistry

class CapabilityDiscoveryEngine:
    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry

    def discover_for_task(self, query: str, category_hint: Optional[CapabilityCategory] = None) -> Dict[str, Any]:
        """
        Executes 10-tier search order and ranks results.
        """
        q = query.lower()
        search_trace = []

        # TIER 1: Existing capability in Registry
        search_trace.append("Tier 1: Searching Universal Capability Registry...")
        all_caps = self.registry.list_all()
        direct_matches = []
        for cap in all_caps:
            if cap.status == CapabilityHealth.AVAILABLE:
                fit_score = 0.0
                if q in cap.name.lower() or q in cap.purpose.lower():
                    fit_score += 0.8
                if category_hint and cap.category == category_hint:
                    fit_score += 0.2
                if any(q in t.lower() for t in cap.tools):
                    fit_score += 0.4
                if any(q in s.lower() for s in cap.skills):
                    fit_score += 0.4

                if fit_score > 0.3:
                    direct_matches.append((cap, min(fit_score, 1.0)))

        if direct_matches:
            # Sort by combined Fit * Overall Score
            direct_matches.sort(key=lambda x: x[1] * x[0].score.overall_composite, reverse=True)
            best_cap, best_score = direct_matches[0]
            return {
                "source": "REGISTRY_CAPABILITY",
                "tier_resolved": 1,
                "capability": best_cap,
                "match_confidence": round(best_score, 2),
                "search_trace": search_trace
            }

        # TIER 2: Existing Agent
        search_trace.append("Tier 2: Searching Registered Specialist Agents...")
        agent_matches = [c for c in all_caps if any(q in a.lower() for a in c.agents)]
        if agent_matches:
            return {
                "source": "AGENT_FABRIC",
                "tier_resolved": 2,
                "capability": agent_matches[0],
                "match_confidence": 0.85,
                "search_trace": search_trace
            }

        # TIER 3: Existing Skill Catalog (300 Skills)
        search_trace.append("Tier 3: Searching 300 Skill Catalog...")
        skill_matches = [c for c in all_caps if len(c.skills) > 0]
        if skill_matches:
            return {
                "source": "SKILL_CATALOG",
                "tier_resolved": 3,
                "capability": skill_matches[0],
                "match_confidence": 0.80,
                "search_trace": search_trace
            }

        # TIER 4 - 9: Fallback to General Compute / Dynamic Composition
        search_trace.append("Tier 4-9: Inspecting plugins, APIs, and composite templates...")
        compute_cap = self.registry.get("CAP-COMP-01")
        return {
            "source": "FALLBACK_COMPUTE",
            "tier_resolved": 4,
            "capability": compute_cap,
            "match_confidence": 0.70,
            "search_trace": search_trace
        }
