"""
Unit tests for N8nClient in e:\anti\n8n\n8n_client.py
"""

import os
import unittest
from unittest.mock import MagicMock, patch
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from n8n_client import N8nClient


class TestN8nClient(unittest.TestCase):

    def setUp(self):
        self.client = N8nClient(base_url="http://localhost:5678", api_key="test-api-key")

    def test_init_and_headers(self):
        self.assertEqual(self.client.base_url, "http://localhost:5678")
        self.assertEqual(self.client.api_key, "test-api-key")
        headers = self.client._headers
        self.assertEqual(headers.get("X-N8N-API-KEY"), "test-api-key")
        self.assertEqual(headers.get("Content-Type"), "application/json")

    def test_headers_without_api_key(self):
        client_no_key = N8nClient(base_url="http://127.0.0.1:5678", api_key="")
        headers = client_no_key._headers
        self.assertNotIn("X-N8N-API-KEY", headers)

    @patch("urllib.request.urlopen")
    def test_health_check_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        self.assertTrue(self.client.health_check())

    @patch("urllib.request.urlopen")
    def test_health_check_failure(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Connection refused")
        self.assertFalse(self.client.health_check())

    @patch("urllib.request.urlopen")
    def test_list_workflows(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "data": [
                {"id": "wf-1", "name": "Flow 1", "active": True},
                {"id": "wf-2", "name": "Flow 2", "active": False},
            ]
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        all_wfs = self.client.list_workflows(active_only=False)
        self.assertEqual(len(all_wfs), 2)

        active_wfs = self.client.list_workflows(active_only=True)
        self.assertEqual(len(active_wfs), 1)
        self.assertEqual(active_wfs[0]["id"], "wf-1")

    @patch("urllib.request.urlopen")
    def test_trigger_webhook(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"status": "received"}).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        res = self.client.trigger_webhook("test-hook", {"msg": "hello"}, is_test=False)
        self.assertEqual(res.get("status"), "received")

        # Verify request URL format
        req_arg = mock_urlopen.call_args[0][0]
        self.assertEqual(req_arg.full_url, "http://localhost:5678/webhook/test-hook")
        self.assertEqual(req_arg.get_method(), "POST")

    def test_import_workflow_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.client.import_workflow_file("non_existent_file_xyz.json")


if __name__ == "__main__":
    unittest.main()
