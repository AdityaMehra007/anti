# TEST READY: Bengaluru Referral Strike & 1-Click Dispatch Console E2E Verification Suite

**Status**: READY & DEPLOYED  
**Test Suite Path**: `e:\anti\tests\test_bangalore_referral_strike.py`  
**Execution Command**: `python -m unittest tests/test_bangalore_referral_strike.py`  
**Alternative Runner**: `pytest tests/test_bangalore_referral_strike.py`  
**Timestamp**: 2026-10-24T17:36:00Z  

---

## 1. Test Suite Architecture & Coverage Summary

The canonical E2E automated test suite is deployed to `tests/test_bangalore_referral_strike.py`. It implements comprehensive, opaque-box acceptance tests derived directly from `ORIGINAL_REQUEST.md` and `TEST_INFRA.md`.

| # | Test Method Name | Acceptance Criteria Verified | Current Baseline Status | Notes / Root Cause |
|---|------------------|------------------------------|:-----------------------:|-------------------|
| 1 | `test_01_deliverable_files_exist` | Verifies `index.html`, `bangalore_live_referral_dockets.json`, `cli.py`, `approval_queue.csv`, `approval_queue.json` exist and are non-empty. | **PASSED** | All 5 deliverable files present with non-zero byte size. |
| 2 | `test_02_all_11_mandated_companies_present` | Verifies Accenture, Deloitte, Goldman Sachs, Amazon, IBM, JPMorganChase, KPMG, PwC, Walmart Global Tech, Delhivery, PhonePe are present in `bangalore_live_referral_dockets.json`. | **FAILED** | **PwC is missing** from dockets dataset (45 companies present). Target for Milestone 1. |
| 3 | `test_03_contacts_per_company_thresholds` | Verifies each of the 11 companies has >= 3 contacts, and every contact entry includes valid non-empty `full_name`, `position`, and valid `linkedin_url` (`^https:\/\/[a-z]{2,3}\.linkedin\.com\/in\/[\w\-]+`). | **FAILED** | **PwC has 0 contacts** (caused by missing PwC entry). All 189 existing contacts across 45 companies have 100% valid names, positions, and valid LinkedIn URLs. |
| 4 | `test_04_connection_notes_strict_290_char_limit` | Verifies 100% of connection notes across all contacts are strictly <= 290 characters (and hard ceiling <= 300 characters, zero truncation), and >= 50 characters. | **PASSED** | 189/189 notes evaluated. Min: 235 chars, Max: 262 chars, Over 290: 0, Over 300: 0, Under 50: 0, Truncated: 0. |
| 5 | `test_05_zero_hallucination_profile_alignment` | Verifies that messages reference verified credentials from `data/verified_profile.json` (DSU BBA, Aero India 2025, Instawork 99%+) and contain zero unearned or fabricated claims (MBA, IIM, IIT, PhD). | **PASSED** | 100% notes reference DSU BBA, asks reference Aero India 2025 & Instawork 99%, dockets reference Aditya Mehra, 0 hallucination terms found. |
| 6 | `test_06_corridor_and_domain_coverage` | Verifies all 5 tech corridors (Outer Ring Road, Manyata, Bellandur, Whitefield, Domlur) and all 5 domains (Operations, Supply Chain, Advisory/Risk, Trade Finance, Merchant BD) are properly represented. | **PASSED** | All 5 corridors and all 5 domains have active representation in dataset. |
| 7 | `test_07_console_html_standalone_capabilities` | Verifies `index.html` has inlined data (`const dockets =`), clipboard copy handlers with visual feedback, LinkedIn launchers (`target="_blank"`), localStorage status tracking logic (`Pending`, `Contacted`, `Referral Submitted`), and filter pill elements for Corridors, Companies, and Domains. | **FAILED** | Inlined data, clipboard, localStorage, and corridor pills pass; **Company and Domain filter pills are missing** from `index.html`. Target for Milestone 3. |
| 8 | `test_08_approval_queue_schema_fidelity` | Verifies `data/approval_queue.csv` and `data/approval_queue.json` maintain exact 14 standard columns, sequential numbering, and valid format. | **PASSED** | Headers match exact 14 columns, 604 rows match 1-to-1 between CSV and JSON, Action IDs strictly monotonic and sequential (1..604, ACT-0001 to ACT-0423, REF-0424 to REF-0604). |

---

## 2. Baseline Test Execution Results

Command executed:
```bash
python -m unittest -v tests/test_bangalore_referral_strike.py
```

