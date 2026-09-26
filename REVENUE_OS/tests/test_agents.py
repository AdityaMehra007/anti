import unittest
from REVENUE_OS.agents.agent_mesh import AgentMesh
from REVENUE_OS.agents.permissions import PermissionEnforcer, PermissionDeniedError
from REVENUE_OS.agents.agent_evaluator import AgentEvaluator
from REVENUE_OS.compliance.charter import PermissionTier

class TestAgentMeshAndSecurity(unittest.TestCase):
    def setUp(self):
        self.mesh = AgentMesh()
        self.enforcer = PermissionEnforcer()
        self.evaluator = AgentEvaluator()

    def test_10_specialist_agents_registered(self):
        agents = self.mesh.list_agents()
        expected_roles = [
            "RevenueCommander",
            "MarketScout",
            "LeadResearcher",
            "SalesAssistant",
            "OfferArchitect",
            "ContentAgent",
            "CustomerSuccessAgent",
            "FinanceAgent",
            "CompetitorAgent",
            "AutomationAgent"
        ]
        self.assertEqual(len(agents), 10)
        for role in expected_roles:
            self.assertIn(role, agents, f"Agent {role} is missing from mesh.")

    def test_permission_enforcement_blocks_unauthorized_action(self):
        # MarketScout attempting to APPROVE a financial payout must fail
        with self.assertRaises(PermissionDeniedError):
            self.enforcer.enforce(
                agent_name="MarketScout",
                requested_tier=PermissionTier.APPROVE,
                action_context="Transfer funds to cloud provider"
            )
            
        # SalesAssistant DRAFTING an email is allowed
        self.assertTrue(
            self.enforcer.enforce(
                agent_name="SalesAssistant",
                requested_tier=PermissionTier.DRAFT,
                action_context="Draft cold email to prospect"
            )
        )

    def test_revenue_commander_daily_triage(self):
        commander = self.mesh.get_agent("RevenueCommander")
        triage = commander.run_daily_triage(
            revenue_yesterday_inr=0.0,
            revenue_month_inr=70000.0,
            pipeline_inr=245000.0,
            biggest_opportunity="Apex Dynamics Technologies - ₹35k/mo AI Pipeline Retainer",
            biggest_risk="Domain warmup speed limit"
        )
        self.assertIn("what_made_money", triage)
        self.assertIn("what_can_make_money", triage)
        self.assertIn("what_stopped_us", triage)
        self.assertIn("what_should_happen_next", triage)
        self.assertEqual(len(triage["top_3_actions"]), 3)

    def test_agent_evaluator(self):
        score = self.evaluator.evaluate_agent(
            agent_name="LeadResearcher",
            revenue_attributed_inr=35000.0,
            hours_saved=20.0,
            error_count=0,
            total_tasks=50,
            agent_cost_usd=2.50
        )
        self.assertGreater(score["roi_ratio"], 10.0)
        self.assertEqual(score["accuracy_pct"], 100.0)

if __name__ == "__main__":
    unittest.main()
