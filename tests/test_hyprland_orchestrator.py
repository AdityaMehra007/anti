"""
Unit & Integration Test Suite for Hyprland Autonomous Orchestrator
==================================================================
Verifies the complete Hyprland SDK, state machine, dynamic workspaces,
tiling dispatchers, visual bling, Bezier physics, modular config generator,
and the 12-Phase Sovereign Lifecycle execution.
"""

import os
import sys
import json
import unittest
from dataclasses import asdict

from hyprland_orchestrator import (
    HyprlandClient,
    HyprlandConfig,
    HyprlandOrchestrator,
    Monitor,
    Workspace,
    Client,
    DecorationConfig
)


class TestHyprlandOrchestrator(unittest.TestCase):

    def setUp(self):
        # Force mock simulation mode for deterministic test execution
        self.config = HyprlandConfig(mock_mode=True)
        self.client = HyprlandClient(self.config)
        self.orchestrator = HyprlandOrchestrator(self.client)

    def test_01_initialization_and_telemetry(self):
        info = self.client.get_info()
        self.assertEqual(info.mode, "mock_simulation")
        self.assertTrue(info.version.startswith("v0."))
        self.assertEqual(info.aquamarine_version, "0.4.2")
        self.assertGreaterEqual(info.active_monitors, 1)
        self.assertGreaterEqual(info.total_workspaces, 1)

    def test_02_monitors_topology(self):
        monitors = self.client.get_monitors()
        self.assertGreaterEqual(len(monitors), 2)
        m0 = monitors[0]
        self.assertEqual(m0.name, "DP-1")
        self.assertEqual(m0.width, 3840)
        self.assertEqual(m0.height, 2160)
        self.assertEqual(m0.refreshRate, 144.0)
        self.assertTrue(m0.vrr)

    def test_03_workspaces_and_navigation(self):
        workspaces = self.client.get_workspaces()
        ws_ids = [w.id for w in workspaces]
        self.assertIn(1, ws_ids)
        self.assertIn(2, ws_ids)

        # Dispatch workspace switch
        res = self.client.dispatch("workspace", "5")
        self.assertEqual(res.get("status"), "ok")
        updated_workspaces = self.client.get_workspaces()
        self.assertIn(5, [w.id for w in updated_workspaces])

    def test_04_clients_and_active_window(self):
        clients = self.client.get_clients()
        self.assertGreaterEqual(len(clients), 4)

        active = self.client.get_active_window()
        self.assertIsNotNone(active)
        self.assertEqual(active.address, "0x55a9b802")
        self.assertIn("neovim", active.title)

    def test_05_dispatchers_lifecycle(self):
        # Test spawn
        initial_count = len(self.client.get_clients())
        res_exec = self.client.dispatch("exec", "alacritty")
        self.assertEqual(res_exec.get("status"), "ok")
        self.assertEqual(len(self.client.get_clients()), initial_count + 1)

        # Test toggle floating
        active = self.client.get_active_window()
        initial_floating = active.floating
        self.client.dispatch("togglefloating")
        active_after = self.client.get_active_window()
        self.assertEqual(active_after.floating, not initial_floating)

        # Revert floating
        self.client.dispatch("togglefloating")

        # Test movetoworkspace
        self.client.dispatch("movetoworkspace", "4")
        self.assertEqual(self.client.get_active_window().workspace["id"], 4)

    def test_06_visual_bling_decorations(self):
        decs = self.client.set_decorations(
            rounding=16,
            blur_size=10,
            blur_passes=4,
            drop_shadow=True,
            active_border="rgba(ff0055ee) 45deg"
        )
        self.assertEqual(decs.rounding, 16)
        self.assertEqual(decs.blur_size, 10)
        self.assertEqual(decs.blur_passes, 4)
        self.assertEqual(decs.active_border, "rgba(ff0055ee) 45deg")

    def test_07_bezier_animations(self):
        rule = self.client.set_animation("windows", enabled=True, speed=8, curve="myBezier", style="popin 80%")
        self.assertEqual(rule.speed, 8)
        self.assertEqual(rule.curve, "myBezier")
        self.assertIn("windows", self.client.state_store.animation_rules)

    def test_08_window_rules(self):
        initial_rules = len(self.client.state_store.window_rules)
        rule = self.client.add_window_rule("opacity 0.9", "class:^(thunar)$")
        self.assertEqual(len(self.client.state_store.window_rules), initial_rules + 1)
        self.assertEqual(rule.pattern, "class:^(thunar)$")

    def test_09_realtime_events_stream(self):
        initial_events = len(self.client.get_events())
        self.client.dispatch("workspace", "2")
        events = self.client.get_events()
        self.assertGreater(len(events), initial_events)
        latest = events[-1]
        self.assertEqual(latest["event"], "workspace")
        self.assertEqual(latest["payload"], "2")

    def test_10_config_generator_and_validator(self):
        configs = self.client.generate_modular_config()
        self.assertIn("hyprland.conf", configs)
        self.assertIn("monitors.conf", configs)
        self.assertIn("decoration.conf", configs)
        self.assertIn("animations.conf", configs)
        self.assertIn("windowrules.conf", configs)
        self.assertIn("keybinds.conf", configs)

        val = self.client.validate_config(configs["hyprland.conf"])
        self.assertTrue(val["valid"])
        self.assertGreaterEqual(val["total_lines"], 40)
        self.assertGreaterEqual(val["sections_count"], 4)

    def test_11_sovereign_12_phase_lifecycle(self):
        manifest = self.orchestrator.do_everything()
        self.assertEqual(manifest["total_phases"], 12)
        self.assertEqual(manifest["passed_phases"], 12)
        self.assertEqual(manifest["overall_status"], "SOVEREIGN_CERTIFIED")
        self.assertLess(manifest["total_duration_seconds"], 2.0)

        # Verify manifest JSON file on disk
        self.assertTrue(os.path.exists(self.client.config.manifest_path))
        with open(self.client.config.manifest_path, "r", encoding="utf-8") as f:
            disk_data = json.load(f)
        self.assertEqual(disk_data["overall_status"], "SOVEREIGN_CERTIFIED")
        self.assertEqual(len(disk_data["phases"]), 12)


if __name__ == "__main__":
    unittest.main()
