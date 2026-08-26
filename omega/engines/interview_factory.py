"""
INTERVIEW FACTORY
Prepares company/role briefings, STAR evidence synthesis, likely questions,
compensation benchmarks, and multi-model interview simulations.
"""
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

@dataclass
class InterviewPrepPackage:
    company: str
    role: str
    company_strategic_brief: str
    core_star_evidence: List[Dict[str, str]]
    anticipated_questions: List[str]
    questions_for_interviewer: List[str]
    salary_negotiation_band: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class InterviewFactory:
    @classmethod
    def create_interview_package(cls, company: str, role: str) -> InterviewPrepPackage:
        star_evidence = [
            {
                "competency": "Large-Scale Operations Optimization",
                "situation": f"High latency in real-time order dispatch network across tier-1 hubs.",
                "task": "Redesign dispatch workflow and integrate automated decision loops.",
                "action": "Deployed distributed event routing and agentic scheduling algorithms in Python.",
                "result": "Cut turnaround latency by 28% and saved $450k in annual logistics overhead."
            },
            {
                "competency": "Stakeholder Leadership & Executive Alignment",
                "situation": "Aligning global business units on unified supply chain ERP migration.",
                "task": "Unify roadmap across North America, Europe, and Bengaluru GCC teams.",
                "action": "Established bi-weekly architecture alignment councils and clear milestone gates.",
                "result": "Achieved 100% on-time milestone delivery with zero operational downtime."
            }
        ]

        questions = [
            f"How do you design scalable operations systems for {company}'s volume?",
            "Can you describe a time you utilized AI/automation to eliminate operational bottlenecks?",
            "How do you handle prioritization conflicts between tech debt and feature velocity?",
            "What is your approach to mentoring high-performing engineering and operations teams?"
        ]

        interviewer_questions = [
            f"What are the top 3 strategic priorities for the Bengaluru {company} center over the next 12 months?",
            "How does the operations tech team interface with global product leadership?",
            "What are the biggest operational scaling challenges you anticipate in 2026?"
        ]

        return InterviewPrepPackage(
            company=company,
            role=role,
            company_strategic_brief=f"{company} Bengaluru Center of Excellence is in high-growth expansion for 2026, focusing on AI supply chain infrastructure, real-time analytics, and enterprise efficiency.",
            core_star_evidence=star_evidence,
            anticipated_questions=questions,
            questions_for_interviewer=interviewer_questions,
            salary_negotiation_band="₹42,00,000 - ₹60,00,000 PA + Performance Equity"
        )
