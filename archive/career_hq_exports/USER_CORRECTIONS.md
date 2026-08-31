# USER CORRECTIONS & PREFERENCES LOG

- **CORR-001 (2026-08-26):** **No Fake Provider Data**. Replace hardcoded latency, cost, and health scores with live discovery and empirical runtime telemetry.
- **CORR-002 (2026-08-26):** **Seed Isolation Invariant**. Seeded template jobs must remain `SEEDED_NOT_VERIFIED`. Only live HTTP 200 probes can mark a job as `CONFIRMED_OPENING`.
- **CORR-003 (2026-08-26):** **No Fake Submissions**. `READY != SUBMITTED`, `SUBMITTED != DELIVERED`. Downgrade test fixture submissions to `READY`. Require genuine external portal receipts.
- **CORR-004 (2026-08-26):** **Outreach Truth Standard**. Recruiter messages without dispatch receipts remain strictly `DRAFT`. Human approval required for dispatch.
- **CORR-005 (2026-08-26):** **Automation Execution Standard**. Classify automated schedulers as `CONFIGURED_NOT_EXECUTED` until real background daemon execution is logged.
- **CORR-006 (2026-08-26):** **Zero Silent Simulation**. Never return simulated mock strings when tools or models are offline. Fail loudly.
- **CORR-007 (2026-08-31):** **Strict Location Scope**. Location restriction set strictly to **Bengaluru, India** (Kadubeesanahalli, Bellandur, EGL, Koramangala, Manyata, Electronic City).
- **CORR-008 (2026-08-31):** **Candidate Profile Scope**. Role positioning set to **BBA in International Business** (Operations, Global Trade, Supply Chain, Logistics, BizOps). Never generate software engineering resumes.
- **CORR-009 (2026-08-31):** **Mandatory E: Drive Storage**. All persistent project data and knowledge stored on `E:\` drive (`E:\anti`, `E:\OMNI_OS`, `E:\antigravity_workspace`).
- **CORR-010 (2026-08-31):** **Verified Resume PDF**. Master canonical resume file set strictly to `Aditya_Mehra_Resume.pdf`.
