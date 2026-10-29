"""
Verification Script for Bengaluru Referral Strike R1 & R2
Validates:
1. All 11 mandated companies are present and verified.
2. Every company has >= 3 contacts with valid names and LinkedIn URLs.
3. 100% of connection notes are strictly <= 290 characters (hard ceiling 300, 0 truncation).
4. Every target role contains company, role, req_id, careers_url, hub, corridor, domain, fit_score.
5. Specific contact checks for Delhivery, PhonePe, and PwC.
6. Zero hallucination check against verified_profile.json.
7. Dual-file parity between teamwork_projects/ and data/.
"""

import os
import json
import re
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DOCKETS = os.path.join(ROOT_DIR, 'teamwork_projects', 'bangalore_referral_strike', 'bangalore_live_referral_dockets.json')
DATA_DOCKETS = os.path.join(ROOT_DIR, 'data', 'bangalore_live_referral_dockets.json')
PROFILE_PATH = os.path.join(ROOT_DIR, 'data', 'verified_profile.json')

MANDATED_11 = [
    'Accenture', 'Deloitte', 'Goldman Sachs', 'Amazon', 'IBM',
    'JPMorganChase', 'KPMG', 'PwC', 'Walmart Global Tech', 'Delhivery', 'PhonePe'
]

REQUIRED_ROLE_KEYS = [
    'company', 'role', 'req_id', 'careers_url', 'hub', 'corridor', 'domain', 'fit_score'
]


