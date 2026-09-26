# ADI OMNI OS ? System Architecture Overview
**Directory:** `docs/architecture/`  
**Constitution:** `ADI_OMNI_CODEX.md` (Version OMNI-X)  

## System Layers
1. **Constitution & Governance:** `ADI_OMNI_CODEX.md`, `AGENTS.md`, `CONTEXT.md`.
2. **Intelligence Layer:** `career_brain.py` (100-pt scoring model + Sales Exclusion Engine), `bangalore_market_intelligence_engine.py`.
3. **Application & Delivery Layer:** `resume_adi.md`, `resume_variants/`, `READY_OUTREACH_ACTIONS.md`, `job_applications.csv`.
4. **Data & Truth Layer:** `data/jobs_master.csv`, `data/referral_targets.csv`, `system_memory_store.json`, `DATA_DICTIONARY.md`.
5. **Execution & Automation Layer:** `RUN_AUTONOMOUS_PIPELINE.py`, `AUTOMATION_SUITE.bat`, `master_orchestrator.py`.
6. **Quality & Verification Layer:** `tests/test_career_brain.py`, `.codex/evaluations/eval_runner.py`.
