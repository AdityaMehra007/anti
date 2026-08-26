import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import unittest
import json
import tempfile
import datetime

# Ensure omega core is in Python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORE_DIR = os.path.join(BASE_DIR, "core")
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

from data_core import OmegaDataCore
from truth_engine import OmegaTruthEngine, TruthValidationError
from career_brain import OmegaCareerBrain
from agent_swarm import (
    OmegaAgentSwarmCoordinator,
    JobScoutAgent,
    CompanyResearcherAgent,
    OpportunityScorerAgent,
    ATSAgent,
    OutreachAgent,
    FollowUpAgent,
    InterviewCoachAgent,
    CareerAnalystAgent
)
from daemon_verifier import OmegaDaemonVerifier


class TestOmegaDataCore(unittest.TestCase):
    """Unit and integration tests for Omega Unified Data Core."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_omega.db")
        self.json_path = os.path.join(self.temp_dir, "test_state.json")
        self.core = OmegaDataCore(db_path=self.db_path, state_json_path=self.json_path)

    def test_01_schema_and_tables_creation(self):
        """Verify all 6 core tables and indexes are created successfully."""
        with self.core.get_connection() as conn:
            tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            for expected_table in ["companies", "contacts", "opportunities", "pipeline_records", "interview_records", "learning_metrics"]:
                self.assertIn(expected_table, tables)

    def test_02_companies_crud_and_query(self):
        """Verify CRUD operations and filtering for companies."""
        cid = self.core.add_company({
            "name": "Test Global Tech GCC",
            "industry": "Cloud & AI Operations",
            "corridor": "Outer Ring Road (Bellandur)",
            "headcount": 5000,
            "gcc_tier": "Tier 1 Global GCC",
            "tier_rating": 1.35
        })
        self.assertTrue(cid.startswith("COMP-"))

        comp = self.core.get_company(cid)
        self.assertIsNotNone(comp)
        self.assertEqual(comp["name"], "Test Global Tech GCC")

        filtered = self.core.list_companies(corridor="Outer Ring Road")
        self.assertGreaterEqual(len(filtered), 1)

    def test_03_opportunities_and_pipeline_crud(self):
        """Verify opportunities and pipeline records creation and cross-linking."""
        cid = self.core.add_company({"name": "Test Logistics GCC", "corridor": "Whitefield"})
        oid = self.core.add_opportunity({
            "company_id": cid,
            "role_title": "EXIM & Logistics Operations Specialist",
            "compensation_median": 1000000,
            "ev_score": 92.5
        })
        self.assertTrue(oid.startswith("OPP-"))

        pid = self.core.add_pipeline_record({
            "opportunity_id": oid,
            "stage": "PREPARED",
            "proof_hash": "sha256:11223344556677889900aabbccddeeff",
            "payload_data": json.dumps({"test": "initial draft"})
        })
        self.assertTrue(pid.startswith("PIP-"))

        lineage = self.core.get_pipeline_full_lineage(pid)
        self.assertIsNotNone(lineage)
        self.assertEqual(lineage["pipeline"]["stage"], "PREPARED")
        self.assertEqual(lineage["opportunity"]["role_title"], "EXIM & Logistics Operations Specialist")

    def test_04_json_state_export(self):
        """Verify state synchronization to omega_state.json."""
        export_path = self.core.export_unified_state()
        self.assertTrue(os.path.exists(export_path))
        with open(export_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["os_name"], "ADI OMEGA OS")
            self.assertIn("candidate", data)
            self.assertIn("kpis", data)
            self.assertEqual(data["candidate"]["name"], "Aditya Mehra")


class TestOmegaTruthEngine(unittest.TestCase):
    """Unit tests for Truth Engine cryptographic verification and state enforcement."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.audit_path = os.path.join(self.temp_dir, "test_truth_audit.jsonl")
        self.truth = OmegaTruthEngine(audit_log_path=self.audit_path)

    def test_01_valid_sequential_transitions(self):
        """Verify legal progression PREPARED -> SENT -> DELIVERED -> REPLIED -> INTERVIEW -> OFFER."""
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # 1. INITIAL -> PREPARED
        r1 = self.truth.record_transition(
            record_id="PIP-T1",
            current_stage="INITIAL",
            target_stage="PREPARED",
            payload={"timestamp": now, "payload_type": "ATS_MATCH_DRAFT"}
        )
        self.assertEqual(r1["status"], "SUCCESS")
        self.assertTrue(r1["proof_hash"].startswith("sha256:"))

        # 2. PREPARED -> SENT
        r2 = self.truth.record_transition(
            record_id="PIP-T1",
            current_stage="PREPARED",
            target_stage="SENT",
            payload={"timestamp": now, "message_id": "<test-msg-001@omega.io>", "outbound_channel": "Cold Email"},
            parent_proof_hash=r1["proof_hash"]
        )
        self.assertEqual(r2["status"], "SUCCESS")

        # 3. SENT -> DELIVERED
        r3 = self.truth.record_transition(
            record_id="PIP-T1",
            current_stage="SENT",
            target_stage="DELIVERED",
            payload={"timestamp": now, "delivery_receipt": "SMTP 250 OK Delivered"},
            parent_proof_hash=r2["proof_hash"]
        )
        self.assertEqual(r3["status"], "SUCCESS")

        # 4. DELIVERED -> REPLIED
        r4 = self.truth.record_transition(
            record_id="PIP-T1",
            current_stage="DELIVERED",
            target_stage="REPLIED",
            payload={"timestamp": now, "reply_text": "Let's schedule a call this Friday.", "sentiment": "POSITIVE"},
            parent_proof_hash=r3["proof_hash"]
        )
        self.assertEqual(r4["status"], "SUCCESS")

        # 5. REPLIED -> INTERVIEW
        r5 = self.truth.record_transition(
            record_id="PIP-T1",
            current_stage="REPLIED",
            target_stage="INTERVIEW",
            payload={"timestamp": now, "interview_round": "Round 1 Case Study", "invite_artifact": "invite.eml"},
            parent_proof_hash=r4["proof_hash"]
        )
        self.assertEqual(r5["status"], "SUCCESS")

        # 6. INTERVIEW -> OFFER
        r6 = self.truth.record_transition(
            record_id="PIP-T1",
            current_stage="INTERVIEW",
            target_stage="OFFER",
            payload={"timestamp": now, "ctc_offered_inr": 1200000, "offer_letter_artifact": "offer_letter.pdf"},
            parent_proof_hash=r5["proof_hash"]
        )
        self.assertEqual(r6["status"], "SUCCESS")

    def test_02_illegal_state_skips_strictly_rejected(self):
        """Verify that illegal transitions (e.g. PREPARED -> OFFER) raise TruthValidationError."""
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # PREPARED directly to OFFER must be rejected
        with self.assertRaises(TruthValidationError):
            self.truth.record_transition(
                record_id="PIP-ILLEGAL-1",
                current_stage="PREPARED",
                target_stage="OFFER",
                payload={"timestamp": now, "ctc_offered_inr": 1200000, "offer_letter_artifact": "fake.pdf"}
            )

        # PREPARED directly to INTERVIEW must be rejected
        with self.assertRaises(TruthValidationError):
            self.truth.record_transition(
                record_id="PIP-ILLEGAL-2",
                current_stage="PREPARED",
                target_stage="INTERVIEW",
                payload={"timestamp": now, "interview_round": "Case Study", "invite_artifact": "invite.eml"}
            )

        # SENT directly to OFFER must be rejected
        with self.assertRaises(TruthValidationError):
            self.truth.record_transition(
                record_id="PIP-ILLEGAL-3",
                current_stage="SENT",
                target_stage="OFFER",
                payload={"timestamp": now, "ctc_offered_inr": 1200000, "offer_letter_artifact": "fake.pdf"}
            )

    def test_03_missing_required_payload_keys_rejected(self):
        """Verify transitions lacking mandatory verification keys fail validation."""
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # SENT missing message_id / outbound_channel
        with self.assertRaises(TruthValidationError):
            self.truth.record_transition(
                record_id="PIP-MISSING-KEYS",
                current_stage="PREPARED",
                target_stage="SENT",
                payload={"timestamp": now}  # Missing message_id and outbound_channel
            )


