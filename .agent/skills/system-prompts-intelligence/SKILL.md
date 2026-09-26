---
name: system-prompts-intelligence
description: Reference library and CLI intelligence tool for querying, inspecting, and applying system prompt architectures from 423 leaked production AI models (Anthropic Claude Code, Google Antigravity, OpenAI Codex, Cursor, Grok, etc.).
---

# System Prompts Intelligence & Agent Scaffolding

This skill equips any autonomous coding agent in this workspace with operational access to the **423 leaked production system prompts** stored locally in `e:\anti\research\system_prompts_leaks`.

---

## 1. When to Use This Skill

- When designing or updating agent system prompts, roles, subagents, or task definitions.
- When selecting tool signatures and parameter schemas (e.g., atomic chunk replacement vs unified diff vs bash execution).
- When implementing planning modes, safety gates, or anti-jailbreak negative constraints.
- When benchmarking or comparing how different labs (Google, Anthropic, OpenAI, xAI, Microsoft) instruct their models.

---

## 2. Using the CLI Intelligence Tool

The repository provides a fast, deterministic CLI tool located at `e:\anti\research\prompt_cli.py`. Agents and humans can invoke it directly via terminal:

### A. List Prompts
```powershell
# List all prompts with tool calling
python e:\anti\research\prompt_cli.py list --has-tools --limit 20

# Filter by provider
python e:\anti\research\prompt_cli.py list --provider Google
python e:\anti\research\prompt_cli.py list --provider Anthropic
python e:\anti\research\prompt_cli.py list --provider OpenAI
```

### B. Search Prompts
```powershell
# Search prompts by model name or keyword
python e:\anti\research\prompt_cli.py search "code-review"
python e:\anti\research\prompt_cli.py search "plan mode" --deep
```

### C. Show Raw Prompt
```powershell
# View full text of a system prompt
python e:\anti\research\prompt_cli.py show "antigravity-cli.md"
python e:\anti\research\prompt_cli.py show "claude-code-fable-5.1.md" --lines 100
python e:\anti\research\prompt_cli.py show "gpt-6-astra.md"
```

### D. Architectural Comparison
```powershell
# Compare two prompts side-by-side
python e:\anti\research\prompt_cli.py compare "antigravity" "fable-5.1"
python e:\anti\research\prompt_cli.py compare "gpt-5.6" "cursor"
```

### E. Extracted Tool Signatures
```powershell
# View all detected tools and their origins
python e:\anti\research\prompt_cli.py tools
```

---

## 3. Core Architectural Blueprints

When building agents, consult the following synthesized documents:

1. **[`APEX_AGENT_SYSTEM_PROMPT.md`](file:///e:/anti/research/APEX_AGENT_SYSTEM_PROMPT.md)**:
   The ultimate plug-and-play meta-prompt combining Google Antigravity, Anthropic Claude Code, OpenAI Codex, and Cursor.
2. **[`AGENT_TOOLING_PATTERNS.md`](file:///e:/anti/research/AGENT_TOOLING_PATTERNS.md)**:
   Deep breakdown of the 4 mutation paradigms, the Two-Phase State Machine, and high-impact negative constraints.
3. **[`AGENT_TOOLS_MANIFEST.json`](file:///e:/anti/research/AGENT_TOOLS_MANIFEST.json)**:
   Standardized JSON manifest of 57 production tools extracted from the repository.
4. **[`SYSTEM_PROMPTS_COMPENDIUM.md`](file:///e:/anti/research/SYSTEM_PROMPTS_COMPENDIUM.md)**:
   Human-readable catalog organized by provider.

---

## 4. Key Rules for Agent Prompt Design

1. **Ponytail Minimalism**: Never invent speculative code or unnecessary abstractions. Stop at the lowest rung of The Ladder.
2. **Root-Cause Repair**: Treat bug reports as symptoms. Trace callers and fix the shared origin once rather than scattering defensive guards.
3. **Strict Planning Gating**: Enforce a read-only exploration phase before executing code mutations. Require explicit user or orchestrator confirmation.
4. **Reactive Wakeups (No Polling)**: Never poll task status or use sleep loops. Yield execution turn and react only when background events trigger.
5. **Atomic Replacements**: Prefer exact unique string replacement bounded by line numbers over whole-file overwrites.
