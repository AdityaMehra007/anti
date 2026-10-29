# Project: Bengaluru Job Referral Strike & 1-Click Dispatch Console

## Architecture
- Product Directory: `e:\anti\teamwork_projects\bangalore_referral_strike`
- Data Architecture: Inlined JSON (`dockets`) in `index.html` + `bangalore_live_referral_dockets.json` with 46 companies, 194+ verified contacts.
- UI Architecture: Standalone responsive HTML/CSS/JS with 4-dimensional filter pill interaction, 1-click clipboard copy with dual visual feedback (toast + button state change), direct LinkedIn URL launcher, and localStorage state persistence (`blr_referral_status_{contact_id}`).
- Message Synthesis Architecture:
  - Connection Note: Strict length <= 290 chars (hard limit <= 300 chars, 0 truncation), zero hallucination.
  - InMail / Message Referral Ask: Polite 3-4 paragraph message with 0-day notice, specific Req ID, and proof-of-work.
  - Internal Referral Docket: 3-bullet proof-of-work summary formatted for employee internal portal paste.
- Approval Queue Architecture:
  - Synchronize P0/P1 referral actions into `data/approval_queue.csv` and `data/approval_queue.json` preserving the exact 14 columns, sequential numbering starting at `REF-0605`, with `(Person, Company, Job)` deduplication.
- Verification Architecture:
  - Standalone automated Python test suite `tests/test_bangalore_referral_strike.py` asserting all 8 acceptance categories.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Target Matching & Data Completion | Complete dataset for 11 target employers (adding PwC BLR-JOB-013 with 3-5 verified contacts), map to 5 corridors & 5 domains, produce verified `bangalore_live_referral_dockets.json` | M1 | Survey |
| 2 | Personalized Message Synthesis | Synthesize 3 message assets per contact (Connection note <= 290 chars, InMail Ask, 3-Bullet Internal Docket) strictly anchored in `data/verified_profile.json` | M2 | Survey |
| 3 | Interactive 1-Click Dispatch Console | Build responsive standalone HTML/CSS/JS UI in `teamwork_projects/bangalore_referral_strike/index.html` with Corridor/Company/Domain/Status filter pills, dual-layer copy feedback, LinkedIn launch, and localStorage persistence | M3 | Survey |
| 4 | Canonical Approval Queue Sync | Sync all generated P0/P1 referral actions into `data/approval_queue.csv` and `data/approval_queue.json` (14 standard columns, sequence from `REF-0605`) | M4 | Survey |
| 5 | E2E Testing Suite & Infrastructure | Implement comprehensive automated test suite `tests/test_bangalore_referral_strike.py` covering dataset completeness, character bounds, profile alignment, and UI/storage capabilities | M-TEST | Survey |
| 6 | Full E2E Verification & Adversarial Hardening | Run full test suite, verify UI in browser, adversarial edge case audit, and final integrity audit | M5 | Survey |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M-TEST | E2E Testing Track | Automated test suite `tests/test_bangalore_referral_strike.py` & test infra | none | PLANNED |
| M1 | Target Data Completion | Add PwC, verify all 11 companies (3-5 contacts each), map 5 corridors, generate refreshed `bangalore_live_referral_dockets.json` | none | PLANNED |
| M2 | Message Synthesis & Bounds | Synthesize Connection Note (<= 290c), InMail Ask, Internal Docket for all contacts; verify <= 290c & zero hallucination | M1 | PLANNED |
| M3 | 1-Click Dispatch Console UI | Update `index.html` with inlined data, Corridor/Company/Domain/Status filter pills, copy feedback, LinkedIn links, localStorage | M1, M2 | PLANNED |
| M4 | Canonical Approval Queue Sync | Sync referral actions to `data/approval_queue.csv` and `data/approval_queue.json` without breaking schema | M1, M2 | PLANNED |
| M5 | Final E2E Pass & Adversarial Hardening | 100% test pass, challenger stress testing, forensic integrity audit | M-TEST, M3, M4 | PLANNED |

## Interface Contracts
### Data Engine ↔ Message Synthesizer (M1 ↔ M2)
- Input: `data/verified_profile.json`, `data/Connections_clean.csv`, `data/61_job_complete_referral_audit.csv`.
- Output: `bangalore_live_referral_dockets.json` containing 46 companies (including all 11 mandated employers), with list of contacts per company having `full_name`, `position`, `linkedin_url`, `connection_note`, `referral_ask`, `referral_docket`.
- Error Handling: Missing LinkedIn URL drops contact; connection notes > 290 chars trigger truncation fallback.

### Message Synthesizer ↔ Console UI (M2 ↔ M3)
- Interface: Embedded JavaScript variable `const dockets = [...]` within `teamwork_projects/bangalore_referral_strike/index.html`.
- Contract: Array of company objects, each with `company`, `hub`, `corridor`, `domain`, `role`, `req_id`, `careers_url`, `fit_score`, and `contacts` array.

### Data Engine ↔ Approval Queue (M1/M2 ↔ M4)
- Input: Generated contact actions for all 11 core employers.
- Output: Appended rows to `data/approval_queue.csv` and array items to `data/approval_queue.json`.
- Columns: 14 exact columns: `Action ID`, `Person`, `Company`, `Job`, `Channel`, `Draft Message`, `Reason / Evidence`, `Priority`, `Approval Required`, `Status`, `Staged Timestamp`, `Approved Timestamp`, `Dispatched Timestamp`, `Dispatch Packet`.
- Sequence: Start after highest existing Action ID (`REF-0604` -> start at `REF-0605`). Deduplicate against `(Person, Company, Job)`.

### Console UI ↔ Browser LocalStorage (M3)
- Key format: `blr_referral_status_{contact_id}` where `contact_id` is sanitized string (e.g. `{company}_{full_name}`).
- Values: `'pending'`, `'contacted'`, `'submitted'`.
- Fallback: In-memory store `window.__fallbackStore` if localStorage is restricted.

## Code Layout
- `teamwork_projects/bangalore_referral_strike/index.html` — Interactive 1-click dispatch console UI
- `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json` — Authoritative dataset
- `teamwork_projects/bangalore_referral_strike/cli.py` — Console runner CLI
- `data/approval_queue.csv` — Canonical approval queue CSV (14 columns)
- `data/approval_queue.json` — Canonical approval queue JSON
- `tests/test_bangalore_referral_strike.py` — Automated verification test suite