class TestOmegaCareerBrain(unittest.TestCase):
    """Unit tests for Career Brain Expected Value formula and commute matrix."""

    def setUp(self):
        self.brain = OmegaCareerBrain()

    def test_01_expected_value_calculation(self):
        """Verify mathematical calculation of multi-factor EV Score."""
        result = self.brain.calculate_expected_value(
            role_title="Global Operations Analyst - Supply Chain Logistics",
            company_name="Walmart Global Tech",
            corridor="Outer Ring Road (Cessna Business Park)",
            compensation_median=1100000,
            gcc_tier="Tier 1 Global GCC",
            jd_text="Vendor SLA governance, 15% cost savings, run-of-show logistics, Incoterms 2020."
        )
        self.assertIn("ev_score", result)
        self.assertGreaterEqual(result["ev_score"], 80.0)
        self.assertLessEqual(result["ev_score"], 100.0)
        self.assertIn("breakdown", result)
        self.assertGreater(result["breakdown"]["p_interview"], 0.8)
        self.assertGreater(result["breakdown"]["p_offer"], 0.8)

    def test_02_commute_friction_matrix(self):
        """Verify transit matrix returns lower friction for nearby hubs and higher for distant hubs."""
        f_ecity, info_ecity = self.brain.calculate_commute_friction("Electronic City")
        f_manyata, info_manyata = self.brain.calculate_commute_friction("Manyata Tech Park")
        f_whitefield, info_whitefield = self.brain.calculate_commute_friction("Whitefield ITPL")

        self.assertLess(f_ecity, f_manyata)
        self.assertLess(f_manyata, f_whitefield)
        self.assertEqual(info_ecity["metro_access"], "Yellow Line Direct")

    def test_03_skill_gap_analysis(self):
        """Verify matching skills identification and penalty assignment."""
        good_jd = "Operations coordinator, vendor SLA management, cost savings, Incoterms 2020, customs clearance, B2B."
        penalty_low, matched, missing = self.brain.calculate_skill_gap(good_jd)
        self.assertEqual(penalty_low, 0.0)
        self.assertGreaterEqual(len(matched), 5)

        bad_jd = "Senior React Native & Kubernetes backend developer with 10 years C++ systems architecture."
        penalty_high, matched_bad, missing_bad = self.brain.calculate_skill_gap(bad_jd)
        self.assertGreater(penalty_high, 10.0)


