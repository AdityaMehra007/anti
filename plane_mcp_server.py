#!/usr/bin/env python3
"""
Plane Autonomous MCP (Model Context Protocol) Server
===================================================
Exposes Plane Autonomous Suite (workspaces, projects, issues, cycles, modules,
pages, triage, analytics, and 12-phase lifecycle) to AI agents, subagents, and LLMs
via standard JSON-RPC 2.0 stdio protocol.

Supported tools:
- plane_get_info
- plane_list_workspaces
- plane_list_projects
- plane_create_project
- plane_list_issues
- plane_create_issue
- plane_update_issue
- plane_list_cycles
- plane_create_cycle
- plane_get_burndown
- plane_list_modules
- plane_create_module
- plane_list_pages
- plane_create_page
- plane_list_triage
- plane_triage_action
- plane_get_analytics
- plane_do_everything
"""

import sys
import json
import logging
from typing import Any, Dict

from plane_orchestrator import PlaneOrchestrator

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("plane_mcp")

orchestrator = PlaneOrchestrator()

TOOLS = [
    {
        "name": "plane_get_info",
        "description": "Get real-time Plane system telemetry, version, connection mode (live vs mock), and entity counts.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "plane_list_workspaces",
        "description": "List all accessible workspaces with slug, owner, and company size.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "plane_list_projects",
        "description": "List projects in the specified or default workspace.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace_slug": {"type": "string", "description": "Optional workspace slug (defaults to configured workspace, e.g. omega)"}
            }
        }
    },
    {
        "name": "plane_create_project",
        "description": "Create a new project within a workspace with identifier and description.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Project title"},
                "identifier": {"type": "string", "description": "Uppercase identifier code (e.g. CORE, SEC, FLEET)"},
                "description": {"type": "string", "description": "Project scope description"},
                "emoji": {"type": "string", "description": "Icon emoji (default: ⚡)"},
                "workspace_slug": {"type": "string", "description": "Workspace slug"}
            },
            "required": ["name", "identifier"]
        }
    },
    {
        "name": "plane_list_issues",
        "description": "List and filter issues/work items by project ID, cycle ID, or state group.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "Filter by project ID"},
                "cycle_id": {"type": "string", "description": "Filter by sprint cycle ID"},
                "state_group": {"type": "string", "description": "Filter by group (backlog, unstarted, started, completed, cancelled)"}
            }
        }
    },
    {
        "name": "plane_create_issue",
        "description": "Create a new work item / issue with priority, story point estimate, and cycle attachment.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Issue title"},
                "project_id": {"type": "string", "description": "Target project ID"},
                "description_html": {"type": "string", "description": "Rich HTML / Markdown description"},
                "priority": {"type": "string", "enum": ["urgent", "high", "medium", "low", "none"], "description": "Priority tier"},
                "estimate_point": {"type": "integer", "description": "Fibonacci story point estimate"},
                "cycle_id": {"type": "string", "description": "Sprint cycle ID to attach"},
                "module_id": {"type": "string", "description": "Epic module ID to attach"}
            },
            "required": ["name", "project_id"]
        }
    },
    {
        "name": "plane_update_issue",
        "description": "Update properties of an existing issue (state, priority, assignees).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "issue_id": {"type": "string", "description": "ID of issue to update"},
                "updates": {"type": "object", "description": "Dictionary of fields to update"}
            },
            "required": ["issue_id", "updates"]
        }
    },
    {
        "name": "plane_list_cycles",
        "description": "List sprint cycles for a project with start/end dates, total points, and progress.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "Target project ID"}
            }
        }
    },
    {
        "name": "plane_create_cycle",
        "description": "Create a new sprint cycle with date bounds.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Cycle name (e.g. Sprint 26)"},
                "project_id": {"type": "string", "description": "Project ID"},
                "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                "description": {"type": "string", "description": "Cycle objective"}
            },
            "required": ["name", "project_id", "start_date", "end_date"]
        }
    },
    {
        "name": "plane_get_burndown",
        "description": "Calculate burndown chart points, weekly velocity, and on-track status for a cycle.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cycle_id": {"type": "string", "description": "Sprint cycle ID"}
            },
            "required": ["cycle_id"]
        }
    },
    {
        "name": "plane_list_modules",
        "description": "List epic milestone modules and their completion percentages.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "Target project ID"}
            }
        }
    },
    {
        "name": "plane_create_module",
        "description": "Create a high-level epic module milestone.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Module title"},
                "project_id": {"type": "string", "description": "Project ID"},
                "description": {"type": "string", "description": "Module scope description"},
                "lead_id": {"type": "string", "description": "Lead assignee ID"},
                "target_date": {"type": "string", "description": "Target delivery date (YYYY-MM-DD)"}
            },
            "required": ["name", "project_id"]
        }
    },
    {
        "name": "plane_list_pages",
        "description": "List collaborative knowledge base documentation pages in a project.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "Target project ID"}
            }
        }
    },
    {
        "name": "plane_create_page",
        "description": "Create a collaborative knowledge base documentation page.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Page title"},
                "description_html": {"type": "string", "description": "Rich HTML or Markdown text"},
                "project_id": {"type": "string", "description": "Project ID"},
                "summary_ai": {"type": "string", "description": "AI summary of documentation"}
            },
            "required": ["title", "description_html", "project_id"]
        }
    },
    {
        "name": "plane_list_triage",
        "description": "List incoming triage requests waiting for promotion or rejection.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "Target project ID"}
            }
        }
    },
    {
        "name": "plane_triage_action",
        "description": "Accept (promote to active issue) or reject a triage request.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "triage_id": {"type": "string", "description": "Triage item ID"},
                "action": {"type": "string", "enum": ["accept", "reject"], "description": "Action"}
            },
            "required": ["triage_id", "action"]
        }
    },
    {
        "name": "plane_get_analytics",
        "description": "Calculate project velocity, lead time, cycle time, and workload distribution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "Project ID"}
            }
        }
    },
    {
        "name": "plane_do_everything",
        "description": "Execute the comprehensive 12-Phase Sovereign Plane Lifecycle and generate cryptographic attestation.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]


def handle_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Any:
    if tool_name == "plane_get_info":
        return orchestrator.get_info()

    elif tool_name == "plane_list_workspaces":
        return orchestrator.list_workspaces()

    elif tool_name == "plane_list_projects":
        return orchestrator.list_projects(arguments.get("workspace_slug"))

    elif tool_name == "plane_create_project":
        return orchestrator.create_project(
            name=arguments["name"],
            identifier=arguments["identifier"],
            description=arguments.get("description", ""),
            emoji=arguments.get("emoji", "⚡"),
            workspace_slug=arguments.get("workspace_slug")
        )

    elif tool_name == "plane_list_issues":
        return orchestrator.list_issues(
            project_id=arguments.get("project_id"),
            cycle_id=arguments.get("cycle_id"),
            state_group=arguments.get("state_group")
        )

    elif tool_name == "plane_create_issue":
        return orchestrator.create_issue(
            name=arguments["name"],
            project_id=arguments["project_id"],
            description_html=arguments.get("description_html", ""),
            priority=arguments.get("priority", "medium"),
            estimate_point=arguments.get("estimate_point"),
            cycle_id=arguments.get("cycle_id"),
            module_id=arguments.get("module_id")
        )

    elif tool_name == "plane_update_issue":
        return orchestrator.update_issue(
            issue_id=arguments["issue_id"],
            updates=arguments["updates"]
        )

    elif tool_name == "plane_list_cycles":
        return orchestrator.list_cycles(arguments.get("project_id"))

    elif tool_name == "plane_create_cycle":
        return orchestrator.create_cycle(
            name=arguments["name"],
            project_id=arguments["project_id"],
            start_date=arguments["start_date"],
            end_date=arguments["end_date"],
            description=arguments.get("description", "")
        )

    elif tool_name == "plane_get_burndown":
        return orchestrator.get_burndown(arguments["cycle_id"])

    elif tool_name == "plane_list_modules":
        return orchestrator.list_modules(arguments.get("project_id"))

    elif tool_name == "plane_create_module":
        return orchestrator.create_module(
            name=arguments["name"],
            project_id=arguments["project_id"],
            description=arguments.get("description", ""),
            lead_id=arguments.get("lead_id", "omega-prime"),
            target_date=arguments.get("target_date")
        )

    elif tool_name == "plane_list_pages":
        return orchestrator.list_pages(arguments.get("project_id"))

    elif tool_name == "plane_create_page":
        return orchestrator.create_page(
            title=arguments["title"],
            description_html=arguments["description_html"],
            project_id=arguments["project_id"],
            summary_ai=arguments.get("summary_ai", "")
        )

    elif tool_name == "plane_list_triage":
        return orchestrator.list_triage(arguments.get("project_id"))

    elif tool_name == "plane_triage_action":
        return orchestrator.triage_action(
            triage_id=arguments["triage_id"],
            action=arguments["action"]
        )

    elif tool_name == "plane_get_analytics":
        return orchestrator.get_analytics(arguments.get("project_id"))

    elif tool_name == "plane_do_everything":
        return orchestrator.do_everything()

    raise ValueError(f"Unknown tool: {tool_name}")


def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
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
                            {"type": "text", "text": json.dumps(out, indent=2)}
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
                    "serverInfo": {"name": "plane-mcp-server", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
