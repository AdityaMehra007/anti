# NOTES.md — User World, Channels, and Operations

## Workspace Context
- **Workspace**: E:\anti & E:\anti\aios
- **Core Stacks**:
  - **AIOS (Antigravity OMEGA)**: Local AI Gateway (`:8090`), Master Command UI (`:3000`), Ollama GPU Inference (`:11434`, Qwen 2.5 Coder 3B on GTX 960M), SQLite WAL (`data/master.db`), n8n Automation Bridge (`:5678`).
  - **Career OS / Omega Platform**: Job matching (`data/global_10000_targets.db`), auto-apply pipeline (`scripts/auto_apply_job_pipeline.py`), outreach tracker (`data/outreach_tracker.db`).
  - **SaaS Factory & Agent Harness**: Multi-stack project generator (`projects/saas_factory.py`) and autonomous agent harness (`projects/agent_harness.py`).

## Channels & Entry Points
- Email / Resumes / Job portals (Auto-apply pipeline -> Gmail / RFC 822 EML)
- Local HTTP Webhooks & n8n event triggers (`:8090/v1/automation/trigger`)
- AIOS Command Center Dashboard (`http://127.0.0.1:3000/`)
- Git repositories & Codebases (Software factory)

## Active Workflows Specified
1. [`career_os_outreach_loop.md`](file:///e:/anti/workflows/career_os_outreach_loop.md): High-tempo job matching, STAR tailoring against Truth Layer, Gmail compose URL synthesis, and SHA-256 proof logging.
2. [`aios_system_watchdog_loop.md`](file:///e:/anti/workflows/aios_system_watchdog_loop.md): SRE host sensor collection, GPU thermal guarding, passive SQLite WAL checkpointing, and telemetry indexing.
3. [`saas_venture_builder_loop.md`](file:///e:/anti/workflows/saas_venture_builder_loop.md): Event-driven multi-stack SaaS scaffolding with pluggable feature modules and bounded autonomous agent harnesses.
4. [`morning_career_dispatch_loop.md`](file:///e:/anti/workflows/morning_career_dispatch_loop.md): 15-minute morning application dispatch, 6-factor opportunity scoring, dual-format resume staging, Day-3 follow-up alerts, and push-right checkpoint brief.
5. [`eventops_vendor_sla_audit_loop.md`](file:///e:/anti/workflows/eventops_vendor_sla_audit_loop.md): Event-driven vendor quote auditor, rate inflation detection against Bangalore master baseline, contractual delay penalty calculation (5%/hr), and counter-letter generation.
6. [`weekly_portfolio_showcase_loop.md`](file:///e:/anti/workflows/weekly_portfolio_showcase_loop.md): Friday 05:00 PM scheduled showcase cycle auditing Git activity, test passes, pipeline velocity, and drafting humanized LinkedIn posts for corporate recruiters.

## Canonical Vocabulary
- **Loop**: A recurring pattern in the user's operations, life, or system.
- **Workflow**: The markdown specification of one loop (`workflows/*.md`).
- **Trigger**: What fires each run (Event or Schedule).
- **Checkpoint**: A human-in-the-loop decision or review point, pushed as far right as possible.
- **Brief**: A decision-ready summary presented at checkpoints, never a raw draft.

