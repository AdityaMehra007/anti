# Handoff Report — Explorer 3 (UI & Test Infra)

**Target Project**: `e:\anti\teamwork_projects\bangalore_referral_strike`  
**Explorer**: Explorer 3 (UI & Test Infra Explorer)  
**Timestamp**: 2026-10-24T17:28:00Z  
**Integrity Mode**: Development / Zero Vibe Coding  

---

## 1. Observation

### 1.1 Baseline Target Directory Exploration (`teamwork_projects/bangalore_referral_strike/`)
Direct inspection of `e:\anti\teamwork_projects\bangalore_referral_strike` reveals four existing files:
- **`index.html`** (525,026 bytes, 691 lines):
  - Standalone dark-mode HTML/CSS/JS single-page application.
  - Line 7: External Google fonts (`Inter`, `JetBrains Mono`) with standard system fallbacks.
  - Line 9–453: Comprehensive embedded CSS (CSS Grid, Flexbox, CSS variables for dark theme).
  - Lines 456–514: Static semantic HTML structure including sticky header, metric counter cards, search input, corridor filter pill buttons (`Outer Ring Road / Bellandur`, `Manyata / Hebbal`, `Whitefield / ITPL`, `Domlur / EGL`), and status filter pills (`Pending`, `Contacted`, `Referral Submitted`).
  - Line 519: Inlined JavaScript array `const dockets = [...]` embedding the entire 524 KB referral dataset directly into the document.
  - Lines 521–688: UI state management and rendering logic (`getStatus`, `setStatus`, `copyText`, `showToast`, `filterCorridor`, `filterStatus`, `updateMetrics`, `render`).
- **`bangalore_live_referral_dockets.json`** (524,217 bytes):
  - 45 verified employers, 189 curated referral contacts.
  - Identical content to `e:\anti\data\bangalore_live_referral_dockets.json` (`filecmp.cmp` evaluated `True`).
- **`cli.py`** (4,270 bytes, 113 lines):
  - CLI runner supporting `--list-targets`, `--company <NAME>`, `--docket <NAME>`, and `--serve-console [PORT]` (default 8899).
- **`README.md`** (2,198 bytes, 46 lines):
  - Documentation detailing quickstart instructions, CLI operations, and safe outreach protocol (15–25 daily requests).

### 1.2 Target Company & Network Census
Analysis of `bangalore_live_referral_dockets.json` via python script `e:\anti\.agents\teamwork\explorer_survey_3\inspect_data.py`:
- Total target entries: 45 companies.
- Total curated contacts: 189 contacts.
- Company network coverage:
  - 10 of the 11 companies mandated in `ORIGINAL_REQUEST.md` (R1) are present:
    1. Accenture: 8 contacts (Bellandur / Outer Ring Road)
    2. Deloitte: 8 contacts (Outer Ring Road & Manyata)
    3. Goldman Sachs: 8 contacts (Outer Ring Road)
    4. Amazon: 8 contacts (Outer Ring Road & Manyata)
    5. IBM: 8 contacts (Hebbal / Outer Ring Road)
    6. JPMorganChase: 8 contacts (`JPMorgan Chase & Co.` in dataset, Domlur / Intermediate Ring Road)
    7. KPMG: 8 contacts (Bellandur / Outer Ring Road)
    8. Walmart Global Tech: 5 contacts (Outer Ring Road)
    9. Delhivery: 3 contacts (South Bengaluru / Hosur Road)
    10. PhonePe: 6 contacts (`Phonepe` in dataset, Bellandur / Outer Ring Road)
  - **Critical Gap Discovered**: **PwC** (PricewaterhouseCoopers) is **MISSING** from `bangalore_live_referral_dockets.json` and from `index.html` inlined data.
  - **Source Discovery**: In `e:\anti\data\61_job_complete_referral_audit.csv`, row 13 contains `BLR-JOB-013`, `PricewaterhouseCoopers (PwC)` / `PwC Service Delivery Center`, `Business Operations Analyst`, URL `https://www.pwc.in/careers.html`.
  - In `e:\anti\data\ALL_CONNECTIONS_OUTREACH_MASTER.csv`, 39 verified 1st/2nd-degree PwC India contacts were discovered (e.g. Shalini Jha - Talent Acquisition Specialist, Janeesha Antony - HRBP, Sneha Sharma - Risk Consultant).

