import json
from datetime import datetime

class AdaptiveEducationEngine:
    '''Personalized Learning Ecosystem & Mastery State Engine.'''
    def __init__(self):
        self.curriculum = {
            "BBA_IB_CORE": [
                {"id": "MOD-01", "name": "Global Supply Chain Logistics & Incoterms", "difficulty": "Intermediate"},
                {"id": "MOD-02", "name": "Financial Modeling for Business Analysts", "difficulty": "Advanced"},
                {"id": "MOD-03", "name": "Corporate Event Management & High-Stakes Operations", "difficulty": "Applied"}
            ]
        }

    def assess_mastery(self, student_id, module_id, quiz_score_pct):
        mastery_state = "MASTERED" if quiz_score_pct >= 85 else ("DEVELOPING" if quiz_score_pct >= 60 else "NEEDS_REVIEW")
        return {
            "student_id": student_id,
            "module_id": module_id,
            "score_pct": quiz_score_pct,
            "mastery_state": mastery_state,
            "recommended_next_step": "Proceed to Advanced Case Studies" if mastery_state == "MASTERED" else "Review foundational lecture notes.",
            "assessed_at": datetime.now().isoformat()
        }
