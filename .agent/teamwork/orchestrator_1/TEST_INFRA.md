# E2E Test Infra: Bengaluru Job Referral Strike & 1-Click Dispatch Console

## Test Philosophy
- Opaque-box, requirement-driven derived from `ORIGINAL_REQUEST.md`.
- No dependency on internal implementation quirks; tests against public deliverables:
  - `teamwork_projects/bangalore_referral_strike/index.html`
  - `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json`
  - `data/approval_queue.csv` & `data/approval_queue.json`
- Methodology: Category-Partition + Boundary Value Analysis + Pairwise + Workload Testing.

## Feature Inventory & Test Coverage
| # | Feature | Requirement | Tier 1 (Coverage) | Tier 2 (Boundary) | Tier 3 (Cross-Feature) | Tier 4 (Real-World) |
|---|---------|-------------|:-----------------:|:-----------------:|:---------------------:|:-------------------:|
| 1 | Target Company Matching | 11 mandated employers with >= 3 contacts | 11 tests (all present) | Edge: exactly 3 contacts (Delhivery) | Paired with Corridors | All 11 verified |
| 2 | Corridor & Domain Mapping | 5 corridors, 5 domains | 5 corridor + 5 domain checks | Edge: multi-campus corridors | Corridor × Domain combinations | Search & filter by corridor |
| 3 | Message Synthesis & Bounds | Connection Note <= 290c (ceiling 300c), InMail, Docket | 100% notes checked | Max length note <= 290c | Name length variance | Full copy workflow |
| 4 | Zero Hallucination | Grounded in verified_profile.json | DSU, Aero India, Instawork | Negative: no MBA/IIM | Alignment across all 3 assets | True candidate claims |
| 5 | Interactive Web Console | Standalone HTML/JS, 4-filter pills, clipboard, storage | DOM & script elements | localStorage exception fallback | Corridor ∩ Company ∩ Status | Browser dispatch simulation |
| 6 | Canonical Approval Queue | 14 columns, REF-0605+ sequence, deduplication | Schema & row count | Sequence boundary & empty timestamps | Queue sync from console dockets | CLI tracking readiness |

## Test Architecture
- Test Suite File: `tests/test_bangalore_referral_strike.py`
- Runner: `python -m unittest tests/test_bangalore_referral_strike.py`
- Output: Standard unittest TAP/verbose results.
- Minimum Passing Threshold: 100% of tests passing with exit code 0.