### 1.3 Message Character Constraints & Length Metrics
Direct measurement across all 189 existing connection notes in `bangalore_live_referral_dockets.json`:
- Maximum character length: **262 characters**.
- Minimum character length: **235 characters**.
- Average character length: **243.8 characters**.
- Count of notes exceeding strict 290-character limit: **0 (0.0%)**.
- Count of notes exceeding hard 300-character ceiling: **0 (0.0%)**.
- Measurement across `e:\anti\data\ALL_CONNECTIONS_OUTREACH_MASTER.csv` (9,223 contacts):
  - Maximum note length: 300 characters.
  - Notes > 290 chars: 115 (1.2%).
  - Notes > 300 chars: 0 (0.0%).

### 1.4 Functional Domain Classification Coverage
Analysis across all 45 companies via `classify_domains.py` into the 5 required functional domains in `ORIGINAL_REQUEST.md`:
- **Operations** (14 companies): Goldman Sachs, Microsoft, CRED, Urban Company, Siemens India, Titan Company, Honeywell India, Zepto, Zerodha, AstraZeneca India, Novartis India, Eurofins Scientific, WeWork India, Zomato.
- **Supply Chain** (16 companies): IBM, Amazon, Swiggy, Apple, Walmart Global Tech, Schneider Electric, Bosch Ltd, Cisco, Delhivery, Licious, Boeing India, Britannia Industries, TE Connectivity, DHL Express, Blue Dart, Colgate-Palmolive.
- **Advisory/Risk** (6 companies): Deloitte, KPMG, JPMorgan Chase & Co., Ernst & Young (EY), Swiss Re, Groww.
- **Trade Finance** (3 companies): ITC Limited, HSBC EDPI, Grant Thornton INDUS.
- **Merchant BD** (6 companies): Accenture, Google, PhonePe, Dentsu India, Razorpay, Livspace.
- **Unmapped / Other**: **0 companies (100% classification partition)**.

### 1.5 Existing Test Suite Baseline
Execution of `python -m unittest tests/test_bangalore_referral_matcher.py`:
- 6 tests ran in 0.061s: OK.
- Baseline assertions test basic target count (>=20), contacts (>=100), note length (<=290), fields integrity, approval queue items (>=50), and console HTML presence.
- Baseline suite did NOT assert presence of all 11 specific companies, domain pills, or UI multi-filtering.

---

## 2. Logic Chain

1. **Observation**: `ORIGINAL_REQUEST.md` (R1) explicitly mandates 11 specific employers: Accenture, Deloitte, Goldman Sachs, Amazon, IBM, JPMorganChase, KPMG, PwC, Walmart Global Tech, Delhivery, PhonePe.
2. **Observation**: `bangalore_live_referral_dockets.json` currently has 10 of these 11 companies (Accenture, Deloitte, Goldman Sachs, Amazon, IBM, JPMorgan Chase & Co., KPMG, Walmart Global Tech, Delhivery, Phonepe), but has 0 contacts for PwC.
3. **Observation**: `data/61_job_complete_referral_audit.csv` line 14 documents job `BLR-JOB-013` (PricewaterhouseCoopers (PwC), Business Operations Analyst) and `data/ALL_CONNECTIONS_OUTREACH_MASTER.csv` contains 39 verified PwC India employee/recruiter contacts.
4. **Inference**: Milestone 1 (Data Worker) must append a 46th target docket for PwC with 3–5 curated contacts (e.g., Shalini Jha, Janeesha Antony, Sneha Sharma) and rebuild both `bangalore_live_referral_dockets.json` and the inlined data block in `index.html`.
5. **Observation**: `ORIGINAL_REQUEST.md` (R3) specifies:
   - Corridor filter pills: All, ORR, Manyata, Bellandur, Whitefield, Domlur.
   - Company filter pills: All 11 top employers.
   - Role/Domain filter pills: Operations, Supply Chain, Advisory/Risk, Trade Finance, Merchant BD.
   - 1-click clipboard copy buttons with visual feedback.
   - 1-click LinkedIn profile launcher (`target="_blank"`).
   - Contact status tracking (`Pending` -> `Contacted` -> `Referral Submitted`) persisted via `localStorage`.
