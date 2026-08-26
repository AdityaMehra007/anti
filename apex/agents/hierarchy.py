"""
APEX Agent Organizational Hierarchy
Defines Executive C-Suite (CEO, CTO, CPO, CFO, CMO, CRO, CISO, CHRO), Domain Leads, and Specialist Agents with explicit responsibilities and authority bounds.
"""
from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class ApexAgentProfile:
    agent_id: str
    role_name: str
    title: str
    tier: str  # EXECUTIVE, DOMAIN_LEAD, SPECIALIST, EPHEMERAL
    responsibilities: List[str]
    max_autonomy: str  # A0 to A5
    primary_skills: List[str]
    assigned_tools: List[str]

class ApexOrganizationHierarchy:
    def __init__(self):
        self.agents: Dict[str, ApexAgentProfile] = {}
        self._initialize_hierarchy()

    def _initialize_hierarchy(self):
        # 1. Executive Suite
        executives = [
            ("CEO", "Chief Executive Officer", ["Strategic alignment", "Capital allocation", "Executive decisions"], "A4"),
            ("CTO", "Chief Technology Officer", ["Architecture governance", "Infrastructure scaling", "Engineering quality"], "A4"),
            ("CPO", "Chief Product Officer", ["Product roadmap", "User experience", "Feature prioritization"], "A4"),
            ("CFO", "Chief Financial Officer", ["P&L governance", "Cost optimization", "Budget allocation"], "A3"),
            ("CMO", "Chief Marketing Officer", ["Brand strategy", "GTM campaigns", "Customer acquisition"], "A4"),
            ("CRO", "Chief Revenue Officer", ["Sales pipeline", "Enterprise deals", "Revenue retention"], "A4"),
            ("CISO", "Chief Information Security Officer", ["Security policy", "Audit compliance", "Threat remediation"], "A5"),
            ("CHRO", "Chief Human Resources Officer", ["Talent strategy", "Performance reviews", "People operations"], "A3")
        ]
        for role, title, resps, autonomy in executives:
            self.agents[role] = ApexAgentProfile(
                agent_id=f"EXEC-{role}",
                role_name=role,
                title=title,
                tier="EXECUTIVE",
                responsibilities=resps,
                max_autonomy=autonomy,
                primary_skills=[f"{role.lower()}-strategy", "executive-governance"],
                assigned_tools=["system_health_check", "view_file", "search_web"]
            )

        # 2. Domain Leads
        domain_leads = [
            ("LEAD_ENG", "Engineering Lead", ["Code reviews", "CI/CD supervision", "Refactoring"], "A3"),
            ("LEAD_DATA", "Data & BI Lead", ["Data pipelines", "ETL validation", "DAX models"], "A3"),
            ("LEAD_SALES", "B2B Sales Lead", ["Lead qualification", "Proposal review", "CRM hygiene"], "A3"),
            ("LEAD_EXIM", "International Trade Lead", ["Incoterms compliance", "Customs clearance", "L/C audits"], "A3"),
            ("LEAD_AI", "AI & SDK Architect", ["Agentic orchestration", "MCP servers", "Eval suites"], "A4")
        ]
        for role, title, resps, autonomy in domain_leads:
            self.agents[role] = ApexAgentProfile(
                agent_id=f"LEAD-{role}",
                role_name=role,
                title=title,
                tier="DOMAIN_LEAD",
                responsibilities=resps,
                max_autonomy=autonomy,
                primary_skills=[f"{role.lower()}-coordination"],
                assigned_tools=["grep_search", "run_command", "view_file"]
            )

    def get_agent(self, role: str) -> ApexAgentProfile:
        return self.agents.get(role)

    def list_tier(self, tier: str) -> List[ApexAgentProfile]:
        return [a for a in self.agents.values() if a.tier == tier]
