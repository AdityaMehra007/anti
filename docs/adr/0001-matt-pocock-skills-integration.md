# ADR 0001: Integration of Matt Pocock Engineering Skills

## Status
Accepted

## Date
2026-09-05

## Context
The repository houses an autonomous enterprise career intelligence and multi-agent system comprising 3,000+ skills, autonomous swarms, ATS parsers, and data pipelines. To ensure rigorous software engineering discipline, prevent architecture degradation, and eliminate misalignment, a standardized set of engineering and productivity agent skills was needed.

## Decision
We have adopted and integrated Matt Pocock's Skills framework (`mattpocock/skills`) directly into `.agents/skills/` and registered them in `.agents/skills.json`.
1. **Grilling & Alignment**: Adopted `/grill-me`, `/grill-with-docs`, and `grilling` to resolve all decision branches before implementation.
2. **Ubiquitous Language**: Standardized system entities and terms in `CONTEXT.md`.
3. **Engineering Rigor**: Mandated Red-Green-Refactor via `/tdd` and structured hypothesis testing via `/diagnosing-bugs`.
4. **Architecture Maintenance**: Enabled deep module surveys via `/improve-codebase-architecture` and `/codebase-design`.
5. **Issue & Spec Workflow**: Established local markdown issue tracking in `.scratch/` with `/to-spec`, `/to-tickets`, and `/wayfinder`.

## Consequences
- Agents operate with consistent terminology and strict feedback loops.
- Decisions are documented in `docs/adr/` and issues are tracked in `.scratch/`.
- No reliance on brittle "vibe coding"; every change is gated by verification and tests.
