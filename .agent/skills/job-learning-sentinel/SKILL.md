---
name: job-learning-sentinel
description: Continuous online learning agent and web scraper that monitors company career portals, extracts hiring velocity, culture DNA, interview questions, and evolving ATS keywords.
---

# JOB LEARNING SENTINEL

Autonomous intelligence harvester that transforms raw job postings, career portals, and company publications into structured career intelligence.

## Capabilities
- Continuous crawling across Greenhouse, Lever, Workday, LinkedIn, Indeed, Naukri, and Wellfound.
- Automated extraction of high-frequency ATS keywords categorized into Operations, B2B Sales, AI & Tech, EXIM, and Leadership.
- Heuristic extraction of real interview questions and candidate experiences from online snippets.
- Real-time updates to the SQLite Knowledge Vault (`data/omega_career_learning_vault.db`) with WAL mode and FTS5 search.

## Python Usage
```python
from apex_career_os.core.knowledge_learning_vault import KnowledgeLearningVault
from apex_career_os.agents.sentinel_learner import SentinelLearnerAgent

vault = KnowledgeLearningVault()
sentinel = SentinelLearnerAgent(vault=vault)

# Run full harvest & learning cycle
result = sentinel.run_harvest_and_learn_cycle(limit=100)
print(f"Mined {result['total_jobs_mined']} jobs, profiled {result['unique_companies_profiled']} companies")

# Deep-dive learn from company web text
sentinel.learn_company_deep_dive("CRED", [
    "During my interview for Member Operations at CRED, they asked me: 'How would you scale high-trust operations with zero fraud?'"
])
```
