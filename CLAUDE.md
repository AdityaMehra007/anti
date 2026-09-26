# CLAUDE.md — Instructions for Claude Code in ADI CAREER OS & OMEGA ∞
 
Autonomous AI Founder, Venture Intelligence, Job Search & Operations System for **Aditya Mehra (Adi)**.
 
**Supreme Constitution**: [`OMEGA_CONSTITUTION.md`](OMEGA_CONSTITUTION.md) (OMEGA ∞: 120 Master Directives).  
**Operational Codex**: [`ADI_OMNI_CODEX.md`](ADI_OMNI_CODEX.md) (330 directives).  
**Engineering Principles**: [`AGENTS.md`](AGENTS.md).  
**Ubiquitous Language & Context**: [`CONTEXT.md`](CONTEXT.md).  
 
---

## 1. Candidate Ground Truth & Strict Invariants

- **Candidate**: Aditya Mehra (Adi)
- **Education**: Bachelor of Business Administration (BBA) in International Business, Dayananda Sagar University (DSU), Bengaluru (Graduating 2026).
- **Location**: Bengaluru, Karnataka, India.
- **Contact**: `adityamehra799@gmail.com` | `+91-7003456624` | [LinkedIn Profile](https://www.linkedin.com/in/aditya-mehra)
- **Target Roles**: Operations & Logistics Executive, Business Development & Commercial Ops Analyst, Supply Chain & EXIM Logistics Specialist, AI Product Operations Analyst, PMO Coordinator.
- **Target Geographies**: Bengaluru (Outer Ring Road, Whitefield, Electronic City, Manyata, Koramangala, CBD).

### Invariant Guardrails
1. **ZERO HALLUCINATION**:
   - NEVER invent or exaggerate credentials, graduation dates, or employer claims.
   - Only cite verified proof of work:
     * **AERO India 2025**: Lead Operations & Logistics Coordinator (Yelahanka AFB, 100k+ footfall, 12 staging points, 0% shrinkage).
     * **Commercial Operations LLP**: 300+ brand activations for **Puma India**, **Tata Communications**, **Dyson**; vendor SLA rate cards and liquidated damages recovery.
     * **Instawork AI**: AI Data Operations & Curation Lead (99%+ precision threshold for LLM annotation).
     * **EXIM Compliance**: Incoterms 2020 rules (FOB/CIF/DAP), ICEGATE customs duty and tariff classification.
2. **100% SALES EXCLUSION**:
   - Strictly filter out telecalling, cold-calling insurance/credit card sales, retail store staffing, and commission-only SDR roles.
3. **ZERO-TRUST APPROVAL GATE**:
   - All target jobs and outreach must be staged in `data/omega_approvals.db` and approved before live external dispatches.

---

## 2. Workspace Layout & Key Assets

- **Master CLI Orchestrator**: `python adi_career_os.py` (15 autonomous agents).
- **24/7 Daily Autonomous Ecosystem**: `python AUTONOMOUS_DAILY_ECOSYSTEM.py --once`.
- **Master Pipeline Orchestrator**: `python RUN_AUTONOMOUS_PIPELINE.py`.
- **Bangalore Application Controller**: `python scripts/apply_all_bangalore.py --status`.
- **Application Packages**:
  * All 61 Bangalore Openings: `applications_generated/bangalore_61_packages/`
  * 25 Tier-1 MNC Packages: `applications_generated/mnc_packages/`
  * RFC-822 `.eml` Outbox: `applications_generated/eml_outbox/`
- **Interactive Web Studios**:
  * 61 Requisitions Studio: `apps/job_application_studio/bangalore_master_strike_studio.html`
  * 4,500 Bangalore Employers Mega-Studio: `apps/job_application_studio/mega_studio.html`
  * Target 300 Strike Studio: `apps/job_application_studio/strike_300.html`
- **Portfolio Deliverables**:
  * Project 1: `portfolio/PROJECT_1_AERO_INDIA_OPERATIONS.md`
  * Project 2: `portfolio/PROJECT_2_VENDOR_SLA_COST_MODEL.py` & `.md`
  * Project 3: `portfolio/PROJECT_3_EXIM_CUSTOMS_COMPLIANCE_MATRIX.md`
  * Project 4: `portfolio/PROJECT_4_AI_DATA_OPS_QUALITY_PIPELINE.py` & `.md`
- **Live Background Services**:
  * Hermes Web Dashboard: `http://127.0.0.1:9119`

---

## 3. Standard Verification Commands

```powershell
# Run the complete test suite (must be 100% pass)
pytest tests/test_adi_career_os.py

# Run the 6-phase daily ecosystem audit
python AUTONOMOUS_DAILY_ECOSYSTEM.py --once

# Audit Bangalore all-companies strike status
python scripts/apply_all_bangalore.py --status

# Verify Hermes dashboard health
python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:9119').status)"
```

---

## 4. Coding & Architecture Standards

- **Python**: Python 3.13+, UTF-8 encoding reconfigure on sys.stdout/sys.stderr, standard library preference, dataclasses, SQLite PRAGMA checks.
- **HTML/CSS/JS**: Self-contained, responsive dark-mode styling with Inter and JetBrains Mono fonts, local storage persistence for applied tracking, no broken external CDNs.
- **PowerShell compatibility**: On Windows, avoid complex nested double quotes in inline commands; use dedicated script files in `scripts/`.
- **Ponytail Minimalism**: Write the minimum code that works. Avoid speculative abstractions.
