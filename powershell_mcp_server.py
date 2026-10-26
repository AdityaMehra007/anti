#!/usr/bin/env python3
"""
PowerShell Autonomous MCP (Model Context Protocol) Server
=========================================================
Exposes PowerShell 7+ / Windows PowerShell Autonomous Ecosystem to AI agents,
subagents, and LLMs via standard JSON-RPC 2.0 stdio protocol.

Supported tools:
- powershell_get_telemetry
- powershell_execute_command
- powershell_analyze_ast
- powershell_script_analyzer
- powershell_list_modules
- powershell_find_gallery_module
- powershell_list_runbooks
- powershell_run_runbook
- powershell_cis_benchmark_audit
- powershell_cloud_infra_recon
- powershell_benchmark
- powershell_do_everything
"""

import sys
import json
import logging
from typing import Any, Dict

from powershell_orchestrator import PowerShellClient, PowerShellOrchestrator

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("powershell_mcp")

client = PowerShellClient()
orchestrator = PowerShellOrchestrator(client)

TOOLS = [
    {
        "name": "powershell_get_telemetry",
        "description": "Get real-time telemetry, runtime edition (Core vs Desktop), CLR version, active runspaces, and execution policies.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powershell_execute_command",
        "description": "Execute a PowerShell command or pipeline script and receive structured deserialized JSON objects.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "PowerShell command or script string"},
                "as_json": {"type": "boolean", "description": "Wrap with ConvertTo-Json for typed object serialization", "default": True}
            },
            "required": ["command"]
        }
    },
    {
        "name": "powershell_analyze_ast",
        "description": "Parse PowerShell script using System.Management.Automation AST parser to inspect functions, parameters, tokens, and detect syntax errors.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "script_content": {"type": "string", "description": "PowerShell script code"}
            },
            "required": ["script_content"]
        }
    },
    {
        "name": "powershell_script_analyzer",
        "description": "Run PSScriptAnalyzer rules on script code to detect credential leakage, code injection, and architectural code smells.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "script_content": {"type": "string", "description": "PowerShell script code"}
            },
            "required": ["script_content"]
        }
    },
    {
        "name": "powershell_list_modules",
        "description": "List installed PowerShell modules, versions, authors, and export counts.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powershell_find_gallery_module",
        "description": "Search PSGallery repository for modules, scripts, and extensions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "Search term"},
                "category": {"type": "string", "description": "Package category filter"}
            }
        }
    },
    {
        "name": "powershell_list_runbooks",
        "description": "List enterprise runbooks (CIS Hardening, Cloud Recon, AD Audit, Network Latency, Service Watchdog).",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powershell_run_runbook",
        "description": "Execute a registered enterprise runbook by ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "runbook_id": {"type": "string", "description": "ID of runbook (cis_hardening, cloud_recon, ad_audit, network_diag, self_healing)"},
                "params": {"type": "object", "description": "Optional parameters to pass to runbook"}
            },
            "required": ["runbook_id"]
        }
    },
    {
        "name": "powershell_cis_benchmark_audit",
        "description": "Execute the CIS Benchmark Operating System Hardening runbook to audit endpoint security compliance.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powershell_cloud_infra_recon",
        "description": "Execute Multi-Cloud Infrastructure Recon runbook to identify orphaned disks, idle compute, and cost leakage.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "powershell_benchmark",
        "description": "Benchmark PowerShell object pipeline streaming and serialization throughput.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "iterations": {"type": "integer", "description": "Number of iterations", "default": 5}
            }
        }
    },
    {
        "name": "powershell_do_everything",
        "description": "Execute the Complete 12-Phase Sovereign PowerShell Lifecycle and generate signed execution manifest.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]


def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Any:
    if name == "powershell_get_telemetry":
        return client.get_telemetry()
    elif name == "powershell_execute_command":
        res = client.execute(arguments["command"], as_json=arguments.get("as_json", True))
        return {
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.exit_code,
            "execution_time_ms": res.execution_time_ms,
            "success": res.success,
            "objects": res.objects
        }
    elif name == "powershell_analyze_ast":
        ast_res = client.parse_ast(arguments["script_content"])
        return {
            "tokens_count": ast_res.tokens_count,
            "functions": ast_res.functions,
            "parameters": ast_res.parameters,
            "pipeline_calls": ast_res.pipeline_calls,
            "variables_referenced": ast_res.variables_referenced,
            "syntax_errors": ast_res.syntax_errors,
            "has_errors": ast_res.has_errors
        }
    elif name == "powershell_script_analyzer":
        diags = client.analyze_script(arguments["script_content"])
        return [
            {
                "rule_name": d.rule_name,
                "severity": d.severity,
                "message": d.message,
                "line_number": d.line_number,
                "suggested_fix": d.suggested_fix
            }
            for d in diags
        ]
    elif name == "powershell_list_modules":
        return client.list_modules()
    elif name == "powershell_find_gallery_module":
        return client.find_gallery_module(arguments.get("keyword", ""), arguments.get("category", ""))
    elif name == "powershell_list_runbooks":
        return client.list_runbooks()
    elif name == "powershell_run_runbook":
        return client.execute_runbook(arguments["runbook_id"], params=arguments.get("params"))
    elif name == "powershell_cis_benchmark_audit":
        return orchestrator.audit_cis_hardening()
    elif name == "powershell_cloud_infra_recon":
        return orchestrator.audit_cloud_infra()
    elif name == "powershell_benchmark":
        return orchestrator.benchmark_pipeline(iterations=arguments.get("iterations", 5))
    elif name == "powershell_do_everything":
        return orchestrator.do_everything()
    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                try:
                    result_data = handle_call_tool(tool_name, tool_args)
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result_data, indent=2)
                                }
                            ]
                        }
                    }
                except Exception as ex:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32000, "message": str(ex)}
                    }
            elif method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "powershell-autonomous-mcp-server",
                            "version": "1.0.0"
                        }
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
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {e}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
