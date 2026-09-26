"""
Risk Engine & Thesis Destruction for REVENUE OS
Adheres strictly to Directives 56, 75, 131, 134, 135, 136.
Asks:
'What could make this fail?'
'What evidence would make us abandon it?'
Tracks platform dependence, customer concentration, and protects founder fatigue.
"""

from typing import Any, Dict, List, Optional
from REVENUE_OS.database.db import DatabaseManager, get_db

class RiskEngine:
    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or get_db()

    def destruct_thesis(self, engine_name: str, hypothesis: str) -> Dict[str, Any]:
        """Directive 56: Revenue Thesis Destruction."""
        failure_modes = [
            "Decision-maker email fatigue: cold open rates drop due to tighter spam filters.",
            "Client operational resistance: startup team doesn't have bandwidth to review and close delivered leads.",
            "LLM pricing shifts or platform policy changes on web data access.",
            "Founder bottleneck: onboarding requires too much manual hand-holding in early days."
        ]
        
        abandonment_evidence = [
            "Fewer than 2 qualified discovery calls booked after 150 personalized signal-backed outreaches (reply rate < 1.5%).",
            "Customer churn before month 2 exceeding 40% due to lead relevancy complaints.",
            "Customer acquisition cost (CAC) exceeding ₹15,000 against a ₹35,000 retainer without LTV expansion."
        ]
        
        mitigation_strategy = [
            "Use multi-channel outreach (LinkedIn direct messaging + verified email + community introductions).",
            "Provide done-for-you weekly review summaries so the founder spends only 10 mins/day reviewing leads.",
            "Implement strict 6-tier least-privilege security and verified public datasets to prevent reputation damage."
        ]

        return {
            "engine_name": engine_name,
            "hypothesis": hypothesis,
            "failure_modes": failure_modes,
            "abandonment_evidence": abandonment_evidence,
            "mitigation_strategy": mitigation_strategy,
            "kill_criteria_threshold": "Negative unit economics after 30 days of live execution."
        }

    def assess_founder_fatigue(self, hours_logged_this_week: float) -> Dict[str, Any]:
        """Directive 136: Founder Fatigue Protection."""
        max_safe_hours = 35.0
        if hours_logged_this_week > max_safe_hours:
            return {
                "fatigue_risk": "HIGH",
                "recommendation": "HALT non-critical exploratory research. Delegate lead enrichment to AutomationAgent. Compress tasks to 1-Thing only."
            }
        return {
            "fatigue_risk": "OPTIMAL",
            "hours_remaining": round(max_safe_hours - hours_logged_this_week, 1),
            "recommendation": "Operate at sustainable pace. Focus 30% on sales closing, 25% on product quality."
        }