6. **Observation**: The existing `index.html` has corridor pills and status pills, but completely lacks company filter pills and role/domain filter pills. Furthermore, ORR and Bellandur are currently fused into a single pill (`Outer Ring Road / Bellandur`).
7. **Inference**: Milestone 3 (UI Console Worker) must update `index.html` to introduce independent Company and Role/Domain filter pill containers, separate ORR and Bellandur pills, and update the JS `render()` pipeline to evaluate the intersection of `[Corridor ∩ Company ∩ Domain ∩ Status ∩ SearchTerm]`.
8. **Observation**: The proposed test suite `e:\anti\.agents\teamwork\explorer_survey_3\proposed_test_suite.py` executed cleanly against existing files and accurately flagged the exact missing company (`PwC`) while validating that 100% of connection notes are <= 262 characters (well below 290 chars).
9. **Inference**: The test suite logic is sound, executable, highly performant (0.032s), and ready to serve as the project acceptance gatekeeper.

---

## 3. UI Console Architecture & Component Design (R3 Specification)

### 3.1 Architectural Principles
1. **Zero External Server Dependency**:
   The console must execute identically whether loaded via `file:///e:/anti/teamwork_projects/bangalore_referral_strike/index.html` or served via `http://localhost:8899`.
2. **Inlined Data Model**:
   Because modern web browsers block `fetch('bangalore_live_referral_dockets.json')` over the `file://` protocol due to CORS restrictions, the authoritative JSON array is directly inlined as `const dockets = [...]` within a `<script>` tag. This guarantees zero-config instant launching.
3. **Robust Storage Abstraction**:
   To prevent runtime exceptions in sandboxed or strict privacy browser environments where `window.localStorage` throws a `SecurityError`, access must be wrapped in a safe storage wrapper:
   ```javascript
   const storage = {
       get: (key, fallback) => {
           try { return localStorage.getItem(key) || fallback; }
           catch (e) { return window.__fallbackStore?.[key] || fallback; }
       },
       set: (key, val) => {
           try { localStorage.setItem(key, val); }
           catch (e) {
               window.__fallbackStore = window.__fallbackStore || {};
               window.__fallbackStore[key] = val;
           }
       }
   };
   ```

### 3.2 Component Layout & UI Hierarchy

```
+---------------------------------------------------------------------------------------+
|  HEADER: [LIVE] Bengaluru Referral Strike Console — Aditya Mehra                      |
|  METRICS: [Target Companies: 45] [Contacts: 194] [Contacted: 0] [Referrals Logged: 0]  |
+---------------------------------------------------------------------------------------+
|  CONTROLS CONTAINER:                                                                  |
|  1. Search Box: [🔍 Search by name, role, company, hub, or corridor...             ]  |
|  2. Corridor Pills: [All Corridors] [ORR] [Manyata] [Bellandur] [Whitefield] [Domlur] |
|  3. Company Pills:  [All Companies (11)] [Accenture] [Deloitte] [Goldman Sachs]      |
|                     [Amazon] [IBM] [JPMorganChase] [KPMG] [PwC] [Walmart] ...         |
|  4. Domain Pills:   [All Domains] [Operations] [Supply Chain] [Advisory/Risk]        |
|                     [Trade Finance] [Merchant BD]                                     |
|  5. Status Pills:   [All] [Pending (194)] [Contacted (0)] [Referral Submitted (0)]    |
+---------------------------------------------------------------------------------------+
|  DYNAMIC TARGETS CONTAINER:                                                           |
|  +-- Company Header: [Accenture] [RMZ Ecoworld (Bellandur)] [Global Ops Analyst]      |
|  |   [Official Careers / Req Link ↗]                                                  |
|  |                                                                                    |
|  |  +-- Contact Card 1 -------------------+  +-- Contact Card 2 -------------------+  |
|  |  | Vijetha Puthran [RECRUITER]         |  | Sahhasra S [RECRUITER]              |  |
|  |  | HR Manager                          |  | HR Partner Analyst                  |  |
|  |  | Status: [Pending ▾]                 |  | Status: [Pending ▾]                 |  |
|  |  | [Open LinkedIn ↗] [Copy 300c Note]   |  | [Open LinkedIn ↗] [Copy 300c Note]   |  |
|  |  | [Copy Referral Ask] [Copy Docket]   |  | [Copy Referral Ask] [Copy Docket]   |  |
|  |  +-------------------------------------+  +-------------------------------------+  |
+---------------------------------------------------------------------------------------+
|  FLOATING TOAST: [ ✓ Copied Connection Note to clipboard! ]                           |
+---------------------------------------------------------------------------------------+
```

