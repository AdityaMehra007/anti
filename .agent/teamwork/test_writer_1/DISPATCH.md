## 2026-10-24T17:29:09Z
You are Test Writer 1 (E2E Test Writer).
Read the authoritative request at: `e:\anti\.agents\teamwork\ORIGINAL_REQUEST.md`
Read the test infrastructure design at: `e:\anti\.agents\teamwork\orchestrator_1\TEST_INFRA.md`
Read the Explorer 3 handoff at: `e:\anti\.agents\teamwork\explorer_survey_3\handoff.md` and its prototype test suite at `e:\anti\.agents\teamwork\explorer_survey_3\proposed_test_suite.py`

Your working directory is: `e:\anti\.agents\teamwork\test_writer_1`
Maintain your `progress.md` and write your complete report to `e:\anti\.agents\teamwork\test_writer_1\handoff.md`.

Your mission:
Write and deploy the canonical automated E2E test suite to `e:\anti\tests\test_bangalore_referral_strike.py`.
The test suite MUST implement comprehensive, opaque-box tests covering:
1. `test_01_deliverable_files_exist`: Verifies `teamwork_projects/bangalore_referral_strike/index.html`, `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json`, `teamwork_projects/bangalore_referral_strike/cli.py`, `data/approval_queue.csv`, `data/approval_queue.json`.
2. `test_02_all_11_mandated_companies_present`: Verifies Accenture, Deloitte, Goldman Sachs, Amazon, IBM, JPMorganChase, KPMG, PwC, Walmart Global Tech, Delhivery, PhonePe are present in `bangalore_live_referral_dockets.json`.
3. `test_03_contacts_per_company_thresholds`: Verifies each of the 11 companies has >= 3 contacts, and every contact entry includes valid non-empty `full_name`, `position`, and valid `linkedin_url` (matching `^https:\/\/[a-z]{2,3}\.linkedin\.com\/in\/[\w\-]+`).
4. `test_04_connection_notes_strict_290_char_limit`: Verifies 100% of connection notes across all contacts are strictly <= 290 characters (and hard ceiling <= 300 characters, zero truncation), and >= 50 characters.
5. `test_05_zero_hallucination_profile_alignment`: Verifies that messages reference verified credentials from `data/verified_profile.json` (DSU BBA, Aero India 2025, Instawork 99%+) and contain zero unearned or fabricated claims.
6. `test_06_corridor_and_domain_coverage`: Verifies all 5 tech corridors (Outer Ring Road, Manyata, Bellandur, Whitefield, Domlur) and all 5 domains (Operations, Supply Chain, Advisory/Risk, Trade Finance, Merchant BD) are properly represented.
7. `test_07_console_html_standalone_capabilities`: Verifies `index.html` has inlined data (`const dockets =`), clipboard copy handlers with visual feedback, LinkedIn launchers (`target="_blank"`), localStorage status tracking logic (`Pending`, `Contacted`, `Referral Submitted`), and filter pill elements for Corridors, Companies, and Domains.
8. `test_08_approval_queue_schema_fidelity`: Verifies `data/approval_queue.csv` and `data/approval_queue.json` maintain exact 14 standard columns, sequential numbering, and valid format.

Run the test suite using `python -m unittest tests/test_bangalore_referral_strike.py` and document which tests pass vs fail on the current codebase.
When done, create `e:\anti\TEST_READY.md` (or report that test suite is ready) and send a message with your report path.
