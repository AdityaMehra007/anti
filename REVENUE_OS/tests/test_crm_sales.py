import unittest
from pathlib import Path
from REVENUE_OS.database.db import DatabaseManager
from REVENUE_OS.leads.lead_engine import LeadEngine
from REVENUE_OS.crm.crm_pipeline import CRMPipeline
from REVENUE_OS.sales.sales_assistant import SalesAssistant

class TestCRMandSales(unittest.TestCase):
    def setUp(self):
        self.test_db_path = Path("e:/anti/REVENUE_OS/database/test_crm_sales.db")
        if self.test_db_path.exists():
            self.test_db_path.unlink()
        self.db = DatabaseManager(db_path=self.test_db_path)
        self.db.initialize()
        
        self.lead_engine = LeadEngine(db=self.db)
        self.crm = CRMPipeline(db=self.db)
        self.sales = SalesAssistant(db=self.db)

    def tearDown(self):
        self.db.close()
        if self.test_db_path.exists():
            try:
                self.test_db_path.unlink()
            except Exception:
                pass

    def test_ethical_lead_ingestion_and_scoring(self):
        lead_id = self.lead_engine.ingest_lead({
            "company": "Apex Dynamics Technologies",
            "website": "https://apexdynamics.example.com",
            "industry": "B2B SaaS / FinTech",
            "geography": "Bengaluru, India",
            "company_size": "25-50",
            "contact_name": "Rohan Deshmukh",
            "contact_role": "VP Sales & Growth",
            "contact_email": "rohan@apexdynamics.example.com",
            "buying_trigger": "Closed $2M Seed round, hiring 3 SDRs",
            "source": "LinkedIn Verified Company Job Postings",
            "icp_fit_score": 9.5,
            "pain_score": 9.0,
            "trigger_score": 9.5,
            "ability_to_pay_score": 9.0,
            "urgency_score": 8.5,
            "reachability_score": 9.0,
        })
        self.assertIsNotNone(lead_id)
        
        lead = self.lead_engine.get_lead(lead_id)
        self.assertGreaterEqual(lead["total_lead_score"], 85.0)
        self.assertEqual(lead["status"], "QUALIFIED")

    def test_crm_deal_progression_and_pipeline_weight(self):
        # Ingest lead first
        lead_id = self.lead_engine.ingest_lead({
            "company": "ScalePulse Cloud",
            "industry": "DevOps / Cloud Infrastructure",
            "geography": "Bengaluru, India",
            "contact_name": "Priya Sharma",
            "contact_role": "Founder & CEO",
            "source": "Warm Alumni Referral",
            "icp_fit_score": 9.0,
            "pain_score": 8.5,
            "trigger_score": 9.0,
            "ability_to_pay_score": 8.5,
            "urgency_score": 8.0,
            "reachability_score": 9.0,
        })
        
        deal_id = self.crm.create_deal(
            lead_id=lead_id,
            deal_name="ScalePulse AI Pipeline Retainer",
            deal_value_inr=35000.0,
            stage="DISCOVERY"
        )
        self.assertIsNotNone(deal_id)
        
        # Check initial weighted value (DISCOVERY has 25% probability)
        deal = self.crm.get_deal(deal_id)
        self.assertEqual(deal["stage"], "DISCOVERY")
        self.assertAlmostEqual(deal["win_probability"], 0.25)
        self.assertAlmostEqual(deal["expected_revenue_inr"], 35000.0 * 0.25)
        
        # Advance to PROPOSAL (60% probability)
        self.crm.advance_stage(deal_id, new_stage="PROPOSAL")
        updated_deal = self.crm.get_deal(deal_id)
        self.assertEqual(updated_deal["stage"], "PROPOSAL")
        self.assertAlmostEqual(updated_deal["win_probability"], 0.60)
        self.assertAlmostEqual(updated_deal["expected_revenue_inr"], 35000.0 * 0.60)
        
        # Summary pipeline metric
        pipeline_stats = self.crm.get_pipeline_summary()
        self.assertGreater(pipeline_stats["total_pipeline_value_inr"], 0)
        self.assertGreater(pipeline_stats["weighted_pipeline_value_inr"], 0)

    def test_sales_assistant_generates_compliant_outreach(self):
        lead = {
            "company": "Nexus Logistics",
            "contact_name": "Vikram Sethi",
            "contact_role": "Head of BD",
            "buying_trigger": "Expanding cross-border shipping across UAE & Singapore",
            "industry": "Global Trade Logistics"
        }
        draft = self.sales.draft_personalized_outreach(lead)
        self.assertIn("Vikram", draft["body"])
        self.assertIn("UAE", draft["body"])
        self.assertIn("opt out", draft["body"].lower()) # Must comply with Ethical Charter
        self.assertFalse(draft["requires_approval"]) # Drafting alone is not sending

if __name__ == "__main__":
    unittest.main()
