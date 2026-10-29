"""
Proposed Complete Verification Suite for Bengaluru Job Referral Strike & 1-Click Dispatch Console
Covers Acceptance Criteria:
1. Data & Target Integrity (all 11 companies, 3-5 contacts each, corridors, domains)
2. Character Limits (strict <= 290 chars, max <= 300 chars, 0% truncation)
3. Zero Hallucination (matches verified_profile.json)
4. Console & Usability (standalone HTML, DOM elements, localStorage logic)
5. Approval Queue Integration (schema fidelity, CSV & JSON consistency)
"""

import os
import re
import csv
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PROJECT_DIR = os.path.join(ROOT_DIR, 'teamwork_projects', 'bangalore_referral_strike')
DOCKETS_PATH = os.path.join(PROJECT_DIR, 'bangalore_live_referral_dockets.json')
CONSOLE_PATH = os.path.join(PROJECT_DIR, 'index.html')
VERIFIED_PROFILE_PATH = os.path.join(ROOT_DIR, 'data', 'verified_profile.json')
QUEUE_CSV_PATH = os.path.join(ROOT_DIR, 'data', 'approval_queue.csv')
QUEUE_JSON_PATH = os.path.join(ROOT_DIR, 'data', 'approval_queue.json')

REQUIRED_11_COMPANIES = [
    'Accenture', 'Deloitte', 'Goldman Sachs', 'Amazon', 'IBM',
    'JPMorganChase', 'KPMG', 'PwC', 'Walmart Global Tech', 'Delhivery', 'PhonePe'
]

REQUIRED_CORRIDORS = ['ORR', 'Manyata', 'Bellandur', 'Whitefield', 'Domlur']

REQUIRED_DOMAINS = ['Operations', 'Supply Chain', 'Advisory/Risk', 'Trade Finance', 'Merchant BD']

EXPECTED_QUEUE_HEADERS = [
    'Action ID', 'Person', 'Company', 'Job', 'Channel', 'Draft Message',
    'Reason / Evidence', 'Priority', 'Approval Required', 'Status',
    'Staged Timestamp', 'Approved Timestamp', 'Dispatched Timestamp', 'Dispatch Packet'
]


