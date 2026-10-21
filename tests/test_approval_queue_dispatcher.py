#!/usr/bin/env python3
"""
test_approval_queue_dispatcher.py - Unit Test Suite for Approval Queue & Dispatch Engine
========================================================================================
"""

import unittest
import csv
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
import scripts.dispatch_approval_queue as dispatcher

class TestApprovalQueueDispatcher(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_csv = self.temp_dir / "test_approval_queue.csv"
        self.test_json = self.temp_dir / "test_approval_queue.json"
        self.test_dispatch_dir = self.temp_dir / "dispatched_actions"
        self.test_audit_ledger = self.temp_dir / "test_audit_ledger.jsonl"

        # Seed sample rows
        self.sample_rows = [
            {
                "Action ID": "ACT-TEST-001",
                "Person": "Jane Doe",
                "Company": "Anthropic AI",
                "Job": "Operations Lead",
                "Channel": "LinkedIn InMail",
                "Draft Message": "Hi Jane, I would love to connect regarding the Operations Lead role.",
                "Reason / Evidence": "Score: 92/100 | Strong Fit",
                "Priority": "P0 - High Opportunity",
                "Approval Required": "TRUE",
                "Status": "PENDING_APPROVAL",
                "Staged Timestamp": "2026-10-21T12:00:00"
            },
            {
                "Action ID": "ACT-TEST-002",
                "Person": "John Smith",
                "Company": "DeepMind",
                "Job": "Systems Analyst",
                "Channel": "Direct Email",
                "Draft Message": "Hi John, expressing interest in Systems Analyst.",
                "Reason / Evidence": "Score: 88/100 | Strong Fit",
                "Priority": "P1 - Secondary Outreach",
                "Approval Required": "TRUE",
                "Status": "PENDING_APPROVAL",
                "Staged Timestamp": "2026-10-21T12:05:00"
            }
        ]

        fieldnames = list(self.sample_rows[0].keys())
        with open(self.test_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.sample_rows)

        # Patch module paths to use temporary directories
        self.patch_csv = patch.object(dispatcher, "QUEUE_CSV", self.test_csv)
        self.patch_json = patch.object(dispatcher, "QUEUE_JSON", self.test_json)
        self.patch_dispatch = patch.object(dispatcher, "DISPATCH_DIR", self.test_dispatch_dir)
        self.patch_audit = patch.object(dispatcher, "AUDIT_LEDGER", self.test_audit_ledger)

        self.patch_csv.start()
        self.patch_json.start()
        self.patch_dispatch.start()
        self.patch_audit.start()

    def tearDown(self):
        self.patch_csv.stop()
        self.patch_json.stop()
        self.patch_dispatch.stop()
        self.patch_audit.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_and_save_queue(self):
        rows = dispatcher.load_queue()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["Action ID"], "ACT-TEST-001")

        rows[0]["Status"] = "APPROVED"
        dispatcher.save_queue(rows)

        reloaded = dispatcher.load_queue()
        self.assertEqual(reloaded[0]["Status"], "APPROVED")
        self.assertTrue(self.test_json.exists())

    def test_approve_actions_by_id(self):
        count = dispatcher.approve_actions(action_ids="ACT-TEST-001")
        self.assertEqual(count, 1)

        rows = dispatcher.load_queue()
        self.assertEqual(rows[0]["Status"], "APPROVED")
        self.assertEqual(rows[1]["Status"], "PENDING_APPROVAL")

    def test_approve_top(self):
        count = dispatcher.approve_actions(top_n=2)
        self.assertEqual(count, 2)

        rows = dispatcher.load_queue()
        self.assertEqual(rows[0]["Status"], "APPROVED")
        self.assertEqual(rows[1]["Status"], "APPROVED")

    def test_reject_actions(self):
        count = dispatcher.reject_actions("ACT-TEST-002")
        self.assertEqual(count, 1)

        rows = dispatcher.load_queue()
        self.assertEqual(rows[1]["Status"], "REJECTED")

    def test_dispatch_approved_actions(self):
        dispatcher.approve_actions(action_ids="ACT-TEST-001")
        dispatched_count = dispatcher.dispatch_approved()
        self.assertEqual(dispatched_count, 1)

        rows = dispatcher.load_queue()
        self.assertEqual(rows[0]["Status"], "DISPATCHED")
        self.assertIn("Dispatched Timestamp", rows[0])

        # Verify packet created
        packet_file = self.test_dispatch_dir / "ACT-TEST-001_AnthropicAI_dispatch_packet.md"
        self.assertTrue(packet_file.exists())
        packet_text = packet_file.read_text(encoding="utf-8")
        self.assertIn("Jane Doe", packet_text)
        self.assertIn("Anthropic AI", packet_text)
        self.assertIn("Operations Lead", packet_text)

        # Verify audit ledger entry
        self.assertTrue(self.test_audit_ledger.exists())
        ledger_lines = self.test_audit_ledger.read_text(encoding="utf-8").strip().split("\n")
        self.assertEqual(len(ledger_lines), 1)
        entry = json.loads(ledger_lines[0])
        self.assertEqual(entry["action_id"], "ACT-TEST-001")
        self.assertEqual(entry["company"], "Anthropic AI")

if __name__ == "__main__":
    unittest.main()
