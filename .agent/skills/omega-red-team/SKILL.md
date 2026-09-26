---
name: omega-red-team
description: Adversarial stress-testing and failure-mode analysis applying the 12 core red team probes from OMEGA Constitution Section 14.
---

# OMEGA Red Team Skill

This skill enforces Section 14 of [`OMEGA_CONSTITUTION.md`](../../OMEGA_CONSTITUTION.md) to stress-test plans, strategies, codebases, and operations before real-world deployment.

## The 12 Adversarial Probes
For every proposal or release candidate, rigorously answer:
1. **What could fail?** (Identify all failure modes across infrastructure, logic, and assumptions).
2. **What assumption is weakest?** (Isolate unverified beliefs and single-source dependencies).
3. **What are we missing?** (Surface blind spots and omitted operational requirements).
4. **What would a brilliant competitor do?** (Simulate counter-moves, price-cuts, and feature copies).
5. **What would a customer hate?** (Identify friction, latency, unexpected costs, and confusing UX).
6. **What could cause catastrophic failure?** (Analyze systemic risks and existential threats).
7. **What could destroy trust?** (Examine data leakage, false claims, and broken promises).
8. **What could bankrupt us?** (Stress-test burn rate, unit economics, and token runaways).
9. **What makes this obsolete?** (Analyze technological disruption and paradigm shifts).
10. **What happens if the market is 50% smaller?** (Model low-demand survival scenarios).
11. **What happens if acquisition cost doubles?** (Stress-test unit economics and organic referral loops).
12. **What happens if key technology or dependencies fail?** (Model vendor outage, API deprecation, and fallback redundancy).

## Output Format
Deliver a structured Red Team Dossier:
- **Critical Vulnerabilities (P0)**: Existential threats requiring immediate redesign.
- **Moderate Risks (P1)**: Assumptions requiring cheap experiment validation.
- **Resilience Safeguards**: Specific defensive measures, fallbacks, and circuit breakers.
