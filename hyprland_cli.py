#!/usr/bin/env python3
"""
Hyprland Universal Autonomous CLI
=================================
Command-line interface for managing Hyprland displays, dynamic workspaces,
client windows, window rules, visual aesthetics (dual-kawase blur, shadows, rounding),
cubic-bezier animations, real-time IPC socket2 event stream, and executing the
12-Phase Sovereign Lifecycle.

Usage:
  python hyprland_cli.py info
  python hyprland_cli.py monitors
  python hyprland_cli.py workspaces
  python hyprland_cli.py clients
  python hyprland_cli.py active-window
  python hyprland_cli.py dispatch workspace 2
  python hyprland_cli.py dispatch togglefloating
  python hyprland_cli.py dispatch killactive
  python hyprland_cli.py keyword decoration:rounding 12
  python hyprland_cli.py decorations [--rounding 12] [--blur-size 8] [--blur-passes 3]
  python hyprland_cli.py rules
  python hyprland_cli.py add-rule "opacity 0.9" "class:^(alacritty)$"
  python hyprland_cli.py animations
  python hyprland_cli.py devices
  python hyprland_cli.py config-generate [--output-dir hyprland/configs]
  python hyprland_cli.py config-validate [--file hyprland/configs/hyprland.conf]
  python hyprland_cli.py events [--limit 10]
  python hyprland_cli.py do-everything
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Optional
from dataclasses import asdict

from hyprland_orchestrator import HyprlandClient, HyprlandConfig, HyprlandOrchestrator


def format_json(data: object) -> str:
    return json.dumps(data, indent=2, default=str)


def main(args: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hyprland_cli",
        description="Hyprland Sovereign Autonomous CLI (hyprwm/Hyprland)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # info
    subparsers.add_parser("info", help="Display compositor telemetry and connection status")

    # monitors
    subparsers.add_parser("monitors", help="List display outputs and geometries")

    # workspaces
    subparsers.add_parser("workspaces", help="List active and persistent workspaces")

    # clients
    subparsers.add_parser("clients", help="List all open client windows")

    # active-window
    subparsers.add_parser("active-window", help="Inspect currently focused window")

    # dispatch
    disp_p = subparsers.add_parser("dispatch", help="Dispatch a compositor action")
    disp_p.add_argument("action", help="Dispatcher name (e.g. workspace, killactive, togglefloating, exec)")
    disp_p.add_argument("argument", nargs="?", default="", help="Dispatcher argument")

    # keyword
    kw_p = subparsers.add_parser("keyword", help="Modify dynamic runtime parameter")
    kw_p.add_argument("key", help="Configuration key (e.g. decoration:rounding)")
    kw_p.add_argument("value", help="Configuration value")

    # decorations
    dec_p = subparsers.add_parser("decorations", help="Inspect or update visual bling")
    dec_p.add_argument("--rounding", type=int, help="Corner rounding radius")
    dec_p.add_argument("--blur-size", type=int, help="Blur size in pixels")
    dec_p.add_argument("--blur-passes", type=int, help="Number of blur downsample passes")
    dec_p.add_argument("--active-border", type=str, help="Active border gradient string")
    dec_p.add_argument("--drop-shadow", choices=["true", "false"], help="Enable/disable drop shadow")

    # rules
    subparsers.add_parser("rules", help="List window rules")

    # add-rule
    ar_p = subparsers.add_parser("add-rule", help="Add a dynamic window rule")
    ar_p.add_argument("rule_type", help="Rule type (e.g. float, opacity 0.9, workspace 3)")
    ar_p.add_argument("pattern", help="Matcher pattern (e.g. class:^(kitty)$)")

    # animations
    subparsers.add_parser("animations", help="List Bezier curves and animation rules")

    # devices
    subparsers.add_parser("devices", help="List input devices (keyboards, mice, touchpads)")

    # config-generate
    cg_p = subparsers.add_parser("config-generate", help="Synthesize modular configuration files")
    cg_p.add_argument("--output-dir", "-o", default=os.path.join("hyprland", "configs"), help="Directory to save configs")

    # config-validate
    cv_p = subparsers.add_parser("config-validate", help="Validate a configuration file")
    cv_p.add_argument("--file", "-f", default=os.path.join("hyprland", "configs", "hyprland.conf"), help="Config file path")

    # events
    ev_p = subparsers.add_parser("events", help="Query real-time event stream buffer")
    ev_p.add_argument("--limit", type=int, default=10, help="Number of recent events to display")

    # do-everything
    subparsers.add_parser("do-everything", help="Execute Complete 12-Phase Sovereign Lifecycle")

    parsed = parser.parse_args(args)
    if not parsed.command:
        parser.print_help()
        return 0

    client = HyprlandClient()

    if parsed.command == "info":
        info = client.get_info()
        print(format_json(asdict(info)))

    elif parsed.command == "monitors":
        monitors = client.get_monitors()
        print(format_json([asdict(m) for m in monitors]))

    elif parsed.command == "workspaces":
        workspaces = client.get_workspaces()
        print(format_json([asdict(w) for w in workspaces]))

    elif parsed.command == "clients":
        clients = client.get_clients()
        print(format_json([asdict(c) for c in clients]))

    elif parsed.command == "active-window":
        active = client.get_active_window()
        if active:
            print(format_json(asdict(active)))
        else:
            print(json.dumps({"active_window": None}))

    elif parsed.command == "dispatch":
        res = client.dispatch(parsed.action, parsed.argument)
        print(format_json(res))

    elif parsed.command == "keyword":
        res = client.set_keyword(parsed.key, parsed.value)
        print(format_json(res))

    elif parsed.command == "decorations":
        updates = {}
        if parsed.rounding is not None:
            updates["rounding"] = parsed.rounding
        if parsed.blur_size is not None:
            updates["blur_size"] = parsed.blur_size
        if parsed.blur_passes is not None:
            updates["blur_passes"] = parsed.blur_passes
        if parsed.active_border is not None:
            updates["active_border"] = parsed.active_border
        if parsed.drop_shadow is not None:
            updates["drop_shadow"] = parsed.drop_shadow == "true"

        if updates:
            decs = client.set_decorations(**updates)
            print(format_json(asdict(decs)))
        else:
            print(format_json(asdict(client.state_store.decorations)))

    elif parsed.command == "rules":
        rules = client.state_store.window_rules
        print(format_json([asdict(r) for r in rules]))

    elif parsed.command == "add-rule":
        rule = client.add_window_rule(parsed.rule_type, parsed.pattern)
        print(format_json(asdict(rule)))

    elif parsed.command == "animations":
        res = {
            "beziers": [asdict(b) for b in client.state_store.beziers.values()],
            "rules": [asdict(r) for r in client.state_store.animation_rules.values()]
        }
        print(format_json(res))

    elif parsed.command == "devices":
        devices = client.state_store.input_devices
        print(format_json([asdict(d) for d in devices]))

    elif parsed.command == "config-generate":
        configs = client.generate_modular_config()
        os.makedirs(parsed.output_dir, exist_ok=True)
        for fname, content in configs.items():
            fpath = os.path.join(parsed.output_dir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Generated: {fpath} ({len(content.splitlines())} lines)")

    elif parsed.command == "config-validate":
        if not os.path.exists(parsed.file):
            print(f"File not found: {parsed.file}")
            return 1
        with open(parsed.file, "r", encoding="utf-8") as f:
            content = f.read()
        res = client.validate_config(content)
        print(format_json(res))

    elif parsed.command == "events":
        events = client.get_events()
        recent = events[-parsed.limit:] if len(events) >= parsed.limit else events
        print(format_json(recent))

    elif parsed.command == "do-everything":
        print("=" * 70)
        print("  OMEGA HYPRLAND SOVEREIGN LIFECYCLE EXECUTION")
        print("=" * 70)
        orch = HyprlandOrchestrator(client)
        manifest = orch.do_everything()
        for p in manifest["phases"]:
            print(f"  Phase {p['phase']:02d}: {p['name']:<58} [{p['status']}] ({p['duration_ms']}ms)")
        print("-" * 70)
        print(f"  Status:   {manifest['overall_status']}")
        print(f"  Score:    {manifest['passed_phases']}/{manifest['total_phases']} Phases Passed")
        print(f"  Duration: {manifest['total_duration_seconds']}s")
        print(f"  Manifest: {client.config.manifest_path}")
        print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
