import os

class ProductivityAgent:
    """Priority Matrix (Impact x Urgency x Probability) Engine."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace

    def get_top_daily_priorities(self):
        return [
            {"rank": 1, "action": "Review approval_queue.csv & dispatch EY GDS & Deloitte recruiter InMails", "impact": "High", "urgency": "Today"},
            {"rank": 2, "action": "Send 5 staged email drafts from Email_Drafts/ for priority analyst roles", "impact": "High", "urgency": "Today"},
            {"rank": 3, "action": "Review interview STAR defense narratives in interview_prep.json", "impact": "Medium", "urgency": "This Week"},
            {"rank": 4, "action": "Run independent_system_auditor.py to verify system integrity", "impact": "High", "urgency": "Periodic"}
        ]