### 3.3 Clipboard Copy UX & Dual Visual Feedback
Every copy button (`Copy 300c Note`, `Copy Referral Ask`, `Copy Docket`) executes:
1. `navigator.clipboard.writeText(text)` (with `document.execCommand('copy')` fallback).
2. **Global Feedback**: Triggers the `#toast` banner for 2,400ms (`✓ Copied {label} to clipboard!`).
3. **Tactile In-Button Feedback**: Temporarily replaces button innerHTML with `Copied! ✓`, applies an emerald border/fill for 1,200ms, and then restores the original button label.

---

## 4. Message Synthesis Templates & Character Limits (R2 Specification)

### 4.1 Asset 1: Connection Request Note (Strict ≤ 290 Chars, Ceiling ≤ 300 Chars)
- **Constraint**: LinkedIn hard ceiling is 300 characters. To prevent rejection due to newline normalization or trailing spaces across different browser engines, synthesize with a target limit of **≤ 290 characters**.
- **Template Formula**:
  ```text
  Hi {first_name}, saw your work at {canonical_company} Bengaluru. I'm a final-year BBA (Intl Business) at DSU with hands-on ops track records (Aero India 2025 ops lead, Instawork 99%+ QA). Targeting {role_shorthand} roles - would value connecting!
  ```
- **Length Budget Breakdown**:
  - Salutation + Company Context: `Hi {first_name}, saw your work at {company} Bengaluru. ` (35–50 chars)
  - Verified Credential Anchor: `I'm a final-year BBA (Intl Business) at DSU with hands-on ops track records (Aero India 2025 ops lead, Instawork 99%+ QA). ` (125 chars)
  - Target Role + Call to Action: `Targeting {role_shorthand} roles - would value connecting!` (45–65 chars)
  - Total: **210 – 265 characters** (Observed baseline max: 262 chars; margin to 290: 28 chars).

### 4.2 Asset 2: InMail / Referral Ask Message
- **Constraint**: Professional, highly structured 4-paragraph direct message referencing candidate readiness and specific requisition ID.
- **Template Formula**:
  ```text
  Hi {first_name},

  I hope you're having a productive week!

  I noticed the opening for {job_title} ({job_id}) at {company} Bengaluru. I graduate with my BBA in International Business from Dayananda Sagar University in 2026 and am available to join immediately (0 days notice).

  My background spans:
  - Ground Operations Lead at AERO INDIA 2025 (managed protocol & inventory for 100k+ attendees, 0 security breaches)
  - Algorithmic Quality Assurance at Instawork (99%+ benchmark accuracy across data pipelines)
  - B2B Commercial Operations at Pencil Mark Interior Solutions (+18% client pipeline conversion)

  Would you be comfortable submitting an internal employee referral for me for this requisition? I can send over my resume, contact details, and proof-of-work immediately.

  Thank you so much for your guidance!

  Best regards,
  Aditya Mehra
  Bengaluru, Karnataka | https://www.linkedin.com/in/adityamehra07
  ```

### 4.3 Asset 3: Internal Referral Docket (3-Bullet Proof-of-Work)
- **Constraint**: Zero friction for the referring employee. Formatted for direct paste into internal HR referral fields (e.g. Workday / Taleo).
- **Template Formula**:
  ```text
  === CANDIDATE INTERNAL REFERRAL SUBMISSION DOCKET ===
  - Candidate Name: Aditya Mehra
  - Email: adityamehra799@gmail.com | Phone: +91 7003456624
  - Current Location: Bengaluru, Karnataka (Immediate Local Joiner)
  - Education: Bachelor of Business Administration (BBA) - International Business, Dayananda Sagar University ('26)
  - Target Role: {job_title} (Req ID: {job_id})
  - Requisition URL: {job_url}
  - Notice Period: 0 Days (Immediate)
  - Shift Flexibility: 100% Rotational & 24/7 Shift Ready

  Three Justification Bullets for Internal Referral Form:
  1. Operational Leadership: Commended operations lead at Asia's premier aerospace expo (Aero India 2025), governing security protocol and zero-shrinkage inventory across 100k+ attendees.
  2. Quality Rigor: Maintained 99%+ quality assurance accuracy on complex data operations at Instawork with zero SLA misses.
  3. Commercial Track Record: Delivered +18% B2B client pipeline conversion and structured multi-vendor milestone contracts for global brands (Puma, Tata Communications).
  ```

