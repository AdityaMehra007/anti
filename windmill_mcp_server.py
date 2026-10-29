#!/usr/bin/env python3
"""
Windmill Autonomous MCP (Model Context Protocol) Server
======================================================
Exposes Windmill Developer Platform & Workflow Engine capabilities to AI agents,
subagents, and LLMs via standard JSON-RPC stdio protocol.

Supported tools:
- windmill_get_system_info
- windmill_list_workspaces
- windmill_list_scripts
- windmill_get_script
- windmill_run_script
- windmill_list_flows
- windmill_get_flow
- windmill_execute_flow
- windmill_list_jobs
- windmill_get_job_status
- windmill_approve_job
- windmill_list_resources
- windmill_create_resource
- windmill_list_apps
- windmill_search_hub
- windmill_import_hub_flow
"""

import sys
import json
import logging
from typing import Any, Dict

from windmill_orchestrator import WindmillClient, WindmillOrchestrator

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("windmill_mcp")

client = WindmillClient()
orchestrator = WindmillOrchestrator(client)

TOOLS = [
    {
        "name": "windmill_get_system_info",
        "description": "Get real-time telemetry, worker nodes count, active concurrency, and overall health of the Windmill cluster.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "windmill_list_workspaces",
        "description": "List all multi-tenant workspaces, subscription tiers, and owner accounts.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "windmill_list_scripts",
        "description": "List all runnable scripts (Python, TypeScript, SQL, Bash) registered in the workspace.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "windmill_get_script",
        "description": "Inspect metadata, parameter schema, summary, and language for a specific script.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "script_path": {"type": "string", "description": "Script path (e.g. 'u/admin/cbam_carbon_audit')"}
            },
            "required": ["script_path"]
        }
    },
    {
        "name": "windmill_run_script",
        "description": "Execute a Python, TypeScript, SQL, or Bash script with JSON arguments in a sandboxed worker.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "script_path": {"type": "string", "description": "Script path (e.g. 'u/admin/cbam_carbon_audit')"},
                "args": {"type": "object", "default": {}, "description": "Arguments dictionary matching script schema"}
            },
            "required": ["script_path"]
        }
    },
    {
        "name": "windmill_list_flows",
        "description": "List all composed DAG workflows with their step counts and descriptions.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "windmill_get_flow",
        "description": "Inspect workflow DAG definition, topological steps, branch conditions, and input transforms.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "flow_path": {"type": "string", "description": "Flow path (e.g. 'u/admin/enterprise_client_onboarding_dag')"}
            },
            "required": ["flow_path"]
        }
    },
    {
        "name": "windmill_execute_flow",
        "description": "Trigger execution of a multi-step DAG flow with inputs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "flow_path": {"type": "string", "description": "Flow path (e.g. 'u/admin/enterprise_client_onboarding_dag')"},
                "args": {"type": "object", "default": {}, "description": "Input arguments for the workflow"}
            },
            "required": ["flow_path"]
        }
    },
    {
        "name": "windmill_list_jobs",
        "description": "List recent job executions, filter by status (COMPLETED, SUSPENDED, ERROR), with duration telemetry.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 20, "description": "Max number of jobs"},
                "status": {"type": "string", "description": "Filter by status: COMPLETED, SUSPENDED, ERROR"}
            }
        }
    },
    {
        "name": "windmill_get_job_status",
        "description": "Retrieve status, runtime duration, output result, and execution logs for a specific job.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "job_id": {"type": "string", "description": "The Windmill Job ID"}
            },
            "required": ["job_id"]
        }
    },
    {
        "name": "windmill_approve_job",
        "description": "Resume or reject a suspended workflow job awaiting executive human sign-off.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "job_id": {"type": "string", "description": "The suspended Job ID"},
                "approved": {"type": "boolean", "default": True, "description": "True to approve and resume, False to reject"},
                "notes": {"type": "string", "default": "", "description": "Audit notes for executive sign-off"}
            },
            "required": ["job_id"]
        }
    },
    {
        "name": "windmill_list_resources",
        "description": "List typed resources (PostgreSQL, Slack, OpenAI, AWS S3) configured in the workspace.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "windmill_create_resource",
        "description": "Create a new typed resource with credentials or configuration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Resource path (e.g. 'u/admin/db_custom')"},
                "resource_type": {"type": "string", "description": "Type: postgresql, slack, openai, s3, etc."},
                "value": {"type": "object", "description": "Resource payload credentials dictionary"},
                "description": {"type": "string", "default": "", "description": "Optional summary"}
            },
            "required": ["path", "resource_type", "value"]
        }
    },
    {
        "name": "windmill_list_apps",
        "description": "List low-code applications built with Windmill App Builder.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "windmill_search_hub",
        "description": "Search the Windmill Hub catalog of 40+ curated community scripts, integrations, and flows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "default": "", "description": "Search query keyword"},
                "category": {"type": "string", "default": "", "description": "Category filter"}
            }
        }
    },
    {
        "name": "windmill_import_hub_flow",
        "description": "Import an open-source template or integration directly from the Windmill Hub into local workspace.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hub_id": {"type": "string", "description": "Hub item ID (e.g. 'hub/scripts/slack_post_message')"}
            },
            "required": ["hub_id"]
        }
    },
    {
        "name": "windmill_list_schedules",
        "description": "List all registered automated cron schedules and trigger configurations.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "windmill_trigger_schedule",
        "description": "Trigger an automated cron schedule run immediately on demand.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Schedule path (e.g. 'u/admin/hourly_carbon_audit_schedule')"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "windmill_list_variables",
        "description": "List workspace configuration variables and encrypted secrets.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "windmill_set_variable",
        "description": "Set or update a workspace variable or secret.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Variable path"},
                "value": {"description": "Variable value"},
                "is_secret": {"type": "boolean", "default": False, "description": "Whether to encrypt as secret"},
                "description": {"type": "string", "default": "", "description": "Description"}
            },
            "required": ["path", "value"]
        }
    },
    {
        "name": "windmill_do_everything",
        "description": "Execute complete 12-phase sovereign Windmill workflow and developer platform cycle.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]


def handle_tool_call(name: str, args: Dict[str, Any]) -> Any:
    if name == "windmill_get_system_info":
        return client.get_telemetry()
    elif name == "windmill_list_workspaces":
        return client.list_workspaces()
    elif name == "windmill_list_scripts":
        return client.list_scripts()
    elif name == "windmill_get_script":
        return client.get_script(args["script_path"])
    elif name == "windmill_run_script":
        return client.run_script(args["script_path"], args.get("args", {}))
    elif name == "windmill_list_flows":
        return client.list_flows()
    elif name == "windmill_get_flow":
        return client.get_flow(args["flow_path"])
    elif name == "windmill_execute_flow":
        return client.execute_flow(args["flow_path"], args.get("args", {}))
    elif name == "windmill_list_jobs":
        return client.list_jobs(limit=args.get("limit", 20), status=args.get("status"))
    elif name == "windmill_get_job_status":
        return client.get_job(args["job_id"])
    elif name == "windmill_approve_job":
        return client.approve_job(args["job_id"], approved=args.get("approved", True), notes=args.get("notes", ""))
    elif name == "windmill_list_resources":
        return client.list_resources()
    elif name == "windmill_create_resource":
        return client.create_resource(
            path=args["path"],
            resource_type=args["resource_type"],
            value=args["value"],
            description=args.get("description", "")
        )
    elif name == "windmill_list_apps":
        return client.list_apps()
    elif name == "windmill_search_hub":
        return client.search_hub(query=args.get("query", ""), category=args.get("category", ""))
    elif name == "windmill_import_hub_flow":
        return client.import_from_hub(args["hub_id"])
    elif name == "windmill_list_schedules":
        return client.list_schedules()
    elif name == "windmill_trigger_schedule":
        return client.trigger_schedule(args["path"])
    elif name == "windmill_list_variables":
        return client.list_variables()
    elif name == "windmill_set_variable":
        return client.set_variable(
            path=args["path"],
            value=args["value"],
            is_secret=args.get("is_secret", False),
            description=args.get("description", "")
        )
    elif name == "windmill_do_everything":
        return orchestrator.do_everything()
    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    """Main JSON-RPC stdio protocol loop."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            try:
                output = handle_tool_call(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(output, indent=2)}]
                    }
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "windmill-mcp-server", "version": "1.0.0"}
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
