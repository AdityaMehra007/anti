"""
interview_master.py - Agent 5: Real-World Interview Simulator & STAR Coach
===========================================================================
Draws live company questions from the KnowledgeLearningVault, formats STAR/CAR
responses using verified truth claims, and delivers rigorous mock interview sessions.
"""

from typing import Dict, List, Any, Optional
from apex_career_os.core.truth_layer import STAR_REPOSITORY, get_candidate_profile
from apex_career_os.core.knowledge_learning_vault import KnowledgeLearningVault

class InterviewMasterAgent:
    def __init__(self, vault: Optional[KnowledgeLearningVault] = None):
        self.vault = vault or KnowledgeLearningVault()
        self.candidate = get_candidate_profile()

    def generate_interview_prep_pack(self, company: str, role: str) -> Dict[str, Any]:
        """Generates a complete tailored interview prep pack for a specific company and role."""
        company_intel = self.vault.get_company_intelligence(company)
        learned_questions = self.vault.get_interview_questions_for_company(company, limit=6)

        # Build STAR situational responses
        tailored_answers = []
        for q in learned_questions:
            q_text = q.get("question_text", "")
            matched_star = self._match_star_framework(q_text)
            tailored_answers.append({
                "question": q_text,
                "round_type": q.get("round_type", "Behavioral"),
                "recommended_star_framework": matched_star,
                "coaching_tip": "Focus on the quantified result and zero-defect execution."
            })

        curveball_defense = self._generate_curveball_defenses()

        return {
            "target_company": company,
            "target_role": role,
            "company_culture_dna": company_intel.get("culture_dna") if company_intel else "Execution-driven, high accountability",
            "interview_stages": company_intel.get("interview_stages") if company_intel else ["HR Screen", "Functional Loop", "Leadership Fit"],
            "tailored_qa_bank": tailored_answers,
            "curveball_defenses": curveball_defense
        }

    def _match_star_framework(self, question: str) -> Dict[str, str]:
        q_lower = question.lower()
        if any(x in q_lower for x in ["distributed", "reconciliation", "latency", "concurrency", "circuit breaker", "saga", "idempotency", "throughput"]):
            star = STAR_REPOSITORY[4] # STAR-005: ApexFlow
        elif any(x in q_lower for x in ["agent", "llm", "tokens", "budget", "hallucination", "sandbox", "guardrail"]):
            star = STAR_REPOSITORY[5] # STAR-006: ApexAgentic
        elif any(x in q_lower for x in ["market", "yield", "trade", "ucp", "letter of credit", "customs", "icegate", "fx", "incoterms"]):
            star = STAR_REPOSITORY[6] # STAR-007: Omega Global Markets
        elif any(x in q_lower for x in ["pressure", "deadline", "crisis", "security", "high-stakes", "threatened"]):
            star = STAR_REPOSITORY[0] # STAR-001: Aero India
        elif any(x in q_lower for x in ["vendor", "cost", "negotiate", "supplier", "procurement", "budget"]):
            star = STAR_REPOSITORY[1] # STAR-002: 15% Vendor savings
        elif any(x in q_lower for x in ["sales", "client", "commercial", "revenue", "persuade", "convert"]):
            star = STAR_REPOSITORY[2] # STAR-003: Pencil Mark BD
        elif any(x in q_lower for x in ["quality", "ai", "data", "accuracy", "detail", "process"]):
            star = STAR_REPOSITORY[3] # STAR-004: Instawork AI
        else:
            star = STAR_REPOSITORY[0]

        return {
            "situation": star["situation"],
            "task": star["task"],
            "action": star["action"],
            "result": star["result"]
        }

    def _generate_curveball_defenses(self) -> List[Dict[str, str]]:
        return [
            {
                "curveball": "Why should we hire a BBA graduate over an engineering graduate for this operational or analyst role?",
                "bulletproof_defense": (
                    "While engineering graduates bring strong technical theory, I bring 8+ years of battle-tested operational grit, "
                    "formal training in International Business, Incoterms, and landed cost modeling, and proven frontline leadership. "
                    "I have negotiated directly with primary fabricators to save 15% hard cash and managed 100,000+ visitors at Aero India "
                    "with zero security breaches. I execute from Day 1 without requiring months of commercial acclimation."
                )
            },
            {
                "curveball": "Can someone from a business background really build distributed systems that process 56,000 transactions/second?",
                "bulletproof_defense": (
                    "Yes, because I do not 'vibe code'—I build from first principles. In ApexFlow, I implemented lazy async locking "
                    "to prevent event loop deadlocks, cryptographic SHA-256 idempotency hashing with SQLite WAL, self-healing circuit breakers, "
                    "and asynchronous saga rollback DAGs. The engine was benchmarked at 56,179 records/sec at <18 microseconds latency with 100% "
                    "green automated tests. My business background ensures I build high-ROI systems without speculative bloat."
                )
            },
            {
                "curveball": "What happens when a primary vendor or supplier fails 2 hours before a major launch?",
                "bulletproof_defense": (
                    "In 300+ live event and exhibition deployments, contingency is standard operating procedure. I maintain an indexed "
                    "redundancy roster of secondary tier-1 vendors across Bangalore with pre-agreed emergency dispatch SLAs. "
                    "At Bangalore Club's Trilogy concert, when secondary AV wiring showed interference, my team hot-swapped to backup lines "
                    "in under 4 minutes with zero artist interruption."
                )
            },
            {
                "curveball": "How do you justify targeting ₹18L-₹30L+ compensation when standard fresher campus packages are ₹4L-₹7L?",
                "bulletproof_defense": (
                    "Standard campus hires require 6 months of onboarding, handholding, and commercial ramp-up. I bring 8+ years of business exposure, "
                    "a verified track record of ₹1.5L+ commercial sales closures, 15% hard procurement cost cuts, and production-tested software systems "
                    "with 114 passing tests. I am not entering as a student trainee; I enter as an immediate high-velocity operator and systems "
                    "builder whose first-quarter impact pays for my compensation several times over."
                )
            },
            {
                "curveball": "Where do you see yourself in 3 to 5 years?",
                "bulletproof_defense": (
                    "In 3 years, I plan to have mastered your operational or commercial pipeline, taking full ownership of multi-million "
                    "rupee vendor contracts or high-growth account portfolios. By Year 5, my goal is to transition into Founders' Office, "
                    "Strategic Program Direction, or Operations Leadership, scaling organizational leverage and profitability."
                )
            }
        ]
