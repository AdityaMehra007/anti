#!/usr/bin/env python
# ==============================================================================
# SOVEREIGN COMPREHENSIVE 5-TIER VERIFICATION TEST SUITE
# ==============================================================================
import os, sys, unittest, time, json

# Setup paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORE_DIR = os.path.join(BASE_DIR, "core")
APPS_DIR = os.path.join(BASE_DIR, "apps")

sys.path.insert(0, CORE_DIR)
sys.path.insert(0, os.path.join(APPS_DIR, "game_studio"))
sys.path.insert(0, os.path.join(APPS_DIR, "memory_os"))
sys.path.insert(0, os.path.join(APPS_DIR, "agentic_seo"))
sys.path.insert(0, os.path.join(APPS_DIR, "secure_platform"))
sys.path.insert(0, os.path.join(APPS_DIR, "crm_business_os"))
sys.path.insert(0, os.path.join(APPS_DIR, "education_platform"))
sys.path.insert(0, os.path.join(APPS_DIR, "media_factory"))
sys.path.insert(0, os.path.join(APPS_DIR, "dev_discovery"))
sys.path.insert(0, os.path.join(APPS_DIR, "skills_marketplace"))
sys.path.insert(0, os.path.join(APPS_DIR, "personal_os"))
sys.path.insert(0, os.path.join(APPS_DIR, "job_intelligence"))
sys.path.insert(0, os.path.join(APPS_DIR, "business_intel"))
sys.path.insert(0, os.path.join(APPS_DIR, "research_workbench"))
sys.path.insert(0, os.path.join(APPS_DIR, "software_factory"))

from database import SovereignDB
from memory import SovereignMemory
from task_queue import TaskQueue
from agents import AgentRegistry
from permissions import PermissionGuard
from observability import SovereignObservability
from self_healing import SelfHealingEngine

from game_engine import GameStudioEngine
from semantic_memory import SemanticMemoryOS
from seo_auditor import AgenticSEOEngine
from secure_app import SecurePrivatePlatform
from crm_engine import SovereignCRM
from education_engine import AdaptiveEducationEngine
from media_engine import AIMediaFactory
from dev_discovery import DeveloperDiscoveryEngine
from skills_engine import SkillsMarketplaceEngine
from personal_os import PersonalDecisionOS
from job_intel_app import AutonomousJobIntelligencePlatform
from bi_engine import SovereignBIEngine
from research_workbench import ScientificResearchWorkbench
from software_factory_engine import SovereignSoftwareFactory

class TestSovereignEcosystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = SovereignDB()
        cls.mem = SovereignMemory(cls.db)
        cls.tasks = TaskQueue(cls.db)
        cls.agents = AgentRegistry(cls.db)
        cls.perms = PermissionGuard(cls.db)
        cls.obs = SovereignObservability(cls.db)
        cls.healing = SelfHealingEngine(cls.mem)

    def test_01_database_and_tables(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            table_names = [r[0] for r in tables]
            for req in ["projects", "agents", "tasks", "memories", "audit_logs", "telemetry"]:
                self.assertIn(req, table_names)

    def test_02_10_layer_memory(self):
        mem_id = self.mem.store("DECISION", "PROJECT_ATHENA", "TEST_KEY", {"decision": "Adopt SQLite WAL"})
        self.assertTrue(mem_id.startswith("MEM-"))
        records = self.mem.retrieve(layer="DECISION", key_tag="TEST_KEY")
        self.assertGreaterEqual(len(records), 1)

    def test_03_task_queue_dag(self):
        t_id = self.tasks.create_task("PROJ-01", "Implement Core Engine", assigned_agent="AGENT-CTO", priority="HIGH")
        self.assertTrue(t_id.startswith("TSK-"))
        self.tasks.update_status(t_id, "COMPLETED", {"status": "SUCCESS"})

    def test_04_agent_registry(self):
        agents = self.agents.get_all_agents()
        self.assertGreaterEqual(len(agents), 6)
        roles = [a["role"] for a in agents]
        self.assertIn("CEO", roles)
        self.assertIn("CTO", roles)

    def test_05_permission_guard(self):
        # Level 2 check
        res_safe = self.perms.check_and_audit("AGENT-ENG-FE", "WRITE_LOCAL_UI", 2)
        self.assertEqual(res_safe["status"], "APPROVED_BY_POLICY")
        # Level 5 check
        res_crit = self.perms.check_and_audit("AGENT-CEO", "DISPATCH_EXTERNAL_COMM", 5)
        self.assertEqual(res_crit["status"], "PENDING_APPROVAL")
        self.assertTrue(res_crit["requires_human_approval"])

    def test_06_observability_and_cost(self):
        self.obs.record_telemetry("TSK-TEST", "AGENT-CTO", 1.25, estimated_tokens=450)
        metrics = self.obs.get_summary_metrics()
        self.assertIn("total_agents", metrics)
        self.assertIn("total_memories", metrics)

    def test_07_self_healing_engine(self):
        try:
            raise ValueError("Test Synthetic Failure for Self-Healing Loop")
        except Exception as e:
            diagnosis, mem_id = self.healing.diagnose_and_record("TestComponent", e)
            self.assertEqual(diagnosis["error_type"], "ValueError")
            self.assertTrue(mem_id.startswith("MEM-"))

    def test_08_flagship_portfolio_apps(self):
        # Project A: Game Studio
        game = GameStudioEngine("test_game_state.json")
        res_game = game.simulate_turn("MINE_RESOURCES")
        self.assertEqual(res_game["status"], "SUCCESS")
        if os.path.exists("test_game_state.json"): os.remove("test_game_state.json")

        # Project D: SEO
        seo = AgenticSEOEngine()
        res_seo = seo.audit_content("This is an international business analyst document for supply chain consulting.", "international business analyst")
        self.assertGreater(res_seo["keyword_count"], 0)

        # Project E: Security Platform
        sec = SecurePrivatePlatform()
        tok = sec.create_session("USER-001", role="MANAGER")
        auth, _ = sec.verify_permission(tok, "ANALYST")
        self.assertTrue(auth)

        # Project F: CRM
        crm = SovereignCRM()
        lead = crm.add_lead("Tata Communications", "Operations Lead", 850000)
        inv = crm.generate_invoice(lead["id"], 850000)
        self.assertEqual(inv["subtotal_inr"], 850000)

        # Project G: Education
        edu = AdaptiveEducationEngine()
        mastery = edu.assess_mastery("STU-01", "MOD-01", 90)
        self.assertEqual(mastery["mastery_state"], "MASTERED")

        # Project H: Media
        media = AIMediaFactory()
        sb = media.create_storyboard("Antigravity Autonomous Systems")
        self.assertEqual(sb["total_scenes"], 3)

        # Project I: Dev Discovery
        dev = DeveloperDiscoveryEngine()
        prof = dev.register_profile("DEV-01", "Aditya Mehra", ["Python", "Operations", "AI Agents"], ["anti"])
        self.assertEqual(prof["name"], "Aditya Mehra")

        # Project J: Skills Marketplace
        skills_mkt = SkillsMarketplaceEngine()
        cat = skills_mkt.scan_skills_catalog()
        self.assertGreaterEqual(cat["total_skills_available"], 3000)

        # Project K: Personal OS
        pos = PersonalDecisionOS()
        acts = pos.evaluate_next_action([{"title": "Send Recruiter InMails", "impact": 9, "urgency": 9, "probability": 0.85}])
        self.assertEqual(acts[0]["quadrant"], "DO_NOW")

        # Project L: Job Intelligence
        job_app = AutonomousJobIntelligencePlatform(r"e:\anti")
        p_info = job_app.get_pipeline_overview()
        self.assertIn("total_active_jobs", p_info)

        # Project M: Business Intelligence
        bi = SovereignBIEngine()
        v = bi.analyze_variance("Pipeline Conversion Rate", 18.5, 12.0)
        self.assertGreater(v["percentage_change"], 0)

        # Project N: Research Workbench
        rw = ScientificResearchWorkbench()
        hyp = rw.record_hypothesis("1st-degree warm introductions achieve 4x conversion over cold ATS portals", "Empirical LinkedIn Network Dataset")
        self.assertEqual(hyp["confidence"], "HIGH")

        # Project O: Software Factory
        factory = SovereignSoftwareFactory()
        spec = factory.create_software_spec({"name": "Sovereign CRM", "target_users": "Enterprise Sales"})
        self.assertEqual(len(spec["core_features"]), 4)

if __name__ == "__main__":
    unittest.main()