### Verbose Output:
```
test_01_deliverable_files_exist (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_01_deliverable_files_exist)
1. Verifies existence and non-zero size of all 5 primary deliverable files. ... ok
test_02_all_11_mandated_companies_present (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_02_all_11_mandated_companies_present)
2. Verifies all 11 mandated employers are present in bangalore_live_referral_dockets.json. ... FAIL
test_03_contacts_per_company_thresholds (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_03_contacts_per_company_thresholds)
3. Verifies each of the 11 companies has >= 3 contacts, with valid name, position, and LinkedIn URL. ... FAIL
test_04_connection_notes_strict_290_char_limit (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_04_connection_notes_strict_290_char_limit)
4. Verifies 100% of connection notes across all contacts are strictly <= 290 chars (hard ceiling <= 300) and >= 50 chars. ... ok
test_05_zero_hallucination_profile_alignment (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_05_zero_hallucination_profile_alignment)
5. Verifies messages reference verified credentials from verified_profile.json with zero fabricated claims. ... ok
test_06_corridor_and_domain_coverage (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_06_corridor_and_domain_coverage)
6. Verifies all 5 tech corridors and all 5 functional domains are properly represented in the dataset. ... ok
test_07_console_html_standalone_capabilities (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_07_console_html_standalone_capabilities)
7. Verifies index.html has inlined data, clipboard copy handlers, LinkedIn launchers, localStorage tracking, and filter pills. ... FAIL
test_08_approval_queue_schema_fidelity (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_08_approval_queue_schema_fidelity)
8. Verifies data/approval_queue.csv and data/approval_queue.json maintain exact 14 standard columns, sequential IDs, and valid format. ... ok

======================================================================
FAIL: test_02_all_11_mandated_companies_present (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_02_all_11_mandated_companies_present)
2. Verifies all 11 mandated employers are present in bangalore_live_referral_dockets.json.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "E:\anti\tests\test_bangalore_referral_strike.py", line 184, in test_02_all_11_mandated_companies_present
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        missing_companies, [],
        ^^^^^^^^^^^^^^^^^^^^^^
        f"Mandated top employers missing from bangalore_live_referral_dockets.json: {missing_companies}"
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: Lists differ: ['PwC'] != []

First list contains 1 additional elements.
First extra element 0:
'PwC'

- ['PwC']
+ [] : Mandated top employers missing from bangalore_live_referral_dockets.json: ['PwC']

======================================================================
FAIL: test_03_contacts_per_company_thresholds (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_03_contacts_per_company_thresholds)
3. Verifies each of the 11 companies has >= 3 contacts, with valid name, position, and LinkedIn URL.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "E:\anti\tests\test_bangalore_referral_strike.py", line 222, in test_03_contacts_per_company_thresholds
    self.assertEqual(errors, [], "Contact threshold / integrity validation failed:\n" + "\n".join(errors))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ["Company 'PwC' has no docket entries (expected >= 3 contacts)"] != []

First list contains 1 additional elements.
First extra element 0:
"Company 'PwC' has no docket entries (expected >= 3 contacts)"

- ["Company 'PwC' has no docket entries (expected >= 3 contacts)"]
+ [] : Contact threshold / integrity validation failed:
Company 'PwC' has no docket entries (expected >= 3 contacts)

======================================================================
FAIL: test_07_console_html_standalone_capabilities (tests.test_bangalore_referral_strike.TestBengaluruReferralStrikeE2E.test_07_console_html_standalone_capabilities)
7. Verifies index.html has inlined data, clipboard copy handlers, LinkedIn launchers, localStorage tracking, and filter pills.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "E:\anti\tests\test_bangalore_referral_strike.py", line 389, in test_07_console_html_standalone_capabilities
    self.assertTrue(has_company_filter, "Console HTML missing dedicated company filter pill elements / UI (filterCompany)")
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : Console HTML missing dedicated company filter pill elements / UI (filterCompany)

----------------------------------------------------------------------
Ran 8 tests in 0.165s

FAILED (failures=3)
```

**Summary**: 5 tests PASSED, 3 tests FAILED.  
The failures accurately isolate implementation gaps in Milestone 1 and Milestone 3 without false positives.

---

## 3. Escalations & Implementation Action Items

### Item 1: Milestone 1 (Data Matching & Docket Expansion)
- **Defect**: PwC (PricewaterhouseCoopers) is missing from `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json`.
- **Impact**: Causes `test_02_all_11_mandated_companies_present` and `test_03_contacts_per_company_thresholds` to fail.
- **Action for Data Worker**: Add target docket for `PricewaterhouseCoopers (PwC)` (Job: `BLR-JOB-013`, `Business Operations Analyst`, URL: `https://www.pwc.in/careers.html`, Corridor: `Bellandur / Outer Ring Road`) with 3–5 curated contacts from `data/ALL_CONNECTIONS_OUTREACH_MASTER.csv` (e.g., Shalini Jha, Janeesha Antony, Sneha Sharma).

### Item 2: Milestone 3 (Interactive Web Console)
- **Defect**: `teamwork_projects/bangalore_referral_strike/index.html` lacks Company and Domain/Role filter pills.
- **Impact**: Causes `test_07_console_html_standalone_capabilities` to fail.
- **Action for UI Worker**: Add Company filter pills container (11 core companies) and Domain filter pills container (5 functional domains) to `index.html`, and update `render()` to perform intersection filtering across `[Corridor ∩ Company ∩ Domain ∩ Status ∩ SearchTerm]`. Also sync updated inlined dockets into `const dockets = [...]`.
