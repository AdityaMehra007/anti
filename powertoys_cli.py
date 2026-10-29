#!/usr/bin/env python3
"""
Microsoft PowerToys Universal CLI
=================================
Command-line interface for managing and testing Microsoft PowerToys utilities,
window layouts, Awake power policies, PowerToys Run launcher, and the 12-phase sovereign lifecycle.

Usage:
  python powertoys_cli.py info
  python powertoys_cli.py modules
  python powertoys_cli.py toggle FancyZones --disable
  python powertoys_cli.py fancyzones --layout priority-grid-01 --resolution 3840x2160
  python powertoys_cli.py awake --mode indefinite --keep-display
  python powertoys_cli.py run-launcher "sqrt(144) + 12"
  python powertoys_cli.py keyboard
  python powertoys_cli.py keyboard --remap-key CapsLock LeftCtrl
  python powertoys_cli.py hosts
  python powertoys_cli.py hosts --add 127.0.0.1 local.api.test "Dev API"
  python powertoys_cli.py advanced-paste --text "user_account_id" --format snake_to_camel
  python powertoys_cli.py workspaces --launch "Full-Stack Dev"
  python powertoys_cli.py ocr --bbox 100 100 600 400
  python powertoys_cli.py security-audit
  python powertoys_cli.py benchmark --iterations 2000
  python powertoys_cli.py do-everything
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List

from powertoys_orchestrator import PowerToysOrchestrator


def format_json(data: object) -> str:
    return json.dumps(data, indent=2)


def main(args: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="powertoys_cli",
        description="Microsoft PowerToys Sovereign Autonomous CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Subcommand: info
    subparsers.add_parser("info", help="Display PowerToys runtime telemetry and status")

    # Subcommand: modules
    subparsers.add_parser("modules", help="List all 24 PowerToys utility modules")

    # Subcommand: toggle
    toggle_p = subparsers.add_parser("toggle", help="Toggle a PowerToys utility module on or off")
    toggle_p.add_argument("module", help="Name of module (e.g. FancyZones, Awake, Peek)")
    toggle_p.add_argument("--enable", action="store_true", help="Explicitly enable the module")
    toggle_p.add_argument("--disable", action="store_true", help="Explicitly disable the module")

    # Subcommand: fancyzones
    fz_p = subparsers.add_parser("fancyzones", help="Calculate FancyZones layout coordinates")
    fz_p.add_argument("--layout", default="priority-grid-01", help="Layout ID")
    fz_p.add_argument("--resolution", default="1920x1080", help="Display resolution (e.g. 1920x1080, 3840x2160, 5120x1440)")

    # Subcommand: awake
    awake_p = subparsers.add_parser("awake", help="Configure Awake power stay-awake policy")
    awake_p.add_argument("--mode", choices=["passive", "indefinite", "timed"], default="indefinite", help="Awake mode")
    awake_p.add_argument("--minutes", type=int, default=60, help="Duration in minutes (for timed mode)")
    awake_p.add_argument("--keep-display", action="store_true", default=True, help="Keep display on")

    # Subcommand: run-launcher
    run_p = subparsers.add_parser("run-launcher", help="Execute a query via PowerToys Run modular launcher")
    run_p.add_argument("query", help="Search query (e.g. 'calc', '100 km in miles', '> ipconfig', 'time')")

    # Subcommand: keyboard
    kbm_p = subparsers.add_parser("keyboard", help="View or add Keyboard Manager remaps")
    kbm_p.add_argument("--remap-key", nargs=2, metavar=("ORIGINAL", "TARGET"), help="Remap a physical key")

    # Subcommand: hosts
    hosts_p = subparsers.add_parser("hosts", help="Inspect or add Windows hosts DNS entries")
    hosts_p.add_argument("--add", nargs=3, metavar=("IP", "HOSTNAME", "COMMENT"), help="Add a new DNS record")

    # Subcommand: advanced-paste
    paste_p = subparsers.add_parser("advanced-paste", help="Transform clipboard text via Advanced Paste pipeline")
    paste_p.add_argument("--text", required=True, help="Input string")
    paste_p.add_argument("--format", choices=["plain_text", "json_prettify", "json_minify", "markdown_to_json", "snake_to_camel", "camel_to_snake", "redact_pii", "ai_summary"], default="plain_text", help="Transformation preset")

    # Subcommand: workspaces
    ws_p = subparsers.add_parser("workspaces", help="Manage multi-application workspaces")
    ws_p.add_argument("--launch", metavar="NAME", default="Full-Stack Dev", help="Launch a workspace by name")

    # Subcommand: ocr
    ocr_p = subparsers.add_parser("ocr", help="Simulate Text Extractor OCR bounding box extraction")
    ocr_p.add_argument("--bbox", nargs=4, type=int, default=[100, 100, 600, 400], metavar=("X", "Y", "W", "H"), help="Screen coordinates bounding box")

    # Subcommand: security-audit
    subparsers.add_parser("security-audit", help="Run CIS Windows Workstation & PowerToys security hardening audit")

    # Subcommand: benchmark
    bench_p = subparsers.add_parser("benchmark", help="Run microsecond latency and throughput benchmarks")
    bench_p.add_argument("--iterations", type=int, default=1000, help="Iteration count")

    # Subcommand: do-everything
    subparsers.add_parser("do-everything", help="Execute complete 12-Phase Sovereign PowerToys Lifecycle")

    parsed = parser.parse_args(args)
    if not parsed.command:
        parser.print_help()
        return 0

    orchestrator = PowerToysOrchestrator()

    if parsed.command == "info":
        print(format_json(orchestrator.get_info()))

    elif parsed.command == "modules":
        print(format_json(orchestrator.list_modules()))

    elif parsed.command == "toggle":
        state = None
        if parsed.enable:
            state = True
        elif parsed.disable:
            state = False
        res = orchestrator.toggle_module(parsed.module, state)
        print(format_json(res))

    elif parsed.command == "fancyzones":
        try:
            w_str, h_str = parsed.resolution.lower().split("x")
            res_tuple = (int(w_str), int(h_str))
        except Exception:
            res_tuple = (1920, 1080)
        res = orchestrator.calculate_fancyzones(parsed.layout, res_tuple)
        print(format_json(res))

    elif parsed.command == "awake":
        res = orchestrator.set_awake(parsed.mode, parsed.minutes, parsed.keep_display)
        print(format_json(res))

    elif parsed.command == "run-launcher":
        res = orchestrator.query_pt_run(parsed.query)
        print(format_json(res))

    elif parsed.command == "keyboard":
        if parsed.remap_key:
            orig, tgt = parsed.remap_key
            res = orchestrator.add_key_remap(orig, tgt)
            print(format_json(res))
        else:
            print(format_json(orchestrator.get_keyboard_remaps()))

    elif parsed.command == "hosts":
        if parsed.add:
            ip, host, comment = parsed.add
            res = orchestrator.add_hosts(ip, host, comment)
            print(format_json(res))
        else:
            print(format_json(orchestrator.get_hosts()))

    elif parsed.command == "advanced-paste":
        res = orchestrator.transform_paste(parsed.text, parsed.format)
        print(format_json(res))

    elif parsed.command == "workspaces":
        res = orchestrator.launch_workspace(parsed.launch)
        print(format_json(res))

    elif parsed.command == "ocr":
        x, y, w, h = parsed.bbox
        res = orchestrator.extract_ocr((x, y, w, h))
        print(format_json(res))

    elif parsed.command == "security-audit":
        print(format_json(orchestrator.audit_security()))

    elif parsed.command == "benchmark":
        print(format_json(orchestrator.benchmark(parsed.iterations)))

    elif parsed.command == "do-everything":
        print(format_json(orchestrator.do_everything()))

    return 0


if __name__ == "__main__":
    sys.exit(main())
