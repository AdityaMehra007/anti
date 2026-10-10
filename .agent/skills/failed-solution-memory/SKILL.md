---
name: failed-solution-memory
description: Immutable indexing and querying of disproven hypotheses, architectural dead ends, and failure modes to enforce zero regression.
---

# Failed Solution Memory Skill

This skill operationalizes OMEGA Constitution Directive 123 and Directive 22 of the Master Specification: **Immutable memory of what did not work, why it failed, and under what conditions.**

---

## 1. The Zero-Regression Mandate

An organization that forgets its failed experiments expends its most valuable assets—time, computation, and capital—re-proving known dead ends.

Every architectural failure, aborted pivot, negative empirical benchmark, or broken simulation must be indexed immediately into [`FailedSolutionMemory`](file:///e:/anti/sovereign_continuum/capability_engine.py).

---

## 2. Postmortem Ingestion Schema

Every failed solution record requires:
- `problem_id`: Reference node in the Universal Problem Graph.
- `hypothesis`: The precise assumption tested.
- `failure_mode`: The observable symptom and break condition.
- `root_cause_analysis`: The shared physical, mathematical, economic, or regulatory origin.
- `conditions_under_which_it_failed`: Environmental variables (scale, temperature, latency, rate limits).
- `lessons_learned`: Explicit negative constraints preventing future agents from repeating the error.

---

## 3. Pre-Commit Interrogation Protocol

Before creating a new branch, designing a subsystem, or writing speculative code:
1. Query [`FailedSolutionMemory`](file:///e:/anti/sovereign_continuum/capability_engine.py):
   ```python
   from sovereign_continuum.capability_engine import FailedSolutionMemory

   memory = FailedSolutionMemory()
   match = memory.has_failed_previously(
       hypothesis=proposed_plan_text,
       problem_id=current_problem_id,
   )
   if match:
       raise RuntimeError(f"Hypothesis rejected by Failed Solution Memory: {match.record_id} - {match.failure_mode}")
   ```
2. If a match is found: **Halt immediately**. Read `lessons_learned` and modify the hypothesis before proceeding.
