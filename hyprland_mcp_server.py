#!/usr/bin/env python3
"""
Hyprland Autonomous MCP (Model Context Protocol) Server
======================================================
Exposes Hyprland Autonomous Suite (monitors, dynamic workspaces, client windows,
window rules, visual bling & blurs, cubic-bezier animations, real-time events,
and 12-phase sovereign lifecycle) to AI agents, subagents, and LLMs
via standard JSON-RPC 2.0 stdio protocol.

Supported tools:
- hyprland_get_info
- hyprland_list_monitors
- hyprland_list_workspaces
- hyprland_list_clients
- hyprland_get_active_window
- hyprland_dispatch_command
- hyprland_switch_workspace
- hyprland_move_to_workspace
- hyprland_kill_active
- hyprland_toggle_floating
- hyprland_set_decoration
- hyprland_set_animation
- hyprland_add_window_rule
- hyprland_generate_config
- hyprland_stream_events
- hyprland_do_everything
"""

from __future__ import annotations

import sys
import json
import logging
from typing import Any, Dict
from dataclasses import asdict

from hyprland_orchestrator import HyprlandClient, HyprlandOrchestrator

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("hyprland_mcp")

client = HyprlandClient()
orchestrator = HyprlandOrchestrator(client)

TOOLS = [
    {
        "name": "hyprland_get_info",
        "description": "Get real-time Hyprland compositor telemetry, version, Aquamarine backend version, active signature, and window counts.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "hyprland_list_monitors",
        "description": "List all active display outputs, resolutions, refresh rates, scaling factors, and VRR states.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "hyprland_list_workspaces",
        "description": "List all active workspaces with monitor binding, window count, and fullscreen status.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "hyprland_list_clients",
        "description": "List all managed client windows with address, class, title, PID, geometry, and tiled/floating status.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "hyprland_get_active_window",
        "description": "Get detailed attributes of the currently focused client window.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "hyprland_dispatch_command",
        "description": "Dispatch any Hyprland compositor action (e.g. 'workspace 3', 'killactive', 'togglefloating', 'exec kitty').",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Dispatcher name (e.g. workspace, killactive, togglefloating, exec)"},
                "argument": {"type": "string", "description": "Optional argument for the dispatcher"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "hyprland_switch_workspace",
        "description": "Switch active desktop focus to specified workspace ID or name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace_id": {"type": "string", "description": "Workspace ID (e.g. '2' or 'special:scratchpad')"}
            },
            "required": ["workspace_id"]
        }
    },
    {
        "name": "hyprland_move_to_workspace",
        "description": "Move the currently focused window to a target workspace.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace_id": {"type": "string", "description": "Target workspace ID"}
            },
            "required": ["workspace_id"]
        }
    },
    {
        "name": "hyprland_kill_active",
        "description": "Terminate the currently focused client window.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "hyprland_toggle_floating",
        "description": "Toggle floating state of the currently focused client window.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "hyprland_set_decoration",
        "description": "Configure visual bling properties (rounding, dual-kawase blur size/passes, drop shadow, and active/inactive gradient border).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rounding": {"type": "integer", "description": "Corner radius in pixels"},
                "blur_size": {"type": "integer", "description": "Kawase blur radius"},
                "blur_passes": {"type": "integer", "description": "Blur downsampling iterations"},
                "active_border": {"type": "string", "description": "Gradient string (e.g. 'rgba(33ccffee) rgba(00ff99ee) 45deg')"},
                "drop_shadow": {"type": "boolean", "description": "Enable drop shadows"}
            }
        }
    },
    {
        "name": "hyprland_set_animation",
        "description": "Configure or register a window/workspace animation rule and cubic-bezier curve.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Animation target (e.g. windows, workspaces, fade, border)"},
                "enabled": {"type": "boolean", "description": "Enable/disable animation"},
                "speed": {"type": "integer", "description": "Speed factor"},
                "curve": {"type": "string", "description": "Bézier curve name (e.g. myBezier, smoothOut, default)"},
                "style": {"type": "string", "description": "Optional animation style (e.g. 'popin 80%', 'slide')"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "hyprland_add_window_rule",
        "description": "Add a dynamic windowrulev2 placement or behavior rule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rule_type": {"type": "string", "description": "Rule action (e.g. 'float', 'opacity 0.9', 'workspace 3')"},
                "pattern": {"type": "string", "description": "Window match regex (e.g. 'class:^(kitty)$')"}
            },
            "required": ["rule_type", "pattern"]
        }
    },
    {
        "name": "hyprland_generate_config",
        "description": "Synthesize a complete modular Hyprland configuration set (hyprland.conf, decoration.conf, animations.conf, monitors.conf, windowrules.conf, keybinds.conf).",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "hyprland_stream_events",
        "description": "Fetch real-time socket2 event buffer since a given sequence ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "since_id": {"type": "integer", "description": "Starting event sequence ID (default: 0)"}
            }
        }
    },
    {
        "name": "hyprland_do_everything",
        "description": "Execute the Complete 12-Phase Sovereign Hyprland Lifecycle certification and emit cryptographic manifest.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]


def handle_tool_call(name: str, args: Dict[str, Any]) -> Any:
    if name == "hyprland_get_info":
        return asdict(client.get_info())

    elif name == "hyprland_list_monitors":
        return [asdict(m) for m in client.get_monitors()]

    elif name == "hyprland_list_workspaces":
        return [asdict(w) for w in client.get_workspaces()]

    elif name == "hyprland_list_clients":
        return [asdict(c) for c in client.get_clients()]

    elif name == "hyprland_get_active_window":
        act = client.get_active_window()
        return asdict(act) if act else None

    elif name == "hyprland_dispatch_command":
        return client.dispatch(args.get("action", ""), args.get("argument", ""))

    elif name == "hyprland_switch_workspace":
        return client.dispatch("workspace", str(args.get("workspace_id", "1")))

    elif name == "hyprland_move_to_workspace":
        return client.dispatch("movetoworkspace", str(args.get("workspace_id", "1")))

    elif name == "hyprland_kill_active":
        return client.dispatch("killactive")

    elif name == "hyprland_toggle_floating":
        return client.dispatch("togglefloating")

    elif name == "hyprland_set_decoration":
        decs = client.set_decorations(**args)
        return asdict(decs)

    elif name == "hyprland_set_animation":
        rule = client.set_animation(
            name=args.get("name", "windows"),
            enabled=args.get("enabled", True),
            speed=int(args.get("speed", 7)),
            curve=args.get("curve", "default"),
            style=args.get("style", "")
        )
        return asdict(rule)

    elif name == "hyprland_add_window_rule":
        rule = client.add_window_rule(args.get("rule_type", ""), args.get("pattern", ""))
        return asdict(rule)

    elif name == "hyprland_generate_config":
        return client.generate_modular_config()

    elif name == "hyprland_stream_events":
        return client.get_events(since_id=args.get("since_id", 0))

    elif name == "hyprland_do_everything":
        return orchestrator.do_everything()

    raise ValueError(f"Unknown tool: {name}")


def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": TOOLS}
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            t_name = params.get("name")
            t_args = params.get("arguments", {})
            try:
                out = handle_tool_call(t_name, t_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(out, indent=2, default=str)}
                        ]
                    }
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "hyprland-mcp-server", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
