# Matt Pocock Skills Catalog & Integration

All skills from [`mattpocock/skills`](https://github.com/mattpocock/skills) have been installed into `.agents/skills/` and registered into `.agents/skills.json`.

**Total Installed Skills:** 36


## Matt Pocock Engineering

| Skill Name | Invocation Mode | Description | Path |
| :--- | :--- | :--- | :--- |
| `ask-matt` | User-Invoked | Ask which skill or flow fits your situation. A router over the skills in this repo. | [`.agents/skills/ask-matt/SKILL.md`](.agents/skills/ask-matt/SKILL.md) |
| `code-review` | Model-Invoked | "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"." | [`.agents/skills/code-review/SKILL.md`](.agents/skills/code-review/SKILL.md) |
| `codebase-design` | Model-Invoked | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary. | [`.agents/skills/codebase-design/SKILL.md`](.agents/skills/codebase-design/SKILL.md) |
| `diagnosing-bugs` | Model-Invoked | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. | [`.agents/skills/diagnosing-bugs/SKILL.md`](.agents/skills/diagnosing-bugs/SKILL.md) |
| `domain-modeling` | Model-Invoked | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR. | [`.agents/skills/domain-modeling/SKILL.md`](.agents/skills/domain-modeling/SKILL.md) |
| `grill-with-docs` | User-Invoked | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. | [`.agents/skills/grill-with-docs/SKILL.md`](.agents/skills/grill-with-docs/SKILL.md) |
| `implement` | User-Invoked | "Implement a piece of work based on a spec or set of tickets." | [`.agents/skills/implement/SKILL.md`](.agents/skills/implement/SKILL.md) |
| `improve-codebase-architecture` | User-Invoked | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. | [`.agents/skills/improve-codebase-architecture/SKILL.md`](.agents/skills/improve-codebase-architecture/SKILL.md) |
| `prototype` | Model-Invoked | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like. | [`.agents/skills/prototype/SKILL.md`](.agents/skills/prototype/SKILL.md) |
| `research` | Model-Invoked | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent. | [`.agents/skills/research/SKILL.md`](.agents/skills/research/SKILL.md) |
| `resolving-merge-conflicts` | Model-Invoked | "Use when you need to resolve an in-progress git merge/rebase conflict." | [`.agents/skills/resolving-merge-conflicts/SKILL.md`](.agents/skills/resolving-merge-conflicts/SKILL.md) |
| `setup-matt-pocock-skills` | User-Invoked | "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills." | [`.agents/skills/setup-matt-pocock-skills/SKILL.md`](.agents/skills/setup-matt-pocock-skills/SKILL.md) |
| `tdd` | Model-Invoked | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. | [`.agents/skills/tdd/SKILL.md`](.agents/skills/tdd/SKILL.md) |
| `to-spec` | User-Invoked | "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed." | [`.agents/skills/to-spec/SKILL.md`](.agents/skills/to-spec/SKILL.md) |
| `to-tickets` | User-Invoked | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker). | [`.agents/skills/to-tickets/SKILL.md`](.agents/skills/to-tickets/SKILL.md) |
| `triage` | User-Invoked | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs. | [`.agents/skills/triage/SKILL.md`](.agents/skills/triage/SKILL.md) |
| `wayfinder` | User-Invoked | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. | [`.agents/skills/wayfinder/SKILL.md`](.agents/skills/wayfinder/SKILL.md) |
| `wizard` | Model-Invoked | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself. | [`.agents/skills/wizard/SKILL.md`](.agents/skills/wizard/SKILL.md) |

## Matt Pocock Productivity

| Skill Name | Invocation Mode | Description | Path |
| :--- | :--- | :--- | :--- |
| `grill-me` | User-Invoked | A relentless interview to sharpen a plan or design. | [`.agents/skills/grill-me/SKILL.md`](.agents/skills/grill-me/SKILL.md) |
| `grilling` | Model-Invoked | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. | [`.agents/skills/grilling/SKILL.md`](.agents/skills/grilling/SKILL.md) |
| `handoff` | User-Invoked | Compact the current conversation into a handoff document for another agent to pick up. | [`.agents/skills/handoff/SKILL.md`](.agents/skills/handoff/SKILL.md) |
| `teach` | User-Invoked | Teach the user a new skill or concept, within this workspace. | [`.agents/skills/teach/SKILL.md`](.agents/skills/teach/SKILL.md) |
| `to-questionnaire` | User-Invoked | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. | [`.agents/skills/to-questionnaire/SKILL.md`](.agents/skills/to-questionnaire/SKILL.md) |
| `wait-what` | User-Invoked | "Stop. That last message did not land: re-pitch it." | [`.agents/skills/wait-what/SKILL.md`](.agents/skills/wait-what/SKILL.md) |
| `writing-for-agents` | Model-Invoked | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. | [`.agents/skills/writing-for-agents/SKILL.md`](.agents/skills/writing-for-agents/SKILL.md) |

## Matt Pocock Misc

| Skill Name | Invocation Mode | Description | Path |
| :--- | :--- | :--- | :--- |
| `git-guardrails-claude-code` | Model-Invoked | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code. | [`.agents/skills/git-guardrails-claude-code/SKILL.md`](.agents/skills/git-guardrails-claude-code/SKILL.md) |
| `migrate-to-shoehorn` | Model-Invoked | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data. | [`.agents/skills/migrate-to-shoehorn/SKILL.md`](.agents/skills/migrate-to-shoehorn/SKILL.md) |
| `scaffold-exercises` | Model-Invoked | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section. | [`.agents/skills/scaffold-exercises/SKILL.md`](.agents/skills/scaffold-exercises/SKILL.md) |
| `setup-pre-commit` | Model-Invoked | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing. | [`.agents/skills/setup-pre-commit/SKILL.md`](.agents/skills/setup-pre-commit/SKILL.md) |

## Matt Pocock In-Progress

| Skill Name | Invocation Mode | Description | Path |
| :--- | :--- | :--- | :--- |
| `claude-handoff` | User-Invoked | Hand the current conversation off to a fresh background agent that picks up the work immediately. | [`.agents/skills/claude-handoff/SKILL.md`](.agents/skills/claude-handoff/SKILL.md) |
| `implement-spec` | User-Invoked | "Implement a specification in code." | [`.agents/skills/implement-spec/SKILL.md`](.agents/skills/implement-spec/SKILL.md) |
| `loop-me` | User-Invoked | Grill me about specs for the workflows I want to build, within this workspace. | [`.agents/skills/loop-me/SKILL.md`](.agents/skills/loop-me/SKILL.md) |
| `setup-ts-deep-modules` | User-Invoked | Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable only through its entry-point files. User-invoked. | [`.agents/skills/setup-ts-deep-modules/SKILL.md`](.agents/skills/setup-ts-deep-modules/SKILL.md) |
| `writing-beats` | User-Invoked | Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it. | [`.agents/skills/writing-beats/SKILL.md`](.agents/skills/writing-beats/SKILL.md) |
| `writing-fragments` | User-Invoked | "Writing, explore: mine raw fragments, no structure yet." | [`.agents/skills/writing-fragments/SKILL.md`](.agents/skills/writing-fragments/SKILL.md) |
| `writing-shape` | User-Invoked | "Writing, exploit: shape raw material into an article, paragraph by paragraph." | [`.agents/skills/writing-shape/SKILL.md`](.agents/skills/writing-shape/SKILL.md) |
