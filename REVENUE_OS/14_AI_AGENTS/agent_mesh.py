"""
Agent Mesh for REVENUE OS
Adheres strictly to Directives 2, 13, 161.
Implements the 10 specialist agents and their standard operating procedures.
"""

from typing import Any, Dict, List, Optional
from REVENUE_OS.compliance.charter import PermissionTier
import importlib

# Dynamic import to avoid circular dependency
_perms = importlib.import_module("REVENUE_OS.14_AI_AGENTS.permissions")
PermissionEnforcer = _perms.PermissionEnforcer

class BaseSpecialistAgent:
    def __init__(self, name: str, role: str, max_tier: PermissionTier):
        self.name = name
        self.role = role
        self.max_tier = max_tier
        self.enforcer = PermissionEnforcer()

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "max_permission_tier": self.max_tier.value,
            "status": "READY"
        }

class RevenueCommander(BaseSpecialistAgent):
    def __init__(self):
        super().__init__(
            name="RevenueCommander",
            role="Chief Intelligence & Orchestration Officer",
            max_tier=PermissionTier.RECOMMEND
        )

    def run_daily_triage(
        self,
        revenue_yesterday_inr: float,
        revenue_month_inr: float,
        pipeline_inr: float,
        biggest_opportunity: str,
        biggest_risk: str
    ) -> Dict[str, Any]:
        what_made_money = (
            f"Yesterday: ₹{revenue_yesterday_inr:,.2f} | MTD: ₹{revenue_month_inr:,.2f} generated from "
            "active retainers and productized pipeline audit deliveries."
            if revenue_yesterday_inr > 0 or revenue_month_inr > 0
            else "Zero recorded cash inflow yesterday. Pipeline maturation and outreach in progress."
        )
        
        what_can_make_money = (
            f"Active Pipeline: ₹{pipeline_inr:,.2f}. Highest-ROI focus: '{biggest_opportunity}'."
        )
        
        what_stopped_us = (
            f"Primary bottleneck / risk: '{biggest_risk}'. Outbound response latency and scheduling friction."
        )
        
        top_3_actions = [
            f"Send 5 custom-researched account teardowns to qualified decision-makers for '{biggest_opportunity.split('-')[0].strip()}'.",
            "Review pending proposals in Founder Approval Center and dispatch approved agreements.",
            "Inspect newly scored leads from overnight Market Scout run and promote top-tier accounts to CRM."
        ]

        return {
            "what_made_money": what_made_money,
            "what_can_make_money": what_can_make_money,
            "what_stopped_us": what_stopped_us,
            "what_should_happen_next": "Execute top 3 actions today. Free up founder hours for high-value closing.",
            "top_3_actions": top_3_actions,
            "founder_approval_required": False
        }

class MarketScout(BaseSpecialistAgent):
    def __init__(self):
        super().__init__("MarketScout", "Market & Buying-Signal Scout", PermissionTier.ANALYZE)

class LeadResearcher(BaseSpecialistAgent):
    def __init__(self):
        super().__init__("LeadResearcher", "Prospect Research & ICP Scoring", PermissionTier.DRAFT)

class SalesAssistant(BaseSpecialistAgent):
    def __init__(self):
        super().__init__("SalesAssistant", "Personalized Sales & Outbound Preparation", PermissionTier.DRAFT)

class OfferArchitect(BaseSpecialistAgent):
    def __init__(self):
        super().__init__("OfferArchitect", "High-Margin Offer & Value Prop Design", PermissionTier.DRAFT)

class ContentAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__("ContentAgent", "Content-to-Pipeline & Authority Creation", PermissionTier.DRAFT)

class CustomerSuccessAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__("CustomerSuccessAgent", "Retention, Onboarding & Churn Guard", PermissionTier.DRAFT)

class FinanceAgentAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__("FinanceAgent", "Cash Flow, Unit Economics & Expense Audit", PermissionTier.ANALYZE)

class CompetitorAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__("CompetitorAgent", "Competitor Radar & Niche Gap Analysis", PermissionTier.ANALYZE)

class AutomationAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__("AutomationAgent", "Workflow Automation & Pipeline Maintenance", PermissionTier.EXECUTE)

class AgentMesh:
    def __init__(self):
        self._agents: Dict[str, BaseSpecialistAgent] = {
            "RevenueCommander": RevenueCommander(),
            "MarketScout": MarketScout(),
            "LeadResearcher": LeadResearcher(),
            "SalesAssistant": SalesAssistant(),
            "OfferArchitect": OfferArchitect(),
            "ContentAgent": ContentAgent(),
            "CustomerSuccessAgent": CustomerSuccessAgent(),
            "FinanceAgent": FinanceAgentAgent(),
            "CompetitorAgent": CompetitorAgent(),
            "AutomationAgent": AutomationAgent(),
        }

    def list_agents(self) -> List[str]:
        return list(self._agents.keys())

    def get_agent(self, name: str) -> BaseSpecialistAgent:
        if name not in self._agents:
            raise KeyError(f"Specialist agent '{name}' not found.")
        return self._agents[name]

    def get_all_agent_statuses(self) -> List[Dict[str, Any]]:
        return [agent.get_info() for agent in self._agents.values()]
