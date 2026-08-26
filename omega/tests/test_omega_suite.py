#!/usr/bin/env python
# ==============================================================================
# OMEGA EXTREME COMPREHENSIVE VERIFICATION TEST SUITE
# ==============================================================================
import os, sys, unittest, time, json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORE_DIR = os.path.join(BASE_DIR, "core")
FACT_DIR = os.path.join(BASE_DIR, "factories")

sys.path.insert(0, CORE_DIR)
sys.path.insert(0, FACT_DIR)

from database import OmegaDB
from control_plane import OmegaControlPlane
from executive_council import ExecutiveCouncil
from debate_engine import MultiAgentDebateEngine
from memory import OmegaMemory
from knowledge_graph import OmegaKnowledgeGraph
from security import OmegaSecurityCenter
from observability import OmegaObservabilityCenter
from orchestrator import OmegaMasterOrchestrator

from software_factory import OmegaSoftwareFactory
from business_factory import OmegaBusinessFactory
from research_engine import OmegaResearchEngine
from simulation_lab import OmegaSimulationLab

class TestOmegaEcosystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = OmegaDB()
        cls.cp = OmegaControlPlane(cls.db)
        cls.council = ExecutiveCouncil()
        cls.debate = MultiAgentDebateEngine()
        cls.mem = OmegaMemory(cls.db)
        cls.kg = OmegaKnowledgeGraph()
        cls.sec = OmegaSecurityCenter(cls.db)
        cls.obs = OmegaObservabilityCenter(cls.db)
        cls.orch = OmegaMasterOrchestrator(cls.db)
        cls.sw_fact = OmegaSoftwareFactory()
        cls.biz_fact = OmegaBusinessFactory()
        cls.res_eng = OmegaResearchEngine()
        cls.sim_lab = OmegaSimulationLab()

    def test_01_omega_db_and_tables(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            table_names = [r[0] for r in tables]
            for req in ["missions", "tasks", "agents", "memories", "audit_logs", "telemetry"]:
                self.assertIn(req, table_names)

    def test_02_control_plane_state(self):
        state = self.cp.get_system_state()
        self.assertEqual(state["system_status"], "ONLINE & OPERATIONAL")

    def test_03_executive_council_review(self):
        review = self.council.convene_board_review({"title": "Deploy Omega Flagship Factory"})
        self.assertEqual(review["consensus"], "APPROVED_FOR_EXECUTION")

    def test_04_multi_agent_debate(self):
        res = self.debate.debate_decision("Database Architecture", "SQLite WAL Engine")
        self.assertEqual(len(res["perspectives"]), 3)
        self.assertIn("consensus_decision", res["synthesis"])

    def test_05_10_layer_memory(self):
        mem_id = self.mem.store("DECISION", "OMEGA_CORE", "TEST_KEY", {"action": "Adopt Zero-Trust Security"})
        self.assertTrue(mem_id.startswith("MEM-"))
        records = self.mem.retrieve(layer="DECISION", key_tag="TEST_KEY")
        self.assertGreaterEqual(len(records), 1)

    def test_06_knowledge_graph(self):
        self.kg.add_node("NODE:OMEGA", "System", {"name": "Omega Control Plane"})
        self.kg.add_node("NODE:CEO", "Agent", {"name": "Omega CEO"})
        self.kg.add_edge("NODE:CEO", "NODE:OMEGA", "MANAGES")
        graph = self.kg.export_graph()
        self.assertGreaterEqual(len(graph["nodes"]), 2)
        self.assertGreaterEqual(len(graph["edges"]), 1)

    def test_07_security_and_approval_gate(self):
        res_safe = self.sec.evaluate_action_permission("OMEGA-ENG", "WRITE_LOCAL_CODE", 2)
        self.assertEqual(res_safe["status"], "APPROVED_BY_POLICY")
        res_crit = self.sec.evaluate_action_permission("OMEGA-CEO", "DISPATCH_INMAIL", 5)
        self.assertEqual(res_crit["status"], "PENDING_APPROVAL")
        self.assertTrue(res_crit["requires_human_approval"])

    def test_08_observability_and_health(self):
        self.obs.record_telemetry("TSK-OMEGA-TEST", "OMEGA-CTO", 0.75, tokens=300)
        health = self.obs.calculate_health_score()
        self.assertGreaterEqual(health["omega_health_score"], 90.0)

    def test_09_master_orchestrator_cycle(self):
        m_result = self.orch.execute_mission("Autonomous Enterprise Bootstrap", "Initialize all Omega subsystems")
        self.assertEqual(m_result["status"], "COMPLETED")
        self.assertTrue(m_result["mission_id"].startswith("MSN-"))

    def test_10_specialized_factories(self):
        # Software Factory
        spec = self.sw_fact.build_software_package({"name": "Omega SaaS"})
        self.assertEqual(spec["deployment_status"], "READY_FOR_DEPLOYMENT")

        # Business Factory
        econ = self.biz_fact.model_unit_economics("B2B Event Platform", 250000, 75000, 20)
        self.assertEqual(econ["gross_margin_percentage"], 70.0)

        # Research Engine
        res_eval = self.res_eng.evaluate_hypothesis("1st-degree referrals convert 4x better than cold ATS", [{"confidence": 0.95}, {"confidence": 0.90}])
        self.assertEqual(res_eval["evidence_grade"], "SOURCE-BACKED")

        # Simulation Lab
        sim_res = self.sim_lab.run_stress_scenarios("Monthly Active Pipeline Jobs", 61)
        self.assertIn("EXTREME_STRESS_CASE", sim_res["scenarios"])

if __name__ == "__main__":
    unittest.main()
