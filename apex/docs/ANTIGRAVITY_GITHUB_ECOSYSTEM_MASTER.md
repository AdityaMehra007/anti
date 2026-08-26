# 🌐 GOOGLE ANTIGRAVITY — COMPLETE GITHUB ECOSYSTEM INDEX

**Audit Date:** 24/8/2026 IST  
**Ecosystem Standard:** Google Antigravity (Gemini 3 Agent-First Architecture)  

---

## 🏛️ 1. Official Google Antigravity Repositories

| Repository | Purpose | Surface Type |
| :--- | :--- | :---: |
| **`google-antigravity/antigravity-sdk-python`** | Official Python SDK (`google-antigravity`) for building custom agents | Python SDK |
| **`google/antigravity-cli`** | Official binary CLI agent harness (`agy.exe`) | CLI / Terminal |
| **`google/antigravity-ide`** | VS Code-based Agent-First IDE distribution | Desktop IDE |

---

## 🌟 2. Leading Community Repositories & Awesome Lists

| Repository | GitHub URL | Description & Strengths |
| :--- | :--- | :--- |
| **`ZhangYu-zjut/awesome-Antigravity`** | [GitHub Repo](https://github.com/ZhangYu-zjut/awesome-Antigravity) | The primary ecosystem hub with searchable prompts, rate-limit workarounds, and mission templates ([awesome-antigravity.com](https://awesome-antigravity.com)). |
| **`benjaminasterA/antigravity-awesome-skills`** | [GitHub Repo](https://github.com/benjaminasterA/antigravity-awesome-skills) | *Antigravity Awesome Skills (AAS)* — Curated collection of 800+ SOP markdown skill files. |
| **`irahardianto/awesome-agv`** | [GitHub Repo](https://github.com/irahardianto/awesome-agv) | Opinionated rules, security boundary protocols, and architectural patterns. |
| **`brandonhimpfen/awesome-google-antigravity`** | [GitHub Repo](https://github.com/brandonhimpfen/awesome-google-antigravity) | Curated catalog of developer tools, extensions, and integration patterns. |
| **`AntigravityManager`** | [GitHub Topic](https://github.com/topics/antigravity) | Electron & CLI process manager for session state and token cache isolation. |
| **`antigravity-mastery-handbook`** | [GitHub Topic](https://github.com/topics/antigravity) | Full-stack engineering handbook for agentic orchestration with Gemini 3. |

---

## 🔌 3. Model Context Protocol (MCP) Standard Registries

The ecosystem standard MCP servers configured in Antigravity:
- **`@modelcontextprotocol/server-filesystem`**: Scoped read/write access to project repositories.
- **`@modelcontextprotocol/server-memory`**: Persistent graph & key-value associative memory.
- **`@modelcontextprotocol/server-github`**: Repository inspection, PR management, and branch creation.
- **`@modelcontextprotocol/server-postgres`**: Database schema inspection and SQL querying.
- **`@modelcontextprotocol/server-brave-search`**: Web indexing and primary search extraction.

Configured locally at: [`e:\anti\.agents\mcp_config.json`](file:///e:/anti/.agents/mcp_config.json).

---

## ⚙️ 4. APEX Integration Status

APEX V3 natively ingests and coordinates all of these standards:
- **Skills Fabric**: 300 domain SOP skills stored locally in [`.agents/skills/`](file:///e:/anti/.agents/skills).
- **SDK Runtime**: Connected to `google-antigravity` (0.1.14) in [`apex/agents/runtime.py`](file:///e:/anti/apex/agents/runtime.py).
- **CLI Automation**: Controlled via `agy` in terminal execution scripts.
- **Capability Fabric**: Dynamic discovery across the 13 universal categories.
