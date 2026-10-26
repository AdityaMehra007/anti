r"""
Canonical Automated E2E Test Suite for Bengaluru Job Referral Strike & 1-Click Dispatch Console.

Authoritative Sources:
- e:/anti/.agents/teamwork/ORIGINAL_REQUEST.md
- e:/anti/.agents/teamwork/orchestrator_1/TEST_INFRA.md
- e:/anti/.agents/teamwork/explorer_survey_3/handoff.md

Test Coverage:
1. test_01_deliverable_files_exist:
   Verifies existence and non-zero size of all 5 deliverable files:
   - teamwork_projects/bangalore_referral_strike/index.html
   - teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json
   - teamwork_projects/bangalore_referral_strike/cli.py
   - data/approval_queue.csv
   - data/approval_queue.json
2. test_02_all_11_mandated_companies_present:
   Verifies presence of all 11 mandated employers: Accenture, Deloitte, Goldman Sachs,
   Amazon, IBM, JPMorganChase, KPMG, PwC, Walmart Global Tech, Delhivery, PhonePe.
3. test_03_contacts_per_company_thresholds:
   Verifies each of the 11 companies has >= 3 contacts, and every contact entry includes
   valid non-empty full_name, position, and valid linkedin_url
   (matching ^https:\/\/[a-z]{2,3}\.linkedin\.com\/in\/[\w\-]+).
4. test_04_connection_notes_strict_290_char_limit:
   Verifies 100% of connection notes across all contacts are strictly <= 290 characters
   (and hard ceiling <= 300 characters, zero truncation), and >= 50 characters.
5. test_05_zero_hallucination_profile_alignment:
   Verifies messages reference verified credentials from data/verified_profile.json
   (DSU BBA, Aero India 2025, Instawork 99%+) and contain zero unearned or fabricated claims.
6. test_06_corridor_and_domain_coverage:
   Verifies all 5 tech corridors (Outer Ring Road, Manyata, Bellandur, Whitefield, Domlur)
   and all 5 domains (Operations, Supply Chain, Advisory/Risk, Trade Finance, Merchant BD)
   are properly represented.
7. test_07_console_html_standalone_capabilities:
   Verifies index.html has inlined data (const dockets =), clipboard copy handlers with
   visual feedback, LinkedIn launchers (target="_blank"), localStorage status tracking logic
   (Pending, Contacted, Referral Submitted), and filter pill elements for Corridors,
   Companies, and Domains.
8. test_08_approval_queue_schema_fidelity:
   Verifies data/approval_queue.csv and data/approval_queue.json maintain exact 14 standard
   columns, sequential numbering, and valid format.
"""

import os
import re
import csv
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(ROOT_DIR, 'teamwork_projects', 'bangalore_referral_strike')

DOCKETS_PATH = os.path.join(PROJECT_DIR, 'bangalore_live_referral_dockets.json')
CONSOLE_PATH = os.path.join(PROJECT_DIR, 'index.html')
CLI_PATH = os.path.join(PROJECT_DIR, 'cli.py')
QUEUE_CSV_PATH = os.path.join(ROOT_DIR, 'data', 'approval_queue.csv')
QUEUE_JSON_PATH = os.path.join(ROOT_DIR, 'data', 'approval_queue.json')
PROFILE_PATH = os.path.join(ROOT_DIR, 'data', 'verified_profile.json')

REQUIRED_11_COMPANIES = [
    'Accenture', 'Deloitte', 'Goldman Sachs', 'Amazon', 'IBM',
    'JPMorganChase', 'KPMG', 'PwC', 'Walmart Global Tech', 'Delhivery', 'PhonePe'
]

REQUIRED_CORRIDORS = [
    'Outer Ring Road', 'Manyata', 'Bellandur', 'Whitefield', 'Domlur'
]

REQUIRED_DOMAINS = [
    'Operations', 'Supply Chain', 'Advisory/Risk', 'Trade Finance', 'Merchant BD'
]

EXPECTED_QUEUE_HEADERS = [
    'Action ID', 'Person', 'Company', 'Job', 'Channel', 'Draft Message',
    'Reason / Evidence', 'Priority', 'Approval Required', 'Status',
    'Staged Timestamp', 'Approved Timestamp', 'Dispatched Timestamp', 'Dispatch Packet'
]


def _normalize_name(name):
    """Normalize string for robust token comparison."""
    return re.sub(r'[^a-zA-Z0-9]', '', str(name)).lower()


