"""
Permission Enforcer for REVENUE OS
Adheres strictly to Directives 5, 14, 72, 73, 129, 130.
Enforces the 6 tiers: READ -> ANALYZE -> DRAFT -> RECOMMEND -> EXECUTE -> APPROVE.
Guarantees that APPROVE is strictly reserved for the human founder for all consequential operations.
"""

from typing import Dict, Set
from REVENUE_OS.compliance.charter import PermissionTier

class PermissionDeniedError(Exception):
    """Raised when an agent attempts an action beyond its authorized tier."""
    pass

class PermissionEnforcer:
    """
    Enforces maximum permission ceilings per agent role.
    """
    
    # Maximum allowed ceiling per agent role
    AGENT_MAX_TIERS: Dict[str, PermissionTier] = {
        "RevenueCommander": PermissionTier.RECOMMEND,
        "MarketScout": PermissionTier.ANALYZE,
        "LeadResearcher": PermissionTier.DRAFT,
        "SalesAssistant": PermissionTier.DRAFT,
        "OfferArchitect": PermissionTier.DRAFT,
        "ContentAgent": PermissionTier.DRAFT,
        "CustomerSuccessAgent": PermissionTier.DRAFT,
        "FinanceAgent": PermissionTier.ANALYZE,
        "CompetitorAgent": PermissionTier.ANALYZE,
        "AutomationAgent": PermissionTier.EXECUTE, # For safe, internal scripted tasks
        "Founder": PermissionTier.APPROVE          # The only role permitted to APPROVE
    }

    TIER_RANK = {
        PermissionTier.READ: 1,
        PermissionTier.ANALYZE: 2,
        PermissionTier.DRAFT: 3,
        PermissionTier.RECOMMEND: 4,
        PermissionTier.EXECUTE: 5,
        PermissionTier.APPROVE: 6,
    }

    def enforce(self, agent_name: str, requested_tier: PermissionTier, action_context: str) -> bool:
        max_tier = self.AGENT_MAX_TIERS.get(agent_name, PermissionTier.READ)
        
        # If requested tier is higher than allowed ceiling, raise violation
        if self.TIER_RANK[requested_tier] > self.TIER_RANK[max_tier]:
            raise PermissionDeniedError(
                f"Security Gate: Agent '{agent_name}' (Ceiling: {max_tier.value}) is not authorized "
                f"to execute '{requested_tier.value}' for action: '{action_context}'. "
                f"Consequential actions require Human Founder signoff."
            )
            
        # If APPROVE is requested by anyone other than Founder, block
        if requested_tier == PermissionTier.APPROVE and agent_name != "Founder":
            raise PermissionDeniedError(
                f"Security Gate: Autonomous agents cannot APPROVE consequential actions. "
                f"Must be queued to Founder Approval Center."
            )
            
        return True
