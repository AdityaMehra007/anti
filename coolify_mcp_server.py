#!/usr/bin/env python3
"""
Coolify Autonomous MCP (Model Context Protocol) Server
======================================================
Exposes Coolify v4 PaaS orchestration capabilities to agentic coding tools,
subagents, and LLMs via standard JSON-RPC stdio protocol.

Supported tools:
- coolify_get_cluster_status
- coolify_list_servers
- coolify_validate_server
- coolify_cleanup_docker
- coolify_list_applications
- coolify_create_application
- coolify_deploy_resource
- coolify_get_deployment_status
- coolify_list_databases
- coolify_create_database
- coolify_search_templates
- coolify_export_compose
- coolify_provision_omega_stack
"""

import sys
import json
import logging
from typing import Any, Dict

from coolify_orchestrator import CoolifyClient, CoolifyOrchestrator, CoolifyTemplateCatalog
from coolify_compose_exporter import CoolifyComposeExporter

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("coolify_mcp")

client = CoolifyClient()
orchestrator = CoolifyOrchestrator(client)
catalog = CoolifyTemplateCatalog()
exporter = CoolifyComposeExporter()

TOOLS = [
    {
        "name": "coolify_get_cluster_status",
        "description": "Get real-time telemetry and health for the Coolify cluster, nodes, apps, and databases.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "coolify_list_servers",
        "description": "List all managed server nodes, their IP addresses, reachability, and proxy configurations.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "coolify_validate_server",
        "description": "Validate SSH connectivity, Docker daemon status, OS, CPU, and RAM on a specific server node.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "server_uuid": {"type": "string", "description": "The UUID of the server to validate"}
            },
            "required": ["server_uuid"]
        }
    },
    {
        "name": "coolify_cleanup_docker",
        "description": "Trigger Docker cleanup to prune dangling containers, unused images, networks, and build cache.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "server_uuid": {"type": "string", "description": "Server UUID"}
            },
            "required": ["server_uuid"]
        }
    },
    {
        "name": "coolify_list_applications",
        "description": "List all registered applications with their Git repositories, build packs, and public FQDNs.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "coolify_create_application",
        "description": "Register a new application from a Git repository or Docker image in Coolify.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Application display name"},
                "git_repository": {"type": "string", "description": "Git repository URL"},
                "git_branch": {"type": "string", "default": "main", "description": "Git branch to track"},
                "build_pack": {"type": "string", "default": "nixpacks", "description": "Build pack (nixpacks, dockerfile, dockerimage)"},
                "fqdn": {"type": "string", "description": "Public domain URL (e.g. https://app.example.com)"},
                "ports_exposes": {"type": "string", "default": "80", "description": "Container exposed port"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "coolify_deploy_resource",
        "description": "Trigger automated zero-downtime rolling deployment for an application, service, or database.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "resource_uuid": {"type": "string", "description": "UUID of the application or service"},
                "force_rebuild": {"type": "boolean", "default": False, "description": "Whether to invalidate cache and force rebuild"}
            },
            "required": ["resource_uuid"]
        }
    },
    {
        "name": "coolify_get_deployment_status",
        "description": "Check deployment queue status and stream execution logs for a specific deployment.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "deployment_uuid": {"type": "string", "description": "Deployment UUID"}
            },
            "required": ["deployment_uuid"]
        }
    },
    {
        "name": "coolify_list_databases",
        "description": "List all provisioned standalone databases (PostgreSQL, MySQL, Redis, MongoDB).",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "coolify_create_database",
        "description": "Provision a dedicated standalone database container.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "db_type": {"type": "string", "enum": ["postgresql", "redis", "mysql", "mongodb", "clickhouse"], "description": "Database type"},
                "name": {"type": "string", "description": "Database service name"},
                "server_uuid": {"type": "string", "default": "srv-localhost-000", "description": "Target server node"}
            },
            "required": ["db_type", "name"]
        }
    },
    {
        "name": "coolify_search_templates",
        "description": "Search the 352+ open-source one-click service templates catalog (e.g. n8n, Supabase, AnythingLLM, Plausible).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Keyword search (e.g. 'llm', 'analytics', 'database')"},
                "category": {"type": "string", "description": "Category filter (e.g. 'ai', 'database', 'cms')"}
            }
        }
    },
    {
        "name": "coolify_export_compose",
        "description": "Extract, decode, and generate standalone docker-compose.yml and .env files for any of the 352 services.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template_id": {"type": "string", "description": "Template ID (e.g. 'anythingllm', 'n8n', 'supabase')"},
                "domain": {"type": "string", "default": "localhost", "description": "Target domain for FQDN routing"}
            },
            "required": ["template_id"]
        }
    },
    {
        "name": "coolify_provision_omega_stack",
        "description": "Deploy the complete OMEGA autonomous enterprise stack (PostgreSQL + Redis + n8n automation).",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "coolify_do_everything",
        "description": "Execute the comprehensive 8-phase autonomous Coolify PaaS orchestration cycle across nodes, databases, services, applications, and template stacks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "server_uuid": {"type": "string", "default": "srv-localhost-000", "description": "Target server node"}
            }
        }
    }
]


def handle_tool_call(name: str, args: Dict[str, Any]) -> Any:
    if name == "coolify_get_cluster_status":
        return orchestrator.get_cluster_status()
    elif name == "coolify_list_servers":
        return client.list_servers()
    elif name == "coolify_validate_server":
        return client.validate_server(args["server_uuid"])
    elif name == "coolify_cleanup_docker":
        return client.cleanup_docker(args["server_uuid"])
    elif name == "coolify_list_applications":
        return client.list_applications()
    elif name == "coolify_create_application":
        return client.create_application(
            name=args["name"],
            git_repository=args.get("git_repository"),
            git_branch=args.get("git_branch", "main"),
            build_pack=args.get("build_pack", "nixpacks"),
            fqdn=args.get("fqdn"),
            ports_exposes=args.get("ports_exposes", "80")
        )
    elif name == "coolify_deploy_resource":
        return client.deploy(args["resource_uuid"], force_rebuild=args.get("force_rebuild", False))
    elif name == "coolify_get_deployment_status":
        return client.get_deployment_status(args["deployment_uuid"])
    elif name == "coolify_list_databases":
        return client.list_databases()
    elif name == "coolify_create_database":
        return client.create_database(args["db_type"], args["name"], args.get("server_uuid", "srv-localhost-000"))
    elif name == "coolify_search_templates":
        return catalog.search(query=args.get("query", ""), category=args.get("category", ""))
    elif name == "coolify_export_compose":
        compose_yml, env_vars = exporter.export(args["template_id"], domain=args.get("domain", "localhost"))
        return {"docker_compose_yaml": compose_yml, "generated_env": env_vars}
    elif name == "coolify_provision_omega_stack":
        return orchestrator.provision_full_omega_stack()
    elif name == "coolify_do_everything":
        return orchestrator.do_everything(args.get("server_uuid", "srv-localhost-000"))
    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "coolify-mcp-server", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                tool_res = handle_tool_call(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(tool_res, indent=2)}]
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
            err_resp = {
                "jsonrpc": "2.0",
                "id": req.get("id") if "req" in locals() and isinstance(req, dict) else None,
                "error": {"code": -32603, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
