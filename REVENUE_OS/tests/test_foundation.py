import unittest
import os
from pathlib import Path

class TestFoundation(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent

    def test_23_domain_directories_exist(self):
        expected_dirs = [
            "01_COMMAND_CENTER",
            "02_REVENUE",
            "03_MARKET",
            "04_LEADS",
            "05_CRM",
            "06_SALES",
            "07_OFFERS",
            "08_PRODUCTS",
            "09_CONTENT",
            "10_SEO",
            "11_PARTNERS",
            "12_AFFILIATES",
            "13_FINANCE",
            "14_AI_AGENTS",
            "15_AUTOMATIONS",
            "16_CUSTOMERS",
            "17_ANALYTICS",
            "18_RISK",
            "19_KNOWLEDGE",
            "20_FOUNDER_OS",
            "21_FUTURE",
            "22_COMPLIANCE",
            "23_SETTINGS",
        ]
        for dirname in expected_dirs:
            target_path = self.root_dir / dirname
            self.assertTrue(target_path.is_dir(), f"Missing directory: {dirname}")

    def test_config_loader(self):
        from REVENUE_OS.settings.config import get_config
        cfg = get_config()
        self.assertEqual(cfg.founder_name, "Aditya Mehra")
        self.assertEqual(cfg.base_country, "India")
        self.assertTrue(cfg.db_path.name.endswith(".db"))
        self.assertIn("INR", cfg.supported_currencies)
        self.assertIn("USD", cfg.supported_currencies)

    def test_compliance_charter(self):
        from REVENUE_OS.compliance.charter import (
            EthicalCharter,
            PermissionTier,
            SecurityViolationError,
        )
        charter = EthicalCharter()
        # Autonomous financial spend must be rejected without human approval
        self.assertFalse(charter.is_autonomous_action_allowed(PermissionTier.APPROVE))
        self.assertTrue(charter.is_autonomous_action_allowed(PermissionTier.DRAFT))
        
        # Test claim validation
        with self.assertRaises(SecurityViolationError):
            charter.validate_claim("We guarantee 100% passive income in 7 days!")

if __name__ == "__main__":
    unittest.main()
