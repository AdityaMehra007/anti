# Plan — Bengaluru Job Referral Strike & 1-Click Dispatch Console

## Phase 0: Survey & Scope Mapping
1. Dispatch 3 parallel Explorers to investigate:
   - Explorer 1 (Data & Profile): `data/verified_profile.json`, available career intelligence datasets, LinkedIn contacts files, role openings, existing schemas (`data/approval_queue.csv`, `data/approval_queue.json`).
   - Explorer 2 (Domain Requirements & Corridors): Target employers in Bengaluru (Accenture, Deloitte, Goldman Sachs, Amazon, IBM, JPMorganChase, KPMG, PwC, Walmart Global Tech, Delhivery, PhonePe) across tech corridors (ORR, Manyata, Bellandur, Whitefield, Domlur), required job functional areas (Operations, Supply Chain, Advisory/Risk, Trade Finance, Merchant BD).
   - Explorer 3 (UI Console & Integration Architecture): Requirements for standalone responsive HTML/JS console (filter pills, clipboard copy buttons, LinkedIn launcher, localStorage status tracking, zero external server dependencies).
2. Synthesize findings into `PROJECT.md` (Architecture, Feature Inventory, Milestones, Code Layout, Interfaces).

## Phase 1: Track Decomposition
- Track 1 (E2E Testing Track): Formulate test suite and verification scripts (test dataset completeness, <= 290/300 char limits, 1-click clipboard, localStorage persistence, approval queue schemas). Publish `TEST_INFRA.md` and eventually `TEST_READY.md`.
- Track 2 (Implementation Track):
  - Milestone 1: Data Matching & Scoring Engine (`data/verified_profile.json`, Bengaluru job openings, 1,200+ LinkedIn connections mapped 3-5 per company).
  - Milestone 2: Personalized Referral Docket & Message Synthesis (Connection Request Note <= 290 chars, InMail Ask, 3-Bullet Internal Referral Docket).
  - Milestone 3: Interactive 1-Click Dispatch Console (HTML/JS/CSS standalone UI with filtering, copy actions, LinkedIn launching, localStorage).
  - Milestone 4: Canonical Approval Queue Integration (`data/approval_queue.csv` and `data/approval_queue.json` schema-compliant sync).
  - Milestone 5: Full E2E Verification & Adversarial Hardening.

## Phase 2: Execution Loops
- Each milestone executes via Explorer -> Worker -> Reviewer -> Challenger -> Auditor gate loops.
- Pass gate criteria: Tests pass, Reviewers APPROVE, Challengers APPROVE, Auditor CLEAN.

## Phase 3: Final Delivery
- Verify 100% E2E tests pass.
- Generate victory report to parent caller.
