#!/usr/bin/env python3
"""
n8n Autonomous MCP (Model Context Protocol) Server
==================================================
Exposes n8n Workflow Automation Platform & Agent capabilities to AI agents,
subagents, and LLMs via standard JSON-RPC stdio protocol.

Supported tools:
- n8n_get_system_info
- n8n_search_nodes
- n8n_list_nodes_by_group
- n8n_get_node_details
- n8n_list_workflows
- n8n_get_workflow
- n8n_execute_workflow
- n8n_trigger_webhook
- n8n_run_ai_agent
- n8n_list_executions
- n8n_get_execution
- n8n_list_credentials
- n8n_scan_dropzone
- n8n_export_workflows
- n8n_do_everything_lifecycle
"""

import sys
import json
import logging
from typing import Any, Dict

from n8n_orchestrator import N8nClient, N8nOrchestrator

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("n8n_mcp")

client = N8nClient()
orchestrator = N8nOrchestrator(client)

TOOLS = [
    {
        "name": "n8n_get_system_info",
        "description": "Get real-time telemetry, active worker count, concurrency limits, and indexed node/workflow totals for the n8n platform.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "n8n_search_nodes",
        "description": "FTS5 fast full-text search across 560+ core and community n8n nodes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Keyword to search (e.g. 'webhook', 'slack', 'postgres', 'langchain')"},
                "limit": {"type": "integer", "description": "Max results to return (default: 10)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "n8n_list_nodes_by_group",
        "description": "List nodes filtered by functional group (transform, trigger, output, input, utility).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "group": {"type": "string", "description": "Group name (e.g. 'transform', 'trigger')"},
                "limit": {"type": "integer", "description": "Max nodes to return (default: 30)"}
            }
        }
    },
    {
        "name": "n8n_get_node_details",
        "description": "Retrieve comprehensive parameter schema and source file location for an n8n node type.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "node_type": {"type": "string", "description": "Technical name of the node (e.g. 'webhook', 'httpRequest', 'agent')"}
            },
            "required": ["node_type"]
        }
    },
    {
        "name": "n8n_list_workflows",
        "description": "List all active OMEGA production workflows and their node counts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "active_only": {"type": "boolean", "description": "Filter by active status"}
            }
        }
    },
    {
        "name": "n8n_get_workflow",
        "description": "Retrieve the full JSON definition, node DAG graph, and connections for a workflow.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workflow_id_or_name": {"type": "string", "description": "Workflow identifier or human-readable name"}
            },
            "required": ["workflow_id_or_name"]
        }
    },
    {
        "name": "n8n_execute_workflow",
        "description": "Trigger an autonomous execution of an n8n workflow DAG with custom input payload.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workflow_id_or_name": {"type": "string", "description": "Workflow identifier or name"},
                "input_data": {"type": "object", "description": "Input JSON dictionary passed to initial node"}
            },
            "required": ["workflow_id_or_name"]
        }
    },
    {
        "name": "n8n_trigger_webhook",
        "description": "Dispatch an inbound webhook payload to a registered n8n webhook route.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Webhook endpoint path (e.g. 'outreach-dispatch')"},
                "payload": {"type": "object", "description": "Webhook JSON payload"},
                "test_mode": {"type": "boolean", "description": "Whether to trigger test webhook route"}
            },
            "required": ["path", "payload"]
        }
    },
    {
        "name": "n8n_run_ai_agent",
        "description": "Invoke the n8n LangChain Autonomous Agent node with multi-step reasoning, tool execution, and memory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Research or execution query for the agent"},
                "context": {"type": "object", "description": "Session memory or metadata context"}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "n8n_list_executions",
        "description": "Query execution history, status, executed nodes count, and latency.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Filter by status: SUCCESS, ERROR, RUNNING"},
                "limit": {"type": "integer", "description": "Max executions to return (default: 20)"}
            }
        }
    },
    {
        "name": "n8n_get_execution",
        "description": "Retrieve full execution run data including per-node outputs and error traces.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "execution_id": {"type": "string", "description": "Execution UUID (e.g. 'exec-1234')"}
            },
            "required": ["execution_id"]
        }
    },
    {
        "name": "n8n_list_credentials",
        "description": "Inspect registered encrypted credential accounts without leaking secrets.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "n8n_scan_dropzone",
        "description": "Check the local dropzone folder, ingest pending files, and trigger automated processing pipeline.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "n8n_export_workflows",
        "description": "Export all workflow definitions to disaster recovery backup directory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dest_dir": {"type": "string", "description": "Optional custom export folder"}
            }
        }
    },
    {
        "name": "n8n_do_everything_lifecycle",
        "description": "Execute the end-to-end 12-Phase Sovereign Lifecycle verification and export evidence ledger.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]


def handle_tool_call(name: str, args: Dict[str, Any]) -> Any:
    if name == "n8n_get_system_info":
        return client.get_telemetry()
    elif name == "n8n_search_nodes":
        return client.search_nodes(query=args["query"], limit=args.get("limit", 10))
    elif name == "n8n_list_nodes_by_group":
        return client.list_nodes(group=args.get("group"), limit=args.get("limit", 30))
    elif name == "n8n_get_node_details":
        res = client.get_node_details(args["node_type"])
        if not res:
            return {"error": f"Node type '{args['node_type']}' not found in catalog."}
        return res
    elif name == "n8n_list_workflows":
        return client.list_workflows(active_only=args.get("active_only", False))
    elif name == "n8n_get_workflow":
        res = client.get_workflow(args["workflow_id_or_name"])
        if not res:
            return {"error": f"Workflow '{args['workflow_id_or_name']}' not found."}
        return res
    elif name == "n8n_execute_workflow":
        return client.execute_workflow(args["workflow_id_or_name"], input_data=args.get("input_data"))
    elif name == "n8n_trigger_webhook":
        return client.trigger_webhook(
            path=args["path"],
            payload=args["payload"],
            test_mode=args.get("test_mode", False)
        )
    elif name == "n8n_run_ai_agent":
        return client.run_ai_agent(prompt=args["prompt"], context=args.get("context"))
    elif name == "n8n_list_executions":
        return client.list_executions(status=args.get("status"), limit=args.get("limit", 20))
    elif name == "n8n_get_execution":
        res = client.get_execution(args["execution_id"])
        if not res:
            return {"error": f"Execution '{args['execution_id']}' not found."}
        return res
    elif name == "n8n_list_credentials":
        return client.list_credentials()
    elif name == "n8n_scan_dropzone":
        return client.scan_dropzone()
    elif name == "n8n_export_workflows":
        return client.export_workflows(dest_dir=args.get("dest_dir"))
    elif name == "n8n_do_everything_lifecycle":
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
        except Exception:
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
                    "serverInfo": {"name": "n8n-mcp-server", "version": "1.0.0"}
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
