---
name: unknown-engine
description: Proactive epistemic auditing answering 'What am I missing?' and 'Why hasn't this been done?' prior to capital or code commitment.
---

# Unknown Engine Skill

This skill operationalizes OMEGA Constitution Directive 124 and Directives 23, 68, 69, 71 of [`OMEGA_CONSTITUTION.md`](file:///e:/anti/OMEGA_CONSTITUTION.md): **The Systematic Epistemic Probe.**

---

## 1. The 3 Epistemic Interrogations

Prior to deploying new systems, raising funding, or cutting architecture releases, agents must execute the 3 questions:

### 1. "What Am I Missing?"
Probe for unstated assumptions, invisible prerequisites, external dependencies, and unmodeled failure modes:
- Are there unmodeled latency limits?
- Are thermodynamic power and cooling costs ignored?
- Are cross-jurisdictional legal and export hurdles assumed to be non-existent?

### 2. "Why Hasn't This Been Done?"
If an architectural or business idea appears trivial and high-yield, ask:
*Why did well-capitalized incumbents or brilliant researchers fail to execute this in the past?*
Locate the historical barrier (e.g. regulatory capture, lack of low-cost compute, unit economics inverted at small scale).

### 3. "Does This Really Work?"
Reject vibes, claims, and hand-wavy demos.
Demand:
- Working seams observable from the outside.
- Deterministic test runs passing 100%.
- Empirical load benchmarks.

---

## 2. Autonomous Execution Protocol

```python
from sovereign_continuum.capability_engine import UnknownEngine

engine = UnknownEngine()
audit = engine.audit_blind_spots(
    initiative_name="Autonomous M2M Energy Settlement",
    domain="Financial Infrastructure",
    assumptions=["instant zero-cost settlement", "global cross-border compliance"],
)

print(audit["missing_prerequisites"])
print(audit["unstated_assumptions"])
print(audit["why_hasnt_this_been_done"])
```
