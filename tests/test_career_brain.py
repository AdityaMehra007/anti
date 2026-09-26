import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from career_brain import OmegaCareerBrain

class TestOmegaCareerBrain(unittest.TestCase):
    def setUp(self):
        self.brain = OmegaCareerBrain()

    def test_high_priority_business_operations_role(self):
        result = self.brain.score_opportunity(
            job_title='Risk & Business Operations Advisory Analyst',
            company_name='Deloitte US-India',
            location='Bengaluru, India',
            recruiter_count=5,
            job_description='Support risk governance, operational workflows, and client advisory reporting.'
        )
        self.assertGreaterEqual(result['overall_opportunity_score'], 80.0)
        self.assertFalse(result['is_sales_excluded'])
        self.assertEqual(result['sales_risk_score'], 0.0)
        self.assertIn('business_operations', result['explanation']['why'])
        self.assertEqual(result['recommendation'], 'PRIORITY_1_TARGET_APPLY_AND_INMAIL')

    def test_sales_exclusion_telecalling_and_sdr(self):
        result = self.brain.score_opportunity(
            job_title='Remote Sales Development Representative (SDR)',
            company_name='Outbound Corp',
            location='Bengaluru',
            job_description='Responsible for cold calling, aggressive lead generation, commission based quota.'
        )
        self.assertGreaterEqual(result['sales_risk_score'], 70.0)
        self.assertTrue(result['is_sales_excluded'])
        self.assertEqual(result['recommendation'], 'EXCLUDED_SALES_RISK')
        self.assertLess(result['overall_opportunity_score'], 50.0)

    def test_explainability_structure(self):
        result = self.brain.score_opportunity(
            job_title='Business Analyst',
            company_name='EY GDS',
            location='Bengaluru'
        )
        exp = result['explanation']
        self.assertIn('why', exp)
        self.assertIn('evidence', exp)
        self.assertIn('missing_requirements', exp)
        self.assertIn('risks', exp)
        self.assertIn('strongest_advantages', exp)
        self.assertIn('recommended_action', exp)

    def test_component_score_weights_sum_to_100(self):
        result = self.brain.score_opportunity(
            job_title='Business Operations Associate',
            company_name='Amazon',
            location='Bengaluru',
            salary_offered_inr=700000.0,
            recruiter_count=3
        )
        components = result['component_scores']
        self.assertIn('role_fit', components)
        self.assertIn('eligibility', components)
        self.assertIn('hiring_probability', components)
        self.assertIn('company_quality', components)
        self.assertIn('compensation', components)
        self.assertIn('learning', components)
        self.assertIn('ai_relevance', components)
        self.assertIn('career_capital', components)
        self.assertIn('growth', components)
        self.assertIn('location', components)
        # Sum of components equals the overall opportunity score for non-sales roles
        self.assertAlmostEqual(sum(components.values()), result['overall_opportunity_score'], places=1)

if __name__ == '__main__':
    unittest.main()
