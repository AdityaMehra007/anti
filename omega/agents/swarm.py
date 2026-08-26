"""
15 SPECIALIZED AUTONOMOUS AGENTS
All communicate via governed OmniRoute model gateway, A2A protocol, and MCP tool fabric.
"""
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from ..model_router.client import OmniRouteClient, ModelResponse
from ..model_router.router import ModelRouter
from ..model_router.a2a_engine import A2AEngine

@dataclass
class AgentMetadata:
    agent_id: str
    role_name: str
    preferred_model_tier: str
    governance_level: str
    status: str = "ACTIVE"

class BaseAgent:
    def __init__(self, agent_id: str, role_name: str, preferred_tier: str, client: Optional[OmniRouteClient] = None):
        self.agent_id = agent_id
        self.role_name = role_name
        self.preferred_tier = preferred_tier
        self.client = client or OmniRouteClient()
        self.router = ModelRouter()
        self.a2a = A2AEngine()

    def execute_task(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        route = self.router.route(prompt, context)
        resp = self.client.generate(route.primary_model, [{"role": "user", "content": prompt}])
        return {
            "agent_id": self.agent_id,
            "role": self.role_name,
            "model_used": route.primary_model,
            "provider": route.primary_provider,
            "output": resp.content,
            "tokens": resp.total_tokens,
            "latency_ms": resp.latency_ms,
            "status": "COMPLETED"
        }

class CEOAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-ceo", "Chief Executive Officer & Chief Strategy Agent", "FRONTIER_QUALITY", client)

class CTOAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-cto", "Chief Technology Officer & System Resilience Architect", "FRONTIER_QUALITY", client)

class JobScoutAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-job-scout", "Real-Time Opportunity Discovery Lead", "FAST", client)

class CompanyResearchAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-company-research", "Company Intelligence & 365-Day Radar Analyst", "FAST", client)

class NetworkAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-network", "Ethical Recruiter & Hiring Manager Contact Strategist", "FAST", client)

class ApplicationAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-application", "Tailored Resume & ATS Application Factory Lead", "FAST", client)

class OutreachAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-outreach", "Governed Outreach & Recruiter Communication Partner", "FAST", client)

class InterviewAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-interview", "STAR Evidence & Multi-Model Interview Simulator", "FRONTIER_QUALITY", client)

class OfferAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-offer", "Compensation & Strategic Offer Negotiation Architect", "FRONTIER_QUALITY", client)

class SkillAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-skill", "Skill Gap Analytics & Career ROI Strategist", "FAST", client)

class AnalyticsAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-analytics", "Market Demand & Labor Economic Analyst", "FAST", client)

class TruthAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-truth", "Truth Engine Corroboration & Reality Check Auditor", "FRONTIER_QUALITY", client)

class SecurityAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-security", "Prompt-Injection Defense & Permission Guardian", "FRONTIER_QUALITY", client)

class QAAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-qa", "Quality Assurance & Output Verification Specialist", "FAST", client)

class AuditorAgent(BaseAgent):
    def __init__(self, client=None):
        super().__init__("agent-auditor", "Universal System Auditor & Transaction Ledger Reconciler", "FRONTIER_QUALITY", client)

class AgentSwarm:
    def __init__(self, client: Optional[OmniRouteClient] = None):
        self.client = client or OmniRouteClient()
        self.agents: Dict[str, BaseAgent] = {
            "CEO": CEOAgent(self.client),
            "CTO": CTOAgent(self.client),
            "JobScout": JobScoutAgent(self.client),
            "CompanyResearch": CompanyResearchAgent(self.client),
            "Network": NetworkAgent(self.client),
            "Application": ApplicationAgent(self.client),
            "Outreach": OutreachAgent(self.client),
            "Interview": InterviewAgent(self.client),
            "Offer": OfferAgent(self.client),
            "Skill": SkillAgent(self.client),
            "Analytics": AnalyticsAgent(self.client),
            "Truth": TruthAgent(self.client),
            "Security": SecurityAgent(self.client),
            "QA": QAAgent(self.client),
            "Auditor": AuditorAgent(self.client)
        }

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        return self.agents.get(name)

    def list_all_agents(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": name,
                "agent_id": a.agent_id,
                "role": a.role_name,
                "preferred_tier": a.preferred_tier,
                "status": "ACTIVE"
            }
            for name, a in self.agents.items()
        ]
