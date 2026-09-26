---
name: opencode
description: Autonomous operational procedures and architecture for OpenCode (anomalyco/opencode). Use when working with OpenCode agents, running OpenCode CLI, configuring dual-mode build/plan agents, subagents (@general), or integrating OpenCode tools.
---

# OpenCode Operational Skill

Guidance for autonomous agents interacting with, executing, or configuring **OpenCode** (`anomalyco/opencode`).

---

## 1. Core Operating Modes

OpenCode provides two foundational operational personas switched via the `Tab` key or API parameter:

1. **`build` Agent (Default)**:
   - Full read/write access to the workspace.
   - Terminal command execution inside pseudo-terminals (`node-pty`).
   - Active file modification via AST chunk patching and deterministic line matching.
   - Ideal for: Feature development, refactoring, running builds, debugging, and test suites.

2. **`plan` Agent (Read-Only Architectural Gatekeeper)**:
   - Read-only codebase exploration.
   - Denies file edits by default.
   - Asks permission before executing bash commands.
   - Ideal for: Code review, architectural analysis, drafting implementation roadmaps, and bug root-cause investigation.

3. **`@general` Subagent**:
   - Recursive background delegation for complex multi-turn searches.
   - Context isolation: Runs in a child conversation and summarizes findings back to the primary agent to conserve context windows.

---

## 2. CLI Execution & Shortcuts

- **Launch Command**:
  ```powershell
  # Interactive CLI in current directory
  opencode

  # Specify custom workspace
  opencode --dir E:\anti

  # One-click Windows Launcher
  E:\anti\RUN_OPENCODE.bat
  ```

- **Interactive Shortcuts**:
  - `Tab`: Switch between `build` and `plan` modes.
  - `@general`: Invoke general subagent.
  - `@file`: Pin specific file context into prompt.
  - `/clear`: Clear turn history.

---

## 3. Configuration & MCP Servers

OpenCode configuration resides in `opencode.config.json` or `~/.config/opencode/config.json`:

```json
{
  "$schema": "https://opencode.ai/schema.json",
  "theme": "dark",
  "agent": {
    "default": "build"
  },
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "e:/anti"]
      }
    }
  }
}
```

---

## 4. Effect-TS Architecture & Style Rules

When developing inside or extending `packages/core`:
- Keep functions in one scope unless composable or reused.
- Prefer `const` over `let`. Use early returns over nested `if/else`.
- In Effect generators, bind services to named variables before calling methods.
- Use native Bun primitives (`Bun.file()`) where applicable.
- Avoid unnecessary destructuring; use dot notation to preserve context.
