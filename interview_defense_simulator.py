#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY CAREER OS: HIGH-STAKES INTERVIEW DEFENSE SIMULATOR
========================================================================================
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
Purpose:
  Simulates enterprise case and behavioral interviews across Tier-1 GCCs,
  consulting firms, and MNCs (Accenture, Deloitte, Goldman Sachs, Amazon, DHL).
  Evaluates candidate responses against a rigorous 5-pillar STAR + Quantitative Metric rubric.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SCENARIOS_JSON = ROOT_DIR / "data" / "interview_defense_scenarios.json"

@dataclass
class DefenseEvaluation:
    scenario_id: str
    overall_score: float
    star_breakdown: Dict[str, float]
    metrics_cited: int
    strengths: List[str]
    gaps: List[str]
    readiness_status: str

class InterviewDefenseSimulator:
    """Evaluates and coaches candidate responses against defense scenarios."""

    def __init__(self, scenarios_path: Optional[Path] = None):
        self.scenarios_path = scenarios_path or SCENARIOS_JSON
        self.scenarios = self.load_scenarios()

    def load_scenarios(self) -> List[Dict[str, Any]]:
        if self.scenarios_path.exists():
            try:
                with open(self.scenarios_path, "r", encoding="utf-8-sig") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def get_scenario(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        for s in self.scenarios:
            if s["scenario_id"] == scenario_id:
                return s
        return None

    def evaluate_response(self, scenario_id: str, candidate_text: str) -> DefenseEvaluation:
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return DefenseEvaluation(
                scenario_id=scenario_id,
                overall_score=0.0,
                star_breakdown={"situation": 0.0, "task": 0.0, "action": 0.0, "result": 0.0},
                metrics_cited=0,
                strengths=[],
                gaps=["Scenario ID not found in database"],
                readiness_status="INVALID_SCENARIO"
            )

        text_lower = candidate_text.lower()
        strengths = []
        gaps = []

        # 1. Situation Analysis (20 pts)
        sit_stems = ["aero india", "yelahanka", "vendor", "stall", "contract", "activat", "pipelin", "client", "disput", "gate", "shipment"]
        sit_hits = sum(1 for kw in sit_stems if kw in text_lower)
        sit_score = min(20.0, sit_hits * 6.7)
        if sit_score >= 13.0:
            strengths.append("Crisp situational grounding and operational context")
        else:
            gaps.append("Clarify the operational stakes and organizational context upfront")

        # 2. Task & Ownership (20 pts)
        task_stems = ["task", "mandat", "ensur", "protect", "deadlin", "objectiv", "complian", "uptim", "responsib", "sla", "goal"]
        task_hits = sum(1 for kw in task_stems if kw in text_lower)
        task_score = min(20.0, task_hits * 6.7)
        if task_score >= 13.0:
            strengths.append("Clear ownership of the core mandate and delivery constraints")
        else:
            gaps.append("Explicitly state your personal responsibility and deadline")

        # 3. Action Specificity (25 pts)
        action_stems = ["deploy", "direct", "authoriz", "engineer", "coordinat", "negotiat", "execut", "initiat", "dispatch", "decoupl", "quarantin", "analyz", "resolv", "manag"]
        action_hits = sum(1 for kw in action_stems if kw in text_lower)
        action_score = min(25.0, action_hits * 6.25)
        if action_score >= 18.0:
            strengths.append("Decisive operational levers and autonomous leadership demonstrated")
        else:
            gaps.append("Detail the exact procedural steps and tools you executed")

        # 4. Result & Metrics Quantification (25 pts)
        res_stems = ["achiev", "complet", "zero", "shrinkag", "uptim", "preserv", "recover", "margin", "accura", "reduc", "ahead of", "sign-off", "success"]
        res_hits = sum(1 for kw in res_stems if kw in text_lower)
        res_score = min(25.0, res_hits * 6.25)

        # Count quantitative metrics cited
        expected_metrics = scenario.get("key_metrics_to_recite", [])
        metrics_cited = 0
        for em in expected_metrics:
            tokens = [t.lower() for t in re.findall(r"\b(?:\d+[\.,]?\d*[%kL]?|zero|100%)\b", em.lower())]
            if any(tok in text_lower for tok in tokens if len(tok) > 1):
                metrics_cited += 1

        if metrics_cited >= 2:
            strengths.append(f"Strong quantitative proof-of-work: cited {metrics_cited} core metrics")
        else:
            gaps.append("Anchor the conclusion with exact numbers (e.g. percentages, INR saved, attendee footfall)")

        # 5. Delivery Conciseness & Structure (10 pts)
        word_count = len(candidate_text.split())
        structure_score = 10.0 if (35 <= word_count <= 250) else (5.0 if word_count > 250 else 3.0)

        metrics_bonus = min(10.0, metrics_cited * 5.0)
        overall = round(min(100.0, sit_score + task_score + action_score + res_score + structure_score + metrics_bonus), 1)

        if overall >= 80.0:
            status = "INTERVIEW_READY_EXEMPLAR"
        elif overall >= 60.0:
            status = "SOLID_FOUNDATION"
        else:
            status = "NEEDS_REHEARSAL"

        return DefenseEvaluation(
            scenario_id=scenario_id,
            overall_score=overall,
            star_breakdown={
                "situation": sit_score,
                "task": task_score,
                "action": action_score,
                "result": res_score,
                "structure": structure_score
            },
            metrics_cited=metrics_cited,
            strengths=strengths,
            gaps=gaps,
            readiness_status=status
        )

def main():
    sim = InterviewDefenseSimulator()
    scenarios = sim.load_scenarios()
    print("=" * 80)
    print(f"  ANTIGRAVITY CAREER OS: INTERVIEW DEFENSE SIMULATOR ({len(scenarios)} SCENARIOS)")
    print("=" * 80)
    for idx, s in enumerate(scenarios, 1):
        print(f"{idx}. [{s['scenario_id']}] {s['title']}")
        print(f"   Target: {', '.join(s['target_companies'])}")
        print(f"   Probe:  \"{s['tough_interviewer_probe']}\"")
        print()

if __name__ == "__main__":
    main()
