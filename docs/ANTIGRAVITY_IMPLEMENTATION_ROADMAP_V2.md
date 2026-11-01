# Implementation Roadmap v2

## Stage 0: Safe baseline
- [ ] Confirm the intended workspace and Antigravity surface/version.
- [ ] Inspect Git status, existing user changes and existing configuration.
- [ ] Inventory supported skills/rules/plugins/MCP paths using current official docs.
- [ ] Record environment facts, constraints, data classes and baseline checks.
- [ ] Create `docs/ANTIGRAVITY_BASELINE.md`.

## Stage 1: Objective and system map
- [ ] Write objective, acceptance criteria, non-goals, success metrics and budget constraints.
- [ ] Map current vs proposed components, trust boundaries, data flows and failure points.
- [ ] Identify the single highest-leverage bottleneck before choosing tools.

## Stage 2: Instructions and reusable skills
- [ ] Merge rules; don't overwrite existing instruction files blindly.
- [ ] Validate skill paths and YAML frontmatter for the actual Antigravity surface.
- [ ] Use focused skills, not one huge always-active instruction file.
- [ ] Migrate legacy workflows only after making backups and checking current docs.

## Stage 3: Repository/integration vetting
- [ ] Use the catalogue as a menu, not an installation list.
- [ ] Check license, maintenance, compatibility, install scripts, dependencies, outbound data, permissions, security and cost.
- [ ] Score candidates and document confidence/evidence.
- [ ] Select at most 3–7 first-wave integrations with an evidenced use case.

## Stage 4: Small safe implementation
- [ ] Integrate one component at a time.
- [ ] Use least-privilege/test credentials/read-only defaults.
- [ ] Ask approval for global installs, credentials, external writes, paid resources and production operations.
- [ ] Verify one representative task and document disable/uninstall/rollback.

## Stage 5: Quality, evaluation and security
- [ ] Run relevant tests, type checks, lint, build, secret scan and dependency checks.
- [ ] Add regression tests and a small golden evaluation set for AI workflows.
- [ ] Verify prompt-injection resistance, authorization and error/fallback behavior.
- [ ] Inspect diff and generated artifacts.

## Stage 6: Operationalize
- [ ] Document task state, findings, decisions, known issues and runbooks.
- [ ] Add observability and cost tracking if proportionate to the workload.
- [ ] Define backup, restore, rollback and incident procedures for systems that need them.

## Stage 7: Measure and improve
- [ ] Compare to baseline; record measured improvements or no improvement.
- [ ] Remove redundant tools and failed experiments.
- [ ] Prioritize by impact, effort, risk, confidence and maintenance cost.

## Completion requirements
A stage requires evidence or a clearly documented blocker. Don't mark boxes complete just because a prompt was written or a command was attempted.