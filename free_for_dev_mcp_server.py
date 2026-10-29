#!/usr/bin/env python3
"""
OMEGA Free-For-Dev Model Context Protocol (MCP) Server
======================================================
Autonomous JSON-RPC 2.0 stdio interface exposing 9 developer cloud tools
for AI Agents, Claude Code, and Antigravity.

Tools:
  - free_for_dev_get_telemetry
  - free_for_dev_list_categories
  - free_for_dev_search_services
  - free_for_dev_get_service_detail
  - free_for_dev_synthesize_zero_dollar_stack
  - free_for_dev_compare_services
  - free_for_dev_audit_architecture
  - free_for_dev_list_no_card_services
  - free_for_dev_run_sovereign_lifecycle
"""

import sys
import json
import traceback
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from free_for_dev_orchestrator import FreeForDevOrchestrator

ORCHESTRATOR = FreeForDevOrchestrator(auto_ingest=True)

TOOLS_REGISTRY = [
    {
        "name": "free_for_dev_get_telemetry",
        "description": "Returns full catalog telemetry for ripienaar/free-for-dev (total services, categories, no-credit-card %, commercial valuation).",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "free_for_dev_list_categories",
        "description": "Lists all 57 developer capability categories with service counts.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "free_for_dev_search_services",
        "description": "Searches 1,396+ developer free-tier services by query, category, credit card requirement, tier rating, and architectural role.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword or service name (e.g. 'postgres', 'docker', 'email')"},
                "category": {"type": "string", "description": "Category slug or name filter"},
                "no_card_only": {"type": "boolean", "description": "If true, strictly filters services requiring NO credit card"},
                "tier": {"type": "string", "enum": ["S", "A", "B", "C"], "description": "Filter by tier rating"},
                "role": {"type": "string", "description": "Architectural role filter (e.g. 'relational_db', 'frontend_hosting', 'auth_identity')"},
                "limit": {"type": "integer", "description": "Maximum results to return (default 25)"}
            }
        }
    },
    {
        "name": "free_for_dev_get_service_detail",
        "description": "Retrieves comprehensive quota, website URL, category, credit card requirement, and tier details for a single service.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "service_id": {"type": "string", "description": "Unique ID or name of the service (e.g. 'supabase', 'neon', 'cloudflare-pages')"}
            },
            "required": ["service_id"]
        }
    },
    {
        "name": "free_for_dev_synthesize_zero_dollar_stack",
        "description": "Synthesizes an optimal production architecture stack that costs exactly $0.00/month by combining developer free tiers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "archetype": {
                    "type": "string",
                    "enum": [
                        "jamstack_saas", "ai_agent_platform", "mobile_app_backend",
                        "microservices_api", "ecommerce_store", "sovereign_no_card", "analytics_data_pipeline"
                    ],
                    "description": "Target architecture archetype"
                }
            }
        }
    },
    {
        "name": "free_for_dev_compare_services",
        "description": "Executes side-by-side differential comparison of 2 to 5 developer providers with direct metrics and recommendation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "provider_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of provider IDs or names to compare (e.g. ['supabase', 'neon', 'turso'])"
                }
            },
            "required": ["provider_ids"]
        }
    },
    {
        "name": "free_for_dev_audit_architecture",
        "description": "Audits a list of software requirements or dependencies against free developer tiers, computing coverage and annual savings.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "requirements": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of components or requirements (e.g. ['Postgres', 'Next.js', 'Redis', 'User Auth', 'Sentry'])"
                }
            },
            "required": ["requirements"]
        }
    },
    {
        "name": "free_for_dev_list_no_card_services",
        "description": "Lists top friction-free developer services verified to require zero credit card credentials.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max items to return (default 25)"}
            }
        }
    },
    {
        "name": "free_for_dev_run_sovereign_lifecycle",
        "description": "Executes the 12-phase sovereign lifecycle protocol for Free-For-Dev and produces the verified OMEGA JSON manifest.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Any:
    if name == "free_for_dev_get_telemetry":
        return ORCHESTRATOR.get_telemetry()
    elif name == "free_for_dev_list_categories":
        return ORCHESTRATOR.list_categories()
    elif name == "free_for_dev_search_services":
        return ORCHESTRATOR.search_services(
            query=arguments.get("query", ""),
            category=arguments.get("category", ""),
            no_card_only=arguments.get("no_card_only", False),
            tier=arguments.get("tier", ""),
            role=arguments.get("role", ""),
            limit=arguments.get("limit", 25)
        )
    elif name == "free_for_dev_get_service_detail":
        sid = arguments.get("service_id", "")
        res = ORCHESTRATOR.get_service(sid)
        return res or {"error": f"Service not found: {sid}"}
    elif name == "free_for_dev_synthesize_zero_dollar_stack":
        arch = arguments.get("archetype", "jamstack_saas")
        return ORCHESTRATOR.architect_zero_dollar_stack(arch)
    elif name == "free_for_dev_compare_services":
        pids = arguments.get("provider_ids", [])
        return ORCHESTRATOR.compare_providers(pids)
    elif name == "free_for_dev_audit_architecture":
        reqs = arguments.get("requirements", [])
        return ORCHESTRATOR.audit_architecture(reqs)
    elif name == "free_for_dev_list_no_card_services":
        return ORCHESTRATOR.search_services(no_card_only=True, limit=arguments.get("limit", 25))
    elif name == "free_for_dev_run_sovereign_lifecycle":
        return ORCHESTRATOR.execute_sovereign_lifecycle()
    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    sys.stderr.write("[*] Free-For-Dev MCP Server started on stdio.\n")
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line_clean = line.strip()
        if not line_clean:
            continue

        try:
            req = json.loads(line_clean)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS_REGISTRY}
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                result_data = handle_tool_call(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": json.dumps(result_data, indent=2)}
                        ]
                    }
                }
            elif method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {
                            "name": "free-for-dev-mcp-server",
                            "version": "1.0.0"
                        },
                        "capabilities": {"tools": {}}
                    }
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"Error handling MCP request: {e}\n{traceback.format_exc()}\n")
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
