#!/usr/bin/env python3
"""
Microsoft PowerToys Autonomous MCP (Model Context Protocol) Server
==================================================================
Exposes Microsoft PowerToys Autonomous Suite to AI agents, subagents, and LLMs
via standard JSON-RPC 2.0 stdio protocol.

Supported tools:
- powertoys_get_status
- powertoys_list_modules
- powertoys_toggle_module
- powertoys_calculate_fancyzones
- powertoys_query_pt_run
- powertoys_set_awake
- powertoys_get_keyboard_remaps
- powertoys_add_key_remap
- powertoys_list_hosts
- powertoys_add_hosts_entry
- powertoys_transform_paste
- powertoys_extract_ocr
- powertoys_launch_workspace
- powertoys_security_audit
- powertoys_benchmark
- powertoys_do_everything
"""

import sys
import json
import logging
from typing import Any, Dict

from powertoys_orchestrator import PowerToysOrchestrator

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("powertoys_mcp")

orchestrator = PowerToysOrchestrator()

TOOLS = [
    {
        "name": "powertoys_get_status",
        "description": "Get real-time PowerToys runner telemetry, version, architecture, active FancyZones layout, and Awake power mode.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powertoys_list_modules",
        "description": "Enumerate all 24 PowerToys utility modules with their enabled statuses, categories, hotkeys, and CPU/memory stats.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powertoys_toggle_module",
        "description": "Enable or disable a specific PowerToys utility module (e.g. FancyZones, PowerToys Run, Awake, Peek, Text Extractor).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "module": {"type": "string", "description": "Module name"},
                "enabled": {"type": "boolean", "description": "Target enabled state (optional, defaults to toggle)"}
            },
            "required": ["module"]
        }
    },
    {
        "name": "powertoys_calculate_fancyzones",
        "description": "Calculate pixel bounding boxes for FancyZones multi-monitor window snapping for standard, 4K, or 32:9 Super UltraWide screens.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "layout_id": {"type": "string", "description": "Layout ID (priority-grid-01, grid-2x2, ultrawide-coder, focus-central)", "default": "priority-grid-01"},
                "resolution": {"type": "string", "description": "Screen resolution formatted as WxH (e.g. 1920x1080, 3840x2160, 5120x1440)", "default": "1920x1080"}
            }
        }
    },
    {
        "name": "powertoys_query_pt_run",
        "description": "Execute a search query through PowerToys Run multi-plugin engine (Calculator, Unit Converter, Programs, Windows, Shell).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Query string (e.g. 'calc', 'sqrt(144) + 10', '100 km in miles', '> ipconfig')"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "powertoys_set_awake",
        "description": "Configure Awake stay-awake policy, keep-display-on assertion, and custom countdown timer.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "enum": ["PASSIVE", "INDEFINITE", "TIMED"], "default": "INDEFINITE"},
                "duration_minutes": {"type": "integer", "description": "Duration in minutes (for TIMED mode)", "default": 60},
                "keep_display_on": {"type": "boolean", "default": True}
            },
            "required": ["mode"]
        }
    },
    {
        "name": "powertoys_get_keyboard_remaps",
        "description": "Retrieve all active Keyboard Manager physical key and shortcut remap rules with collision detection.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powertoys_add_key_remap",
        "description": "Remap a physical key to another target key (e.g., CapsLock -> LeftCtrl).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "original_key": {"type": "string", "description": "Physical key name (e.g. CapsLock, ScrollLock)"},
                "new_key": {"type": "string", "description": "Target key to remap to (e.g. LeftCtrl, Mute)"}
            },
            "required": ["original_key", "new_key"]
        }
    },
    {
        "name": "powertoys_list_hosts",
        "description": "Read and parse the Windows hosts DNS routing table into structured JSON records.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powertoys_add_hosts_entry",
        "description": "Safely add or update a hostname resolution record in the Windows hosts file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ip": {"type": "string", "description": "IPv4 or IPv6 address (e.g. 127.0.0.1)"},
                "host": {"type": "string", "description": "Target hostname (e.g. app.local)"},
                "comment": {"type": "string", "description": "Descriptive comment", "default": ""}
            },
            "required": ["ip", "host"]
        }
    },
    {
        "name": "powertoys_transform_paste",
        "description": "Transform clipboard text via Advanced Paste pipelines (plain_text, markdown_to_json, json_prettify, snake_to_camel, redact_pii, ai_summary).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Raw input string to transform"},
                "transformation": {
                    "type": "string",
                    "enum": ["plain_text", "markdown_to_json", "json_prettify", "json_minify", "snake_to_camel", "camel_to_snake", "redact_pii", "ai_summary"],
                    "default": "plain_text"
                },
                "prompt": {"type": "string", "description": "Custom AI prompt instructions if using ai mode"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "powertoys_extract_ocr",
        "description": "Simulate Text Extractor Optical Character Recognition (OCR) over screen bounding coordinates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bbox": {"type": "array", "items": {"type": "integer"}, "description": "[x, y, width, height] screen rectangle", "default": [100, 100, 600, 400]}
            }
        }
    },
    {
        "name": "powertoys_launch_workspace",
        "description": "Launch a pre-configured multi-application workspace profile into its assigned FancyZones layout.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace_name": {"type": "string", "description": "Workspace name", "default": "Full-Stack Dev"}
            }
        }
    },
    {
        "name": "powertoys_security_audit",
        "description": "Audit PowerToys security boundaries, privacy telemetry opt-out, and hosts file integrity against CIS standards.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powertoys_benchmark",
        "description": "Benchmark microsecond execution latency and throughput for FancyZones snapping, PT Run search, and clipboard transforms.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "iterations": {"type": "integer", "description": "Number of iterations", "default": 1000}
            }
        }
    },
    {
        "name": "powertoys_do_everything",
        "description": "Execute the comprehensive 12-Phase Sovereign PowerToys Lifecycle and output an attested cryptographic manifest.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]


def handle_tool_call(name: str, args: Dict[str, Any]) -> Any:
    if name == "powertoys_get_status":
        return orchestrator.get_info()

    elif name == "powertoys_list_modules":
        return orchestrator.list_modules()

    elif name == "powertoys_toggle_module":
        return orchestrator.toggle_module(args["module"], args.get("enabled"))

    elif name == "powertoys_calculate_fancyzones":
        layout_id = args.get("layout_id", "priority-grid-01")
        res_str = args.get("resolution", "1920x1080")
        try:
            w, h = map(int, res_str.lower().split("x"))
        except Exception:
            w, h = (1920, 1080)
        return orchestrator.calculate_fancyzones(layout_id, (w, h))

    elif name == "powertoys_query_pt_run":
        return orchestrator.query_pt_run(args["query"])

    elif name == "powertoys_set_awake":
        return orchestrator.set_awake(args["mode"], args.get("duration_minutes", 60), args.get("keep_display_on", True))

    elif name == "powertoys_get_keyboard_remaps":
        return orchestrator.get_keyboard_remaps()

    elif name == "powertoys_add_key_remap":
        return orchestrator.add_key_remap(args["original_key"], args["new_key"])

    elif name == "powertoys_list_hosts":
        return orchestrator.get_hosts()

    elif name == "powertoys_add_hosts_entry":
        return orchestrator.add_hosts(args["ip"], args["host"], args.get("comment", ""))

    elif name == "powertoys_transform_paste":
        return orchestrator.transform_paste(args["text"], args.get("transformation", "plain_text"), args.get("prompt"))

    elif name == "powertoys_extract_ocr":
        bbox = tuple(args.get("bbox", [100, 100, 600, 400]))
        return orchestrator.extract_ocr(bbox)

    elif name == "powertoys_launch_workspace":
        return orchestrator.launch_workspace(args.get("workspace_name", "Full-Stack Dev"))

    elif name == "powertoys_security_audit":
        return orchestrator.audit_security()

    elif name == "powertoys_benchmark":
        return orchestrator.benchmark(args.get("iterations", 1000))

    elif name == "powertoys_do_everything":
        return orchestrator.do_everything()

    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        msg_id = req.get("id")
        method = req.get("method")

        if method == "tools/list":
            res = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                result_data = handle_tool_call(name, arguments)
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result_data, indent=2)}]
                    }
                }
            except Exception as e:
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32603, "message": str(e)}
                }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "powertoys-mcp-server", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        else:
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method {method} not found"}
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
