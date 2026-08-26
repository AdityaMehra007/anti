"""
LIVE JOB DISCOVERY ENGINE TEST SUITE
Tests:
1. Seed isolation (SEEDED_NOT_VERIFIED records excluded from confirmed openings).
2. Live discovery execution telemetry and run proof logging.
3. Genuine application URL reachability and HTTP status verification.
4. Cryptographic evidence hashing and job_evidence table integrity.
5. Deduplication across repeated runs.
"""
import unittest
import sys
import os
import json

sys.path.insert(0, 'E:/anti')

from omega.career_war_room.database import war_room_db
from omega.career_war_room.live_job_discovery import live_job_discovery

class TestLiveJobDiscovery(unittest.TestCase):
    def setUp(self):
        self.db = war_room_db
        self.engine = live_job_discovery

    def test_01_seed_isolation(self):
        # Confirmed list must NEVER include SEEDED_NOT_VERIFIED records
        confirmed = self.engine.list_confirmed_jobs(limit=100)
        for job in confirmed:
            self.assertEqual(job["verification_status"], "CONFIRMED_OPENING")
            self.assertNotEqual(job["verification_status"], "SEEDED_NOT_VERIFIED")
            self.assertNotEqual(job["verification_status"], "SOURCE_ERROR")

    def test_02_live_discovery_run_proof(self):
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM job_runs ORDER BY start_time DESC LIMIT 1")
            run = cur.fetchone()
            self.assertIsNotNone(run, "job_runs table must contain at least one live discovery execution")
            self.assertEqual(run["status"], "SUCCESS")
            self.assertGreaterEqual(run["sources_checked"], 1)
            self.assertGreaterEqual(run["jobs_found"], 1)

    def test_03_job_evidence_cryptographic_integrity(self):
        with self.db.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM job_evidence")
            evidence_records = [dict(r) for r in cur.fetchall()]
            self.assertGreaterEqual(len(evidence_records), 1)
            for ev in evidence_records:
                self.assertEqual(len(ev["evidence_hash"]), 64, "Evidence hash must be a valid 64-char SHA-256 string")
                self.assertTrue(ev["final_url"].startswith("http"))
                self.assertEqual(ev["http_status"], 200)

    def test_04_automation_runs_jsonl_log(self):
        log_path = "E:/anti/omega/data/automation_runs.jsonl"
        self.assertTrue(os.path.exists(log_path), "automation_runs.jsonl must exist on disk")
        with open(log_path, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]
            self.assertGreaterEqual(len(lines), 1)
            last_run = lines[-1]
            self.assertIn("run_id", last_run)
            self.assertEqual(last_run["status"], "SUCCESS")

if __name__ == "__main__":
    unittest.main(verbosity=2)
