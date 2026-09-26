import os, json

class SalesAgent:
    """B2B Lead Qualification, ICP Mapping & Commercial Outreach Strategist."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace

    def build_icp_profile(self):
        return {
            "ideal_customer_profile": "Mid-to-Large Enterprise Operations & Marketing Heads in Bengaluru",
            "qualification_criteria": ["Company size > 100", "Regular event/activation budgets", "Direct C-Suite access"],
            "discovery_questions": [
                "What is your current bottleneck in vendor coordination during live corporate activations?",
                "How do you currently track multi-channel ROI on brand activation summits?"
            ]
        }
