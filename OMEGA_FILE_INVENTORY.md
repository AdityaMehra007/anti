# OMEGA MASTER FILE INVENTORY

### Core Production Components (`E:\anti\omega\`)
| Relative Path | Size (Bytes) | Category | Description | Status |
| :--- | :---: | :---: | :--- | :---: |
| `omega/career_war_room/live_job_discovery.py` | ~8.5 KB | `CORE` | Live discovery pipeline & API scraper | `ACTIVE` |
| `omega/career_war_room/database.py` | ~12.5 KB | `CORE` | 18 Normalized SQLite schemas | `ACTIVE` |
| `omega/career_war_room/job_truth_auditor.py` | ~4.2 KB | `CORE` | Cryptographic evidence & change detector | `ACTIVE` |
| `omega/career_war_room/application_proof.py` | ~3.8 KB | `CORE` | Application submission & proof auditor | `ACTIVE` |
| `omega/career_war_room/company_intelligence.py`| ~11.5 KB | `CORE` | 20 Monitored Bangalore GCC dossiers | `ACTIVE` |
| `omega/career_war_room/ats_engine.py` | ~3.1 KB | `CORE` | Zero-fabrication keyword & fit scorer | `ACTIVE` |
| `omega/career_war_room/resume_engine.py` | ~5.3 KB | `CORE` | 8 Domain-specific resume variants | `ACTIVE` |
| `omega/career_war_room/application_manager.py` | ~5.2 KB | `CORE` | 13-Stage truth state machine | `ACTIVE` |
| `omega/career_war_room/outreach_engine.py` | ~5.5 KB | `CORE` | Recruiter InMail & email generator | `ACTIVE` |
| `omega/career_war_room/call_assistant.py` | ~2.9 KB | `CORE` | Phone briefing & objection defense | `ACTIVE` |
| `omega/career_war_room/radar_365.py` | ~2.5 KB | `CORE` | Scheduled execution & run proof logger | `ACTIVE` |
| `omega/career_war_room/career_brain.py` | ~3.9 KB | `CORE` | Master daily war room briefing | `ACTIVE` |
| `omega/model_router/client.py` | ~6.5 KB | `CORE` | OmniRoute client & fallback router | `ACTIVE` |
| `omega/model_router/provider_discovery.py` | ~7.2 KB | `CORE` | Live discovery of local/cloud providers | `ACTIVE` |
| `omega/model_router/sensitive_guard.py` | ~4.8 KB | `CORE` | Sensitive data gatekeeper (Local only) | `ACTIVE` |
| `omega/engines/disaster_recovery.py` | ~5.1 KB | `CORE` | Automated snapshot & backup engine | `ACTIVE` |
| `omega/control_tower/cli.py` | ~17.5 KB | `CORE` | Master unified CLI interface | `ACTIVE` |

### Test Suites (`E:\anti\tests\` & `E:\anti\omega\tests\`)
- `tests/test_omniroute_live.py`: 18 Tests (P0 Hardening & Health)
- `omega/tests/test_omega_pipeline_e2e.py`: 4 Tests (End-to-End Pipeline)
- `omega/tests/test_omega_career_war_room.py`: 11 Tests (War Room Engines)
- `omega/tests/test_omega_career_war_room_v2.py`: 7 Tests (Truth Auditor & Proofs)
- `omega/tests/test_reality_audit.py`: 6 Tests (Reality Rejection Invariants)
- `omega/tests/test_live_job_discovery.py`: 4 Tests (Live Discovery & Seed Isolation)
