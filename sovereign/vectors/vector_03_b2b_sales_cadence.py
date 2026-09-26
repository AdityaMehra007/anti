"""Vector 3: Automated B2B Outbound, Lead Generation & Sales Cadences (30 Capabilities)."""
from typing import Dict, Any, List

class B2BOutboundSalesEngine:
    @staticmethod
    def generate_personalized_cadence(company_name: str, decision_maker: str, pain_point: str) -> List[Dict[str, str]]:
        return [
            {
                "touchpoint": "Day 1: Email 1 (Initial Value Hook)",
                "subject": f"Reducing operations overhead at {company_name}",
                "body": f"Hi {decision_maker}, noticed your team is scaling. Our direct primary vendor negotiation framework eliminated 15% in subcontracting markups. Would you be open to a 10-minute briefing?"
            },
            {
                "touchpoint": "Day 3: LinkedIn Connection & Note",
                "body": f"Hi {decision_maker}, following up on my email regarding operational efficiency and vendor optimization at {company_name}."
            },
            {
                "touchpoint": "Day 7: Email 2 (Case Study Evidence)",
                "subject": f"Case study: 15% cost reduction for {company_name}",
                "body": f"Hi {decision_maker}, sharing a 1-page summary of how we structured vendor rate cards across 300+ deployments. Worth a brief discussion?"
            }
        ]
