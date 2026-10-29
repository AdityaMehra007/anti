"""
Automated Test Suite for Bengaluru Live Job Referral Strike System
"""

import os
import json
import csv
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, 'data', 'bangalore_live_referral_dockets.json')
QUEUE_CSV = os.path.join(ROOT_DIR, 'data', 'approval_queue.csv')
QUEUE_JSON = os.path.join(ROOT_DIR, 'data', 'approval_queue.json')
CONSOLE_HTML = os.path.join(ROOT_DIR, 'BANGALORE_LIVE_REFERRAL_CONSOLE.html')

class TestBangaloreReferralStrike(unittest.TestCase):

    def setUp(self):
        self.assertTrue(os.path.exists(DATA_PATH), f"Dockets file not found at {DATA_PATH}")
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def test_target_companies_count(self):
        """Ensure we have at least 20 target employers in Bangalore."""
        self.assertGreaterEqual(len(self.data), 20)

    def test_contacts_presence(self):
        """Ensure total contacts are > 100."""
        total_contacts = sum(len(t['contacts']) for t in self.data)
        self.assertGreaterEqual(total_contacts, 100)

    def test_connection_notes_length(self):
        """Verify strict LinkedIn connection note length constraint (<= 290 chars)."""
        for t in self.data:
            for c in t['contacts']:
                note = c['connection_note']
                self.assertLessEqual(
                    len(note), 290,
                    f"Connection note exceeds 290 chars for {c['full_name']} at {t['company']}: len={len(note)}"
                )
                self.assertGreater(len(note), 50, f"Note too short for {c['full_name']}")

    def test_contact_fields_integrity(self):
        """Verify required fields exist and are non-empty."""
        for t in self.data:
            self.assertTrue(t['canonical_company'], "Missing company name")
            self.assertTrue(t['job_title'], "Missing job title")
            self.assertTrue(t['job_url'], "Missing job URL")
            self.assertTrue(t['corridor'], "Missing corridor")
            
            for c in t['contacts']:
                self.assertTrue(c['full_name'], "Missing contact name")
                self.assertTrue(c['linkedin_url'].startswith('http'), f"Invalid LinkedIn URL: {c['linkedin_url']}")
                self.assertTrue(c['referral_ask'], "Missing referral ask message")
                self.assertTrue(c['referral_docket'], "Missing referral docket")

    def test_approval_queue_sync(self):
        """Verify approval queue contains synced referral items."""
        self.assertTrue(os.path.exists(QUEUE_CSV), "Missing approval_queue.csv")
        self.assertTrue(os.path.exists(QUEUE_JSON), "Missing approval_queue.json")
        
        with open(QUEUE_CSV, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            referral_items = [r for r in reader if 'LinkedIn Employee Referral' in r.get('Channel', '')]
            self.assertGreaterEqual(len(referral_items), 50, "Fewer than 50 referral items in approval queue")

    def test_html_consoles_exist(self):
        """Verify the HTML consoles exist and contain data."""
        self.assertTrue(os.path.exists(CONSOLE_HTML), "Missing root HTML console")
        project_html = os.path.join(ROOT_DIR, 'teamwork_projects', 'bangalore_referral_strike', 'index.html')
        self.assertTrue(os.path.exists(project_html), "Missing project index.html")
        
        with open(CONSOLE_HTML, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Bengaluru Referral Strike Console", content)
            self.assertIn("Aditya Mehra", content)
            self.assertIn("copyText", content)

if __name__ == '__main__':
    unittest.main()