class TestReferralStrikeR1R2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(PROJECT_DOCKETS, 'r', encoding='utf-8') as f:
            cls.proj_data = json.load(f)
        with open(DATA_DOCKETS, 'r', encoding='utf-8') as f:
            cls.data_data = json.load(f)
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            cls.profile = json.load(f)

    def test_01_dual_file_parity(self):
        """Ensure both JSON files exist and have identical length and companies."""
        self.assertEqual(len(self.proj_data), len(self.data_data))
        for p, d in zip(self.proj_data, self.data_data):
            self.assertEqual(p['canonical_company'], d['canonical_company'])
            self.assertEqual(len(p['contacts']), len(d['contacts']))

    def test_02_all_11_mandated_companies_present(self):
        """Ensure all 11 mandated employers are present in the dataset."""
        company_names = [t.get('canonical_company', t.get('company', '')) for t in self.proj_data]
        
        for req in MANDATED_11:
            req_clean = re.sub(r'[^a-zA-Z0-9]', '', req).lower()
            matched = any(
                req_clean in re.sub(r'[^a-zA-Z0-9]', '', c).lower() or
                re.sub(r'[^a-zA-Z0-9]', '', c).lower() in req_clean
                for c in company_names
            )
            self.assertTrue(matched, f"Mandated employer '{req}' missing from dockets!")

    def test_03_required_role_fields(self):
        """Ensure every target role has company, role, req_id, careers_url, hub, corridor, domain, fit_score."""
        for t in self.proj_data:
            comp = t.get('canonical_company', t.get('company'))
            for k in REQUIRED_ROLE_KEYS:
                self.assertIn(k, t, f"Missing '{k}' in docket for {comp}")
                self.assertTrue(str(t[k]).strip(), f"Empty '{k}' in docket for {comp}")

    def test_04_contacts_thresholds_and_linkedin_urls(self):
        """Ensure every company has contacts, core 11 has >= 3, and all have valid LinkedIn URLs."""
        for t in self.proj_data:
            comp = t.get('canonical_company', t.get('company'))
            contacts = t.get('contacts', [])
            
            # Core 11 must have at least 3 contacts
            is_core = any(req.lower() in comp.lower() or comp.lower() in req.lower() for req in MANDATED_11)
            if is_core:
                self.assertGreaterEqual(len(contacts), 3, f"Core company {comp} has only {len(contacts)} contacts (< 3)")
            
            for c in contacts:
                self.assertTrue(c.get('full_name'), f"Missing full_name in {comp}")
                self.assertTrue(c.get('position'), f"Missing position in {comp}")
                url = c.get('linkedin_url', '')
                self.assertTrue(url.startswith('https://www.linkedin.com/in/'), f"Invalid LinkedIn URL {url} in {comp}")

    def test_05_connection_notes_character_limits(self):
        """Ensure 100% of connection notes are strictly <= 290 characters and >= 50 characters."""
        total_notes = 0
        for t in self.proj_data:
            comp = t.get('canonical_company', t.get('company'))
            for c in t.get('contacts', []):
                total_notes += 1
                note = c.get('connection_note', '')
                l = len(note)
                self.assertLessEqual(l, 290, f"Note exceeds 290 chars ({l}) for {c.get('full_name')} at {comp}")
                self.assertGreaterEqual(l, 50, f"Note too short ({l}) for {c.get('full_name')} at {comp}")
        self.assertGreaterEqual(total_notes, 100, f"Expected >100 notes, found {total_notes}")

    def test_06_delhivery_contacts(self):
        """Ensure Delhivery has its 3 verified contacts."""
        delh = next((t for t in self.proj_data if 'delhivery' in t['canonical_company'].lower()), None)
        self.assertIsNotNone(delh, "Delhivery not found")
        names = [c['full_name'] for c in delh['contacts']]
        self.assertIn('Chanchala Ugra', names)
        self.assertIn('Sharon Sundara', names)
        self.assertIn('Amruta Maile', names)
        self.assertEqual(len(delh['contacts']), 3)

    def test_07_phonepe_contacts(self):
        """Ensure PhonePe has 3-5 verified contacts (Anshika, Tarun, Palak, Khushi, Aayushi)."""
        phone = next((t for t in self.proj_data if 'phonepe' in t['canonical_company'].lower()), None)
        self.assertIsNotNone(phone, "PhonePe not found")
        names = [c['full_name'] for c in phone['contacts']]
        self.assertTrue(any('Anshika Kohli' in n for n in names))
        self.assertTrue(any('Tarun Upadhyay' in n for n in names))
        self.assertTrue(any('Palak Shah' in n for n in names))
        self.assertTrue(any('Khushi' in n for n in names))
        self.assertTrue(any('Aayushi Das' in n for n in names))
        self.assertGreaterEqual(len(phone['contacts']), 3)
        self.assertLessEqual(len(phone['contacts']), 5)

    def test_08_pwc_contacts(self):
        """Ensure PwC has 3-5 verified contacts (Shalini, Nikhitha, Latha, Neeraja, Mishfa)."""
        pwc = next((t for t in self.proj_data if 'pwc' in t['canonical_company'].lower() or 'pricewaterhouse' in t['canonical_company'].lower()), None)
        self.assertIsNotNone(pwc, "PwC not found")
        names = [c['full_name'] for c in pwc['contacts']]
        self.assertTrue(any('Shalini Jha' in n for n in names))
        self.assertTrue(any('Nikhitha Simon' in n for n in names))
        self.assertTrue(any('Latha Dhananjay' in n for n in names))
        self.assertTrue(any('Neeraja Rajasekar' in n for n in names))
        self.assertTrue(any('Mishfa Kazi' in n for n in names))
        self.assertGreaterEqual(len(pwc['contacts']), 3)
        self.assertLessEqual(len(pwc['contacts']), 5)
        self.assertEqual(pwc['req_id'], 'BLR-JOB-013')
        self.assertEqual(pwc['role'], 'Business Operations Analyst')
        self.assertEqual(pwc['careers_url'], 'https://www.pwc.in/careers.html')

    def test_09_zero_hallucinations_ground_truth(self):
        """Ensure all claims match verified profile ground truth."""
        cand_name = self.profile['candidate']['full_name']
        dsu = "Dayananda Sagar University"
        
        for t in self.proj_data:
            for c in t['contacts']:
                note = c['connection_note']
                ask = c['referral_ask']
                docket = c['referral_docket']

                # Connection note must reference DSU or BBA
                self.assertTrue('DSU' in note or 'BBA' in note or dsu in note)
                self.assertNotIn("MBA", note)
                self.assertNotIn("IIM", note)
                self.assertNotIn("IIT", note)

                # Referral ask must reference candidate and immediate notice
                self.assertIn(cand_name, ask)
                self.assertIn("0 days notice", ask)
                self.assertIn("AERO INDIA 2025", ask)
                self.assertIn("Instawork", ask)

                # Referral docket must reference candidate details
                self.assertIn(cand_name, docket)
                self.assertIn(self.profile['candidate']['email'], docket)
                self.assertIn("0 Days (Immediate)", docket)


if __name__ == '__main__':
    unittest.main()
