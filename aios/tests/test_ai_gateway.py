#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: AI Gateway & Router Automated Test Suite
Zero-dependency Python Standard Library test suite verifying:
- Privacy & PII scrubbing
- Dynamic model registry
- Standard blocking chat completions
- Server-Sent Events (SSE) streaming chat completions
- Master SQLite audit trail logging
"""

import sys
import os
import json
import time
import socket
import threading
import unittest
import urllib.request
import urllib.error
from pathlib import Path

# Add project roots to path
AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "ai"))
sys.path.insert(0, str(AIOS_ROOT / "databases"))
sys.path.insert(0, str(AIOS_ROOT / "scripts"))

import gateway
import db
import health_check

TEST_PORT = 8098
BASE_URL = f"http://127.0.0.1:{TEST_PORT}"


class TestAIGateway(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Starts an isolated Gateway HTTP server on TEST_PORT."""
        cls.server = gateway.ThreadedHTTPServer(("127.0.0.1", TEST_PORT), gateway.GatewayRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        # Give server a brief moment to bind
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        """Shuts down the test server."""
        cls.server.shutdown()
        cls.server.server_close()

    def test_01_privacy_patterns(self):
        """Tests PII and secret detection / redaction."""
        clean_text = "Write a python function to compute factorial"
        self.assertFalse(gateway.contains_pii(clean_text))

        email_text = "Send credentials to admin@example.com immediately"
        self.assertTrue(gateway.contains_pii(email_text))
        redacted = gateway.anonymize_text(email_text)
        self.assertNotIn("admin@example.com", redacted)
        self.assertIn("[REDACTED_SENSITIVE]", redacted)

        api_key_text = "Here is my key: sk-abcdefghijklmnopqrstuvwxyz123456789"
        self.assertTrue(gateway.contains_pii(api_key_text))
        redacted_key = gateway.anonymize_text(api_key_text)
        self.assertNotIn("sk-abcdefghijklmnopqrstuvwxyz123456789", redacted_key)

    def test_02_health_endpoint(self):
        """Tests GET /health returns 200 with service metadata."""
        req = urllib.request.Request(f"{BASE_URL}/health")
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertEqual(data.get("status"), "HEALTHY")
            self.assertEqual(data.get("service"), "ANTIGRAVITY_OMEGA_AIOS_GATEWAY")

    def test_03_models_discovery(self):
        """Tests GET /v1/models returns registered models."""
        req = urllib.request.Request(f"{BASE_URL}/v1/models")
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertIn("data", data)
            model_ids = [m["id"] for m in data["data"]]
            # Must include local coder model and cloud entries
            self.assertTrue(any("qwen2.5-coder" in mid for mid in model_ids))
            self.assertIn("gemini-2.0-flash", model_ids)

    def test_04_chat_completion_blocking(self):
        """Tests POST /v1/chat/completions (blocking mode)."""
        payload = {
            "model": "qwen2.5-coder:3b",
            "messages": [{"role": "user", "content": "Reply with precisely the single word: ACK"}]
        }
        req = urllib.request.Request(
            f"{BASE_URL}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=180) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertIn("choices", data)
            self.assertTrue(len(data["choices"]) > 0)
            content = data["choices"][0]["message"]["content"]
            self.assertTrue(len(content) > 0)
            self.assertIn("omega_router", data)
            self.assertEqual(data["omega_router"]["routed_to"], "local_ollama")

    def test_05_chat_completion_streaming(self):
        """Tests POST /v1/chat/completions with SSE streaming."""
        payload = {
            "model": "qwen2.5-coder:3b",
            "messages": [{"role": "user", "content": "Count from 1 to 3."}],
            "stream": True
        }
        req = urllib.request.Request(
            f"{BASE_URL}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=180) as res:
            self.assertEqual(res.status, 200)
            self.assertIn("text/event-stream", res.headers.get("Content-Type", ""))
            
            chunks = []
            done_received = False
            for line in res:
                decoded = line.decode("utf-8").strip()
                if not decoded:
                    continue
                if decoded == "data: [DONE]":
                    done_received = True
                    break
                if decoded.startswith("data: "):
                    chunk_json = json.loads(decoded[6:])
                    chunks.append(chunk_json)

            self.assertTrue(len(chunks) > 0, "Should receive at least one SSE chunk")
            self.assertTrue(done_received, "Should receive terminal [DONE] marker")

    def test_06_cloud_routing_simulation(self):
        """Tests fallback/routing for cloud-targeted model."""
        payload = {
            "model": "claude-3-5-sonnet",
            "messages": [{"role": "user", "content": "Architect an enterprise system"}]
        }
        req = urllib.request.Request(
            f"{BASE_URL}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertEqual(data["omega_router"]["routed_to"], "cloud_gateway")

    def test_07_pii_audit_logged_to_db(self):
        """Tests that queries with detected PII generate audit ledger records in master.db."""
        secret_payload = {
            "model": "gemini-2.0-flash",
            "messages": [{"role": "user", "content": "My secret key is ghp_11112222333344445555666677778888"}]
        }
        req = urllib.request.Request(
            f"{BASE_URL}/v1/chat/completions",
            data=json.dumps(secret_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)

        # Inspect SQLite audit_logs
        with db.get_connection() as con:
            cur = con.execute(
                "SELECT * FROM audit_logs WHERE action = 'CHAT_COMPLETION' ORDER BY id DESC LIMIT 1"
            )
            row = cur.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["actor"], "AIOS_GATEWAY")
            self.assertIn("PII: True", row["details"])


if __name__ == "__main__":
    unittest.main()
