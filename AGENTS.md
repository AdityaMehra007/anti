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

### Supabase Database Ecosystem
Synchronized from [`supabase/agent-skills`](https://github.com/supabase/agent-skills):
- [`supabase-postgres-best-practices`](.agents/skills/supabase-postgres-best-practices/SKILL.md): Schema design, indexing, RLS policy audit, query performance, and connection scaling rules
- [`supabase`](.agents/skills/supabase/SKILL.md): Supabase product integration across Auth, Realtime, Storage, Edge Functions, and Vector search


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

### Launch Video & Product Showcase Engine
- [`brag`](.agents/skills/brag/SKILL.md): Turn the current project website or codebase into a short, polished, shareable launch video using Hyperframes with bundled music, SFX, and custom tone presets.
- [`brag-slim`](.agents/skills/brag-slim/SKILL.md): Lean, zero-dependency launch video generator running locally on native tools (HTML/Canvas/Puppeteer/ffmpeg) for rapid social showcase clips.

### System Prompts Intelligence Ecosystem
- [`system-prompts-intelligence`](.agents/skills/system-prompts-intelligence/SKILL.md): Query and inspect system prompt architectures, extracted tool signatures, and prompt patterns from Google Antigravity, Anthropic Claude Code, OpenAI Codex, Cursor, and Grok.
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

### Issue tracker

Local markdown issue tracking under `.scratch/`. See [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md).

### Triage labels

Five canonical triage roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md).

### Domain docs

Single-context repository layout (`CONTEXT.md` at root and ADRs in `docs/adr/`). See [`docs/agents/domain.md`](docs/agents/domain.md).


