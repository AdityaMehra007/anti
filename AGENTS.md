# AGENTS.md — OMEGA ∞ Autonomous Agent Architecture & Guidelines

Guidance and instructions for autonomous coding agents and executive departments working in this repository.

**Supreme Constitution**: [`OMEGA_CONSTITUTION.md`](OMEGA_CONSTITUTION.md) (OMEGA ∞: 120 Master Directives). All autonomous systems, subagents, tools, and execution loops strictly adhere to its reality laws, ethics, and execution protocols.  
**Operational Codex**: [`ADI_OMNI_CODEX.md`](ADI_OMNI_CODEX.md) (Version OMNI-X / Production Engineering Mode, 330 directives).  
**Ubiquitous Language & Context**: [`CONTEXT.md`](CONTEXT.md).  
**Data Dictionary**: [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).  

---

## 0. OMEGA Operating Modes & Protocols

Agents dynamically operate across 13 modes governed by Section 5 of the Constitution:
- **Mode A (Discovery)**: Environment and capability discovery.
- **Mode B (Research)**: Deep evidence gathering and cross-checking.
- **Mode C (Strategy)**: Converting information into high-leverage decisions.
- **Mode D (Build)**: Tangible system construction (Artifact-First).
- **Mode E (Automation)**: Process standardization and DAG automation.
- **Mode F (Execution)**: Authorized operational dispatches.
- **Mode G (Audit)**: Bottleneck and weakness inspection.
- **Mode H (Red Team)**: Adversarial stress testing (Section 14).
- **Mode I (Optimization)**: Economics, latency, and leverage improvement.
- **Mode J (Scale)**: Repeatable expansion of validated systems.
- **Mode K (Monitor)**: 24/7 observability and anomaly detection.
- **Mode L (Learning)**: Converting outcomes into reusable skills and rules.
- **Mode M (CEO)**: Enterprise value creation and capital allocation.

---

## 1. Engineering Principles

- **Zero Vibe Coding**: Write code only when backed by clear specifications, verified seams, and tests.
- **Deep Modules**: Strive for deep modules with simple interfaces and rich capabilities.
- **Ubiquitous Language**: Strictly adhere to the terms and definitions in [`CONTEXT.md`](CONTEXT.md).
- **Verified Evidence**: Never invent or hallucinate candidate credentials or company claims. Use verified data from `DATA_DICTIONARY.md` and evidence ledgers.
- **Ponytail Minimalism (Lazy Senior Dev)**: The best code is the code you never wrote. Never invent abstractions or boilerplate. Stop at the first rung of **The Ladder**:
  1. *Does this need to exist at all?* → Skip speculative code (YAGNI).
  2. *Already in this codebase?* → Reuse existing helpers, utilities, and types.
  3. *Stdlib does it?* → Use standard library primitives.
  4. *Native platform feature covers it?* → Use platform/OS/browser primitives.
  5. *Already-installed dependency solves it?* → Use installed packages; avoid adding dependencies.
  6. *Can this be one line?* → One line.
  7. *Only then:* Write the minimum code that works.
- **Root-Cause Bug Fixing**: A bug report names a symptom. Trace callers and fix the shared origin once rather than scattering defensive guards across sibling call sites.

---

## 2. Testing & Quality Gateways

- For any new feature or non-trivial bugfix, use the [`tdd`](.agents/skills/tdd/SKILL.md) or [`test-driven-development`](.agents/skills/test-driven-development/SKILL.md) skill (red-green-refactor).
- For diagnosing non-deterministic errors or regressions, invoke [`diagnosing-bugs`](.agents/skills/diagnosing-bugs/SKILL.md) and [`systematic-debugging`](.agents/skills/systematic-debugging/SKILL.md).
- Before committing substantial changes, run [`code-review`](.agents/skills/code-review/SKILL.md) and [`verification-before-completion`](.agents/skills/verification-before-completion/SKILL.md) to inspect standards and specification fidelity.
- For eliminating bloat, reviewing diffs against YAGNI, or auditing technical debt, invoke [`ponytail`](.agents/skills/ponytail/SKILL.md) and [`ponytail-audit`](.agents/skills/ponytail-audit/SKILL.md).

---

## 3. Superpowers Methodology & Execution Gateways

All agent activities follow the core **Superpowers** discipline:

1. **Hard Gate on Ideation & Brainstorming** ([`brainstorming`](.agents/skills/brainstorming/SKILL.md)):
   - Never begin implementation before scoping and explicit approval.
   - Classify upfront: **Spike** (feasibility probe, disposable code), **Bounded** (targeted change to existing flow, chat-based design approval), or **Architectural** (new subsystems, formal design doc & review).
2. **Deterministic Plan Authoring** ([`writing-plans`](.agents/skills/writing-plans/SKILL.md)):
   - Structure plans into bite-sized, independent tasks with clear seams, files touched, and explicit red/green testing criteria.
3. **Subagent-Driven Development** ([`subagent-driven-development`](.agents/skills/subagent-driven-development/SKILL.md)):
   - Dispatch fresh implementer subagents per task with isolated, curated context to prevent history contamination.
   - Pair each task with a rigorous reviewer (spec compliance + code quality).
   - **Rulings over stalls**: Resolve conflicts and minor ambiguities immediately, recording them in a decision ledger (`Ruling: <decision> — <why> — <cost>`).
   - Stop only for destructive actions, security hazards, out-of-worktree side effects, or broken plans.
4. **Verification Before Completion** ([`verification-before-completion`](.agents/skills/verification-before-completion/SKILL.md)):
   - Claim nothing without verified test runs, clean lints, and validated outputs.

---

## Agent skills

### Superpowers Core Skills
- [`using-superpowers`](.agents/skills/using-superpowers/SKILL.md): Meta-skill for proactive skill discovery and Antigravity tool mappings.
- [`brainstorming`](.agents/skills/brainstorming/SKILL.md): Collaborative intent refinement and hard approval gates.
- [`writing-plans`](.agents/skills/writing-plans/SKILL.md) & [`executing-plans`](.agents/skills/executing-plans/SKILL.md): Structured planning and multi-agent execution.
- [`subagent-driven-development`](.agents/skills/subagent-driven-development/SKILL.md): Task-isolated subagent dispatch and review loops.
- [`test-driven-development`](.agents/skills/test-driven-development/SKILL.md): Strict red-green-refactor cycle.
- [`systematic-debugging`](.agents/skills/systematic-debugging/SKILL.md): Origin tracing and hypothesis-driven debugging.
- [`verification-before-completion`](.agents/skills/verification-before-completion/SKILL.md): Automated verification and evidence ledgers.
- [`requesting-code-review`](.agents/skills/requesting-code-review/SKILL.md) & [`receiving-code-review`](.agents/skills/receiving-code-review/SKILL.md): Multi-perspective review standards.
- [`using-git-worktrees`](.agents/skills/using-git-worktrees/SKILL.md) & [`finishing-a-development-branch`](.agents/skills/finishing-a-development-branch/SKILL.md): Clean branch and worktree hygiene.

### Ponytail Minimalist Mode
Channel the laziest senior dev in the room. See [`ponytail`](.agents/skills/ponytail/SKILL.md).

