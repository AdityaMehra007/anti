# OMEGA SYSTEM INVENTORY

| Subsystem Name | Primary Module Path | Classification | Runtime State | Operational Role |
| :--- | :--- | :--- | :--- | :--- |
| **Model Router & Discovery** | `omega/model_router/` | `CORE_AI` | **`LIVE_LOCAL`** | Routes prompts, enforces privacy, probes Ollama on port 11434. |
| **Sensitive Data Guard** | `omega/model_router/sensitive_guard.py` | `SECURITY` | **`ACTIVE`** | Restricts PII/credentials to local Ollama inference only. |
| **MCP Super-Fabric** | `omega/mcp/` | `TOOLING` | **`CONFIGURED`** | Registers Firecrawl, OmniRoute, and custom tool endpoints. |
| **Live Job Discovery** | `omega/career_war_room/live_job_discovery.py`| `CAREER_ENGINE`| **`ACTIVE`** | Live API scraper for Bangalore GCC vacancies. |
| **Job Truth Auditor** | `omega/career_war_room/job_truth_auditor.py` | `GOVERNANCE` | **`ACTIVE`** | Cryptographic SHA-256 evidence hashing & change detection. |
| **Application Proof Engine**| `omega/career_war_room/application_proof.py` | `GOVERNANCE` | **`ACTIVE`** | Validates external receipts; downgrades false submissions. |
| **Company Intelligence** | `omega/career_war_room/company_intelligence.py`| `INTEL` | **`ACTIVE`** | Maintains 20 Bangalore GCC company dossiers. |
| **ATS & Resume Engine** | `omega/career_war_room/resume_engine.py` | `GENERATOR` | **`ACTIVE`** | 8 Zero-fabrication domain resume variants. |
| **Disaster Recovery** | `omega/engines/disaster_recovery.py` | `DEVOPS` | **`ACTIVE`** | Automated backup snapshot & ledger integrity verification. |
| **Control Tower & CLI** | `omega/control_tower/cli.py` | `CLI_UI` | **`ACTIVE`** | Command-line interface and HTML dashboard. |
