import json
from datetime import datetime

class PersonalDecisionOS:
    '''High-ROI Daily Prioritization & Habit Optimization Engine.'''
    def __init__(self):
        self.priorities = []

    def evaluate_next_action(self, candidate_actions):
        scored_actions = []
        for a in candidate_actions:
            # Impact (1-10) * Urgency (1-10) * Probability (0.0-1.0)
            score = a.get("impact", 5) * a.get("urgency", 5) * a.get("probability", 0.8)
            scored_actions.append({
                "action": a.get("title"),
                "roi_score": round(score, 2),
                "quadrant": "DO_NOW" if score >= 35 else "DO_THIS_WEEK"
            })
        scored_actions.sort(key=lambda x: x["roi_score"], reverse=True)
        return scored_actions