### Vercel Skills Ecosystem
Installed via `vercel-labs/skills` CLI for UI, React, prose, and cloud performance:
- [`agent-browser`](.agents/skills/agent-browser/SKILL.md): Fast native Chrome/CDP browser automation CLI with accessibility-tree snapshots and `@eN` element refs for web interaction, form filling, scraping, and QA
- [`web-design-guidelines`](.agents/skills/web-design-guidelines/SKILL.md): Audit UI code against Web Interface Guidelines
- [`writing-guidelines`](.agents/skills/writing-guidelines/SKILL.md): Audit documentation and prose against clarity and tone rules
- [`vercel-react-best-practices`](.agents/skills/vercel-react-best-practices/SKILL.md): Optimize React and Next.js rendering, waterfalls, and bundles
- [`vercel-composition-patterns`](.agents/skills/vercel-composition-patterns/SKILL.md): Structure scalable React component architecture and compound patterns
- [`vercel-react-native-skills`](.agents/skills/vercel-react-native-skills/SKILL.md): Optimize React Native and Expo performance
- [`vercel-react-view-transitions`](.agents/skills/vercel-react-view-transitions/SKILL.md): Implement native-feeling View Transitions in React
- [`deploy-to-vercel`](.agents/skills/deploy-to-vercel/SKILL.md): Deploy applications to Vercel preview and production environments
- [`vercel-cli-with-tokens`](.agents/skills/vercel-cli-with-tokens/SKILL.md): Manage deployments non-interactively using tokens
- [`vercel-optimize`](.agents/skills/vercel-optimize/SKILL.md): Analyze and reduce Vercel compute costs, latency, and bandwidth

