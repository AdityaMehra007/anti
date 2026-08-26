import os, sys, unittest
sys.path.insert(0, os.path.dirname(__file__))
from pipeline_engine import PipelineTrackerEngine, PipelineStage

class TestPipelineLifecycleEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PipelineTrackerEngine()

    def test_01_records_loaded(self):
        self.assertGreaterEqual(len(self.engine.records), 50)

    def test_02_cadence_generation(self):
        cadence = self.engine.generate_4_touch_cadence("John Doe", "Accenture", "Recruiter Outreach")
        self.assertIn("touch_1", cadence)
        self.assertIn("touch_2", cadence)
        self.assertIn("touch_3", cadence)
        self.assertIn("touch_4", cadence)
        self.assertIn("Aero India 2025", cadence["touch_2"]["body"])

    def test_03_valid_state_transitions(self):
        rec_id = self.engine.records[0]["id"]
        success = self.engine.transition_stage(rec_id, PipelineStage.SENT, "Dispatched via LinkedIn")
        self.assertTrue(success)
        success2 = self.engine.transition_stage(rec_id, PipelineStage.FOLLOWUP_1, "Day 3 cadence trigger")
        self.assertTrue(success2)

    def test_04_invalid_state_transition_blocked(self):
        rec_id = self.engine.records[1]["id"]
        fail = self.engine.transition_stage(rec_id, PipelineStage.CALL_SCHEDULED, "Skipping steps")
        self.assertFalse(fail)

    def test_05_export_and_report_generation(self):
        json_path = self.engine.export_pipeline_state()
        self.assertTrue(os.path.exists(json_path))

if __name__ == "__main__":
    unittest.main()
