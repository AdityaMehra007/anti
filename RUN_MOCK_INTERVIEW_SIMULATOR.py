#!/usr/bin/env python3
"""
RUN_MOCK_INTERVIEW_SIMULATOR.py - Interactive STAR Interview Arena & Evaluation Suite
=====================================================================================
Evaluates candidate responses against the STAR framework, verified ground truth claims,
and Level 12/13/14 executive benchmarks across technical and operational domains.

Usage:
  python RUN_MOCK_INTERVIEW_SIMULATOR.py --eval-all       # Run automated benchmark evaluation across all 5 tracks
  python RUN_MOCK_INTERVIEW_SIMULATOR.py --interactive    # Live interactive command-line interview simulation
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Ensure apex_career_os is in path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from apex_career_os.core.truth_layer import (
    CandidateProfile, get_candidate_profile, STAR_REPOSITORY, VERIFIED_EVIDENCE
)
from apex_career_os.agents.interview_master import InterviewMasterAgent

BENCHMARK_INTERVIEW_TRACKS = [
    {
        "track_id": "TRACK-01",
        "title": "High-Concurrency Distributed Systems & Reconciliation",
        "target_companies": ["Razorpay", "Goldman Sachs", "Amazon", "PhonePe"],
        "questions": [
            {
                "qid": "Q-101",
                "question": "Tell me about a time you had to design or operate a high-throughput transaction system where duplicate execution or data drift could cause severe financial loss.",
                "context": "Assesses distributed systems architecture, idempotency, latency, and fault tolerance.",
                "star_id": "STAR-005",
                "target_keywords": ["apexflow", "reconciliation", "idempotency", "sha-256", "56,179", "latency", "circuit breaker", "saga"],
                "model_answer": (
                    "In ERP and fintech procurement, ledger drift and duplicate payments cost millions. Our objective was to guarantee 100% duplicate prevention "
                    "under 50,000+ burst load. To solve this, I architected ApexFlow, a high-throughput 3-way reconciliation engine (PO vs GRN vs Invoice). "
                    "I implemented a cryptographic SHA-256 idempotency ledger with SQLite WAL, a 3-state self-healing circuit breaker, and an async saga rollback DAG. "
                    "Under stress testing, the engine clocked 56,179 records/second with p99 latency under 0.02 milliseconds and 0% duplicate leakage, verified across 15 automated test suites."
                )
            },
            {
                "qid": "Q-102",
                "question": "How do you prevent circular event loop deadlocks and thread-safety race conditions in concurrent Python microservices?",
                "context": "Assesses low-level asynchronous runtime mechanics and memory concurrency.",
                "star_id": "STAR-005",
                "target_keywords": ["lock", "asyncio", "lazy", "rlock", "thread", "deadlock"],
                "model_answer": (
                    "When scaling concurrent microservices, binding asyncio.Lock() at import time attaches it to whatever loop was active at import, causing "
                    "fatal deadlocks when invoked from worker loops. Our objective was 100% thread safety across 50+ concurrent background tasks. "
                    "I implemented lazy property lock initialization so locks bind exclusively inside active running coroutines. Furthermore, for in-memory telemetry "
                    "registries accessed across threads, I upgraded non-reentrant threading.Lock to threading.RLock, allowing re-entrant inspection without self-deadlock. "
                    "This delivered 0 deadlocks across 114 test suites and sustained 56,000 ops/sec."
                )
            }
        ]
    },
    {
        "track_id": "TRACK-02",
        "title": "Autonomous Agent Runtime & AI Guardrails",
        "target_companies": ["OpenAI Ecosystem", "Anthropic Partners", "Enterprise AI Labs"],
        "questions": [
            {
                "qid": "Q-201",
                "question": "Autonomous AI agents frequently get stuck in infinite retry loops and burn thousands of dollars in tokens. How did you solve this?",
                "context": "Assesses cost governors, epistemic failed-solution memory, and agent runtime safety.",
                "star_id": "STAR-006",
                "target_keywords": ["apexagentic", "token governor", "failed solution memory", "sha-256", "hitl", "cost"],
                "model_answer": (
                    "Unconstrained agent loops suffer from cyclic hallucination and runaway token spend. Our task was to enforce hard cost bounds and zero repetitive errors. "
                    "I built the ApexAgentic Task Runtime with three deterministic layers: first, a sliding-window Token & Cost Governor with strict 100,000 token budget caps; "
                    "second, an Epistemic Failed Solution Memory that computes SHA-256 signatures of failed attempts and intercepts repeated dead-ends before calling the LLM; and third, a "
                    "cryptographically signed HITL approval gate for destructive tool invocations. This eliminated 100% of cyclic loops and reduced redundant token spend by 50% across 4 automated test suites."
                )
            }
        ]
    },
    {
        "track_id": "TRACK-03",
        "title": "Quantitative Markets & EXIM Trade Compliance",
        "target_companies": ["Goldman Sachs", "JP Morgan Chase", "Maersk", "DHL Global Forwarding"],
        "questions": [
            {
                "qid": "Q-301",
                "question": "How do you bridge international trade regulations, customs landed costs, and quantitative financial modeling?",
                "context": "Assesses UCP 600 Letter of Credit rules, ICEGATE landed cost formulas, and yield curve mathematics.",
                "star_id": "STAR-007",
                "target_keywords": ["omega", "ucp 600", "nelson-siegel", "icegate", "customs", "landed cost", "letter of credit"],
                "model_answer": (
                    "Through formal International Business training and building the Omega Global Markets Nexus. Our objective was zero document discrepancy leakage "
                    "and accurate landed cost calculation. On the quantitative side, I implemented Nelson-Siegel 4-parameter sovereign yield curve fitting and continuous limit order books. "
                    "On the trade side, I automated UCP 600 Letter of Credit discrepancy audits and built an ICEGATE customs landed-cost calculator applying 10% Basic Customs Duty (BCD), "
                    "10% Social Welfare Surcharge (SWS), and 18% IGST. The engine achieved 0 document discrepancies and 100% green status across 45 test suites."
                )
            }
        ]
    },
    {
        "track_id": "TRACK-04",
        "title": "Mission-Critical Frontline Operations & Crowd Governance",
        "target_companies": ["Amazon Operations", "Aero India / Defense", "Global Event Orgs"],
        "questions": [
            {
                "qid": "Q-401",
                "question": "Describe a crisis situation where you faced extreme crowd pressure, security constraints, and zero margin for error.",
                "context": "Assesses calm under pressure, military-grade protocol enforcement, and physical ops execution.",
                "star_id": "STAR-001",
                "target_keywords": ["aero india", "100,000", "security", "shrinkage", "opening", "badge"],
                "model_answer": (
                    "At Aero India 2025 at Yelahanka Air Force Station, I directed commercial pavilion operations with 100,000+ visitors under strict military security protocols. "
                    "Our objective was to guarantee 100% on-time opening, absolute credential enforcement, and zero stock shrinkage. "
                    "I established a 24-hour advance badge triage system, scheduled automated batch replenishment to eliminate stockouts, and managed our team to "
                    "achieve 100% on-time morning opening daily, zero security breaches, and 0.0% inventory shrinkage across 7 days with 5,000+ qualified leads engaged."
                )
            }
        ]
    },
    {
        "track_id": "TRACK-05",
        "title": "Strategic Procurement, Vendor Governance & B2B Commercials",
        "target_companies": ["Accenture Strategy", "Founders' Office", "High-Growth Scaleups"],
        "questions": [
            {
                "qid": "Q-501",
                "question": "Walk me through how you negotiated with suppliers to drive hard-dollar savings without damaging vendor relationships.",
                "context": "Assesses commercial negotiation, rate cards, and direct tier-1 vendor partnerships.",
                "star_id": "STAR-002",
                "target_keywords": ["vendor", "15%", "savings", "tier-1", "markup", "rate card"],
                "model_answer": (
                    "Third-party event and staging aggregators routinely mark up fabrication, sound, and lighting quotes by 20% to 30%. Over 300+ project deployments, "
                    "our objective was to cut vendor markup by >10% while guaranteeing SLA compliance. I bypassed broker middlemen, identified tier-1 primary fabricators, "
                    "and offered guaranteed volume multi-deployment commitments. In exchange, I negotiated locked-in rate cards yielding 15% net cost savings and 100% on-time delivery across all 300+ events."
                )
            }
        ]
    }
]

class MockInterviewSimulator:
    def __init__(self):
        self.profile = get_candidate_profile()
        self.agent = InterviewMasterAgent()
        self.transcripts_dir = ROOT_DIR / "applications_generated" / "interview_transcripts"
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)

    def evaluate_response(self, candidate_response: str, question_meta: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a candidate response along 4 core dimensions:
        1. STAR / Structure (25 pts)
        2. Metric & Specificity Density (25 pts)
        3. Truth Layer & Keyword Alignment (25 pts)
        4. Conciseness & Executive Tone (25 pts)
        """
        resp_lower = candidate_response.lower()
        words = candidate_response.split()
        word_count = len(words)

        # 1. STAR Structure check
        has_situation = any(w in resp_lower for w in ["at", "during", "when", "in", "faced", "situation"])
        has_task = any(w in resp_lower for w in ["task", "needed to", "goal", "objective", "required", "responsible"])
        has_action = any(w in resp_lower for w in ["built", "implemented", "engineered", "negotiated", "established", "directed", "constructed", "architected"])
        has_result = any(w in resp_lower for w in ["result", "achieved", "reduced", "delivered", "clocked", "%", "saved", "zero"])

        star_score = 0
        star_feedback = []
        if has_situation: star_score += 6.25; star_feedback.append("Situation established")
        else: star_feedback.append("Missing clear context/situation")

        if has_task: star_score += 6.25; star_feedback.append("Task defined")
        else: star_feedback.append("Missing explicit objective/task")

        if has_action: star_score += 6.25; star_feedback.append("Action described")
        else: star_feedback.append("Missing concrete technical/operational actions")

        if has_result: star_score += 6.25; star_feedback.append("Result quantified")
        else: star_feedback.append("Missing quantified business or engineering outcome")

        # 2. Metric & Number Density
        num_count = sum(1 for w in words if any(char.isdigit() for char in w))
        if num_count >= 3:
            metric_score = 25.0
            metric_feedback = f"Excellent quantification ({num_count} metrics cited)"
        elif num_count >= 1:
            metric_score = 15.0
            metric_feedback = f"Moderate quantification ({num_count} metrics cited; add more hard figures)"
        else:
            metric_score = 5.0
            metric_feedback = "Weak quantification: cite specific percentages, throughput numbers, or rupee amounts"

        # 3. Target Keyword & Evidence Alignment
        target_kw = question_meta.get("target_keywords", [])
        matched_kw = [kw for kw in target_kw if kw.lower() in resp_lower]
        kw_ratio = len(matched_kw) / max(len(target_kw), 1)
        kw_score = min(25.0, round(kw_ratio * 30.0, 1))
        kw_feedback = f"Matched {len(matched_kw)}/{len(target_kw)} target technical concepts ({', '.join(matched_kw)})"

        # 4. Conciseness & Word Count Check (Ideal: 75 - 180 words)
        if 60 <= word_count <= 180:
            concise_score = 25.0
            concise_feedback = f"Optimal executive length ({word_count} words)"
        elif word_count < 60:
            concise_score = max(5.0, 25.0 - (60 - word_count) * 0.4)
            concise_feedback = f"Too brief ({word_count} words) - elaborate on specific engineering or operational steps"
        else:
            concise_score = max(10.0, 25.0 - (word_count - 180) * 0.2)
            concise_feedback = f"Verbose ({word_count} words) - tighten response to under 180 words for executive clarity"

        total_score = round(star_score + metric_score + kw_score + concise_score, 1)

        rating = (
            "OFFER EXTENDED (L13/L14 TOP TIER)" if total_score >= 88 else
            "STRONG HIRE (L12)" if total_score >= 75 else
            "LEAN HIRE (ADDITIONAL LOOP)" if total_score >= 60 else
            "NO HIRE (NEEDS RE-ALIGNMENT)"
        )

        return {
            "total_score": total_score,
            "rating": rating,
            "dimensions": {
                "star_structure": {"score": star_score, "max": 25, "feedback": star_feedback},
                "metrics_density": {"score": metric_score, "max": 25, "feedback": metric_feedback},
                "keyword_alignment": {"score": kw_score, "max": 25, "feedback": kw_feedback},
                "conciseness": {"score": round(concise_score, 1), "max": 25, "feedback": concise_feedback}
            }
        }

    def run_benchmark_evaluation(self) -> Dict[str, Any]:
        """Runs the automated benchmark evaluation across all 5 tracks using model candidate responses."""
        print("=" * 80)
        print("    OMEGA APEX CAREER OS - AUTOMATED INTERVIEW BENCHMARK EVALUATOR")
        print("=" * 80)
        print(f"Candidate: {self.profile.full_name} ({self.profile.preferred_name}) | Education: {self.profile.degree}")
        print(f"Compensation Band Anchor: INR {self.profile.min_ctc_inr//100000}L min / INR {self.profile.target_ctc_inr//100000}L target / INR {self.profile.aspirational_ctc_inr//100000}L aspirational")
        print("-" * 80)

        results = []
        overall_scores = []

        for track in BENCHMARK_INTERVIEW_TRACKS:
            print(f"\n[TRACK] {track['track_id']}: {track['title']}")
            print(f"  Target Employers: {', '.join(track['target_companies'])}")

            for q in track["questions"]:
                print(f"\n  [QUESTION {q['qid']}] {q['question']}")
                candidate_resp = q["model_answer"]
                eval_res = self.evaluate_response(candidate_resp, q)
                overall_scores.append(eval_res["total_score"])

                print(f"  --> Score: {eval_res['total_score']}/100 [{eval_res['rating']}]")
                print(f"  --> STAR Feedback: {', '.join(eval_res['dimensions']['star_structure']['feedback'])}")
                print(f"  --> Metrics: {eval_res['dimensions']['metrics_density']['feedback']}")
                print(f"  --> Alignment: {eval_res['dimensions']['keyword_alignment']['feedback']}")
                print(f"  --> Word Count: {eval_res['dimensions']['conciseness']['feedback']}")

                results.append({
                    "track_id": track["track_id"],
                    "track_title": track["title"],
                    "qid": q["qid"],
                    "question": q["question"],
                    "candidate_response": candidate_resp,
                    "evaluation": eval_res
                })

        avg_score = round(sum(overall_scores) / len(overall_scores), 1)
        print("\n" + "=" * 80)
        print(f"FINAL BENCHMARK SCORE: {avg_score} / 100")
        verdict = "UNANIMOUS OFFER - LEVEL 13/14 ARCHITECT & OPERATIONS LEAD" if avg_score >= 85 else "STRONG HIRE"
        print(f"OVERALL COMMITTEE VERDICT: {verdict}")
        print("=" * 80)

        # Save transcript
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = self.transcripts_dir / f"benchmark_evaluation_{timestamp}.json"
        summary = {
            "candidate": self.profile.full_name,
            "timestamp": timestamp,
            "average_score": avg_score,
            "verdict": verdict,
            "evaluations": results
        }
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        print(f"\n[SAVED] Benchmark evaluation report saved to: {out_file}")
        return summary

    def run_interactive_simulation(self):
        """Runs a live command-line mock interview session."""
        print("=" * 80)
        print("    OMEGA APEX CAREER OS - INTERACTIVE MOCK INTERVIEW SIMULATOR")
        print("=" * 80)
        print("Welcome, Aditya. Type your answer to each question, or press ENTER on an empty line")
        print("to submit. Type 'skip' to move to next question, or 'quit' to exit.\n")

        for track in BENCHMARK_INTERVIEW_TRACKS:
            print(f"\n" + "-" * 70)
            print(f"DOMAIN: {track['title']}")
            print("-" * 70)

            for q in track["questions"]:
                print(f"\n[INTERVIEWER] {q['question']}")
                print(f"(Context: {q['context']})")
                print("Your response: ")

                user_input = sys.stdin.readline().strip()
                if not user_input or user_input.lower() == 'skip':
                    print("  [SKIPPED] Reviewing model benchmark response:")
                    print(f"  \"{q['model_answer']}\"")
                    continue
                if user_input.lower() == 'quit':
                    print("\nExiting mock interview session. Keep practicing!")
                    return

                eval_res = self.evaluate_response(user_input, q)
                print("\n[AI EVALUATION]")
                print(f"Score: {eval_res['total_score']}/100 [{eval_res['rating']}]")
                print(f"STAR Structure: {eval_res['dimensions']['star_structure']['score']}/25 ({', '.join(eval_res['dimensions']['star_structure']['feedback'])})")
                print(f"Metrics: {eval_res['dimensions']['metrics_density']['feedback']}")
                print(f"Keywords: {eval_res['dimensions']['keyword_alignment']['feedback']}")
                print(f"Conciseness: {eval_res['dimensions']['conciseness']['feedback']}")
                print("\n[RECOMMENDED BENCHMARK ANSWER]")
                print(f"  \"{q['model_answer']}\"")
                print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description="Run Mock Interview Simulator & STAR Coach")
    parser.add_argument("--eval-all", action="store_true", help="Run automated benchmark evaluation across all tracks")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive CLI interview session")
    args = parser.parse_args()

    simulator = MockInterviewSimulator()
    if args.interactive:
        simulator.run_interactive_simulation()
    else:
        # Default or --eval-all
        simulator.run_benchmark_evaluation()

if __name__ == "__main__":
    main()
