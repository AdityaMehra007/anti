# BRIEFING — 2026-10-24T17:42:00Z

## Mission
Execute Target Data Matching & Gap Closure (R1) and Message Synthesis (R2) for Bangalore Referral Strike across 11 target companies, verifying 100% data integrity against verified profile and connection data.

## 🔒 My Identity
- Archetype: Data & Synthesis Worker (Worker 1)
- Roles: Data engineering, message synthesis, contact verification, referral docket generation
- Working directory: e:\anti\.agents\teamwork\worker_data_1
- Original parent: 42e5a8de-21a9-456c-be57-8301fbb779a8
- Milestone: Bangalore Referral Strike R1 & R2 Synthesis

## 🔒 Key Constraints
- Read-only on other team directories; write ownership strictly on:
  - `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json`
  - `data/bangalore_live_referral_dockets.json`
  - Helper/builder scripts in `scripts/` or `teamwork_projects/bangalore_referral_strike/`
  - Metadata in `e:\anti\.agents\teamwork\worker_data_1/`
- NEVER place source code, tests, or data files in `.agents/teamwork/`
- Zero hallucinations: strictly match `data/verified_profile.json`
- Strict character ceiling: connection notes <= 290 characters (hard ceiling 300, 0 truncation)
- All 11 companies must have >= 3 contacts with valid names and LinkedIn URLs
- No fake/cheating implementations; genuine parsing, generation, and verification

## Current Parent
- Conversation ID: 42e5a8de-21a9-456c-be57-8301fbb779a8
- Updated: 2026-10-24T17:42:00Z

## Investigation State
- **Explored paths**: `data/verified_profile.json`, `data/Connections_clean.csv`, `data/61_job_complete_referral_audit.csv`, `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json`, `scripts/bangalore_referral_matcher.py`, `scripts/bangalore_referral_strike.py`, `tests/test_bangalore_referral_matcher.py`, `tests/test_bangalore_referral_strike.py`
- **Key findings**:
  - Baseline dataset was missing PwC (`BLR-JOB-013`). Curated 5 verified PwC contacts from `data/Connections_clean.csv`: Shalini Jha, Nikhitha Simon, Latha Dhananjay, Neeraja Rajasekar, Mishfa Kazi.
  - Delhivery verified with 3 contacts: Chanchala Ugra, Sharon Sundara, Amruta Maile.
  - PhonePe verified with 5 contacts: Anshika Kohli, Tarun Upadhyay, Palak Shah, Khushi Arora, Aayushi Das.
  - Total curated contacts: 193 across 46 employers.
  - 100% of connection notes meet strict <= 290 character ceiling (max 271 chars, min 235 chars, 0 truncation).
  - Every target role contains `company`, `role`, `req_id`, `careers_url`, `hub`, `corridor`, `domain`, `fit_score` alongside backward-compatible aliases.
- **Unexplored areas**: UI console presentation and approval queue staging (assigned to Worker 2 & Worker 3).

## Key Decisions Made
- Built `scripts/build_verified_referral_dockets.py` to deterministically construct and maintain both target JSON files (`teamwork_projects/` and `data/`).
- Updated `scripts/bangalore_referral_matcher.py` to maintain integration.
- Designed whole-word role title synthesis to avoid awkward substrings like "Analys" while remaining safely under 271 characters.
- Created `scripts/verify_referral_strike.py` and `teamwork_projects/bangalore_referral_strike/verify_dockets.py`.

## Artifact Index
- `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json` — Authoritative project referral dockets (46 employers, 193 contacts)
- `data/bangalore_live_referral_dockets.json` — Synced data repository referral dockets
- `scripts/build_verified_referral_dockets.py` — Deterministic builder engine for referral dockets
- `scripts/verify_referral_strike.py` — 9-point verification suite
- `teamwork_projects/bangalore_referral_strike/verify_dockets.py` — Local project verification runner
- `scripts/bangalore_referral_matcher.py` — Updated matcher entrypoint
- `e:\anti\.agents\teamwork\worker_data_1\handoff.md` — Complete 5-component handoff report
