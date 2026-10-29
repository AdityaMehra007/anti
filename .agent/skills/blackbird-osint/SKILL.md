---
name: blackbird-osint
description: "Use when conducting OSINT reconnaissance, handle and username discovery across 600+ platforms, attack surface auditing, digital footprint intelligence, credential stuffing exposure assessment, and defensive OPSEC hardening."
metadata:
  author: OMEGA Autonomous Core
  version: "2.4.0"
---

# Blackbird Autonomous OSINT & Defensive Intelligence Suite

Autonomous standard operating procedure and programmatic interface for multi-platform username and email reconnaissance, identity correlation, digital footprint analysis, and defensive OPSEC threat modeling using Blackbird and the WhatsMyName intelligence engine.

---

## 1. Architectural Architecture & Core Components

Blackbird aggregates community-maintained platform signatures (WhatsMyName 692+ site registry) and performs asynchronous HTTP response probing to discover public profiles, extract metadata, and evaluate exposure:

```
+-----------------------------------------------------------------------------------+
|               Blackbird OSINT & Defensive Intelligence Suite                      |
+-----------------------------------------------------------------------------------+
                                         |
                +------------------------+------------------------+
                |                                                 |
                v                                                 v
+-------------------------------+               +-----------------------------------+
|   Reconnaissance Engine       |               |    Defensive Intelligence Audit   |
| - 692+ Username Platforms     |               | - Digital Footprint Index (0-100) |
| - 16 Email Endpoints          |               | - Credential Stuffing Surface     |
| - Async High-Concurrency Pool |               | - Handle Impersonation Vulnerab.  |
| - Multi-handle Permutations   |               | - Prioritized Hardening Actions   |
+-------------------------------+               +-----------------------------------+
                |                                                 |
                +------------------------+------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|               Local & AI Behavioral Synthesis (Dual Mode)                        |
| - Inferred Professional Archetypes (Architect, Quant, Creator, Gamer)             |
| - Domain Affinities, Tech Stack Detection, and Operational Risk Flags            |
+-----------------------------------------------------------------------------------+
                                         |
                +------------------------+------------------------+
                |                        |                        |
                v                        v                        v
+-----------------------+ +----------------------+ +--------------------------------+
| JSON / CSV Datasets   | | Executive Markdown   | | Cyber Glass Mission Control    |
| (Raw Audit Artifacts) | | Dossiers (.md)       | | Cockpit (HTML / REST API 8777) |
+-----------------------+ +----------------------+ +--------------------------------+
```

---

## 2. Programmatic Python SDK & CLI Usage

The repository provides a deep-module SDK and CLI at [`blackbird_orchestrator.py`](file:///e:/anti/blackbird_orchestrator.py) and [`blackbird_cli.py`](file:///e:/anti/blackbird_cli.py).

### Quick CLI Commands

```bash
# Display Platform Census and Category Statistics (692 Platforms)
python blackbird_cli.py --stats

# Run Instant High-Fidelity Simulation & OPSEC Audit (Demo)
python blackbird_cli.py --demo

# Probe Specific Username with Defensive Audit & Dossier Exports
python blackbird_cli.py -u johndoe --audit --export-all

# Target Specific Category (e.g. tech, social, finance, gaming)
python blackbird_cli.py -u johndoe -c tech --export-all

# Generate Username Permutations for Multi-Handle Correlation
python blackbird_cli.py -u john doe --permute --export-all

# Launch Mission Control Cockpit Server on Port 8777
python blackbird_cli.py --serve 8777
```

### Python SDK Integration

```python
from blackbird_orchestrator import BlackbirdOrchestrator
import asyncio

orchestrator = BlackbirdOrchestrator()

# Fast simulation / cached audit
result = orchestrator.run_mock_scan(target="octocat")
print("Footprint Index:", result["threat_audit"]["footprint_index"])
print("Threat Tier:", result["threat_audit"]["threat_tier"])

# Live asynchronous probe across 692 platforms
# result = asyncio.run(orchestrator.run_live_username_scan(username="targetuser", site_limit=100))

# Export multi-format dossiers
orchestrator.export_json(result)
orchestrator.export_csv(result)
orchestrator.export_markdown_dossier(result)
orchestrator.export_html_report(result)
```

---

## 3. Defensive OPSEC & Hardening Rules

1. **Authorization & Educational Scope:** Blackbird is deployed strictly for defensive security assessments, attack surface reduction, brand impersonation monitoring, and personal OPSEC auditing.
2. **Defensive Footprint Remediation:**
   - **Footprint Score >= 70 (Critical):** Immediate credential rotation, mandatory hardware MFA/FIDO2 keys, and dormant profile deletion.
   - **Impersonation Vulnerability High:** Proactively claim vacant namespaces on high-trust domains (GitHub, GitLab, Twitter, LinkedIn) before malicious actors can squat them.
   - **PII Decoupling:** Strip phone numbers, personal locations, and email handles from public profile biographies.
3. **Automated Artifact Retention:** All scans auto-generate timestamped audit artifacts in `blackbird_reports/`.
