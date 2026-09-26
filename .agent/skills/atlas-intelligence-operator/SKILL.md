---
name: atlas-intelligence-operator
description: Master operational memory, self-improvement protocols, and query execution engine for ATLAS-GLOBAL business and workforce intelligence OS.
---

# ATLAS-GLOBAL: Intelligence Operator Skill

## 1. Operating Directives & Constitution
This skill governs autonomous operations across the **ATLAS-GLOBAL Data Lake (`atlas.db`)**:
- 7,721 Verified Companies
- 13,300 Public Professional Profiles
- 3,734 Active Job Requisitions
- 17,034 Knowledge Graph Edges
- 24,755 FTS5 Search Tokens

## 2. Core Operational Seams
- **Database Path:** `e:\anti\atlas-global\database\atlas.db`
- **Dashboard Path:** `e:\anti\atlas-global\dashboards\atlas_dashboard.html`
- **Battlecards:** `e:\anti\atlas-global\battlecards/`
- **Proposals:** `e:\anti\atlas-global\proposals/`
- **Tools:** `e:\anti\atlas-global\tools/`
- **Backups:** `e:\anti\atlas-global\backups/`

## 3. Standard Operating Procedures (SOPs)

### A. Sub-Millisecond Search Querying
To query entities by keyword, title, or tech park:
```python
import sqlite3
conn = sqlite3.connect(r"e:\anti\atlas-global\database\atlas.db")
cur = conn.cursor()
query = "SELECT entity_type, name_or_title, company_or_org, contact_point FROM atlas_search_fts WHERE atlas_search_fts MATCH ? LIMIT 10"
for row in cur.execute(query, ("Bellandur",)):
    print(row)
```

### B. Safe Candidate Tool Validation & Testing
All proposed web tools must pass the 10-step lab rubric in `e:\anti\atlas-global\tool-lab\TOOL_DISCOVERY_CATALOG.md`.
Never execute tools requiring payment, trial card authorizations, or anti-bot defense bypass.

### C. Self-Improvement & Continuous Learning Loop
Following each scheduled ingestion or research batch:
1. Audit source failure rates (`atlas.db` -> `sources`).
2. Log deduplication anomalies.
3. Update `reports/quality/data-quality-report.md`.
4. Run `backup_manager.py` to preserve verified state.

## 4. Hard Boundaries
- Zero automated outbound emails or messages.
- Zero private phone numbers or personal emails.
- Total cost must remain strictly **₹0.00**.
