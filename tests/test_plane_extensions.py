"""
Unit and Integration Test Suite for Plane Extended Capabilities:
1. Git-to-Plane Synchronizer & Release Changelog Bridge
2. Plane Workspace Backup, Export, and Restoration Engine
3. Autonomous Webhook Agent Reactor & Verification Logger
"""

import json
import os
from pathlib import Path
import unittest

from omega.integrations.plane_connector import PlaneClient
from omega.orchestration.plane_git_bridge import PlaneGitBridge
from omega.orchestration.plane_backup import PlaneBackupEngine
from omega.orchestration.plane_agent_reactor import PlaneAgentReactor
from omega.orchestration.plane_github_adapter import GitWebhookAdapter


class PlaneExtensionsTestCase(unittest.TestCase):
    """Test suite for Plane Git Bridge, Backup Engine, Agent Reactor, and Git Webhook Adapter."""

    def setUp(self):
        self.mock_client = PlaneClient(dry_run=True)

    # -------------------------------------------------------------------------
    # 1. Git-to-Plane Bridge Tests
    # -------------------------------------------------------------------------
    def test_git_bridge_classification(self):
        bridge = PlaneGitBridge(client=self.mock_client)

        # Explicit tag
        cls_core = bridge.classify_commit("[CORE] Refactor event reactor pipeline")
        self.assertEqual(cls_core["project_id"], "CORE")

        # Explicit issue ref
        cls_fleet = bridge.classify_commit("FLEET-42: Calibrate 6DOF manipulator policy")
        self.assertEqual(cls_fleet["project_id"], "FLEET")
        self.assertEqual(cls_fleet["issue_ref"], "FLEET-42")

        # Keyword inference
        cls_cap = bridge.classify_commit("Update central banking liquidity corridors and DCM")
        self.assertEqual(cls_cap["project_id"], "CAP")

        cls_intel = bridge.classify_commit("Scrape LinkedIn executive HR talent signals")
        self.assertEqual(cls_intel["project_id"], "INTEL")

    def test_git_bridge_sync_and_changelog(self):
        bridge = PlaneGitBridge(client=self.mock_client)
        sample_commits = [
            {"hash": "a1b2c3d4e5f6", "author": "ApexEngineer", "date": "2026-10-01", "message": "[CORE] Deploy Plane CE stack"},
            {"hash": "f6e5d4c3b2a1", "author": "ApexEngineer", "date": "2026-10-01", "message": "CAP-10: Settle M2M multi-currency corridors"},
        ]

        sync_res = bridge.sync_commits_to_plane(sample_commits, workspace_slug="omega")
        self.assertEqual(sync_res["total_processed"], 2)
        self.assertEqual(len(sync_res["synced_entries"]), 2)
        self.assertEqual(sync_res["synced_entries"][0]["status"], "staged")

        changelog = bridge.generate_release_changelog(sample_commits)
        self.assertIn("OMEGA Autonomous Release Changelog", changelog)
        self.assertIn("[CORE]", changelog)
        self.assertIn("[CAP]", changelog)
        self.assertIn("Deploy Plane CE stack", changelog)

    # -------------------------------------------------------------------------
    # 2. Plane Backup & Restoration Tests
    # -------------------------------------------------------------------------
    def test_backup_export_and_restore(self):
        engine = PlaneBackupEngine(client=self.mock_client)

        # 1. Export
        export_data = engine.export_workspace("omega")
        self.assertEqual(export_data["metadata"]["workspace"], "omega")
        self.assertGreaterEqual(len(export_data["projects"]), 4)

        # 2. Save backup
        saved_file = engine.save_backup(export_data, filename="test_backup_temp.json")
        self.assertTrue(os.path.exists(saved_file))

        try:
            # 3. Dossier Markdown
            dossier = engine.generate_dossier_markdown(export_data)
            self.assertIn("Plane CE Backup Dossier", dossier)
            self.assertIn("CORE", dossier)
            self.assertIn("CAP", dossier)

            # 4. Restore
            restore_res = engine.restore_backup(saved_file, target_workspace="omega-restored")
            self.assertEqual(restore_res["restored_workspace"], "omega-restored")
            self.assertGreaterEqual(restore_res["projects_restored"], 4)
            self.assertGreaterEqual(restore_res["cycles_restored"], 1)
            self.assertGreaterEqual(restore_res["issues_restored"], 1)
        finally:
            if os.path.exists(saved_file):
                os.remove(saved_file)

    # -------------------------------------------------------------------------
    # 3. Plane Agent Reactor Tests
    # -------------------------------------------------------------------------
    def test_agent_reactor_events(self):
        reactor = PlaneAgentReactor(client=self.mock_client)

        # Issue created event
        create_event = {
            "data": {
                "id": "iss-500",
                "project_id": "CORE",
                "name": "Urgent security audit for proxy container",
            }
        }
        res_create = reactor.process_event("issue.created", create_event)
        self.assertEqual(res_create["action"], "acknowledged")
        self.assertEqual(res_create["priority"], "urgent")

        # Issue updated event (completed)
        update_event = {
            "data": {
                "id": "iss-500",
                "project_id": "CORE",
                "name": "Urgent security audit for proxy container",
                "state": "completed",
            }
        }
        res_update = reactor.process_event("issue.updated", update_event)
        self.assertEqual(res_update["action"], "updated")
        self.assertIn("verified_completion_logged", res_update["sub_actions"])

    # -------------------------------------------------------------------------
    # 4. GitHub & GitLab Webhook Adapter Tests
    # -------------------------------------------------------------------------
    def test_github_gitlab_webhook_adapter(self):
        adapter = GitWebhookAdapter(client=self.mock_client)

        # Test issue key extraction
        keys = adapter.extract_issue_keys("feat(core): CORE-101 and CAP-202 fixes #303 and iss-abc")
        self.assertIn("CORE-101", keys)
        self.assertIn("CAP-202", keys)
        self.assertIn("303", keys)
        self.assertIn("iss-abc", keys)

        # Test GitHub push translation
        push_payload = {
            "ref": "refs/heads/master",
            "sender": {"login": "ApexLead"},
            "commits": [
                {
                    "id": "abc12345678",
                    "message": "CORE-101: Deploy sovereign agent cluster",
                    "author": {"name": "ApexLead"},
                }
            ],
        }
        res_push = adapter.handle_github_push(push_payload, workspace_slug="omega", default_project="CORE")
        self.assertEqual(res_push["action"], "github_push")
        self.assertEqual(res_push["commits_processed"], 1)
        self.assertEqual(res_push["updates"][0]["status"], "COMMENT_CREATED")

        # Test GitHub PR translation
        pr_payload = {
            "action": "closed",
            "pull_request": {
                "number": 105,
                "title": "Resolve CAP-202 liquidity clearing",
                "body": "Fixes CAP-202 with verification ledger.",
                "merged": True,
            },
            "sender": {"login": "ApexLead"},
        }
        res_pr = adapter.handle_github_pull_request(pr_payload, workspace_slug="omega", default_project="CAP")
        self.assertEqual(res_pr["action"], "github_pull_request")
        self.assertTrue(res_pr["merged"])
        self.assertEqual(len(res_pr["updates"]), 1)
        self.assertEqual(res_pr["updates"][0]["issue_key"], "CAP-202")

        # Test GitLab MR translation
        mr_payload = {
            "object_attributes": {
                "iid": 99,
                "title": "FLEET-50: Calibrate autonomous fleet sensors",
                "state": "merged",
            },
            "user": {"username": "OmniBot"},
        }
        res_mr = adapter.handle_gitlab_merge_request(mr_payload, workspace_slug="omega", default_project="FLEET")
        self.assertEqual(res_mr["action"], "gitlab_merge_request")
        self.assertEqual(res_mr["mr_id"], 99)
        self.assertEqual(res_mr["updates"][0]["issue_key"], "FLEET-50")


if __name__ == "__main__":
    unittest.main()
