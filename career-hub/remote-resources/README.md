# Remote Work Ecosystem & Scored Job Intelligence

Structured, machine-readable dataset, multi-metric scoring, and query tooling ingested from [`lukasz-madon/awesome-remote-job`](https://github.com/lukasz-madon/awesome-remote-job).

Total Curated Resources: **520**  
Scoring Engine: **Antigravity Multi-Metric Decision Matrix V22**

---

## Directory Inventory

| File | Format | Description |
| :--- | :--- | :--- |
| `all_entities_ranked_and_scored.csv` | CSV | **Master Ranked Ledger** of all 520 entities sorted by composite score (Rank 1 to 520, Tiers, Scores, Tags). |
| `remote_ecosystem_master.json` | JSON | Complete hierarchical database of all 520 entities, with categories, tags, URLs, and multi-metric score objects. |
| `remote_companies.csv` | CSV | 232 Companies with Remote DNA (Name, Website, Careers Link, Tech Stack / Tags, Description). |
| `remote_job_boards.csv` | CSV | 89 Curated Remote Job Boards & Aggregators (Name, URL, Type, Tags, Description). |
| `remote_tools.csv` | CSV | 51 Remote Infrastructure & HR/Communication/Project Management Tools. |
| `relocation_incentives.csv` | CSV | 6 Financial Grants & Relocation Programs ($10,000 Tulsa, Maine, Vermont, Remote Shoals, etc.). |
| `remote_jobs_explorer.html` | HTML/JS | Standalone, zero-dependency interactive dashboard with instant search, score badges, and sorting. |
| `query_remote_jobs.py` | Python CLI | Terminal search and query interface supporting `--tier1`, `--search`, and tag filtering. |
| `score_entire_ecosystem.py` | Python | Deterministic multi-dimensional scoring pipeline for all categories. |

---

## Scoring Framework (0 - 100 Composite)

1. **Companies**: Candidate Fit (50%) + Remote Maturity (25%) + Compensation Leverage (25%) + Hiring Probability.
2. **Job Boards**: Update Utility & Freshness (40%) + Role Breadth (30%) + Global Geographic Access (30%).
3. **Tools & Infrastructure**: Ecosystem Adoption (60%) + Candidate Operational Mastery (40%).
4. **Relocation Grants**: Net Financial Value (60%) + Applicant Eligibility Feasibility (40%).
5. **Guides & Media**: Authoritative Credibility (50%) + Practical Actionability (50%).

---

## CLI Usage

### View Top Tier-1 Resources
```bash
python query_remote_jobs.py --tier1
```

### Search by Keyword or Tag
```bash
python query_remote_jobs.py --search "AI"
python query_remote_jobs.py --tag "4-Day Week"
```

### View Ecosystem Statistics
```bash
python query_remote_jobs.py --stats
```

---

## Interactive Dashboard

Open [`remote_jobs_explorer.html`](file:///e:/anti/career-hub/remote-resources/remote_jobs_explorer.html) directly in any web browser. It features:
- Score ranking (`★ Score / 100`) on every resource card.
- "Sort by Score (High to Low)", "Name (A-Z)", or "Category".
- Fast filter for "⭐ Tier 1 Elite Only".
