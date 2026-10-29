import re
import json
import unittest

CONSOLE_PATH = r"e:\anti\teamwork_projects\bangalore_referral_strike\index.html"
DOCKETS_PATH = r"e:\anti\teamwork_projects\bangalore_referral_strike\bangalore_live_referral_dockets.json"

class TestConsoleComprehensive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CONSOLE_PATH, "r", encoding="utf-8") as f:
            cls.html = f.read()
        with open(DOCKETS_PATH, "r", encoding="utf-8") as f:
            cls.dockets = json.load(f)

    def test_01_inlined_data_exact_sync(self):
        """Requirement 1: inlined const dockets = [...] synchronized with json file."""
        self.assertIn("const dockets =", self.html)
        start = self.html.find("const dockets = ") + len("const dockets = ")
        end = self.html.find(";\n", start)
        if end == -1:
            end = self.html.find(";\r\n", start)
        inlined = json.loads(self.html[start:end])
        self.assertEqual(len(inlined), 46, "Expected 46 companies in inlined dockets")
        total_contacts = sum(len(x.get("contacts", [])) for x in inlined)
        self.assertEqual(total_contacts, 193, "Expected 193 contacts in inlined dockets")
        self.assertEqual(inlined, self.dockets, "Inlined dockets must match json file exactly")
        
        # Verify PwC BLR-JOB-013 is in dataset
        pwc = [x for x in inlined if x.get("req_id") == "BLR-JOB-013"]
        self.assertEqual(len(pwc), 1, "PwC BLR-JOB-013 missing from inlined dockets")
        self.assertGreaterEqual(len(pwc[0].get("contacts", [])), 3)

    def test_02_all_11_company_filter_pills(self):
        """Requirement 2: Dedicated company filter pill buttons for all 11 mandated employers."""
        expected_buttons = [
            'All Companies', 'Accenture', 'Deloitte', 'Goldman Sachs', 'Amazon', 'IBM',
            'JPMorganChase', 'KPMG', 'PwC', 'Walmart Global Tech', 'Delhivery', 'PhonePe'
        ]
        for btn in expected_buttons:
            self.assertIn(btn, self.html, f"Missing company filter pill: {btn}")
        self.assertIn("filterCompany", self.html)
        self.assertIn("company-pill", self.html)

    def test_03_corridor_filter_pills(self):
        """Requirement 3: Dedicated corridor filter pills."""
        expected_corridors = [
            'All Corridors', 'Outer Ring Road', 'Bellandur', 'Manyata', 'Whitefield', 'Domlur'
        ]
        for corr in expected_corridors:
            self.assertIn(corr, self.html, f"Missing corridor filter pill: {corr}")
        self.assertIn("filterCorridor", self.html)
        self.assertIn("corridor-pill", self.html)

    def test_04_domain_filter_pills(self):
        """Requirement 4: Dedicated domain filter pills."""
        expected_domains = [
            'All Domains', 'Operations', 'Supply Chain', 'Advisory/Risk', 'Trade Finance', 'Merchant BD'
        ]
        for dom in expected_domains:
            self.assertIn(dom, self.html, f"Missing domain filter pill: {dom}")
        self.assertIn("filterDomain", self.html)
        self.assertIn("domain-pill", self.html)

    def test_05_status_filter_pills(self):
        """Requirement 5: Dedicated status filter pills."""
        expected_statuses = ['All', 'Pending', 'Contacted', 'Referral Submitted']
        for s in expected_statuses:
            self.assertIn(s, self.html, f"Missing status filter pill: {s}")
        self.assertIn("filterStatus", self.html)
        self.assertIn("status-pill", self.html)

    def test_06_dynamic_metrics_cards(self):
        """Requirement 6: Dynamic metrics cards."""
        self.assertIn('id="totalCompanies"', self.html)
        self.assertIn('id="totalContacts"', self.html)
        self.assertIn('id="contactedCount"', self.html)
        self.assertIn('id="referredCount"', self.html)
        self.assertIn('Target Companies', self.html)
        self.assertIn('Curated Contacts', self.html)
        self.assertIn('Contacted Today', self.html)
        self.assertIn('Referrals Logged', self.html)

    def test_07_clipboard_copy_actions(self):
        """Requirement 7: 1-click clipboard copy actions with dual feedback and fallback."""
        self.assertIn("Copy 300c Note", self.html)
        self.assertIn("Copy Referral Ask", self.html)
        self.assertIn("Copy Docket", self.html)
        self.assertIn("copyText", self.html)
        self.assertIn("navigator.clipboard.writeText", self.html)
        self.assertIn("document.execCommand", self.html)
        self.assertIn("Copied! ✓", self.html)
        self.assertIn("showToast", self.html)
        self.assertIn("1200", self.html)

    def test_08_linkedin_launcher(self):
        """Requirement 8: 1-click external LinkedIn launcher."""
        self.assertIn("Open LinkedIn ↗", self.html)
        self.assertIn('target="_blank"', self.html)
        self.assertIn("contact.linkedin_url", self.html)

    def test_09_localstorage_persistence(self):
        """Requirement 9: Safe storage wrapper with blr_referral_status_ prefix."""
        self.assertIn("localStorage.getItem", self.html)
        self.assertIn("localStorage.setItem", self.html)
        self.assertIn("window.__fallbackStore", self.html)
        self.assertIn("blr_referral_status_", self.html)

    def test_10_multidimensional_filtering(self):
        """Requirement 10: Multi-dimensional intersection filtering."""
        self.assertIn("matchesCorridor", self.html)
        self.assertIn("matchesCompany", self.html)
        self.assertIn("matchesDomain", self.html)
        self.assertIn("activeStatus", self.html)
        self.assertIn("searchTerm", self.html)
        self.assertIn("targetsContainer", self.html)

if __name__ == "__main__":
    unittest.main()
