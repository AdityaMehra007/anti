# ANTIGRAVITY OMNIVERSE: ARCHITECTURAL DECISION LOG (ADR)
## Document ID: `OMNIVERSE-09-DECISIONS` | Status: APPROVED | Mode: OMNI-X PRODUCTION

---

## 1. Governance & Ruling Standard

In accordance with Section 3 of AGENTS.md and the Master Constitution (ADI_OMNI_CODEX.md), all non-trivial technical trade-offs and structural decisions are permanently recorded in this ledger using the canonical format:

Ruling: <decision> — <why> — <cost>

---

## 2. Immutable Decision Ledger

### [DEC-001] Synthesis Without Destruction
- **Ruling**: Wrap and federate existing subsystems (omega/, sovereign/, apex/, nexus_autopilot/, tools_300/) into the omniverse/ namespace via deep module adapters rather than rewriting or displacing them.
- **Why**: Existing subsystems have proven high test maturity (151 audit points passing in 0.47s; 300 tools verified 100%). Displacing working code violates Ponytail Minimalism and risks regression.
- **Cost**: Requires maintaining clean adapter interfaces between legacy directory layouts and the unified omniverse package.

### [DEC-002] Package Structure & PEP 8 Naming
- **Ruling**: Scaffold the physical package root as e:\anti\omniverse/ (lowercase) while exposing the uppercase OMNIVERSE command interface and documentation aliases.
- **Why**: Python PEP 8 standards dictate lowercase module names to prevent cross-platform import anomalies on Windows/Linux.
- **Cost**: Documentation refers to both the concept ANTIGRAVITY OMNIVERSE and the Python package omniverse.

### [DEC-003] Legal Capability Replication Matrix (Levels A through F)
- **Ruling**: Strictly enforce the 6-tier legal replication matrix across all capability ingestion, research, and coding.
- **Why**: Prevents copyright infringement, license violations, or unlawful access to proprietary internals.
- **Cost**: Requires independent mathematical derivation of financial risk and workflow models.

### [DEC-004] Dual Persistence of Architectural Artifacts
- **Ruling**: Author all master system documentation in both the Antigravity artifact store and the workspace repository (omniverse/docs/).
- **Why**: Artifact store provides instant rich rendering in chat UI; repository ensures permanent git version control.
- **Cost**: Minor duplicate file write operations.

### [DEC-005] Zero Vibe Coding & Mandatory Test Green Gate
- **Ruling**: No code or venture feature is considered complete without passing automated tests and maintaining 100% green test suite status.
- **Why**: Verified automated tests are the only true proof of working software.
- **Cost**: Authoring unit tests first and fixing legacy import errors before declaring milestones complete.

### [DEC-006] Strict Human Control Matrix for Side-Effects
- **Ruling**: Actions that spend money, delete master data, alter credentials, or send live external communications are strictly blocked by mandatory Human Approval Checkpoints (Red Tier).
- **Why**: Unrestricted agent autonomy on high-impact external actions introduces unacceptable operational risk.
- **Cost**: Requires user intervention before executing real-world external dispatches.
