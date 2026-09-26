import os, json
from datetime import datetime

class InterviewAgent:
    """STAR Behavioral Frameworks, Technical Q&A & Interview Coach."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.prep_file = os.path.join(workspace, "interview_prep.json")

    def generate_prep_playbook(self):
        prep_data = {
            "candidate": "Aditya Mehra",
            "degree": "BBA International Business",
            "framework": "STAR (Situation, Task, Action, Result) with Concrete Metrics",
            "core_stories": [
                {
                    "title": "Aero India 2025 International Protocol & Operations Lead",
                    "situation": "Coordinating high-security foreign military & civil aerospace delegations under tight timelines.",
                    "task": "Manage pavilion access, VIP guest flow, and cross-functional coordination with international exhibitors.",
                    "action": "Built real-time dispatch schedule and deployed rapid contingency protocols for zero downtime.",
                    "result": "100% on-schedule delegation transit with zero protocol breaches across 5 summit days."
                },
                {
                    "title": "Tata Communications & Puma Large-Scale Brand Activations",
                    "situation": "Executing corporate brand activations across Bengaluru venues with strict sponsor SLA requirements.",
                    "task": "Lead on-ground vendor logistics, technical staging, and attendee engagement workflows.",
                    "action": "Implemented structured vendor check-ins and live attendee crowd-routing.",
                    "result": "Achieved 98% positive sponsor rating and on-budget execution."
                }
            ],
            "likely_questions": [
                "Walk me through your resume and why International Business consulting?",
                "How do you handle a crisis during a live client operation?",
                "Describe a situation where you had to influence senior decision makers.",
                "How do you prioritize multiple conflicting deadlines?"
            ],
            "timestamp": datetime.now().isoformat()
        }
        with open(self.prep_file, "w", encoding="utf-8") as f:
            json.dump(prep_data, f, indent=2)
        return prep_data
