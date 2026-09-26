# Domain Docs

How engineering and agent skills consume this repo's domain documentation.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root: defines the ubiquitous language, system boundaries, and core entities.
- **`docs/adr/`**: read Architecture Decision Records (ADRs) that touch the area you are about to work in.

## File structure

Single-context repo:

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-matt-pocock-skills-integration.md
├── .agents/
│   ├── skills/
│   ├── skills.json
│   └── agents.json
├── docs/agents/
│   ├── issue-tracker.md
│   ├── triage-labels.md
│   └── domain.md
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, or a test name), use the term as defined in `CONTEXT.md`. Avoid drifting to undefined synonyms.

If the concept you need isn't in the glossary yet, that is a signal: either you're inventing language the project doesn't use, or there is a real gap to document via `domain-modeling`.

## Flag ADR conflicts

If your proposal contradicts an existing ADR, surface it explicitly:
> *Contradicts ADR-0001 (...), but worth reopening because...*
