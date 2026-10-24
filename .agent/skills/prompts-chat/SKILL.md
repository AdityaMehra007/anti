---
name: prompts-chat
description: Query, retrieve, interpolate, and improve prompts from the world's largest open-source collection (2,627 curated prompts from f/prompts.chat).
---

# Prompts.chat Autonomous Intelligence & Prompt Engine

Equips agents and engineers with instant access to the **2,627 battle-tested prompts** from [f/prompts.chat](https://github.com/f/prompts.chat), indexed locally into SQLite FTS5 with variable interpolation, quality auditing, and job archetype classification.

---

## 1. When to Use This Skill

- When you need a specialized persona prompt for an agent or subagent (e.g. *Linux Terminal*, *Job Interviewer*, *Ethereum Developer*, *SQL Generator*, *Plagiarism Checker*).
- When parameterizing and filling dynamic prompt templates (`${Variable:Default}`).
- When auditing prompt robustness and constraint density (0-100 quality scoring).
- When improving a vague user prompt using standard prompt-engineering transformation rules.

---

## 2. Using the CLI Intelligence Tool

The repository provides a fast CLI tool at `e:\anti\prompts_chat_cli.py`:

### A. Search Prompts
```powershell
# Search by keyword
python prompts_chat_cli.py --search "interviewer"

# Filter by category and dev flag
python prompts_chat_cli.py --search "terminal" --category "Software & Coding" --for-devs
```

### B. Retrieve & Inspect Prompt
```powershell
# Get exact prompt by Act title or slug
python prompts_chat_cli.py --get "Linux Terminal"
python prompts_chat_cli.py --get "job-interviewer"
```

### C. Parameterize & Fill Variables
```powershell
# Interpolate template variables
python prompts_chat_cli.py --fill "Job Interviewer" --vars Position="Staff Infrastructure Engineer"
```

### D. Quality Audit & Prompt Improvement
```powershell
# Audit a prompt's completeness and constraints
python prompts_chat_cli.py --quality "Act as a python dev and write an API"
```

### E. Launch Interactive Visual Cockpit
```powershell
# Serve web studio and REST API at http://localhost:8877/
python prompts_chat_cli.py --serve 8877
```

---

## 3. Python Deep Module API

Agents can query the engine programmatically:

```python
from prompts_chat_engine import get_engine, VariableExtractor, QualityScorer

engine = get_engine()

# 1. Full-text search
records, total = engine.search("python developer", limit=5)

# 2. Get by Act name
prompt = engine.get_by_act("Linux Terminal")

# 3. Dynamic variable substitution
filled = engine.fill_prompt("Job Interviewer", {"Position": "Chief AI Architect"})

# 4. Quality score (0-100)
score, strengths = QualityScorer.score(prompt.prompt)
```

---

## 4. MCP Server Integration

The local MCP server is running at `e:\anti\prompts_chat_mcp_server.py` and registered with Antigravity:
- `search_prompts`
- `get_prompt`
- `fill_prompt`
- `improve_prompt`
- `analyze_prompt_quality`
- `random_prompt`
- `get_prompts_chat_stats`