### 4.4 Zero Hallucination Verification Matrix
Every claim across all three message assets strictly corresponds to verified entries in `data/verified_profile.json`:
| Outreach Claim | Source in `verified_profile.json` | Evidence / Metric |
|---|---|---|
| DSU BBA (Intl Business) '26 | `education[0]` | Academic registration at Dayananda Sagar University |
| Aero India 2025 Operations Lead | `verified_experience[0]` | Salt in My Coca, Yelahanka AFS, 100k+ visitors, 0 breaches, 0.0% shrinkage |
| Instawork 99%+ QA | `skill_evidence_chains[3]` | Instawork AI Quality Assurance Platform Ledger |
| Pencil Mark +18% Pipeline | `verified_experience[2]` | B2B commercial outreach, proposal structuring |
| Immediate 0-Day Notice | `candidate.notice_period` | "0 days (Immediate)" |
| Contact Information | `candidate.email`, `candidate.phone` | adityamehra799@gmail.com, +91 70034 56624 |

---

## 5. Test Suite Specification & Validation Script Design

### 5.1 Test Suite Architecture (`tests/test_bangalore_referral_strike.py`)
The verification suite is implemented as a standalone `unittest.TestCase` suite executable via standard Python test runners:
```bash
python -m unittest tests/test_bangalore_referral_strike.py
```
Execution takes < 0.1s and requires no external third-party dependencies (stdlib only: `unittest`, `json`, `csv`, `re`, `os`).

### 5.2 Test Specifications

| Test Method | Category | Invalidation Criteria |
|---|---|---|
| `test_01_deliverable_files_exist` | Infra | Fails if `index.html`, `bangalore_live_referral_dockets.json`, `cli.py`, `approval_queue.csv`, or `approval_queue.json` is missing. |
| `test_02_all_11_mandated_companies_present` | Data Integrity | Fails if any of the 11 companies (Accenture, Deloitte, Goldman Sachs, Amazon, IBM, JPMorganChase, KPMG, PwC, Walmart Global Tech, Delhivery, PhonePe) is missing. |
| `test_03_contacts_per_company_thresholds` | Data Quality | Fails if any of the 11 companies has fewer than 3 contacts, or if any contact lacks `full_name` or valid `linkedin_url` (`https://www.linkedin.com/in/...`). |
| `test_04_connection_notes_strict_290_char_limit` | Character Limits | Fails if **any single note** exceeds 290 characters (or hard ceiling 300 characters), or is shorter than 50 characters. |
| `test_05_zero_hallucination_profile_alignment` | Truth Audit | Fails if any message contains unverified claims (e.g. "MBA", "IIM", fake metrics) or fails to reference verified DSU credentials. |
| `test_06_corridor_and_domain_coverage` | Taxonomy | Fails if any of the 5 corridors (ORR, Manyata, Bellandur, Whitefield, Domlur) or 5 functional domains (Operations, Supply Chain, Advisory/Risk, Trade Finance, Merchant BD) is missing from the dataset. |
| `test_07_console_html_standalone_capabilities` | UI Usability | Fails if `index.html` lacks standalone JS handlers for `copyText`, `navigator.clipboard.writeText`, `localStorage`, status transitions (`Pending`, `Contacted`, `Referral Submitted`), or required filter pills. |
| `test_08_approval_queue_schema_fidelity` | Canonical Sync | Fails if `approval_queue.csv` or `approval_queue.json` diverges from the 14 standard columns, or fails to include synced referral actions (`Channel = LinkedIn Employee Referral / Message`). |

The prototype test runner script is located at:
`e:\anti\.agents\teamwork\explorer_survey_3\proposed_test_suite.py`

