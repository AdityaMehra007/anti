#!/usr/bin/env python3
"""
Unit and integration test suite for OMEGA Master MCP Hub & Ecosystem.
"""

import os
import sys
import json
import unittest
from pathlib import Path

WORKSPACE_DIR = Path(r"E:\anti").resolve()
sys.path.insert(0, str(WORKSPACE_DIR))
from mcp_hub import MCPHub

class TestMCPHub(unittest.TestCase):

    def setUp(self):
        self.hub = MCPHub()

    def test_mcp_config_exists_and_valid(self):
        config_path = WORKSPACE_DIR / ".mcp.json"
        self.assertTrue(config_path.exists(), ".mcp.json must exist")
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("mcpServers", data)
        self.assertGreaterEqual(len(data["mcpServers"]), 20)

    def test_catalog_file_integrity(self):
        catalog_path = WORKSPACE_DIR / "data" / "mcp_tools_catalog.json"
        self.assertTrue(catalog_path.exists(), "data/mcp_tools_catalog.json must exist")
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        self.assertGreaterEqual(len(catalog), 20)
        total_tools = sum(len(c.get("tools", [])) for c in catalog)
        self.assertGreaterEqual(total_tools, 200, f"Expected at least 200 tools, found {total_tools}")

    def test_cockpit_html_exists(self):
        cockpit_path = WORKSPACE_DIR / "mcp_master_cockpit.html"
        self.assertTrue(cockpit_path.exists())
        self.assertGreater(cockpit_path.stat().st_size, 50000)

    def test_cursor_and_agents_sync(self):
        cursor_cfg = WORKSPACE_DIR / ".cursor" / "mcp.json"
        agents_cfg = WORKSPACE_DIR / ".agents" / "mcp_config.json"
        self.assertTrue(cursor_cfg.exists(), ".cursor/mcp.json must exist")
        self.assertTrue(agents_cfg.exists(), ".agents/mcp_config.json must exist")

    def test_export_claude_and_cursor(self):
        claude_exp = self.hub.export_config("claude")
        data = json.loads(claude_exp)
        self.assertIn("mcpServers", data)
        self.assertIn("plane", data["mcpServers"])
        self.assertIn("github", data["mcpServers"])

    def test_handshake_plane_mcp(self):
        res = self.hub.test_server("plane", timeout=10.0)
        self.assertEqual(res.get("status"), "OK")
        self.assertGreaterEqual(res.get("tools_count", 0), 10)

    def test_handshake_powershell_mcp(self):
        res = self.hub.test_server("powershell", timeout=10.0)
        self.assertEqual(res.get("status"), "OK")
        self.assertGreaterEqual(res.get("tools_count", 0), 10)


if __name__ == "__main__":
    unittest.main()
