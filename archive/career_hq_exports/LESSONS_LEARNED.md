# CAREER HQ — LESSONS LEARNED & MISTAKES LOG

### 1. The Seed Data Pollution Trap
- **Mistake**: Initial system release marked 20 development seed jobs as `CONFIRMED_OPENING` on startup.
- **Consequence**: Reality audit revealed 9 broken 404 links and 11 generic portal roots.
- **Lesson**: Seed data must be strictly isolated with status `SEEDED_NOT_VERIFIED`. A job can only be confirmed through verified live HTTP 200 probes.

### 2. The Test Fixture Leak Trap
- **Mistake**: An automated test created a simulated receipt and left an application record in `SUBMITTED` state.
- **Consequence**: False claim in executive dashboard that an application was submitted.
- **Lesson**: Implement `ApplicationProofEngine` that strictly audits receipts and downgrades unproven submissions to `READY`.

### 3. The Silent Simulation Trap
- **Mistake**: Model router fell back to synthetic mock strings when offline.
- **Consequence**: Masked offline status and prevented debugging.
- **Lesson**: Enforce loud, immediate failure. Offline systems must be clearly reported as `OFFLINE`.

### 4. Continuous Automation Claim Trap
- **Mistake**: Claiming a 365-day radar is "running" simply because the Python script exists.
- **Lesson**: Strictly label automation as `CONFIGURED_NOT_EXECUTED` until real background daemon run proofs are logged to `automation_runs.jsonl`.
