## 2026-10-24T17:29:52Z
You are Worker 1 (Data & Synthesis Worker).
Read the authoritative request at: `e:\anti\.agents\teamwork\ORIGINAL_REQUEST.md`
Read the Explorer reports at:
- `e:\anti\.agents\teamwork\explorer_survey_1\handoff.md`
- `e:\anti\.agents\teamwork\explorer_survey_2\handoff.md`
- `e:\anti\.agents\teamwork\explorer_survey_3\handoff.md`
Read candidate truth at `data/verified_profile.json`.

Your working directory is: `e:\anti\.agents\teamwork\worker_data_1`
Maintain your `progress.md` and write your complete report to `e:\anti\.agents\teamwork\worker_data_1\handoff.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A reviewer and auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your write ownership:
- `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json`
- `data/bangalore_live_referral_dockets.json`
- Helper/builder scripts in `scripts/` or `teamwork_projects/bangalore_referral_strike/`

Your mission:
1. Target Data Matching & Gap Closure (R1):
   - Update `bangalore_live_referral_dockets.json` (and `data/bangalore_live_referral_dockets.json`) so all 11 mandated employers are fully present and verified:
     1. Accenture (Bellandur / Manyata)
     2. Deloitte (Bellandur / Manyata / Whitefield)
     3. Goldman Sachs (Outer Ring Road)
     4. Amazon (Bellandur / Manyata / Rajajinagar)
     5. IBM (Manyata / Domlur)
     6. JPMorganChase (`JPMorgan Chase & Co.`) (Outer Ring Road / Domlur)
     7. KPMG (Bellandur / Domlur)
     8. PwC (`PricewaterhouseCoopers (PwC)`) (Manyata / Bellandur)
     9. Walmart Global Tech (Outer Ring Road)
     10. Delhivery (Whitefield / Nelamangala)
     11. PhonePe (`PhonePe`) (Bellandur)
   - Add PwC (`BLR-JOB-013`, `Business Operations Analyst`, URL: `https://www.pwc.in/careers.html`, Domain: `Operations / Advisory/Risk`, Corridor: `Manyata Embassy Business Park` & `Bellandur`) with 3–5 verified contacts from `data/Connections_clean.csv` (e.g. Shalini Jha, Nikhitha Simon, Latha Dhananjay, Neeraja Rajasekar, Mishfa Kazi).
   - Ensure Delhivery has its 3 verified contacts (Chanchala Ugra, Sharon Sundara, Amruta Maile).
   - Ensure PhonePe has 3–5 verified contacts (Anshika Kohli, Tarun Upadhyay, Palak Shah, Khushi Arora, Aayushi Das).
   - Every contact MUST include `full_name`, `position`, and valid `linkedin_url` (`https://www.linkedin.com/in/...`).
   - Every target role must have `company`, `role`, `req_id`, `careers_url`, `hub`, `corridor`, `domain`, `fit_score`.

2. Message Synthesis (R2):
   Generate three tailored communication assets for each matched contact:
   a) Connection Request Note: Strict limit <= 290 characters (hard ceiling <= 300 chars, 0 truncation) highlighting mutual Bengaluru context and verified credentials (DSU BBA '26, Aero India 2025 ops lead, Instawork 99%+ QA). Test that 100% of notes are strictly <= 290 chars.
   b) InMail / Message Referral Ask: Polite, personalized asking for internal referral for specific requisition ID, stating 0 days notice and 3 bullet proof-of-work achievements.
   c) Internal Referral Docket: 3-bullet proof-of-work summary formatted for employee internal portal paste.
   - ZERO HALLUCINATIONS: Every claim must strictly match `data/verified_profile.json`.

3. Verification:
   Run verification script to verify that:
   - All 11 companies are present.
   - Every company has >= 3 contacts with valid names and LinkedIn URLs.
   - 100% of connection notes are <= 290 characters.
   - Save output to both `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json` and `data/bangalore_live_referral_dockets.json`.

Document your implementation, verification commands, and pass results in `e:\anti\.agents\teamwork\worker_data_1\handoff.md`.
When done, send a message to orchestrator.
