#!/usr/bin/env python3
"""
OMEGA GitHub Marketplace Model Context Protocol (MCP) Server
============================================================
Autonomous JSON-RPC 2.0 stdio interface exposing 10 curated developer tools
for AI Agents, Claude Code, and Antigravity.

Tools:
  - marketplace_get_info
  - marketplace_list_categories
  - marketplace_search
  - marketplace_get_item_details
  - marketplace_get_top_actions
  - marketplace_get_top_apps
  - marketplace_generate_workflow
  - marketplace_audit_workflow
  - marketplace_get_cross_graph
  - marketplace_run_sovereign_lifecycle
"""

import sys
import json
import traceback
from typing import Dict, Any, List, Optional

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from github_marketplace_orchestrator import (
    engine,
    WorkflowSynthesizer,
    WorkflowSecurityAuditor,
    MANIFEST_JSON_PATH
)

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "omega-github-marketplace"
SERVER_VERSION = "1.0.0"

TOOLS_REGISTRY = [
    {
        "name": "marketplace_get_info",
        "description": "Get real-time telemetry and overview statistics for the GitHub Marketplace ecosystem.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "marketplace_list_categories",
        "description": "List all 19 official GitHub Marketplace domain categories with counts and descriptions.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "marketplace_search",
        "description": "Search across 370+ GitHub Actions and GitHub Apps using sub-millisecond SQLite FTS5 search.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keywords to search (e.g. 'docker', 'python', 'security', 'slack')"
                },
                "category": {
                    "type": "string",
                    "description": "Optional category filter slug (e.g. 'continuous-integration', 'security', 'deployment')"
                },
                "type": {
                    "type": "string",
                    "enum": ["action", "app"],
                    "description": "Filter by 'action' or 'app'"
                },
                "verified_only": {
                    "type": "boolean",
                    "description": "Restrict results to GitHub Verified Creators"
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return (default 20)"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "marketplace_get_item_details",
        "description": "Get complete verified metadata, runner matrix, permissions, and recommended SHA pins for an Action or App.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {
                    "type": "string",
                    "description": "Item id, slug, or repo name (e.g. 'actions-checkout', 'docker-build-push-action', 'app-dependabot')"
                }
            },
            "required": ["slug"]
        }
    },
    {
        "name": "marketplace_get_top_actions",
        "description": "List the most widely installed and starred GitHub Actions across the ecosystem.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of top actions to return (default 20)"
                }
            }
        }
    },
    {
        "name": "marketplace_get_top_apps",
        "description": "List top GitHub Apps for continuous integration, code review, project management, and security.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of top apps to return (default 20)"
                }
            }
        }
    },
    {
        "name": "marketplace_generate_workflow",
        "description": "Synthesize a high-assurance, production-ready GitHub Actions YAML workflow adhering to least privilege and SHA pinning.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stack": {
                    "type": "string",
                    "enum": ["python", "node", "docker", "universal"],
                    "description": "Target software stack"
                },
                "pin_sha": {
                    "type": "boolean",
                    "description": "Pin all action versions to immutable commit SHAs"
                },
                "security_scan": {
                    "type": "boolean",
                    "description": "Include Trivy / CodeQL security scanning jobs"
                },
                "cache": {
                    "type": "boolean",
                    "description": "Enable dependency caching (pip, npm)"
                }
            },
            "required": ["stack"]
        }
    },
    {
        "name": "marketplace_audit_workflow",
        "description": "Audit a GitHub Actions YAML workflow for security vulnerabilities: mutable tags, missing permissions, injection risks, timeouts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "yaml_content": {
                    "type": "string",
                    "description": "Full text of the .github/workflows/*.yml file to audit"
                }
            },
            "required": ["yaml_content"]
        }
    },
    {
        "name": "marketplace_get_cross_graph",
        "description": "Retrieve the action-to-app interoperability topology and recommended pipeline synergy links.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "marketplace_run_sovereign_lifecycle",
        "description": "Execute the 12-phase sovereign attestation lifecycle across all GitHub Marketplace data layers.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if name == "marketplace_get_info":
            total_items = len(engine.items)
            actions_count = sum(1 for it in engine.items.values() if it.type == "action")
            apps_count = sum(1 for it in engine.items.values() if it.type == "app")
            verified_count = sum(1 for it in engine.items.values() if it.verified_creator)
            s_tier = sum(1 for it in engine.items.values() if it.tier == "S")
            avg_score = round(sum(it.security_score for it in engine.items.values()) / max(1, total_items), 1)

            return {
                "total_items": total_items,
                "total_actions": actions_count,
                "total_apps": apps_count,
                "verified_creators": verified_count,
                "s_tier_flagships": s_tier,
                "average_security_score": avg_score,
                "total_categories": len(engine.categories)
            }

        elif name == "marketplace_list_categories":
            return {"categories": list(engine.categories.values())}

        elif name == "marketplace_search":
            q = arguments.get("query", "")
            cat = arguments.get("category")
            itype = arguments.get("type")
            verified = arguments.get("verified_only", False)
            limit = int(arguments.get("limit", 20))

            results = engine.search(
                query=q,
                category=cat,
                item_type=itype,
                verified_only=verified,
                limit=limit
            )
            return {"query": q, "count": len(results), "results": results}

        elif name == "marketplace_get_item_details":
            slug = arguments.get("slug", "")
            item = engine.get_item(slug)
            if not item:
                return {"error": f"Item '{slug}' not found in GitHub Marketplace catalog"}
            return item

        elif name == "marketplace_get_top_actions":
            limit = int(arguments.get("limit", 20))
            actions = [it.to_dict() for it in engine.items.values() if it.type == "action"]
            actions = sorted(actions, key=lambda x: x["stars"], reverse=True)[:limit]
            return {"count": len(actions), "actions": actions}

        elif name == "marketplace_get_top_apps":
            limit = int(arguments.get("limit", 20))
            apps = [it.to_dict() for it in engine.items.values() if it.type == "app"]
            apps = sorted(apps, key=lambda x: x["stars"], reverse=True)[:limit]
            return {"count": len(apps), "apps": apps}

        elif name == "marketplace_generate_workflow":
            stack = arguments.get("stack", "python")
            options = {
                "pin_sha": arguments.get("pin_sha", True),
                "security_scan": arguments.get("security_scan", True),
                "cache": arguments.get("cache", True)
            }
            yaml_code = WorkflowSynthesizer.synthesize(stack, options)
            return {"stack": stack, "options": options, "yaml": yaml_code}

        elif name == "marketplace_audit_workflow":
            yaml_content = arguments.get("yaml_content", "")
            report = WorkflowSecurityAuditor.audit_yaml(yaml_content)
            return report

        elif name == "marketplace_get_cross_graph":
            return {
                "nodes_count": len(engine.items),
                "edges_count": len(engine.graph_edges),
                "edges": engine.graph_edges
            }

        elif name == "marketplace_run_sovereign_lifecycle":
            manifest = engine.do_everything()
            return {
                "status": manifest["status"],
                "execution_id": manifest["execution_id"],
                "total_phases_executed": manifest["total_phases_executed"],
                "elapsed_seconds": manifest["total_elapsed_seconds"],
                "telemetry": manifest["telemetry"]
            }

        else:
            return {"error": f"Unknown tool: {name}"}

    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


def process_message(msg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    msg_id = msg.get("id")
    method = msg.get("method")
    params = msg.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}
            }
        }

    elif method == "notifications/initialized":
        return None

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": TOOLS_REGISTRY}
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        result = handle_tool_call(tool_name, args)
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2, ensure_ascii=False)
                    }
                ]
            }
        }

    elif method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    else:
        if msg_id is not None:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
        return None


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = process_message(req)
            if res is not None:
                sys.stdout.write(json.dumps(res, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            pass
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": f"Internal error: {e}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
