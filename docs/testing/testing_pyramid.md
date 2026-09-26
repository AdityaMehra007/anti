# Testing Strategy & Quality Gateways
**Directory:** `docs/testing/`  
**Directives:** 84, 85, 86, 215 (ADI OMNI CODEX)  

## Test Structure
- **Unit Tests:** `tests/test_career_brain.py` (Verifies 100-pt scoring, sales risk detection, component summation, and explainability).
- **Evaluations / Benchmarks:** `.codex/evaluations/eval_runner.py` (8-case benchmark verifying 100% precision in sales role exclusion).
- **Verification Gate:** No code modification is complete without running unit tests and recording results in the executive walkthrough.