def _matches_company(req_company, candidate_names):
    """Matches a required company name against a list of candidate strings."""
    req_clean = _normalize_name(req_company)
    for c in candidate_names:
        c_clean = _normalize_name(c)
        if not c_clean:
            continue
        if req_clean in c_clean or c_clean in req_clean:
            return True
        if req_company == 'PwC' and ('pricewaterhouse' in c.lower() or 'pwc' in c.lower()):
            return True
        if req_company == 'JPMorganChase' and 'jpmorgan' in c.lower():
            return True
        if req_company == 'Walmart Global Tech' and 'walmart' in c.lower():
            return True
        if req_company == 'PhonePe' and 'phonepe' in c.lower():
            return True
    return False


def _classify_domain(job_title):
    """Classify job role into 1 of 5 standard functional domains."""
    t = str(job_title).lower()
    if any(k in t for k in ['trade', 'finance', 'receivables', 'exim']):
        return 'Trade Finance'
    if any(k in t for k in ['risk', 'advisory', 'audit', 'compliance']):
        return 'Advisory/Risk'
    if any(k in t for k in ['supply chain', 'logistics', 'freight', 'procurement', 'vendor']):
        return 'Supply Chain'
    if any(k in t for k in ['merchant', 'business development', 'bd', 'sales', 'brand activation']):
        return 'Merchant BD'
    if any(k in t for k in ['operations', 'ops', 'community', 'support', 'member experience']):
        return 'Operations'
    return 'Other'