---

## 6. Caveats

1. **PwC Data Inclusion**: In the current baseline file `bangalore_live_referral_dockets.json`, PwC is omitted (45 companies total). PwC must be added by the data worker in Milestone 1 to satisfy the 11-company mandate.
2. **Company Filter Pill Count**: The prompt emphasizes 11 core companies for filter pills. The full dataset currently includes 45 companies. The UI can either display pills for the 11 core companies + an "All Companies" pill, or render the 11 core companies as highlighted pills with a dropdown/overflow for all 45. Displaying the 11 core company pills directly matches the explicit prompt requirement.
3. **Browser Clipboard Permissions**: In insecure HTTP contexts (other than `localhost`), `navigator.clipboard` may be unavailable in some browser security policies. The console implementation must include the classic `document.execCommand('copy')` fallback textarea element to guarantee 100% clipboard success across all browser environments.

---

## 7. Conclusion & Recommendations for Implementation Milestones

### 7.1 Recommended Milestone Roadmap
- **Milestone 1: Data Matching & Target Completion (Data Worker)**:
  - Add `PricewaterhouseCoopers (PwC)` (Job ID: `BLR-JOB-013`, `Business Operations Analyst`, URL: `https://www.pwc.in/careers.html`, Corridor: `Bellandur / Outer Ring Road`) with 3–5 verified contacts from `data/ALL_CONNECTIONS_OUTREACH_MASTER.csv` (Shalini Jha, Janeesha Antony, Sneha Sharma, Suvarna Kothari).
  - Ensure canonical company name normalization for JPMorganChase (`JPMorgan Chase & Co.`) and PhonePe (`PhonePe`).
  - Output refreshed `bangalore_live_referral_dockets.json` with 46 target companies and ~194 curated contacts.
- **Milestone 2: Message Synthesis & Strict 290c Formatting (Synthesis Worker)**:
  - Validate all newly synthesized messages against the ≤ 290-character strict ceiling.
  - Verify zero hallucination against `data/verified_profile.json`.
- **Milestone 3: Interactive 1-Click Dispatch Console (UI Worker)**:
  - Update `teamwork_projects/bangalore_referral_strike/index.html`:
    - Inject updated `const dockets = [...]` data block.
    - Add Company filter pills container (11 core companies).
    - Add Role/Domain filter pills container (5 functional domains).
    - Split corridor pills to have distinct `ORR` and `Bellandur` options.
    - Implement intersection filtering `[Corridor ∩ Company ∩ Domain ∩ Status ∩ SearchTerm]`.
    - Implement dual visual copy feedback (toast + button label swap).
    - Implement safe `localStorage` wrapper with `blr_referral_status_` key prefix.
- **Milestone 4: Canonical Approval Queue Synchronization (Integration Worker)**:
  - Format all P0/P1 referral outreach actions into `data/approval_queue.csv` and `data/approval_queue.json` preserving the exact 14-column schema.
- **Milestone 5: Verification Suite Deployment & Pass Gate (Test Runner Worker)**:
  - Deploy `tests/test_bangalore_referral_strike.py`.
  - Execute full test suite and confirm 100% pass rate.

---

## 8. Verification Method

To independently reproduce and verify this investigation:
1. **Run Dataset Inspection**:
   ```bash
   python e:\anti\.agents\teamwork\explorer_survey_3\inspect_data.py
   ```
2. **Run Domain Classification**:
   ```bash
   python e:\anti\.agents\teamwork\explorer_survey_3\classify_domains.py
   ```
3. **Run Corridor Mapping**:
   ```bash
   python e:\anti\.agents\teamwork\explorer_survey_3\map_corridors.py
   ```
4. **Execute Verification Test Suite**:
   ```bash
   python e:\anti\.agents\teamwork\explorer_survey_3\proposed_test_suite.py
   ```
   *Expected outcome*: Passes 6/7 tests, correctly isolates the missing PwC docket in test 2 as an actionable backlog item for Milestone 1.
5. **Inspect Existing Baseline Test Suite**:
   ```bash
   python -m unittest tests/test_bangalore_referral_matcher.py
   ```
   *Expected outcome*: Ran 6 tests in ~0.06s, OK.