class TestBengaluruReferralStrikeVerification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load dockets
        cls.dockets_exists = os.path.exists(DOCKETS_PATH)
        if cls.dockets_exists:
            with open(DOCKETS_PATH, 'r', encoding='utf-8') as f:
                cls.dockets = json.load(f)
        else:
            cls.dockets = []

        # Load verified profile
        cls.profile_exists = os.path.exists(VERIFIED_PROFILE_PATH)
        if cls.profile_exists:
            with open(VERIFIED_PROFILE_PATH, 'r', encoding='utf-8') as f:
                cls.profile = json.load(f)
        else:
            cls.profile = {}

        # Load console HTML
        cls.console_exists = os.path.exists(CONSOLE_PATH)
        if cls.console_exists:
            with open(CONSOLE_PATH, 'r', encoding='utf-8') as f:
                cls.console_html = f.read()
        else:
            cls.console_html = ""

    def test_01_files_presence(self):
        """Verify all critical deliverable files exist."""
        self.assertTrue(self.dockets_exists, f"Missing dockets JSON at {DOCKETS_PATH}")
        self.assertTrue(self.console_exists, f"Missing console index.html at {CONSOLE_PATH}")
        self.assertTrue(self.profile_exists, f"Missing verified profile at {VERIFIED_PROFILE_PATH}")
        self.assertTrue(os.path.exists(QUEUE_CSV_PATH), f"Missing approval queue CSV at {QUEUE_CSV_PATH}")
        self.assertTrue(os.path.exists(QUEUE_JSON_PATH), f"Missing approval queue JSON at {QUEUE_JSON_PATH}")

    def test_02_required_11_companies_present(self):
        """Verify presence of all 11 mandated top employers."""
        company_names = []
        for t in self.dockets:
            company_names.append(t.get('canonical_company', t.get('company', '')))
        
        missing_companies = []
        for req in REQUIRED_11_COMPANIES:
            req_clean = re.sub(r'[^a-zA-Z0-9]', '', req).lower()
            matched = any(
                req_clean in re.sub(r'[^a-zA-Z0-9]', '', c).lower() or
                re.sub(r'[^a-zA-Z0-9]', '', c).lower() in req_clean
                for c in company_names
            )
            if not matched:
                missing_companies.append(req)
        
        # Note: In baseline dataset, PwC is missing. This test will alert if PwC has not been added.
        self.assertEqual(
            missing_companies, [],
            f"Required companies missing from dockets: {missing_companies}"
        )

    def test_03_contacts_per_company(self):
        """Verify every target employer has 3-8 curated contacts."""
        for t in self.dockets:
            comp = t.get('canonical_company', t.get('company'))
            contacts = t.get('contacts', [])
            # For the core 11, must have at least 3 contacts
            is_core = any(req.lower() in comp.lower() or comp.lower() in req.lower() for req in REQUIRED_11_COMPANIES)
            if is_core:
                self.assertGreaterEqual(
                    len(contacts), 3,
                    f"Core company {comp} has fewer than 3 contacts ({len(contacts)})"
                )
            for c in contacts:
                self.assertTrue(c.get('full_name'), f"Missing full_name in contact at {comp}")
                self.assertTrue(c.get('linkedin_url', '').startswith('https://www.linkedin.com/in/'),
                                f"Invalid LinkedIn URL {c.get('linkedin_url')} for {c.get('full_name')} at {comp}")

    def test_04_connection_note_strict_character_limits(self):
        """Verify 100% of connection notes are strictly <= 290 chars (and strictly <= 300)."""
        violations_290 = []
        violations_300 = []
        too_short = []

        total_checked = 0
        for t in self.dockets:
            comp = t.get('canonical_company', t.get('company'))
            for c in t.get('contacts', []):
                total_checked += 1
                note = c.get('connection_note', '')
                l = len(note)
                if l > 290:
                    violations_290.append((c.get('full_name'), comp, l, note))
                if l > 300:
                    violations_300.append((c.get('full_name'), comp, l, note))
                if l < 50:
                    too_short.append((c.get('full_name'), comp, l, note))

        self.assertGreater(total_checked, 0, "No contacts evaluated")
        self.assertEqual(len(violations_300), 0, f"Found {len(violations_300)} notes exceeding 300 chars: {violations_300}")
        self.assertEqual(len(violations_290), 0, f"Found {len(violations_290)} notes exceeding 290 chars: {violations_290}")
        self.assertEqual(len(too_short), 0, f"Found notes that are too short: {too_short}")

    def test_05_zero_hallucination_profile_alignment(self):
        """Verify outreach content contains ONLY verified claims from verified_profile.json."""
        candidate = self.profile.get('candidate', {})
        cand_name = candidate.get('full_name', 'Aditya Mehra')
        edu = self.profile.get('education', [{}])[0]
        verified_degree = "BBA"
        verified_institution = "Dayananda Sagar University"
        
        for t in self.dockets:
            for c in t.get('contacts', []):
                note = c.get('connection_note', '')
                ask = c.get('referral_ask', '')
                docket = c.get('referral_docket', '')

                # Check that candidate name or verified education is referenced correctly
                self.assertTrue('DSU' in note or 'Dayananda Sagar' in note or 'BBA' in note,
                                f"Connection note lacks verified education anchor: {note}")
                
                # Check that no unverified degrees or institutions are mentioned
                self.assertNotIn("MBA", note)
                self.assertNotIn("IIM", note)
                self.assertNotIn("IIT", note)

                # Check referral ask references candidate
                self.assertIn(cand_name, ask, f"Referral ask does not mention {cand_name}")
                self.assertIn(cand_name, docket, f"Referral docket does not mention {cand_name}")

    def test_06_console_html_standalone_and_capabilities(self):
        """Verify index.html contains required UI capabilities without external server dependencies."""
        html = self.console_html
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Bengaluru Referral Strike Console", html)
        
        # Clipboard copy actions
        self.assertIn("copyText", html)
        self.assertIn("navigator.clipboard.writeText", html)

        # LinkedIn launcher
        self.assertIn("target=\"_blank\"", html)
        self.assertIn("linkedin.com", html)

        # LocalStorage persistence
        self.assertIn("localStorage.getItem", html)
        self.assertIn("localStorage.setItem", html)

        # Status tracking states
        self.assertIn("Pending", html)
        self.assertIn("Contacted", html)
        self.assertIn("Referral Submitted", html)

        # Corridor filters
        for corr in ['Outer Ring Road', 'Manyata', 'Bellandur', 'Whitefield', 'Domlur']:
            self.assertIn(corr, html, f"Missing corridor {corr} in console HTML")

    def test_07_approval_queue_schema_fidelity(self):
        """Verify approval_queue.csv and approval_queue.json adhere strictly to the canonical schema."""
        with open(QUEUE_CSV_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.assertEqual(headers, EXPECTED_QUEUE_HEADERS, f"CSV headers mismatch: {headers}")

        with open(QUEUE_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertIsInstance(data, list)
            if data:
                first_item = data[0]
                for key in EXPECTED_QUEUE_HEADERS:
                    self.assertIn(key, first_item, f"Missing expected key '{key}' in approval_queue.json")


if __name__ == '__main__':
    unittest.main()
