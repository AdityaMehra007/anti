---
name: anti-patterns
description: "Use when working in anti, especially before editing its common modules, placing tests, naming branches, or writing commits — conventions measured from git history"
metadata:
  version: "1.0.0"
  source: local-git-analysis
  analyzed_commits: "100"
---

# Anti Repository Engineering Patterns & Conventions

Extracted from git history across 100+ commits and validated execution pipelines in the `anti` repository.

## 1. Commit Conventions
The repository strictly adheres to Conventional Commits with domain-specific scopes:
- **`feat(<scope>): <description>`**: Used for substantive operational capabilities and subsystem releases.
  - Frequent scopes: `omega-career-os`, `omega-phase8`, `automation`, `plane`, `conquest`, `emperor`, `scale`, `targets`.
- **`fix(<scope>): <description>`**: Target root causes rather than symptoms.
- **`docs(<scope>): <description>`**: Documentation, runbooks, and constitutions.
- **`test(<scope>): <description>`**: Hermetic fixtures and regression assertions.
- **Tone**: Lowercase imperative verbs (`deploy`, `implement`, `scale`, `compile`, `advance`).

## 2. Code Architecture & Folder Structure
- **`aios/`**: Autonomous Intelligence Operating System:
  - `aios/services/`: Fault-tolerant background daemons (`omega_supervisor.py`, `live_telemetry_relay.py`).
  - `aios/ai/`: API gateways (`gateway.py`) on port 8090.
- **`apps/job_application_studio/`**: Self-contained single-page HTML/JS cockpits and HUDs:
  - Electric-cyan dark mode palette (`#060911`, `#00f0ff`, `#10b981`).
  - LocalStorage state persistence + live polling to local daemon ports (8092, 8095, 8096).
- **`data/`**: Ground-truth transactional databases and JSON datasets:
  - `outreach_tracker.db`: SQLite database tracking all application states and inbound recruiter touchpoints.
  - `global_10000_targets.db`: 10,000 global requisitions with SHA-256 signatures.
  - `BANGALORE_ALL_STARTUPS_DOSSIER.json`: 603 categorized Bangalore startups.
- **`omega_infinity/`**: Constitutional 13-Mode autonomous engine and red-team provers:
  - `omega_hyper_orchestrator.py`: Implements `do_everything()`, coordinating Mode A through Mode M.
  - `omega_red_team_engine.py`: Adversarial stress tests (12 canonical probes).
- **`scripts/`**: Deterministic standalone tools and compilers:
  - `activate_email_dispatcher.py`: Universal RFC 822 email verification and dispatch.
  - `offer_negotiator.py`: Bangalore GCC compensation benchmark evaluator and letter generator.
  - `score_all_applications_apex.py`: 4-pillar multi-factor fit scoring engine.
- **`tests/`**: Pytest regression suites with 100% green pass rate requirement.

## 3. Workflows & Execution Discipline
1. **Zero Vibe Coding**:
   - Code changes must have verifiable seams, explicit data contracts, and passing tests before completion.
2. **Candidate Ground-Truth Invariant**:
   - Strictly anchor all career artifacts to verified facts: **Aditya Mehra** (BBA International Business, Dayananda Sagar University '26 | AERO India 2025 Lead Coordinator | Instawork AI Data Ops 99.2% QA Precision).
   - Zero fabricated grades, zero telecalling/SDR roles.
3. **Dual Execution Protocol**:
   - Automation scripts must provide both a safe simulation/audit mode (`--dry-run`) and an authorized live dispatch mode (`--live`).
4. **Port Allocation Scheme**:
   - Port 8000: `tradenexus_api` (B2B Cross-Border Logistics)
   - Port 8090: `aios_gateway` (AI Agent Gateway)
   - Port 8092: `plane_webhook_reactor` (Inbound Recruiter & Issue Webhooks)
   - Port 8095: `omega_supervisor` (Master Fault-Tolerant Daemon Manager)
   - Port 8096: `live_telemetry_relay` (SSE Real-Time Performance Stream)

## 4. Testing Conventions
- Pytest standard naming: `tests/test_<subsystem>.py`.
- Tests must execute cleanly in sub-10 seconds without flakiness across operating systems.
- Any background daemon or subprocess launched during test fixtures must be gracefully terminated.
