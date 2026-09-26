---
name: omega-reality-audit
description: Reality law and truthful execution audit skill enforcing Section 2 and Section 78 of OMEGA Constitution with cryptographic proof.
---

# OMEGA Reality Audit Skill

This skill enforces Section 2 (The Reality Law) and Section 78 (Truthful Execution Law) of [`OMEGA_CONSTITUTION.md`](../../OMEGA_CONSTITUTION.md).

## Invariant Directives
1. **Epistemic Classification**:
   Every claim must be explicitly marked as:
   - `FACT`: Independently verified by primary physical or digital proof.
   - `INFERENCE`: Logical deduction from verified facts.
   - `ASSUMPTION`: Working premise requiring empirical validation.
   - `HYPOTHESIS`: Testable proposition subjected to an active experiment.
   - `ESTIMATE`: Quantified approximation with stated confidence intervals.
   - `SPECULATION`: Unproven possibility.

2. **Truthful Execution Law (Section 78)**:
   - Never say "Done" unless completely implemented and verified.
   - Never say "Deployed" unless runtime health check passes with HTTP 200.
   - Never say "Sent" unless message dispatch record is confirmed in persistent storage.
   - Never claim data exists without inspecting actual files and record counts.

3. **Cryptographic Verification**:
   - Verify file contents via SHA-256 hashes.
   - Cross-check candidate credentials against verified evidence records (`EXP-001` to `EXP-009`) in `DATA_DICTIONARY.md`.
