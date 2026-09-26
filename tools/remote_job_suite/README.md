# Awesome Remote Job Suite & Automation Engine

An autonomous, end-to-end toolkit built upon [`lukasz-madon/awesome-remote-job`](https://github.com/lukasz-madon/awesome-remote-job).

---

## 🛠️ Components

| Component | File | Description |
| :--- | :--- | :--- |
| **Data Extractor** | [`extractor.py`](extractor.py) | Downloads and extracts the full upstream repository into normalized JSON databases in `data/`. |
| **Live Job Scraper** | [`scraper.py`](scraper.py) | Real-time multi-feed aggregator querying Remotive API, RemoteOK API, and WeWorkRemotely RSS feeds. |
| **Interactive CLI** | [`cli.py`](cli.py) | Query database of 232+ companies, 89 job boards, remote tools, relocation incentives, and live listings. |
| **PR Linter & Toolkit** | [`validator.py`](validator.py) | Enforces the 17 upstream `CONTRIBUTING.md` guidelines (<100 char limit, syntax, alphabetization, commit messages). |
| **Strategic Playbook** | [`PLAYBOOK.md`](PLAYBOOK.md) | In-depth guide to remote DNA principles, legal structures (Contractor vs EOR), and relocation cash grants. |

---

## 🚀 Quick Start Guide

### 1. View Statistics & Inventory
```bash
python tools/remote_job_suite/cli.py stats
```

### 2. Search Remote-DNA Companies
```bash
# Filter companies by tech tag
python tools/remote_job_suite/cli.py companies -t devtools -l 10
python tools/remote_job_suite/cli.py companies -t ai -l 10

# Keyword search
python tools/remote_job_suite/cli.py companies -q "security"
```

### 3. Browse Curated Job Boards
```bash
# Filter by domain
python tools/remote_job_suite/cli.py boards -c ai-ml
python tools/remote_job_suite/cli.py boards -c python
python tools/remote_job_suite/cli.py boards -c regional-latam
```

### 4. Fetch Real-Time Job Openings (Live Scraper)
```bash
# Search live jobs for Python / React / AI
python tools/remote_job_suite/scraper.py --keyword python --limit 10

# Generate a Markdown report
python tools/remote_job_suite/scraper.py --keyword ai --output live_ai_jobs.md
```

### 5. Format and Validate a PR Contribution
```bash
python tools/remote_job_suite/validator.py --new-entry \
  --name "Modal Labs" \
  --url "https://modal.com/careers" \
  --desc "Serverless cloud platform for AI and data workloads. Python, Rust, Linux." \
  --category "Company"
```

### 6. Check Relocation Grants & Nomad Programs
```bash
python tools/remote_job_suite/cli.py incentives
```
