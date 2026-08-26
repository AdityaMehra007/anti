"""
CAREER SKILL GAP ENGINE
Extracts requirements from real job postings, aggregates frequencies,
identifies candidate skill gaps, and ranks Skill ROI.
"""
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class SkillMetric:
    skill_name: str
    market_frequency_pct: float
    importance_tier: str  # CRITICAL, HIGH, DESIRABLE
    candidate_has: bool
    skill_gap_status: str # MATCH, GAP, EXPANDING
    roi_score: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class SkillGapEngine:
    CANDIDATE_SKILLS = [
        "python", "operations strategy", "supply chain analytics", "process optimization",
        "sql", "agentic ai", "system design", "distributed systems", "workflow automation"
    ]

    def analyze_skill_gaps(self, job_requirements_list: List[List[str]]) -> List[SkillMetric]:
        skill_counts: Dict[str, int] = {}
        total_postings = max(1, len(job_requirements_list))

        for reqs in job_requirements_list:
            for r in reqs:
                normalized = r.strip().lower()
                skill_counts[normalized] = skill_counts.get(normalized, 0) + 1

        metrics = []
        for skill, count in skill_counts.items():
            freq = round((count / total_postings) * 100, 1)
            has_skill = any(s in skill for s in self.CANDIDATE_SKILLS)
            importance = "CRITICAL" if freq >= 60 else ("HIGH" if freq >= 30 else "DESIRABLE")
            gap_status = "MATCH" if has_skill else "GAP"
            roi = round((freq * 1.5) if not has_skill else (freq * 0.5), 1)

            metrics.append(SkillMetric(
                skill_name=skill.title(),
                market_frequency_pct=freq,
                importance_tier=importance,
                candidate_has=has_skill,
                skill_gap_status=gap_status,
                roi_score=roi
            ))

        metrics.sort(key=lambda m: m.roi_score, reverse=True)
        return metrics
