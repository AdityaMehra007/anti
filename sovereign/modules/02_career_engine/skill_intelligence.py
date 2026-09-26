"""
ADI CAREER OS — SKILL INTELLIGENCE & PRIORITIZATION ENGINE (Sections 27, 28, 29, 60)
Analyzes market demand, computes multi-factor priority score, and generates project artifact blueprints.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any

@dataclass
class SkillMetric:
    skill_name: str
    category: str
    market_demand: float        # 1.0 - 10.0 scale
    career_relevance: float     # 1.0 - 10.0 scale
    salary_impact: float        # 1.0 - 10.0 scale
    practical_utility: float    # 1.0 - 10.0 scale
    learning_speed: float       # 1.0 - 10.0 scale (higher = faster to master)
    candidate_current_level: str # NOVICE, INTERMEDIATE, ADVANCED
    target_artifact: str

    @property
    def priority_score(self) -> float:
        """
        Section 28 Priority Formula:
        Priority = Demand * Career Relevance * Salary Impact * Practical Utility * Learning Speed / 1000
        """
        raw = (self.market_demand * self.career_relevance *
               self.salary_impact * self.practical_utility * self.learning_speed)
        return round(raw / 1000.0, 2)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["priority_score"] = self.priority_score
        return d


class SkillIntelligenceEngine:
    """Evaluates the core 6 skills from Section 29 and ranks learning priorities."""

    DEFAULT_CORE_SKILLS: List[SkillMetric] = [
        SkillMetric(
            skill_name="Advanced Excel & Power Query",
            category="Analytics / Operations",
            market_demand=9.5,
            career_relevance=9.8,
            salary_impact=8.0,
            practical_utility=9.9,
            learning_speed=9.0,
            candidate_current_level="INTERMEDIATE",
            target_artifact="Automated Sales & Inventory Reconciliation Dashboard with dynamic Pivot Models"
        ),
        SkillMetric(
            skill_name="SQL (Queries, Joins, CTEs, Window Functions)",
            category="Data & Analytics",
            market_demand=9.8,
            career_relevance=9.5,
            salary_impact=9.2,
            practical_utility=9.5,
            learning_speed=8.0,
            candidate_current_level="INTERMEDIATE",
            target_artifact="E-commerce Customer Churn & Cohort Retention Analysis database project"
        ),
        SkillMetric(
            skill_name="Power BI (Data Modeling & DAX)",
            category="Business Intelligence",
            market_demand=8.8,
            career_relevance=9.0,
            salary_impact=8.5,
            practical_utility=9.0,
            learning_speed=7.5,
            candidate_current_level="INTERMEDIATE",
            target_artifact="Executive Supply Chain Freight Performance interactive report"
        ),
        SkillMetric(
            skill_name="Business Analysis (BRD, FRD, User Stories, UAT)",
            category="Business Analysis",
            market_demand=9.0,
            career_relevance=9.9,
            salary_impact=8.8,
            practical_utility=9.5,
            learning_speed=8.5,
            candidate_current_level="INTERMEDIATE",
            target_artifact="End-to-End BRD & BPMN 2.0 Process Map for Automated Warehouse Dispatch"
        ),
        SkillMetric(
            skill_name="Operations Engineering (SOPs, Workflow Design, KPI Reporting)",
            category="Operations",
            market_demand=9.2,
            career_relevance=10.0,
            salary_impact=8.2,
            practical_utility=9.8,
            learning_speed=9.0,
            candidate_current_level="ADVANCED",
            target_artifact="Sovereign Incident Management & Service Desk SLA playbook"
        ),
        SkillMetric(
            skill_name="AI & Agentic Workflows (Prompting, Tool Calling, Structured Output)",
            category="AI Engineering",
            market_demand=9.9,
            career_relevance=10.0,
            salary_impact=9.5,
            practical_utility=9.9,
            learning_speed=8.5,
            candidate_current_level="ADVANCED",
            target_artifact="Autonomous Multi-Agent Career Intelligence System with SQLite persistence"
        )
    ]

    @classmethod
    def get_ranked_skills(cls) -> List[Dict[str, Any]]:
        """Returns skills sorted by Section 28 priority score descending."""
        skills = sorted(cls.DEFAULT_CORE_SKILLS, key=lambda s: s.priority_score, reverse=True)
        return [s.to_dict() for s in skills]

    @classmethod
    def audit_job_posting_skills(cls, job_text: str) -> Dict[str, Any]:
        """Audits required skills in a job posting and flags candidate coverage."""
        text = job_text.lower()
        coverage = {}
        for skill in cls.DEFAULT_CORE_SKILLS:
            key_terms = [skill.skill_name.lower().split()[0]]
            if "excel" in skill.skill_name.lower():
                key_terms.extend(["spreadsheet", "vlookup", "pivot"])
            elif "sql" in skill.skill_name.lower():
                key_terms.extend(["database", "queries", "relational"])
            elif "power bi" in skill.skill_name.lower():
                key_terms.extend(["dashboard", "bi tool", "tableau"])

            matched = any(kt in text for kt in key_terms)
            coverage[skill.skill_name] = {
                "in_job": matched,
                "candidate_level": skill.candidate_current_level,
                "proof_artifact": skill.target_artifact
            }

        in_job_count = sum(1 for v in coverage.values() if v["in_job"])
        candidate_covered_count = sum(1 for v in coverage.values() if v["in_job"] and v["candidate_level"] in ["INTERMEDIATE", "ADVANCED"])

        return {
            "total_skills_evaluated": len(cls.DEFAULT_CORE_SKILLS),
            "skills_in_job_count": in_job_count,
            "candidate_competency_match": candidate_covered_count,
            "match_ratio": round(candidate_covered_count / max(in_job_count, 1), 2),
            "breakdown": coverage
        }