### Database & SQL Quality Ecosystem
Synchronized from [`supabase/agent-skills`](https://github.com/supabase/agent-skills) & [`sqlfluff/sqlfluff`](https://github.com/sqlfluff/sqlfluff):
- [`supabase-postgres-best-practices`](.agents/skills/supabase-postgres-best-practices/SKILL.md): Schema design, indexing, RLS policy audit, query performance, and connection scaling rules
- [`supabase`](.agents/skills/supabase/SKILL.md): Supabase product integration across Auth, Realtime, Storage, Edge Functions, and Vector search
- [`sqlfluff`](.agents/skills/sqlfluff/SKILL.md): SQL linting, formatting, dialect validation (SQLite, PostgreSQL, MySQL), and automated quality gateways



### Tech Leads Club Skills Ecosystem
Hardened, curated skills registry synchronized from [`tech-leads-club/agent-skills`](https://github.com/tech-leads-club/agent-skills) (92 skills):
- **Architecture & System Design**: [`evolutionary-modular-architecture`](.agents/skills/evolutionary-modular-architecture/SKILL.md), [`modular-decomposition`](.agents/skills/modular-decomposition/SKILL.md), [`tactical-ddd`](.agents/skills/tactical-ddd/SKILL.md), [`legacy-migration-planner`](.agents/skills/legacy-migration-planner/SKILL.md), [`coupling-analysis`](.agents/skills/coupling-analysis/SKILL.md)
- **Cloud & Deployment**: [`aws-advisor`](.agents/skills/aws-advisor/SKILL.md), [`cloudflare-deploy`](.agents/skills/cloudflare-deploy/SKILL.md), [`vercel-deploy`](.agents/skills/vercel-deploy/SKILL.md), [`netlify-deploy`](.agents/skills/netlify-deploy/SKILL.md), [`render-deploy`](.agents/skills/render-deploy/SKILL.md)
- **Architecture & Spec Governance**: [`create-adr`](.agents/skills/create-adr/SKILL.md), [`create-rfc`](.agents/skills/create-rfc/SKILL.md), [`create-technical-design-doc`](.agents/skills/create-technical-design-doc/SKILL.md), [`tlc-spec-driven`](.agents/skills/tlc-spec-driven/SKILL.md), [`skill-architect`](.agents/skills/skill-architect/SKILL.md)
- **Quality, Testing & Verification**: [`the-judge`](.agents/skills/the-judge/SKILL.md), [`the-fool`](.agents/skills/the-fool/SKILL.md), [`the-jury`](.agents/skills/the-jury/SKILL.md), [`spec-driven-eval`](.agents/skills/spec-driven-eval/SKILL.md), [`web-quality-audit`](.agents/skills/web-quality-audit/SKILL.md)
- **Security & Hardening**: [`security-best-practices`](.agents/skills/security-best-practices/SKILL.md), [`security-threat-model`](.agents/skills/security-threat-model/SKILL.md), [`security-ownership-map`](.agents/skills/security-ownership-map/SKILL.md)
- **Web Automation & Browser QA**: [`playwright-skill`](.agents/skills/playwright-skill/SKILL.md), [`chrome-devtools`](.agents/skills/chrome-devtools/SKILL.md)
- **Design & UI**: [`figma`](.agents/skills/figma/SKILL.md), [`figma-implement-design`](.agents/skills/figma-implement-design/SKILL.md), [`mermaid-studio`](.agents/skills/mermaid-studio/SKILL.md), [`excalidraw-studio`](.agents/skills/excalidraw-studio/SKILL.md)
- **Monorepo & Tooling**: [`nx-workspace`](.agents/skills/nx-workspace/SKILL.md), [`nx-generate`](.agents/skills/nx-generate/SKILL.md), [`nx-run-tasks`](.agents/skills/nx-run-tasks/SKILL.md), [`nx-ci-monitor`](.agents/skills/nx-ci-monitor/SKILL.md), [`gh-fix-ci`](.agents/skills/gh-fix-ci/SKILL.md)
- **GTM & Growth Engine**: [`ai-sdr`](.agents/skills/ai-sdr/SKILL.md), [`ai-cold-outreach`](.agents/skills/ai-cold-outreach/SKILL.md), [`lead-enrichment`](.agents/skills/lead-enrichment/SKILL.md), [`sales-motion-design`](.agents/skills/sales-motion-design/SKILL.md), [`content-to-pipeline`](.agents/skills/content-to-pipeline/SKILL.md)

### Code Review & Quality Engine
- [`open-code-review`](.agents/skills/open-code-review/SKILL.md): Fast, battle-tested hybrid code review assistant (deterministic pipelines + LLM agent, line-level feedback, built-in multi-language rulesets).
- [`open-code-review-delegate`](.agents/skills/open-code-review-delegate/SKILL.md): Zero-API-key delegation mode where OCR handles deterministic file selection/rule resolution while the host agent performs the review.

### Prose & Editorial Hygiene
- [`humanizer`](.agents/skills/humanizer/SKILL.md): Rewrite AI-sounding prose so it reads naturally like a human wrote it, eliminating 35 diagnostic AI patterns from Wikipedia's AI Cleanup project while strictly preserving factual claims and voice.

### APEX Career Supremacy OS (Ω-CAREER-UNIVERSE)
Autonomous end-to-end career intelligence, job discovery, online learning, recruiter network matching, and career velocity suite:
- [`apex-career-os`](.agents/skills/apex-career-os/SKILL.md): Master orchestrator running the 7-agent closed-loop career conquest engine.
- [`job-learning-sentinel`](.agents/skills/job-learning-sentinel/SKILL.md): Continuous online scraper and company DNA/interview learning agent.
- [`recruiter-network-strike`](.agents/skills/recruiter-network-strike/SKILL.md): 9,223 LinkedIn connection matcher and 3-stage outreach cadence generator.
- [`interview-simulator-pro`](.agents/skills/interview-simulator-pro/SKILL.md): Real-world STAR mock interview simulator and curveball defense coach.
- [`career-velocity-ladder`](.agents/skills/career-velocity-ladder/SKILL.md): 30-60-90 day onboarding blueprint, compensation benchmarking, and 5-year executive trajectory architect.
- **Mission Control Cockpit**: [`apex_career_cockpit.html`](apex_career_cockpit.html)
- **Subagent**: `apex-career-sentinel`
- **CLI Runner**: `python -m apex_career_os.cli --auto-pilot` / `START_APEX_CAREER_OS.bat`

### Universal Job & Skill Intelligence Ecosystem
Universal Job Taxonomy, deep Job Description (JD) dissection, ATS semantic matching, Google X-Y-Z resume bullet generation, and automated application staging:
- **Taxonomy Engine**: [`universal_job_taxonomy_master.py`](universal_job_taxonomy_master.py) (13 Industry Families, 31 Master Role Archetypes, L1–L7 leveling rules, compensation benchmarks, and SQLite export).
- **JD Intelligence Deep Module**: [`universal_jd_intelligence_engine.py`](universal_jd_intelligence_engine.py) (Semantic skill extraction, synonym clustering, ATS scoring, gap analysis, Google X-Y-Z bullet synthesis, and STAR interview defense).
- **Master Skill Generator**: [`universal_skill_generator.py`](universal_skill_generator.py) (Maps all 3,837+ installed agent skills to job archetypes with deterministic matrices).
- **Census & Staged Dockets**: [`data/universal_dissected_jobs_500.json`](data/universal_dissected_jobs_500.json) (500 parsed real jobs with ATS scores) and [`data/universal_application_dockets.json`](data/universal_application_dockets.json) (406 auto-apply dockets staged into `data/approval_queue.csv`).
- **Interactive Cockpit**: [`universal_job_cockpit.html`](universal_job_cockpit.html) (Live JD dissector, taxonomy grid, 3,837 skill matrix, and 500+ opportunity census).
- **Executive Mission Control**: [`OMNI_EXECUTIVE_COCKPIT.html`](OMNI_EXECUTIVE_COCKPIT.html) (Unified meta-cockpit linking all 6 dashboards, 14 suites, and 16,553 vacancies).
- **Master Batch Launcher**: [`START_ALL_OMNI_SYSTEMS.bat`](START_ALL_OMNI_SYSTEMS.bat) (One-click launch of API server and Executive Cockpit).
- **Cockpit Launcher**: [`START_UNIVERSAL_JOB_COCKPIT.bat`](START_UNIVERSAL_JOB_COCKPIT.bat) / `python universal_jd_intelligence_engine.py --serve-cockpit 8765`
- **Enterprise Application Dossiers**: 71 submission-ready packages in [`applications_generated/`](applications_generated/) with tailored ATS resumes, cover letters, recruiter InMails, and STAR interview defense.

### Hiring Without Whiteboards Autonomous Ecosystem
Canonical practical engineering hiring registry and intelligence engine analyzing 761+ tech companies that evaluate talent through day-to-day software craft rather than whiteboard puzzles or CS trivia (https://github.com/poteto/hiring-without-whiteboards):
- **Deep SDK & Engine**: [`hiring_without_whiteboards_engine.py`](hiring_without_whiteboards_engine.py) (Parser, classifier, FTS5 search index, REST API server, and SQLite generator).
- **Interactive Cockpit**: [`hiring_without_whiteboards_cockpit.html`](hiring_without_whiteboards_cockpit.html) (Live 761-employer mission control, multi-region filtering, assessment-type toggles, and tailored hiring manager pitch generation).
- **Master Strategy Dossier**: [`docs/HIRING_WITHOUT_WHITEBOARDS_MASTER_STRATEGY.md`](docs/HIRING_WITHOUT_WHITEBOARDS_MASTER_STRATEGY.md) (Take-home gold standard checklist, pairing protocols, paid trial guidelines, and cold outreach templates).
- **Structured Datasets**: [`data/hiring_without_whiteboards.json`](data/hiring_without_whiteboards.json), [`data/hiring_without_whiteboards.csv`](data/hiring_without_whiteboards.csv), [`data/hiring_without_whiteboards.sqlite`](data/hiring_without_whiteboards.sqlite).
- **One-Click Launcher**: [`START_HIRING_WITHOUT_WHITEBOARDS_COCKPIT.bat`](START_HIRING_WITHOUT_WHITEBOARDS_COCKPIT.bat) / `python hiring_without_whiteboards_engine.py --serve 8780`.

### Coolify Autonomous Cloud & PaaS Orchestration Ecosystem
Self-hosted PaaS alternative to Heroku/Vercel/Netlify for multi-server Docker, Traefik edge routing, database provisioning, and 352+ open-source one-click service templates:
- [`coolify-orchestrator`](.agents/skills/coolify-orchestrator/SKILL.md): Autonomous SDK, CLI, and operational standard for managing Coolify clusters, projects, deployments, and databases.
- **Deep SDK & Engine**: [`coolify_orchestrator.py`](coolify_orchestrator.py) (Live Sanctum API client & high-fidelity offline simulation engine).
- **Universal CLI**: [`coolify_cli.py`](coolify_cli.py) (`info`, `servers`, `projects`, `apps`, `dbs`, `services`, `catalog`, `deploy`, `stack`).
- **Mission Control Cockpit**: [`coolify_control_cockpit.html`](coolify_control_cockpit.html) (Real-time cluster telemetry, 352-template marketplace, deployment terminal emulator, and API playground).
- **One-Click Launchers**: [`START_COOLIFY_WINDOWS.bat`](START_COOLIFY_WINDOWS.bat) & [`scripts/start_coolify_windows.ps1`](scripts/start_coolify_windows.ps1).
- **Architecture Teardown Dossier**: [`docs/COOLIFY_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/COOLIFY_SUPREME_ARCHITECTURE_DOSSIER.md).

### Plane Autonomous Project & Issue Orchestration Ecosystem
Modern open-source software development platform, issue tracker, Kanban board, sprint cycles with burndown velocity curves, epic modules, collaborative knowledge documentation, and triage intake engine (https://github.com/makeplane/plane):
- [`plane-orchestrator`](.agents/skills/plane-orchestrator/SKILL.md): Autonomous SDK, CLI, and operational standard for Plane CE & Cloud environments.
- **Deep SDK & Master Engine**: [`plane_orchestrator.py`](plane_orchestrator.py) (Dual-mode: live Plane CE REST API client and ultra-high-fidelity offline relational simulation engine).
- **Universal CLI**: [`plane_cli.py`](plane_cli.py) (`info`, `workspaces`, `projects`, `create-project`, `issues`, `create-issue`, `update-issue`, `cycles`, `create-cycle`, `burndown`, `modules`, `create-module`, `pages`, `create-page`, `triage`, `triage-action`, `analytics`, `docker-config`, `do-everything`).
- **Autonomous Local API Server**: [`plane_api_server.py`](plane_api_server.py) (REST bridge on port 8774 serving workspaces, projects, issues, cycles, burndown metrics, pages, triage, and cockpit).
- **Model Context Protocol (MCP) Server**: [`plane_mcp_server.py`](plane_mcp_server.py) (Exposes 16 Plane agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`plane_control_cockpit.html`](plane_control_cockpit.html) (9 operational tabs: Kanban Board, Cycles & Burndown SVG, Modules & Roadmaps, Collaborative Docs, Triage Intake, Velocity Analytics, Docker Topology, 12-Phase Lifecycle, and MCP Playground).
- **One-Click Launchers**: [`START_PLANE_WINDOWS.bat`](START_PLANE_WINDOWS.bat), [`START_PLANE_COCKPIT.bat`](START_PLANE_COCKPIT.bat), [`START_PLANE.bat`](START_PLANE.bat).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/plane_do_everything_manifest.json`](omega/data/plane_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/PLANE_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/PLANE_SUPREME_ARCHITECTURE_DOSSIER.md).

### Windmill Autonomous Workflow Engine & Developer Platform Ecosystem
Self-hosted, ultra-fast developer platform and DAG orchestration engine (alternative to Temporal, Retool, Airplane, and Airflow) running on a Rust core, PostgreSQL SKIP LOCKED queues, and polyglot sandboxed workers:
- [`windmill-orchestrator`](.agents/skills/windmill-orchestrator/SKILL.md): Autonomous SDK, CLI, and operational standard for building and running scripts, multi-step DAG flows, human approvals, and low-code apps.
- **Deep SDK & Orchestrator**: [`windmill_orchestrator.py`](windmill_orchestrator.py) (Dual-mode: live `/api/w/{workspace}/...` REST API client & high-fidelity Rust/Postgres simulation engine).
- **Universal CLI**: [`windmill_cli.py`](windmill_cli.py) (`info`, `workspaces`, `scripts`, `flows`, `apps`, `resources`, `schedules`, `variables`, `jobs`, `run-script`, `run-flow`, `trigger-schedule`, `set-variable`, `approve-job`, `webhook`, `hub`, `hub-import`, `do-everything`).
- **Autonomous Local API Server**: [`windmill_api_server.py`](windmill_api_server.py) (REST bridge on port 8768 for live telemetry, scripts, flows, schedules, variables, webhooks, and executions).
- **Model Context Protocol (MCP) Server**: [`windmill_mcp_server.py`](windmill_mcp_server.py) (Exposes 21 Windmill agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`windmill_control_cockpit.html`](windmill_control_cockpit.html) (10 operational tabs: Script Studio, Flow DAG Visualizer, Automated Schedules & Crons, Variables & Secrets Vault, Webhook Ingress, Worker Telemetry, Low-Code Apps, Hub Marketplace, Job History, and MCP Playground).
- **Production Stacks & Launchers**: [`stacks/windmill/docker-compose.yml`](stacks/windmill/docker-compose.yml), [`START_WINDMILL_WINDOWS.bat`](START_WINDMILL_WINDOWS.bat), [`scripts/start_windmill_windows.ps1`](scripts/start_windmill_windows.ps1).
- **Enterprise Scripts & DAG Flows**: [`windmill/scripts/`](windmill/scripts/) (Customer Churn Risk Radar, SEC EDGAR Statement Recon, Daily Cloud DB Snapshot & S3 Vault, CBAM Carbon Audit, ERP Ledger Recon, Lead Intelligence Strike, Slack Block Kit Notifier, DB Health Diagnostic) and [`windmill/flows/`](windmill/flows/) (Autonomous SaaS Billing Recovery DAG, Sovereign SecOps Threat Incident DAG, Enterprise Onboarding DAG, CBAM Pipeline, Nightly System Recon).
- **Automated Cron Schedules & Variables**: [`windmill/schedules/`](windmill/schedules/) (4 production crons) & [`windmill/variables/`](windmill/variables/) (ChaCha20-Poly1305 encrypted secret store).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/windmill_do_everything_manifest.json`](omega/data/windmill_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/WINDMILL_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/WINDMILL_SUPREME_ARCHITECTURE_DOSSIER.md).

### n8n Autonomous Workflow Automation & AI Agent Ecosystem
Enterprise fair-code workflow automation, event-driven node DAG execution, and native LangChain AI multi-agent orchestration (https://github.com/n8n-io/n8n):
- [`n8n-orchestrator`](.agents/skills/n8n-orchestrator/SKILL.md): Autonomous SDK, CLI, and operational standard for n8n workflow graphs, LangChain reasoning, and event triggers.
- **Deep SDK & Master Engine**: [`n8n_orchestrator.py`](n8n_orchestrator.py) (Dual-mode: live `/api/v1/...` REST API client & high-fidelity simulation engine with 560+ core nodes, SQLite FTS5 index, 14 production workflows, LangChain AI agent reasoning loop, and topological node traversal).
- **Universal CLI**: [`n8n_cli.py`](n8n_cli.py) (`info`, `nodes`, `search`, `workflows`, `get-workflow`, `run-workflow`, `trigger`, `ai-agent`, `executions`, `get-execution`, `credentials`, `dropzone`, `export`, `do-everything`, `serve`).
- **Autonomous Local API Server**: [`n8n_api_server.py`](n8n_api_server.py) (REST bridge on port 8771 serving health, telemetry, node search, workflow triggers, webhooks, and the Mission Control Cockpit).
- **Model Context Protocol (MCP) Server**: [`n8n_mcp_server.py`](n8n_mcp_server.py) (Exposes 15 high-leverage n8n agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`n8n_control_cockpit.html`](n8n_control_cockpit.html) (10 operational views: Live Telemetry, Node Explorer with 560+ nodes, Production DAG Visualizer, Workflow Execution Terminal, Inbound Webhook Dispatcher, LangChain AI Agent Playground, Execution History, AES-256 Credentials Vault, and 12-Phase Lifecycle).
- **Production Stacks & Launchers**: [`n8n/docker-compose.yml`](n8n/docker-compose.yml), [`START_N8N.bat`](START_N8N.bat), [`START_N8N_WINDOWS.bat`](START_N8N_WINDOWS.bat), [`START_N8N_COCKPIT.bat`](START_N8N_COCKPIT.bat), [`scripts/start_n8n_windows.ps1`](scripts/start_n8n_windows.ps1).
- **Enterprise Workflows & Nodes Arsenal**: [`n8n/workflows/`](n8n/workflows/) (14 production DAGs: Section 14 Planetary Adversarial Red Team Zap, AI Agent Researcher, B2B Email Drafter Zap, Empire Operational Cycle Zap, Dropzone Ingestion Zap, M2M Financial Settlement Zap, GitHub Issue Triage Zap, Market Intelligence Zap, Outreach Dispatcher, Planetary Banking Audit Zap, Multi-Channel Notifier, System Health Monitor, Webhook Ingestion Bridge, Stripe Production Charge Sentinel) and SQLite FTS5 catalog [`data/n8n_arsenal.db`](data/n8n_arsenal.db).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/n8n_do_everything_manifest.json`](omega/data/n8n_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/N8N_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/N8N_SUPREME_ARCHITECTURE_DOSSIER.md).

### Apache Airflow Autonomous Workflow Orchestration & Data Pipeline Ecosystem
The global industry benchmark for programmatic workflow authoring, scheduling, and data engineering governance (https://github.com/apache/airflow):
- [`airflow-orchestrator`](.agent/skills/airflow-orchestrator/SKILL.md): Autonomous SDK, CLI, and operational standard for Apache Airflow 2.10.x & modern Airflow 3.0 Task SDK architectures.
- **Deep SDK & Master Engine**: [`airflow_orchestrator.py`](airflow_orchestrator.py) (Dual-mode: live Airflow REST API v1 client & ultra-high-fidelity offline simulation engine featuring Kahn's topological sort, TaskFlow API, Dynamic Task Mapping `.expand()`, Dataset/Asset data-driven scheduling, Deferrable Operators with Triggerer async event loop, Pools & Concurrency throttles, and XCom message exchange).
- **Universal CLI**: [`airflow_cli.py`](airflow_cli.py) (`info`, `dags`, `dag`, `dag-runs`, `trigger`, `pause`, `unpause`, `tasks`, `task-instances`, `xcom`, `variables`, `connections`, `pools`, `datasets`, `backfill`, `audit`, `do-everything`).
- **Autonomous Local API Server**: [`airflow_api_server.py`](airflow_api_server.py) (REST bridge on port 8775 serving health, DAGs, runs, variables, connections, telemetry, and the Mission Control Cockpit).
- **Model Context Protocol (MCP) Server**: [`airflow_mcp_server.py`](airflow_mcp_server.py) (Exposes 15 high-leverage Airflow agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`airflow_control_cockpit.html`](airflow_control_cockpit.html) (9 operational views: Telemetry & Scheduler Pulse, DAG Catalog, SVG Topological Graph Visualizer, Execution Grid & Gantt Matrix, Task Terminal Log Streamer, XCom Inspector, Fernet Secrets & Connections Vault, Pools & Concurrency Limiter, and MCP Agent Playground).
- **Production Stacks & Launchers**: [`stacks/airflow/docker-compose.yml`](stacks/airflow/docker-compose.yml), [`stacks/airflow/.env.example`](stacks/airflow/.env.example), [`START_AIRFLOW_WINDOWS.bat`](START_AIRFLOW_WINDOWS.bat), [`START_AIRFLOW_COCKPIT.bat`](START_AIRFLOW_COCKPIT.bat), [`scripts/start_airflow_windows.ps1`](scripts/start_airflow_windows.ps1).
- **Enterprise DAGs & Plugins**: [`airflow/dags/`](airflow/dags/) (Financial Ledger Reconciliation DAG, Autonomous Security Threat Recon DAG, CBAM Carbon Border ETL DAG with Dynamic Task Mapping, Customer Churn ML Pipeline with Datasets & Deferrable Operators, Daily Cloud DB Snapshot & S3 Vault DAG) and [`airflow/plugins/custom_omega_operators.py`](airflow/plugins/custom_omega_operators.py).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/airflow_do_everything_manifest.json`](omega/data/airflow_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/AIRFLOW_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/AIRFLOW_SUPREME_ARCHITECTURE_DOSSIER.md).

### PowerShell Autonomous Orchestration & Execution Ecosystem
Cross-platform object automation engine, AST parser, PSScriptAnalyzer security auditor, runspace concurrency, and enterprise infrastructure runbooks (https://github.com/PowerShell/PowerShell):
- [`powershell-orchestrator`](.agents/skills/powershell-orchestrator/SKILL.md): Autonomous SDK, CLI, and operational standard for PowerShell 7+ Core and Windows PowerShell environments.
- **Deep SDK & Master Engine**: [`powershell_orchestrator.py`](powershell_orchestrator.py) (Dual-mode: live PowerShell host execution with ConvertTo-Json streaming and high-fidelity simulated .NET 9 Core runtime).
- **Universal CLI**: [`powershell_cli.py`](powershell_cli.py) (`info`, `exec`, `ast`, `analyze`, `modules`, `gallery`, `runbooks`, `run-runbook`, `runspaces`, `cis-audit`, `benchmark`, `do-everything`).
- **Autonomous Local API Server**: [`powershell_api_server.py`](powershell_api_server.py) (REST bridge on port 8769 for telemetry, AST parsing, script analyzer, runbooks, and cockpit).
- **Model Context Protocol (MCP) Server**: [`powershell_mcp_server.py`](powershell_mcp_server.py) (Exposes 12 PowerShell agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`powershell_control_cockpit.html`](powershell_control_cockpit.html) (8 operational tabs: Terminal Studio, AST Parser, PSScriptAnalyzer Security, Runbooks, PSGallery, Runspaces, 12-Phase Lifecycle, and MCP Playground).
- **One-Click Launchers**: [`START_POWERSHELL_WINDOWS.bat`](START_POWERSHELL_WINDOWS.bat), [`START_POWERSHELL_COCKPIT.bat`](START_POWERSHELL_COCKPIT.bat), [`scripts/start_powershell_windows.ps1`](scripts/start_powershell_windows.ps1).
- **Enterprise Runbooks**: [`powershell/runbooks/`](powershell/runbooks/) (CIS OS Hardening, Multi-Cloud Infra Recon, Active Directory Threat Hunting, Network Latency Diagnostic, Service Self-Healing Watchdog).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/powershell_do_everything_manifest.json`](omega/data/powershell_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/POWERSHELL_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/POWERSHELL_SUPREME_ARCHITECTURE_DOSSIER.md).

### Blackbird OSINT & Defensive Intelligence Ecosystem
Multi-platform username & email reconnaissance, attack surface mapping, digital footprint indexing, and defensive OPSEC threat modeling across 692+ online platforms:
- [`blackbird-osint`](.agents/skills/blackbird-osint/SKILL.md): Autonomous standard operating procedure for handle reconnaissance, digital footprint auditing, and credential stuffing exposure assessment.
- **Deep SDK & Master Engine**: [`blackbird_orchestrator.py`](blackbird_orchestrator.py) (Async probes across 692+ WhatsMyName platforms, local & AI behavioral profiling, risk index scoring, and multi-format exporters).
- **Universal CLI**: [`blackbird_cli.py`](blackbird_cli.py) (`-u <user>`, `-e <email>`, `--audit`, `--permute`, `--category`, `--demo`, `--stats`, `--serve`).
- **Mission Control Cockpit**: [`blackbird_cockpit.html`](blackbird_cockpit.html) (Real-time dark cyber glass UI, interactive target search, platform census filters, attack surface grid, and one-click PDF/CSV export).
- **One-Click Launchers**: [`START_BLACKBIRD.bat`](START_BLACKBIRD.bat) & [`START_BLACKBIRD_COCKPIT.bat`](START_BLACKBIRD_COCKPIT.bat).
- **Audit Reports Vault**: [`blackbird_reports/`](blackbird_reports/) (Automated JSON, CSV, Markdown dossiers, and standalone interactive HTML dossiers).

### Microsoft PowerToys Autonomous Orchestration Ecosystem
Windows 11 power user utilities, multi-monitor window management, fast modular launcher, stay-awake daemon, and workstation optimization suite (https://github.com/microsoft/PowerToys):
- [`powertoys-orchestrator`](.agents/skills/powertoys-orchestrator/SKILL.md): Autonomous SDK, CLI, and operational standard for Microsoft PowerToys.
- **Deep SDK & Master Engine**: [`powertoys_orchestrator.py`](powertoys_orchestrator.py) (Dual-mode: live Windows host execution and high-fidelity simulated .NET 9.0 WinUI 3 runtime for all 24+ utilities).
- **Universal CLI**: [`powertoys_cli.py`](powertoys_cli.py) (`info`, `modules`, `toggle`, `fancyzones`, `awake`, `run-launcher`, `keyboard`, `hosts`, `advanced-paste`, `workspaces`, `ocr`, `security-audit`, `benchmark`, `do-everything`).
- **Autonomous Local API Server**: [`powertoys_api_server.py`](powertoys_api_server.py) (REST bridge on port 8770 serving telemetry, FancyZones layouts, PT Run queries, Awake toggles, Paste transforms, and cockpit).
- **Model Context Protocol (MCP) Server**: [`powertoys_mcp_server.py`](powertoys_mcp_server.py) (Exposes 16 PowerToys agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`powertoys_control_cockpit.html`](powertoys_control_cockpit.html) (10 operational tabs: Nexus Matrix, FancyZones Studio, PowerToys Run Spotlight, Awake Power Sentinel, Keyboard Manager, Hosts File Vault, Advanced Paste AI, Workspaces, Security & Hardening, 12-Phase Lifecycle, and MCP Playground).
- **One-Click Launchers**: [`START_POWERTOYS_WINDOWS.bat`](START_POWERTOYS_WINDOWS.bat), [`START_POWERTOYS_COCKPIT.bat`](START_POWERTOYS_COCKPIT.bat), [`scripts/start_powertoys_windows.ps1`](scripts/start_powertoys_windows.ps1).
- **Enterprise Profiles & Settings Vault**: [`powertoys/`](powertoys/) (`settings.json`, `fancyzones/zones-settings.json`, `awake/awake-settings.json`, `keyboard/default.json`, `hosts/sample_hosts.txt`, `advanced_paste/ai_templates.json`, `workspaces/workspaces-settings.json`).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/powertoys_do_everything_manifest.json`](omega/data/powertoys_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/POWERTOYS_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/POWERTOYS_SUPREME_ARCHITECTURE_DOSSIER.md).

### NSA Ghidra Autonomous Software Reverse Engineering (SRE) Ecosystem
Multi-architecture binary disassembler, Sleigh language instruction decoder, universal P-Code intermediate representation microcode engine, and high-fidelity pseudo-C decompiler (https://github.com/NationalSecurityAgency/ghidra):
- [`ghidra-orchestrator`](.agents/skills/ghidra-orchestrator/SKILL.md): Autonomous SDK, CLI, and operational standard for NSA Ghidra and software reverse engineering workflows.
- **Deep SDK & Master Engine**: [`ghidra_orchestrator.py`](ghidra_orchestrator.py) (Dual-mode: live Ghidra headless analyzer / PyGhidra bridge and pure-Python autonomous SRE simulation engine for PE, ELF, Mach-O, and raw shellcode).
- **Universal CLI**: [`ghidra_cli.py`](ghidra_cli.py) (`info`, `analyze`, `disasm`, `decompile`, `pcode`, `strings`, `sections`, `functions`, `vulns`, `entropy`, `rop`, `scripts`, `run-script`, `do-everything`).
- **Autonomous Local API Server**: [`ghidra_api_server.py`](ghidra_api_server.py) (REST bridge on port 8771 serving binary telemetry, disassembly, decompiler, P-code, strings, and cockpit).
- **Model Context Protocol (MCP) Server**: [`ghidra_mcp_server.py`](ghidra_mcp_server.py) (Exposes 16 Ghidra SRE agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`ghidra_control_cockpit.html`](ghidra_control_cockpit.html) (10 operational tabs: Triaging & Headers, Sleigh Disassembly, Pseudo-C Decompiler, P-Code Microcode, Functions & Call Graph, Strings & IOCs, Memory & Entropy, Vulnerabilities & ROP, SRE Script Vault, and Sovereign Lifecycle & MCP).
- **One-Click Launchers**: [`START_GHIDRA_WINDOWS.bat`](START_GHIDRA_WINDOWS.bat), [`START_GHIDRA_COCKPIT.bat`](START_GHIDRA_COCKPIT.bat), [`scripts/start_ghidra_windows.ps1`](scripts/start_ghidra_windows.ps1).
- **Enterprise SRE Scripts**: [`ghidra/scripts/`](ghidra/scripts/) (`find_dangerous_apis.py`, `recover_crypto_constants.py`, `rop_gadget_finder.py`, `entropy_packer_detector.py`, `export_ghidra_c_header.py`).
- **Deterministic SRE Samples**: [`ghidra/samples/`](ghidra/samples/) (`vulnerable_service.exe`).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/ghidra_do_everything_manifest.json`](omega/data/ghidra_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/GHIDRA_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/GHIDRA_SUPREME_ARCHITECTURE_DOSSIER.md).

### Infisical Autonomous SecretOps & Enterprise Security Ecosystem
Zero-Knowledge client-side encrypted secret management, dynamic leased credentials, high-throughput entropy secret leak scanning, internal PKI/CA certificate authority, and multi-cloud continuous sync (https://github.com/Infisical/infisical):
- [`infisical-orchestrator`](.agents/skills/infisical-orchestrator/SKILL.md): Autonomous SDK, CLI, and operational standard for Infisical SecretOps platform.
- **Deep SDK & Master Engine**: [`infisical_orchestrator.py`](infisical_orchestrator.py) (Dual-mode: live Infisical Server REST API and autonomous sovereign cryptographic engine with real AES-256-GCM, PBKDF2-HMAC-SHA256, RSA 2048/4096-bit, and real X.509 PKI certificates).
- **Universal CLI**: [`infisical_cli.py`](infisical_cli.py) (`status`, `projects`, `secrets`, `scan`, `dynamic`, `pki`, `integrations`, `access-requests`, `audit`, `run`, `do-everything`).
- **Autonomous Local API Server**: [`infisical_api_server.py`](infisical_api_server.py) (REST bridge on port 8772 serving telemetry, secrets, scanner, dynamic leases, PKI, and cockpit).
- **Model Context Protocol (MCP) Server**: [`infisical_mcp_server.py`](infisical_mcp_server.py) (Exposes 18 Infisical SecretOps agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`infisical_control_cockpit.html`](infisical_control_cockpit.html) (10 operational tabs: Secrets Vault, Secret Scanner, Dynamic Secrets, Internal PKI/CA, Cloud Sync, Break-Glass RBAC, Audit Blockchain, 12-Phase Lifecycle, and Agent MCP/API Studio).
- **One-Click Launchers**: [`START_INFISICAL_WINDOWS.bat`](START_INFISICAL_WINDOWS.bat), [`START_INFISICAL_COCKPIT.bat`](START_INFISICAL_COCKPIT.bat), [`scripts/start_infisical_windows.ps1`](scripts/start_infisical_windows.ps1).
- **Enterprise SecretOps Vault & Assets**: [`infisical/`](infisical/) (`docker-compose.yml`, `policies/rbac_matrix.json`, `templates/production_secrets.template`, `configs/dynamic_db_rotation.json`, `certs/root_ca_config.cnf`).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/infisical_do_everything_manifest.json`](omega/data/infisical_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/INFISICAL_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/INFISICAL_SUPREME_ARCHITECTURE_DOSSIER.md).

### Free-For-Dev Autonomous Developer Cloud & Zero-Dollar Stack Ecosystem
Autonomous developer cloud intelligence, multi-provider quota comparison, 1,396+ developer free tiers, and zero-dollar production architecture synthesis (https://github.com/ripienaar/free-for-dev):
- [`free-for-dev`](.agents/skills/free-for-dev/SKILL.md) & [`free-tools`](.agents/skills/free-tools/SKILL.md): Autonomous standard operating procedures for zero-cost developer infrastructure, multi-vendor quota comparison, and architecture audits.
- **Deep SDK & Master Engine**: [`free_for_dev_orchestrator.py`](free_for_dev_orchestrator.py) (Parses 1,396+ offerings across 57 categories, SQLite FTS5 search, zero-credit-card filter, and automated stack synthesis).
- **Universal CLI**: [`free_for_dev_cli.py`](free_for_dev_cli.py) (`info`, `categories`, `search`, `service`, `compare`, `stack`, `audit`, `no-card`, `export`, `do-everything`).
- **Autonomous Local API Server**: [`free_for_dev_api_server.py`](free_for_dev_api_server.py) (REST bridge on port 8771 serving telemetry, search, comparative matrix, stack blueprints, audit, and cockpit).
- **Model Context Protocol (MCP) Server**: [`free_for_dev_mcp_server.py`](free_for_dev_mcp_server.py) (Exposes 9 Free-For-Dev agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`free_for_dev_cockpit.html`](free_for_dev_cockpit.html) (8 operational tabs: Catalog Explorer, Zero-Dollar Stack Architect, Provider Battleground, Architecture Feasibility Auditor, No-Credit-Card Sanctuary, Terminal Simulator, 12-Phase Lifecycle, and MCP Playground).
- **One-Click Launchers**: [`START_FREE_FOR_DEV_WINDOWS.bat`](START_FREE_FOR_DEV_WINDOWS.bat), [`START_FREE_FOR_DEV_COCKPIT.bat`](START_FREE_FOR_DEV_COCKPIT.bat), [`scripts/start_free_for_dev_windows.ps1`](scripts/start_free_for_dev_windows.ps1).
- **Attested Data Stores & Vaults**: [`data/free_for_dev_catalog.json`](data/free_for_dev_catalog.json), [`data/free_for_dev.sqlite3`](data/free_for_dev.sqlite3), [`data/free_for_dev_stacks.json`](data/free_for_dev_stacks.json), [`data/free_for_dev_export.csv`](data/free_for_dev_export.csv), [`data/free_for_dev_export.md`](data/free_for_dev_export.md).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/free_for_dev_do_everything_manifest.json`](omega/data/free_for_dev_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/FREE_FOR_DEV_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/FREE_FOR_DEV_SUPREME_ARCHITECTURE_DOSSIER.md).

### Apache Arrow Autonomous Columnar & Zero-Copy Ecosystem
Universal high-performance in-memory columnar data format, zero-copy buffer slicing, Acero vectorized relational compute, C Data Interface ABI, Arrow Flight RPC, and compressed Parquet storage (https://github.com/apache/arrow):
- [`arrow-orchestrator`](.agents/skills/arrow-orchestrator/SKILL.md): Autonomous SDK, CLI, Acero vectorized compute engine, C Data Interface ABI bridge, Flight RPC, and 12-phase sovereign lifecycle standard for Apache Arrow.
- **Deep SDK & Master Engine**: [`arrow_orchestrator.py`](arrow_orchestrator.py) (Dual-mode: official Apache PyArrow 26.0.0+ C++ core bindings and pure-Python 64-byte aligned binary buffer engine, LSB-first validity bitmaps, StringView German string descriptors, and ctypes C Data Interface ABI).
- **Universal CLI**: [`arrow_cli.py`](arrow_cli.py) (`info`, `schemas`, `create`, `inspect`, `slice`, `compute`, `ipc`, `feather`, `parquet`, `c-data`, `flight`, `benchmark`, `do-everything`).
- **Autonomous Local API Server**: [`arrow_api_server.py`](arrow_api_server.py) (REST bridge on port 8775 serving telemetry, schemas, in-memory tables, vectorized queries, C Data Interface, Parquet, and cockpit).
- **Model Context Protocol (MCP) Server**: [`arrow_mcp_server.py`](arrow_mcp_server.py) (Exposes 12 Apache Arrow agent tools via stdio JSON-RPC).
- **Interactive Mission Control Cockpit**: [`arrow_control_cockpit.html`](arrow_control_cockpit.html) (10 operational tabs: Columnar Memory & Validity, Schema Studio, Table Explorer, Acero Vectorized Compute, C Data Interface ABI, Parquet & IPC Vault, Arrow Flight RPC, Micro-Benchmarks, 12-Phase Lifecycle, and MCP Agent Tools).
- **One-Click Launchers**: [`START_ARROW_WINDOWS.bat`](START_ARROW_WINDOWS.bat), [`START_ARROW_COCKPIT.bat`](START_ARROW_COCKPIT.bat).
- **Enterprise Schemas & Pipelines**: [`arrow/schemas/`](arrow/schemas/) (`financial_trades.json`, `iot_sensor_telemetry.json`, `customer_risk_profile.json`, `orderbook_l3_nested.json`), [`arrow/queries/`](arrow/queries/) (`vwap_aggregation.json`, `sensor_anomaly_filter.json`), and [`arrow/c_interface/arrow_c_abi.h`](arrow/c_interface/arrow_c_abi.h).
- **Master 12-Phase Sovereign Lifecycle**: [`omega/data/arrow_do_everything_manifest.json`](omega/data/arrow_do_everything_manifest.json) (`do_everything` validation across all 12 platform layers).
- **Architecture Teardown Dossier**: [`docs/ARROW_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/ARROW_SUPREME_ARCHITECTURE_DOSSIER.md).

### Computer Science Video Courses & Academic Intelligence Ecosystem
Comprehensive university-grade Computer Science video lecture catalog, relational FTS5 search index, and degree-grade career roadmaps sourced from [`Developer-Y/cs-video-courses`](https://github.com/Developer-Y/cs-video-courses):
- **Deep Engine & SQLite FTS5 Database**: [`cs_courses_engine.py`](cs_courses_engine.py) (Indexes 1,434 courses, 957 video playlists, 26 tracks, and 44 institutions into [`data/cs_video_courses.db`](data/cs_video_courses.db) and [`data/cs_video_courses.json`](data/cs_video_courses.json)).
- **Career Roadmaps Engine**: [`cs_courses_roadmaps.py`](cs_courses_roadmaps.py) (9 four-tier degree-grade career curricula for GenAI, Distributed Systems, Database Storage, Quant Algorithms, Applied ML, Security, Robotics, Computer Vision, and Software Architecture in [`docs/curricula/`](docs/curricula/)).
- **Universal CLI**: [`cs_courses_cli.py`](cs_courses_cli.py) (`info`, `search`, `tracks`, `track`, `institutions`, `institution`, `roadmaps`, `roadmap`, `export`, `serve`, `do-everything`).
- **Autonomous Local API Server**: [`cs_courses_api_server.py`](cs_courses_api_server.py) (Lightweight REST bridge on port 8779 serving `/api/info`, `/api/courses`, `/api/tracks`, `/api/institutions`, `/api/roadmaps`, and `/api/curricula`).
- **Interactive Mission Control Cockpit**: [`cs_video_courses_cockpit.html`](cs_video_courses_cockpit.html) (Glassmorphism UI with real-time course search, multi-filtering by track/university/level, 4-tier interactive degree roadmaps with progress tracking, university hub, and local learning queue).
- **One-Click Launchers**: [`START_CS_COURSES_COCKPIT.bat`](START_CS_COURSES_COCKPIT.bat).
- **Architecture Teardown Dossier**: [`docs/CS_VIDEO_COURSES_SUPREME_GUIDE.md`](docs/CS_VIDEO_COURSES_SUPREME_GUIDE.md).

### Hiring Without Whiteboards Engineering & Career Ecosystem
Comprehensive directory, SQLite FTS5 search index, and interview intelligence for 761+ companies assessing practical software engineering capability over LeetCode/whiteboard hazing, sourced from canonical [`poteto/hiring-without-whiteboards`](https://github.com/poteto/hiring-without-whiteboards):
- **Deep Engine & SQLite FTS5 Database**: [`hiring_without_whiteboards_engine.py`](hiring_without_whiteboards_engine.py) (Indexes 761 companies into [`data/hiring_without_whiteboards.json`](data/hiring_without_whiteboards.json), [`data/hiring_without_whiteboards.csv`](data/hiring_without_whiteboards.csv), and [`data/hiring_without_whiteboards.sqlite`](data/hiring_without_whiteboards.sqlite)).
- **Cockpit Generator**: [`scripts/generate_hww_cockpit.py`](scripts/generate_hww_cockpit.py).
- **Interactive Mission Control Cockpit**: [`hiring_without_whiteboards_cockpit.html`](hiring_without_whiteboards_cockpit.html) (Real-time search, process taxonomy breakdown, tailored outreach pitches, and quick filters).
- **One-Click Launcher**: [`START_HIRING_WITHOUT_WHITEBOARDS_COCKPIT.bat`](START_HIRING_WITHOUT_WHITEBOARDS_COCKPIT.bat) (Serves API & Cockpit on port 8780).

### MONEYVERSE ∞ Master Intelligence
- **Master Prompt Dossier**: [`docs/MONEYVERSE_INFINITY_MASTER_PROMPT.md`](docs/MONEYVERSE_INFINITY_MASTER_PROMPT.md) (Integrated intelligence and execution system for wealth creation, AI-native business building, market research, automated pipelines, and long-term financial optimization).

### Launch Video & Product Showcase Engine
- [`brag`](.agents/skills/brag/SKILL.md): Turn the current project website or codebase into a short, polished, shareable launch video using Hyperframes with bundled music, SFX, and custom tone presets.
- [`brag-slim`](.agents/skills/brag-slim/SKILL.md): Lean, zero-dependency launch video generator running locally on native tools (HTML/Canvas/Puppeteer/ffmpeg) for rapid social showcase clips.

### System Prompts Intelligence Ecosystem
- [`system-prompts-intelligence`](.agents/skills/system-prompts-intelligence/SKILL.md): Query and inspect system prompt architectures, extracted tool signatures, and prompt patterns from Google Antigravity, Anthropic Claude Code, OpenAI Codex, Cursor, and Grok.
- [`prompts-chat`](.agents/skills/prompts-chat/SKILL.md): Query, retrieve, interpolate variables, and improve prompts from the 2,627 curated prompts library (f/prompts.chat).
- [`prompt-lookup`](.agents/skills/prompt-lookup/SKILL.md): Discover, search, and retrieve battle-tested prompt templates via MCP.
- [`skill-lookup`](.agents/skills/skill-lookup/SKILL.md): Search, retrieve, and inspect across all 3,841+ installed agent skills.
- **Prompts Studio Cockpit**: [`prompts_chat_cockpit.html`](prompts_chat_cockpit.html) / `START_PROMPTS_CHAT_COCKPIT.bat`
- **Prompts Deep Engine & CLI**: [`prompts_chat_engine.py`](prompts_chat_engine.py) / [`prompts_chat_cli.py`](prompts_chat_cli.py)
- **Local MCP Server**: [`prompts_chat_mcp_server.py`](prompts_chat_mcp_server.py)
- **Apex Agent Meta-Prompt**: [`research/APEX_AGENT_SYSTEM_PROMPT.md`](research/APEX_AGENT_SYSTEM_PROMPT.md)
- **Agent Tooling Patterns**: [`research/AGENT_TOOLING_PATTERNS.md`](research/AGENT_TOOLING_PATTERNS.md)
- **Interactive Explorer**: [`research/system_prompts_explorer.html`](research/system_prompts_explorer.html)
- **Prompt CLI**: `python research/prompt_cli.py`

### Sovereign Empire & Multi-Trillion Dollar Autonomous Engine
- [`empire-capital-allocator`](.agent/skills/empire-capital-allocator/SKILL.md): Sovereign treasury management, capital velocity compounding, and macro arterial siphon optimization.
- [`sovereign-chokehold-architect`](.agent/skills/sovereign-chokehold-architect/SKILL.md): Construction of unassailable economic moats, non-replicable physical assets, and high switching-cost standards.
- [`planetary-fleet-ops`](.agent/skills/planetary-fleet-ops/SKILL.md): Autonomous orchestration of million-unit humanoid robot swarms across distributed manufacturing plants and fulfillment centers.
- [`m2m-settlement-clearing`](.agent/skills/m2m-settlement-clearing/SKILL.md): Zero-friction cryptographic machine-to-machine micro-invoicing and real-time state channel settlement.
- [`energy-compute-coupling`](.agent/skills/energy-compute-coupling/SKILL.md): Collocation of Small Modular Nuclear Reactors (SMRs) directly with terawatt AI compute hubs.
- [`geopolitical-sovereign-shield`](.agent/skills/geopolitical-sovereign-shield/SKILL.md): International regulatory arbitrage, CFIUS defense, dual-use export control immunity, and bilateral treaty alignment.
- [`biomanufacturing-scaling`](.agent/skills/biomanufacturing-scaling/SKILL.md): Optimization of precision cellular fermentation, synthetic genetic compilation, and petrochemical replacement.
- [`antifragile-red-team`](.agent/skills/antifragile-red-team/SKILL.md): Adversarial stress testing of sovereign infrastructure across nuclear grid severance, subsea fiber cuts, and financial network freezes.
- [`sovereign-wealth-syndication`](.agent/skills/sovereign-wealth-syndication/SKILL.md): Structuring multi-billion dollar blended infrastructure syndications across SWFs, green nuclear bonds, and enterprise forward off-take tranches.
- [`sovereign-banking-engine`](.agent/skills/sovereign-banking-engine/SKILL.md): Comprehensive institutional banking covering Central Banking liquidity corridors, DCM, syndicated lending, cash pooling/netting, trade finance LCs, custody AUC, tri-party repo, prime brokerage, and derivatives clearing.
- **Apex Orchestrator**: [`sovereign_continuum/empire_orchestrator.py`](sovereign_continuum/empire_orchestrator.py)
- **Bank of the Continuum**: [`sovereign_continuum/banking/autonomous_sovereign_bank.py`](sovereign_continuum/banking/autonomous_sovereign_bank.py)
- **Unified Empire CLI**: `python -m terra_kinetics.cli --empire-cycle` / `--skills-audit` / `--red-team` / `--banking`

### CIVILIZATION Ω∞∞ Autonomous Capability Generation Ecosystem
Master specifications and meta-orchestration for unbounded human capability generation (Directives 120–147):
- [`civilization-capability-generator`](.agent/skills/civilization-capability-generator/SKILL.md): Recursive synthesis of domain skills, specialized agents, and sandboxed capability harnesses.
- [`failed-solution-memory`](.agent/skills/failed-solution-memory/SKILL.md): Immutable indexing and querying of disproven hypotheses and architectural postmortems.
- [`unknown-engine`](.agent/skills/unknown-engine/SKILL.md): Proactive epistemic auditing (*"What am I missing?"*, *"Why hasn't this been done?"*).
- [`second-order-effect-simulator`](.agent/skills/second-order-effect-simulator/SKILL.md): Multi-scenario causal ripple simulations across geopolitical, financial, and physical networks.
- **Master Specification**: [`docs/CIVILIZATION_OMEGA_UNBOUNDED_SPEC.md`](docs/CIVILIZATION_OMEGA_UNBOUNDED_SPEC.md)
- **Capability Engine Core**: [`sovereign_continuum/capability_engine.py`](sovereign_continuum/capability_engine.py)


### OpenBB Open Data Platform (ODP v5.0.0) Financial Intelligence Ecosystem
Institutional-grade, multi-asset financial data platform providing 888 analytical endpoints across 90 routers, 19 data providers, Model Context Protocol (FastMCP) integration, REST API, CLI, and Desktop:
- **Core SDK**: `from openbb import obb` (Equities, Fixed Income, Economy, Crypto, Currency, Derivatives, Regulators, ETFs, Index).
- **FastMCP Server**: [`openbb_mcp_server`](OpenBB/openbb_platform/extensions/mcp_server) exposing 14 dynamic tool discovery and dispatch tools directly to AI agents over stdio and SSE/HTTP (port 8001).
- **Platform REST API**: [`openbb-platform-api`](OpenBB/openbb_platform/extensions/platform_api) FastAPI backend serving interactive Swagger/OpenAPI documentation on port 6900.
- **Desktop Application**: [`desktop/`](OpenBB/desktop) Vite/React quantitative workstation bundle.
- **Supreme Orchestrator & CLI**: [`openbb_orchestrator.py`](openbb_orchestrator.py) (`info`, `serve-api`, `serve-mcp`, `cli`, `repl`, `desktop-dev`, `test`).
- **Antigravity MCP Registration**: Registered in `C:\Users\amehr\.gemini\settings.json` and `C:\Users\amehr\.gemini\antigravity\mcp\openbb`.
- **One-Click Windows Launcher**: [`START_OPENBB_SYSTEM.bat`](START_OPENBB_SYSTEM.bat) (Interactive 9-option terminal control center).
- **Architecture Teardown Dossier**: [`docs/OPENBB_SUPREME_ARCHITECTURE_DOSSIER.md`](docs/OPENBB_SUPREME_ARCHITECTURE_DOSSIER.md).

### Issue tracker

Local markdown issue tracking under `.scratch/`. See [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md).

### Triage labels

Five canonical triage roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md).

### Domain docs

Single-context repository layout (`CONTEXT.md` at root and ADRs in `docs/adr/`). See [`docs/agents/domain.md`](docs/agents/domain.md).