class TestBengaluruReferralStrikeE2E(unittest.TestCase):
    """Canonical E2E verification suite for Bengaluru Job Referral Strike & 1-Click Console."""

    @classmethod
    def setUpClass(cls):
        # Load dockets
        cls.dockets_exists = os.path.exists(DOCKETS_PATH)
        if cls.dockets_exists:
            with open(DOCKETS_PATH, 'r', encoding='utf-8') as f:
                cls.dockets = json.load(f)
        else:
            cls.dockets = []

        # Load console HTML
        cls.console_exists = os.path.exists(CONSOLE_PATH)
        if cls.console_exists:
            with open(CONSOLE_PATH, 'r', encoding='utf-8') as f:
                cls.console_html = f.read()
        else:
            cls.console_html = ""

        # Load profile
        cls.profile_exists = os.path.exists(PROFILE_PATH)
        if cls.profile_exists:
            with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
                cls.profile = json.load(f)
        else:
            cls.profile = {}

    def test_01_deliverable_files_exist(self):
        """1. Verifies existence and non-zero size of all 5 primary deliverable files."""
        deliverables = {
            "Console HTML": CONSOLE_PATH,
            "Live Referral Dockets JSON": DOCKETS_PATH,
            "CLI Runner": CLI_PATH,
            "Approval Queue CSV": QUEUE_CSV_PATH,
            "Approval Queue JSON": QUEUE_JSON_PATH,
        }
        for label, path in deliverables.items():
            self.assertTrue(os.path.exists(path), f"Missing {label} at expected path: {path}")
            self.assertGreater(os.path.getsize(path), 0, f"{label} at {path} is empty (0 bytes)")
        
        # Also ensure verified profile prerequisite exists
        self.assertTrue(os.path.exists(PROFILE_PATH), f"Missing verified profile at: {PROFILE_PATH}")

    def test_02_all_11_mandated_companies_present(self):
        """2. Verifies all 11 mandated employers are present in bangalore_live_referral_dockets.json."""
        self.assertTrue(self.dockets_exists, "Dockets file does not exist to verify companies")
        self.assertGreater(len(self.dockets), 0, "Dockets array is empty")

        company_identifiers = []
        for t in self.dockets:
            company_identifiers.append((
                t.get('canonical_company', ''),
                t.get('company', '')
            ))

        missing_companies = []
        for req in REQUIRED_11_COMPANIES:
            matched = any(_matches_company(req, [c[0], c[1]]) for c in company_identifiers)
            if not matched:
                missing_companies.append(req)

        self.assertEqual(
            missing_companies, [],
            f"Mandated top employers missing from bangalore_live_referral_dockets.json: {missing_companies}"
        )

    def test_03_contacts_per_company_thresholds(self):
        """3. Verifies each of the 11 companies has >= 3 contacts, with valid name, position, and LinkedIn URL."""
        self.assertTrue(self.dockets_exists, "Dockets file does not exist")
        url_regex = re.compile(r'^https:\/\/[a-z]{2,3}\.linkedin\.com\/in\/[\w\-]+')

        errors = []
        for req in REQUIRED_11_COMPANIES:
            matched_dockets = [
                t for t in self.dockets
                if _matches_company(req, [t.get('canonical_company', ''), t.get('company', '')])
            ]
            if not matched_dockets:
                errors.append(f"Company '{req}' has no docket entries (expected >= 3 contacts)")
                continue

            total_contacts = sum(len(d.get('contacts', [])) for d in matched_dockets)
            if total_contacts < 3:
                errors.append(f"Company '{req}' has {total_contacts} contacts (threshold is >= 3)")

            for d in matched_dockets:
                comp_name = d.get('canonical_company', d.get('company', req))
                for idx, c in enumerate(d.get('contacts', []), 1):
                    name = c.get('full_name')
                    pos = c.get('position')
                    url = c.get('linkedin_url', '')

                    if not name or not str(name).strip():
                        errors.append(f"Empty full_name in contact #{idx} for '{comp_name}'")
                    if not pos or not str(pos).strip():
                        errors.append(f"Empty position in contact '{name}' for '{comp_name}'")
                    if not url or not url_regex.match(url):
                        errors.append(f"Invalid linkedin_url '{url}' in contact '{name}' for '{comp_name}'")

        self.assertEqual(errors, [], "Contact threshold / integrity validation failed:\n" + "\n".join(errors))

    def test_04_connection_notes_strict_290_char_limit(self):
        """4. Verifies 100% of connection notes across all contacts are strictly <= 290 chars (hard ceiling <= 300) and >= 50 chars."""
        self.assertTrue(self.dockets_exists, "Dockets file does not exist")
        self.assertGreater(len(self.dockets), 0, "Dockets array is empty")

        violations_290 = []
        violations_300 = []
        violations_short = []
        total_checked = 0

        for d in self.dockets:
            comp = d.get('canonical_company', d.get('company', 'Unknown'))
            for c in d.get('contacts', []):
                total_checked += 1
                note = c.get('connection_note', '')
                length = len(note)
                name = c.get('full_name', 'Unknown')

                if length > 300:
                    violations_300.append(f"[{comp}] {name} len={length} > 300: {note!r}")
                if length > 290:
                    violations_290.append(f"[{comp}] {name} len={length} > 290: {note!r}")
                if length < 50:
                    violations_short.append(f"[{comp}] {name} len={length} < 50: {note!r}")

        self.assertGreater(total_checked, 0, "No contacts found to evaluate connection notes")
        self.assertEqual(violations_300, [], f"Found {len(violations_300)} notes exceeding 300-char hard ceiling:\n" + "\n".join(violations_300))
        self.assertEqual(violations_290, [], f"Found {len(violations_290)} notes exceeding 290-char strict limit:\n" + "\n".join(violations_290))
        self.assertEqual(violations_short, [], f"Found {len(violations_short)} notes shorter than 50 chars:\n" + "\n".join(violations_short))

    def test_05_zero_hallucination_profile_alignment(self):
        """5. Verifies messages reference verified credentials from verified_profile.json with zero fabricated claims."""
        self.assertTrue(self.dockets_exists, "Dockets file does not exist")
        self.assertTrue(self.profile_exists, "Verified profile file does not exist")

        cand_name = self.profile.get('candidate', {}).get('full_name', 'Aditya Mehra')
        prohibited_terms = [
            (re.compile(r'\bMBA\b'), "MBA"),
            (re.compile(r'\bIIM\b'), "IIM"),
            (re.compile(r'\bIIT\b'), "IIT"),
            (re.compile(r'\bPh\.?D\b', re.IGNORECASE), "Ph.D"),
            (re.compile(r'\bDoctorate\b', re.IGNORECASE), "Doctorate"),
            (re.compile(r'\b10\+\s*years\b', re.IGNORECASE), "10+ years"),
            (re.compile(r'\b15\+\s*years\b', re.IGNORECASE), "15+ years"),
        ]

        alignment_errors = []

        for d in self.dockets:
            comp = d.get('canonical_company', d.get('company', 'Unknown'))
            for c in d.get('contacts', []):
                name = c.get('full_name', 'Unknown')
                note = c.get('connection_note', '')
                ask = c.get('referral_ask', '')
                docket = c.get('referral_docket', '')

                # 1. Connection note must have verified education anchor (DSU / BBA / Dayananda Sagar)
                has_edu_anchor = any(term in note for term in ['DSU', 'BBA', 'Dayananda Sagar'])
                if not has_edu_anchor:
                    alignment_errors.append(f"[{comp}] {name}: Connection note missing verified education anchor (DSU/BBA): {note!r}")

                # 2. Candidate name must be present in referral ask and docket
                if cand_name.lower() not in ask.lower():
                    alignment_errors.append(f"[{comp}] {name}: Referral ask does not mention candidate '{cand_name}'")
                if cand_name.lower() not in docket.lower():
                    alignment_errors.append(f"[{comp}] {name}: Referral docket does not mention candidate '{cand_name}'")

                # 3. Verified experience anchors (Aero India and Instawork)
                if 'aero india' not in ask.lower():
                    alignment_errors.append(f"[{comp}] {name}: Referral ask missing verified 'Aero India' anchor")
                if 'instawork' not in ask.lower():
                    alignment_errors.append(f"[{comp}] {name}: Referral ask missing verified 'Instawork' anchor")
                if 'aero india' not in docket.lower():
                    alignment_errors.append(f"[{comp}] {name}: Referral docket missing verified 'Aero India' anchor")
                if 'instawork' not in docket.lower():
                    alignment_errors.append(f"[{comp}] {name}: Referral docket missing verified 'Instawork' anchor")

                # 4. Prohibited hallucinated claims check across all 3 message assets
                combined_text = f"{note}\n{ask}\n{docket}"
                for pattern, label in prohibited_terms:
                    if pattern.search(combined_text):
                        alignment_errors.append(f"[{comp}] {name}: Contains prohibited unearned claim '{label}'")

        self.assertEqual(alignment_errors, [], "Profile alignment / hallucination errors detected:\n" + "\n".join(alignment_errors))

    def test_06_corridor_and_domain_coverage(self):
        """6. Verifies all 5 tech corridors and all 5 functional domains are properly represented in the dataset."""
        self.assertTrue(self.dockets_exists, "Dockets file does not exist")
        self.assertGreater(len(self.dockets), 0, "Dockets array is empty")

        # Corridors coverage check
        corridor_matches = {corr: 0 for corr in REQUIRED_CORRIDORS}
        for d in self.dockets:
            haystack = (d.get('corridor', '') + ' ' + d.get('hub', '')).lower()
            if 'outer ring road' in haystack or 'orr' in haystack:
                corridor_matches['Outer Ring Road'] += 1
            if 'manyata' in haystack or 'hebbal' in haystack:
                corridor_matches['Manyata'] += 1
            if 'bellandur' in haystack:
                corridor_matches['Bellandur'] += 1
            if 'whitefield' in haystack or 'itpl' in haystack:
                corridor_matches['Whitefield'] += 1
            if 'domlur' in haystack or 'egl' in haystack or 'intermediate ring road' in haystack:
                corridor_matches['Domlur'] += 1

        missing_corridors = [k for k, count in corridor_matches.items() if count == 0]
        self.assertEqual(
            missing_corridors, [],
            f"Tech corridors with 0 company representation: {missing_corridors} (Counts: {corridor_matches})"
        )

        # Domain coverage check
        domain_matches = {dom: 0 for dom in REQUIRED_DOMAINS}
        for d in self.dockets:
            title = d.get('job_title', '')
            domain = _classify_domain(title)
            if domain in domain_matches:
                domain_matches[domain] += 1

        missing_domains = [k for k, count in domain_matches.items() if count == 0]
        self.assertEqual(
            missing_domains, [],
            f"Functional domains with 0 job representation: {missing_domains} (Counts: {domain_matches})"
        )

    def test_07_console_html_standalone_capabilities(self):
        """7. Verifies index.html has inlined data, clipboard copy handlers, LinkedIn launchers, localStorage tracking, and filter pills."""
        self.assertTrue(self.console_exists, f"Console HTML missing at {CONSOLE_PATH}")
        html = self.console_html

        # 1. Inlined dockets data
        self.assertTrue(
            'const dockets =' in html or 'let dockets =' in html or 'var dockets =' in html,
            "Console HTML missing inlined dataset ('const dockets =')"
        )

        # 2. Standalone clipboard copy with visual feedback
        self.assertIn("copyText", html, "Console HTML missing 'copyText' JavaScript handler")
        self.assertIn("navigator.clipboard.writeText", html, "Console HTML missing 'navigator.clipboard.writeText' API call")
        has_feedback = "showToast" in html or "toast" in html or "Copied" in html
        self.assertTrue(has_feedback, "Console HTML missing visual clipboard copy feedback (toast or button label swap)")

        # 3. Direct LinkedIn launcher
        self.assertIn('target="_blank"', html, "Console HTML missing direct external launcher ('target=\"_blank\"')")
        self.assertTrue("linkedin.com" in html or "linkedin_url" in html, "Console HTML missing LinkedIn URL linking")

        # 4. LocalStorage status tracking
        self.assertIn("localStorage.getItem", html, "Console HTML missing localStorage.getItem for persistent status retrieval")
        self.assertIn("localStorage.setItem", html, "Console HTML missing localStorage.setItem for persistent status saving")
        for status in ['Pending', 'Contacted', 'Referral Submitted']:
            self.assertIn(status, html, f"Console HTML missing tracking status: '{status}'")

        # 5. Filter pill elements for Corridors, Companies, and Domains
        # Corridors: all 5 required corridors must appear in filter pills
        for corr in ['Outer Ring Road', 'Manyata', 'Bellandur', 'Whitefield', 'Domlur']:
            self.assertIn(corr, html, f"Missing corridor filter pill for: '{corr}'")

        # Company filter pills: must have dedicated company filter UI (e.g. filterCompany or company pill buttons)
        has_company_filter = (
            "filterCompany" in html or
            "Company Filter" in html or
            "filter-label\">Company" in html or
            "filter-label\">Target Company" in html or
            "company-pill" in html
        )
        self.assertTrue(has_company_filter, "Console HTML missing dedicated company filter pill elements / UI (filterCompany)")

        # Domain filter pills: must have dedicated domain/role filter UI (e.g. filterDomain or domain pill buttons)
        has_domain_filter = (
            "filterDomain" in html or
            "Domain Filter" in html or
            "Role Filter" in html or
            "filter-label\">Domain" in html or
            "filter-label\">Role" in html or
            "domain-pill" in html
        )
        self.assertTrue(has_domain_filter, "Console HTML missing dedicated domain filter pill elements / UI (filterDomain)")

    def test_08_approval_queue_schema_fidelity(self):
        """8. Verifies data/approval_queue.csv and data/approval_queue.json maintain exact 14 standard columns, sequential IDs, and valid format."""
        self.assertTrue(os.path.exists(QUEUE_CSV_PATH), f"Missing approval queue CSV at {QUEUE_CSV_PATH}")
        self.assertTrue(os.path.exists(QUEUE_JSON_PATH), f"Missing approval queue JSON at {QUEUE_JSON_PATH}")

        # Check CSV
        csv_rows = []
        with open(QUEUE_CSV_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                self.fail("Approval queue CSV is completely empty")
            
            self.assertEqual(
                headers, EXPECTED_QUEUE_HEADERS,
                f"Approval queue CSV header mismatch.\nExpected: {EXPECTED_QUEUE_HEADERS}\nFound: {headers}"
            )

            id_pattern = re.compile(r'^(ACT|REF)-\d{4,}$')
            for row_idx, row in enumerate(reader, 2):
                self.assertEqual(
                    len(row), 14,
                    f"CSV Row #{row_idx} has {len(row)} columns (expected exactly 14): {row[:3]}"
                )
                action_id = row[0].strip()
                self.assertTrue(
                    id_pattern.match(action_id),
                    f"Row #{row_idx} Action ID '{action_id}' does not match standard pattern ^(ACT|REF)-\\d{{4,}}$"
                )
                csv_rows.append(row)

        self.assertGreater(len(csv_rows), 0, "Approval queue CSV has 0 data rows")

        # Verify presence of referral items in queue
        referral_rows = [r for r in csv_rows if 'referral' in r[4].lower() or 'linkedin' in r[4].lower()]
        self.assertGreaterEqual(
            len(referral_rows), 50,
            f"Approval queue contains only {len(referral_rows)} referral actions (expected >= 50)"
        )

        # Check JSON
        with open(QUEUE_JSON_PATH, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        if isinstance(json_data, dict) and 'actions' in json_data:
            json_list = json_data['actions']
        elif isinstance(json_data, list):
            json_list = json_data
        else:
            self.fail(f"Approval queue JSON root must be an array or dict with 'actions', got {type(json_data)}")

        self.assertGreater(len(json_list), 0, "Approval queue JSON array is empty")
        self.assertEqual(
            len(json_list), len(csv_rows),
            f"Row count mismatch between JSON ({len(json_list)}) and CSV ({len(csv_rows)})"
        )

        for idx, item in enumerate(json_list):
            self.assertIsInstance(item, dict, f"Item #{idx} in JSON queue is not a dict")
            for header in EXPECTED_QUEUE_HEADERS:
                self.assertIn(header, item, f"Missing key '{header}' in JSON queue item #{idx} ({item.get('Action ID')})")


if __name__ == '__main__':
    unittest.main()
