import os, json
from datetime import datetime

class CareerIntelligenceAgent:
    """Strategic Career Positioning, Moat Analysis & Multi-Year Roadmap Engine."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.strategy_file = os.path.join(workspace, "career_strategy.json")

    def generate_strategy(self):
        strategy = {
            "candidate": "Aditya Mehra",
            "degree": "BBA - International Business (Dayananda Sagar University)",
            "graduation_year": 2026,
            "core_positioning": "Global Business Operations & Commercial Strategy Lead with proven high-stakes execution experience (Aero India 2025, Puma, Tata Communications, VH1 Supersonic).",
            "career_moats": [
                "Operational Resilience: Hands-on leadership in multi-thousand attendee international summits and corporate activations.",
                "International Trade & EXIM Acumen: Strong academic foundation in supply chain corridors, cross-border customs, and global freight economics.",
                "Commercial BD Track Record: Formal commendation at Pencil Mark Interior Solutions LLP for client acquisition."
            ],
            "target_job_families": [
                {"family": "Management Consulting & Advisory", "target_tier": "Tier A", "top_employers": ["EY GDS", "Deloitte US-India", "PwC SDC", "KPMG", "Accenture"]},
                {"family": "Corporate Strategy & Operations", "target_tier": "Tier A", "top_employers": ["Amazon", "Goldman Sachs", "IBM", "Walmart Global Tech"]},
                {"family": "Global Logistics & EXIM Management", "target_tier": "Tier B", "top_employers": ["Maersk", "DHL Global Forwarding", "Kuehne+Nagel"]}
            ],
            "roadmaps": {
                "1_year_goal": "Secure an Associate / Analyst role at a Tier-A consulting or tech enterprise (?6.5L - ?12.0L CTC base).",
                "3_year_goal": "Advance to Senior Business Operations Consultant / Team Lead managing cross-border commercial accounts.",
                "5_year_goal": "Lead Global Operations Strategy / Director of Business Operations or transition to high-growth startup founder."
            },
            "timestamp": datetime.now().isoformat()
        }
        with open(self.strategy_file, "w", encoding="utf-8") as f:
            json.dump(strategy, f, indent=2)
        return strategy
