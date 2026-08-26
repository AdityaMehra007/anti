# OMEGA DATABASE AUDIT

**Database Path**: `E:\anti\omega\data\omega_master.db`  
**Total Tables**: 18 Normalized Schemas  

### Table Inventory & Row Counts:
| Table Name | Row Count | Primary Key | Verification Standard |
| :--- | :---: | :--- | :--- |
| `companies` | 20 | `company_id` | Verified Bangalore GCC Campuses |
| `jobs` | 44 | `job_id` | 24 Confirmed Live, 11 Seeded, 9 Errors |
| `job_sources` | 8 | `source_id` | Active Portal & API Registry |
| `job_evidence`| 24 | `evidence_id` | SHA-256 Hashes & HTTP 200 Telemetry |
| `job_changes` | 24 | `change_id` | `NEW` / `CHANGED` Transition Logs |
| `job_runs` | 1 | `run_id` | Live Discovery Run Telemetry |
| `applications`| 4 | `application_id` | 4 `READY_FOR_HUMAN`, 0 `SUBMITTED` |
| `outreach` | 3 | `outreach_id` | 3 `DRAFT`, 0 `SENT` |
| `followups` | 3 | `followup_id` | 7-Day / 14-Day Scheduled Radar |
| `interviews` | 1 | `interview_id` | STAR Preparation Briefing |
| `offers` | 0 | `offer_id` | Negotiation Modeling Engine Ready |
| `skills` | 14 | `skill_id` | Verified Candidate Competencies |
| `documents` | 8 | `document_id` | 8 Tailored Resume Variants |
| `model_runs` | 2 | `run_id` | Local Ollama Warm Latency Runs |
| `tool_runs` | 8 | `tool_run_id` | Probe & Discovery Tool Telemetry |
| `truth_events`| 28 | `event_id` | Immutable Delusion Prevention Audit Log |
| `approvals` | 3 | `approval_id` | Human Gatekeeping Request Queue |
| `contacts` | 3 | `contact_id` | Verified Recruiter Directory |