class TestOmegaAgentSwarm(unittest.TestCase):
    """Unit tests for 8-agent swarm coordinator and sequential execution pipeline."""

    def setUp(self):
        self.swarm = OmegaAgentSwarmCoordinator()

    def test_01_all_8_agents_execution_pipeline(self):
        """Verify full pipeline runs across all 8 agents and collects execution traces."""
        sample_req = {
            "company_name": "Walmart Global Tech",
            "role_title": "Global Operations Analyst - Supply Chain Logistics",
            "corridor": "Outer Ring Road (Cessna)",
            "compensation_median": 1100000,
            "gcc_tier": "Tier 1 Global GCC",
            "jd_text": "Vendor SLA governance, 15% cost savings, run-of-show logistics, Incoterms 2020."
        }
        contact = {"full_name": "Priya Sharma"}

        result = self.swarm.run_full_pipeline(sample_req, contact)

        self.assertEqual(result["status"], "SWARM_EXECUTION_COMPLETED")
        self.assertEqual(result["total_agents_activated"], 8)
        self.assertEqual(len(result["trace"]), 8)

        agent_names_in_trace = [t["agent"] for t in result["trace"]]
        expected_agents = [
            "JobScoutAgent",
            "CompanyResearcherAgent",
            "OpportunityScorerAgent",
            "ATSAgent",
            "OutreachAgent",
            "FollowUpAgent",
            "InterviewCoachAgent",
            "CareerAnalystAgent"
        ]
        for exp in expected_agents:
            self.assertIn(exp, agent_names_in_trace)

    def test_02_ats_agent_bullet_generation(self):
        """Verify ATS agent creates verified anchor claims bullets."""
        ats = ATSAgent()
        out = ats.process(jd_text="Operations analysis and vendor SLA management", role_title="Operations Analyst")
        self.assertEqual(len(out["tailored_bullets"]), 3)
        self.assertTrue(any("AERO India 2025 Lead" in b for b in out["tailored_bullets"]))
        self.assertTrue(any("15% net operational cost reduction" in b for b in out["tailored_bullets"]))

    def test_03_outreach_agent_cadence(self):
        """Verify Outreach agent generates 3-stage personalized cadences."""
        outreach = OutreachAgent()
        out = outreach.process(contact_name="Priya Sharma", company_name="Walmart Global Tech", role_title="Operations Analyst")
        self.assertIn("stage_1_initial", out["cadence_stages"])
        self.assertIn("stage_2_followup", out["cadence_stages"])
        self.assertIn("stage_3_polite_close", out["cadence_stages"])
        self.assertIn("Aditya Mehra", out["cadence_stages"]["stage_1_initial"])


class TestOmegaDaemonVerifier(unittest.TestCase):
    """Unit tests for Empirical Daemon Verifier."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.heartbeat_path = os.path.join(self.temp_dir, "test_heartbeat.json")
        self.verifier = OmegaDaemonVerifier(heartbeat_path=self.heartbeat_path)

    def test_01_verify_daemons_and_logs(self):
        """Verify verifier inspects log files, identifies sizes, and saves heartbeat."""
        report = self.verifier.verify_all_daemons()
        self.assertIn("timestamp", report)
        self.assertIn("tasks_audited", report)
        self.assertIn("logs_audited", report)
        self.assertTrue(os.path.exists(self.heartbeat_path))

        with open(self.heartbeat_path, "r", encoding="utf-8") as f:
            saved = json.load(f)
            self.assertEqual(saved["engine"], "Omega Empirical Daemon Verifier v8.0")


def run_all_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestOmegaDataCore))
    suite.addTests(loader.loadTestsFromTestCase(TestOmegaTruthEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestOmegaCareerBrain))
    suite.addTests(loader.loadTestsFromTestCase(TestOmegaAgentSwarm))
    suite.addTests(loader.loadTestsFromTestCase(TestOmegaDaemonVerifier))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
