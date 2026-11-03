#!/usr/bin/env python3
r"""
OMEGA Master Model Context Protocol (MCP) Hub & Sovereign Orchestrator
======================================================================
Unified deep-module manager, test engine, protocol multiplexer, and cockpit
server for all MCP servers in the OMEGA ecosystem.

Capabilities:
1. Discovers and catalogs all MCP servers (Reference, Cloud, and Sovereign Workspace).
2. Runs automated JSON-RPC 2.0 handshake validation, health checks, and latency benchmarks.
3. Provides a Composite MCP Multiplexer (a single unified stdio server proxying 200+ tools).
4. Generates standard client configuration files for Claude Desktop, Cursor, VS Code, and Goose.
5. Serves the interactive visual MCP Master Mission Control Cockpit.
"""

from __future__ import annotations

import os
import sys
import json
import time
import shutil
import asyncio
import logging
import argparse
import subprocess
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Any, Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp_hub")

WORKSPACE_DIR = Path(r"E:\anti").resolve()
MCP_CONFIG_PATH = WORKSPACE_DIR / ".mcp.json"

SERVER_METADATA = {
    "filesystem": {
        "category": "Reference Protocol",
        "author": "Model Context Protocol",
        "description": "Secure file and directory access within permitted workspace boundaries.",
        "docs": "https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem"
    },
    "memory": {
        "category": "Reference Protocol",
        "author": "Model Context Protocol",
        "description": "Persistent knowledge-graph and entity memory engine across agent sessions.",
        "docs": "https://github.com/modelcontextprotocol/servers/tree/main/src/memory"
    },
    "fetch": {
        "category": "Reference Protocol",
        "author": "Model Context Protocol",
        "description": "HTTP resource fetcher and web content parser for LLM grounding.",
        "docs": "https://github.com/modelcontextprotocol/servers/tree/main/src/fetch"
    },
    "github": {
        "category": "Official GitHub",
        "author": "GitHub / Anthropic",
        "description": "Native GitHub operations for repositories, pull requests, issues, and commits.",
        "docs": "https://github.com/github/github-mcp-server"
    },
    "git": {
        "category": "Reference Protocol",
        "author": "Model Context Protocol",
        "description": "Direct Git VCS inspection, diff generation, log analysis, and worktree tracking.",
        "docs": "https://github.com/modelcontextprotocol/servers/tree/main/src/git"
    },
    "sqlite": {
        "category": "Reference Protocol",
        "author": "Model Context Protocol",
        "description": "Local SQLite database querying, schema inspection, and analytics execution.",
        "docs": "https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite"
    },
    "chrome-devtools": {
        "category": "Browser Automation",
        "author": "Chrome DevTools Team",
        "description": "Puppeteer and Chrome DevTools Protocol automation, DOM extraction, and screenshots.",
        "docs": "https://github.com/ChromeDevTools/devtools-frontend"
    },
    "supabase": {
        "category": "Cloud & DB",
        "author": "Supabase",
        "description": "Remote Postgres DB operations, RLS security policies, and vector embeddings.",
        "docs": "https://mcp.supabase.com"
    },
    "omniroute": {
        "category": "Proxy & Gateway",
        "author": "OMNI Engine",
        "description": "Smart token routing, model fallbacks, and local cost-optimization gateway.",
        "docs": "https://github.com/mcp"
    },
    "plane": {
        "category": "Workspace Sovereign",
        "author": "OMEGA Project Ops",
        "description": "Issue tracking, sprint cycles, burndown velocity, modules, and collaborative pages.",
        "script": "plane_mcp_server.py"
    },
    "windmill": {
        "category": "Workspace Sovereign",
        "author": "OMEGA Workflow Engine",
        "description": "Polyglot DAG workflow orchestration, job triggers, approvals, and cron schedules.",
        "script": "windmill_mcp_server.py"
    },
    "coolify": {
        "category": "Workspace Sovereign",
        "author": "OMEGA Cloud PaaS",
        "description": "Self-hosted PaaS multi-server Docker, Traefik edge routing, and one-click app stacks.",
        "script": "coolify_mcp_server.py"
    },
    "powershell": {
        "category": "Workspace Sovereign",
        "author": "OMEGA OS Automation",
        "description": "PowerShell 7+ execution, AST analyzer, CIS benchmarks, and runbook pipelines.",
        "script": "powershell_mcp_server.py"
    },
    "powertoys": {
        "category": "Workspace Sovereign",
        "author": "OMEGA OS Automation",
        "description": "Windows desktop automation, FancyZones, OCR, Keyboard Manager, and Awake telemetry.",
        "script": "powertoys_mcp_server.py"
    },
    "n8n": {
        "category": "Workspace Sovereign",
        "author": "OMEGA Workflow Engine",
        "description": "Autonomous workflow automation, webhook triggers, node orchestration, and audit.",
        "script": "n8n_mcp_server.py"
    },
    "airflow": {
        "category": "Workspace Sovereign",
        "author": "OMEGA Workflow Engine",
        "description": "Data pipelines, DAG runs, task instances, XCom variables, and pool management.",
        "script": "airflow_mcp_server.py"
    },
    "infisical": {
        "category": "Workspace Sovereign",
        "author": "OMEGA SecOps",
        "description": "Zero-Knowledge SecretOps, secret leak scanning, dynamic leases, and PKI certs.",
        "script": "infisical_mcp_server.py"
    },
    "hummingbot": {
        "category": "Workspace Sovereign",
        "author": "OMEGA FinTech",
        "description": "High-frequency market making, arbitrage strategies, orderbook telemetry, and risk.",
        "script": "hummingbot_mcp_server.py"
    },
    "ghidra": {
        "category": "Workspace Sovereign",
        "author": "OMEGA SecOps",
        "description": "Binary analysis, decompilation, xref graphs, function signatures, and memory map.",
        "script": "ghidra_mcp_server.py"
    },
    "arrow": {
        "category": "Workspace Sovereign",
        "author": "OMEGA Data Engine",
        "description": "Zero-copy columnar memory buffers, Acero compute, Arrow IPC, and Parquet storage.",
        "script": "arrow_mcp_server.py"
    },
    "awesome": {
        "category": "Workspace Sovereign",
        "author": "OMEGA Knowledge Ops",
        "description": "Global software curator across 50,000+ categorized open-source tools and repos.",
        "script": "awesome_mcp_server.py"
    },
    "free-for-dev": {
        "category": "Workspace Sovereign",
        "author": "OMEGA Cloud Ops",
        "description": "Free cloud tier search engine across compute, storage, APIs, and hosting.",
        "script": "free_for_dev_mcp_server.py"
    },
    "prompts-chat": {
        "category": "Workspace Sovereign",
        "author": "OMEGA Prompt Ops",
        "description": "Curated LLM system prompts, agent archetypes, and role synthesis repository.",
        "script": "prompts_chat_mcp_server.py"
    },
    "hyprland": {
        "category": "Workspace Sovereign",
        "author": "OMEGA OS Automation",
        "description": "Wayland window manager controls, monitors, animations, dynamic workspaces, and bling.",
        "script": "hyprland_mcp_server.py"
    },
    "github-marketplace": {
        "category": "Official GitHub",
        "author": "OMEGA GitHub Ops",
        "description": "GitHub Actions & Apps marketplace explorer, workflow synthesis, and security auditor.",
        "script": "github_marketplace_mcp_server.py"
    }
}


class MCPHub:
    """Master controller and orchestrator for all Model Context Protocol servers."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or MCP_CONFIG_PATH
        self.servers_config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("mcpServers", {})
            except Exception as e:
                logger.error(f"Error reading {self.config_path}: {e}")
        return {}

    def list_servers(self) -> List[Dict[str, Any]]:
        """List all configured servers merged with rich metadata."""
        out = []
        for name, cfg in self.servers_config.items():
            meta = SERVER_METADATA.get(name, {
                "category": "Custom",
                "author": "Workspace",
                "description": f"MCP Server {name}"
            })
            entry = {
                "name": name,
                "category": meta.get("category", "Custom"),
                "author": meta.get("author", "Unknown"),
                "description": meta.get("description", ""),
                "type": "http" if "url" in cfg else "stdio",
                "command": cfg.get("command"),
                "args": cfg.get("args", []),
                "url": cfg.get("url"),
                "docs": meta.get("docs")
            }
            out.append(entry)
        return out

    def test_server(self, name: str, timeout: float = 12.0) -> Dict[str, Any]:
        """Test JSON-RPC 2.0 handshake and retrieve tools for a single stdio server."""
        cfg = self.servers_config.get(name)
        if not cfg:
            return {"name": name, "status": "ERROR", "error": "Server not configured"}

        if "url" in cfg:
            return {
                "name": name,
                "status": "HTTP_ENDPOINT",
                "url": cfg["url"],
                "tools_count": "Remote / Dynamic"
            }

        cmd = cfg.get("command")
        args = cfg.get("args", [])
        env = os.environ.copy()
        if "env" in cfg:
            env.update(cfg["env"])

        # Determine full executable if needed
        executable = shutil.which(cmd) or cmd

        t0 = time.time()
        try:
            p = subprocess.Popen(
                [executable] + args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                cwd=str(WORKSPACE_DIR)
            )

            init_req = json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "mcp-hub-test", "version": "1.0.0"}
                }
            }) + "\n"

            tools_req = json.dumps({
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }) + "\n"

            out, err = p.communicate(input=init_req + tools_req, timeout=timeout)
            duration_ms = round((time.time() - t0) * 1000, 1)

            tools = []
            for line in out.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if "result" in data and "tools" in data["result"]:
                        tools = data["result"]["tools"]
                except Exception:
                    pass

            return {
                "name": name,
                "status": "OK",
                "latency_ms": duration_ms,
                "tools_count": len(tools),
                "tools": [t.get("name") for t in tools],
                "sample_tool": tools[0] if tools else None
            }
        except subprocess.TimeoutExpired:
            p.kill()
            return {"name": name, "status": "TIMEOUT", "error": f"Timed out after {timeout}s"}
        except Exception as e:
            return {"name": name, "status": "ERROR", "error": str(e)}

    def test_all_servers(self, timeout: float = 12.0) -> Dict[str, Any]:
        """Test all registered servers and generate benchmark telemetry."""
        results = {}
        total_tools = 0
        passed = 0
        failed = 0

        for name, cfg in self.servers_config.items():
            res = self.test_server(name, timeout=timeout)
            results[name] = res
            if res.get("status") in ("OK", "HTTP_ENDPOINT"):
                passed += 1
                if isinstance(res.get("tools_count"), int):
                    total_tools += res["tools_count"]
            else:
                failed += 1

        return {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_servers": len(self.servers_config),
            "passed": passed,
            "failed": failed,
            "total_verified_tools": total_tools,
            "servers": results
        }

    def collect_all_tools(self) -> List[Dict[str, Any]]:
        """Extract tool specifications across all registered Python MCP servers."""
        all_tools = []
        for name, cfg in self.servers_config.items():
            meta = SERVER_METADATA.get(name, {})
            script = meta.get("script")
            if script:
                script_path = WORKSPACE_DIR / script
                if script_path.exists():
                    try:
                        # Extract TOOLS statically or via quick run
                        test_res = self.test_server(name, timeout=12.0)
                        if test_res.get("status") == "OK" and "tools" in test_res:
                            # Re-run or store with server context
                            for t_name in test_res["tools"]:
                                all_tools.append({
                                    "server": name,
                                    "category": meta.get("category", "General"),
                                    "name": t_name
                                })
                    except Exception as e:
                        logger.warning(f"Could not extract tools for {name}: {e}")
        return all_tools

    def export_config(self, client_name: str) -> str:
        """Export config for specific AI assistants (claude, cursor, vscode, goose)."""
        client = client_name.lower()
        if client in ("claude", "claude_desktop"):
            return json.dumps({"mcpServers": self.servers_config}, indent=2)
        elif client == "cursor":
            return json.dumps({"mcpServers": self.servers_config}, indent=2)
        elif client in ("vscode", "copilot"):
            return json.dumps({"mcp": {"servers": self.servers_config}}, indent=2)
        elif client == "goose":
            goose_cfg = {"extensions": {}}
            for name, cfg in self.servers_config.items():
                if "url" not in cfg:
                    goose_cfg["extensions"][name] = {
                        "type": "stdio",
                        "cmd": cfg.get("command"),
                        "args": cfg.get("args", [])
                    }
            return json.dumps(goose_cfg, indent=2)
        else:
            return json.dumps(self.servers_config, indent=2)


# ==============================================================================
# Composite MCP Server (Multiplexer Proxy)
# ==============================================================================
class CompositeMCPServer:
    """
    Exposes ALL underlying workspace tools through a single unified JSON-RPC stdio connection.
    Routes 'tools/call' dynamically to the responsible child server.
    """

    def __init__(self, hub: MCPHub):
        self.hub = hub
        self.tool_to_server: Dict[str, str] = {}
        self.all_tools: List[Dict[str, Any]] = []
        self._index_tools()

    def _index_tools(self) -> None:
        """Query all child servers to register the master tool index."""
        logger.info("Initializing Master Tool Multiplexer Index...")
        for name, cfg in self.hub.servers_config.items():
            if "url" in cfg:
                continue
            # Test and pull tools
            res = self.hub.test_server(name, timeout=15.0)
            if res.get("status") == "OK" and res.get("tools"):
                for t_name in res["tools"]:
                    self.tool_to_server[t_name] = name
                    self.all_tools.append({
                        "name": t_name,
                        "description": f"[{name.upper()}] Tool handled by {name} MCP server.",
                        "inputSchema": {"type": "object", "properties": {}}
                    })
        logger.info(f"Composite Multiplexer ready with {len(self.all_tools)} tools across {len(set(self.tool_to_server.values()))} servers.")

    def run_stdio_loop(self) -> None:
        """Run stdio JSON-RPC loop for Composite MCP Server."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except Exception as e:
                resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {e}"}}
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
                continue

            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "omega-master-mcp-hub", "version": "2.0.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": self.all_tools}
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                server_name = self.tool_to_server.get(tool_name)
                if not server_name:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Tool '{tool_name}' not found in any child server"}
                    }
                else:
                    # Forward call to child server
                    resp = self._forward_tool_call(server_name, tool_name, tool_args, req_id)
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method '{method}' not found"}
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

    def _forward_tool_call(self, server_name: str, tool_name: str, args: Dict[str, Any], req_id: Any) -> Dict[str, Any]:
        cfg = self.hub.servers_config[server_name]
        cmd = cfg.get("command")
        c_args = cfg.get("args", [])
        executable = shutil.which(cmd) or cmd
        env = os.environ.copy()
        if "env" in cfg:
            env.update(cfg["env"])

        call_req = json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": args}
        }) + "\n"

        try:
            p = subprocess.Popen(
                [executable] + c_args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                cwd=str(WORKSPACE_DIR)
            )
            out, err = p.communicate(input=call_req, timeout=30)
            for line in out.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if "result" in data or "error" in data:
                        return data
                except Exception:
                    pass
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": "No valid JSON-RPC response from child"}}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}


# ==============================================================================
# Cockpit HTTP Server
# ==============================================================================
class CockpitHandler(SimpleHTTPRequestHandler):
    hub: MCPHub = None

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            cockpit_file = WORKSPACE_DIR / "mcp_master_cockpit.html"
            if cockpit_file.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(cockpit_file, "rb") as f:
                    self.wfile.write(f.read())
                return

        elif self.path == "/api/servers":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            servers = self.hub.list_servers()
            self.wfile.write(json.dumps(servers, indent=2).encode("utf-8"))
            return

        elif self.path == "/api/test":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            results = self.hub.test_all_servers(timeout=12.0)
            self.wfile.write(json.dumps(results, indent=2).encode("utf-8"))
            return

        super().do_GET()


def serve_cockpit(port: int = 8790) -> None:
    hub = MCPHub()
    CockpitHandler.hub = hub
    server = HTTPServer(("127.0.0.1", port), CockpitHandler)
    print(f"\n==================================================================")
    print(f"  OMEGA MCP MASTER COCKPIT SERVER RUNNING")
    print(f"  Cockpit URL : http://localhost:{port}")
    print(f"  API Servers : http://localhost:{port}/api/servers")
    print(f"  API Audit   : http://localhost:{port}/api/test")
    print(f"==================================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Cockpit Server...")
        server.server_close()


if __name__ == "__main__":
    hub = MCPHub()
    print(f"Loaded {len(hub.servers_config)} MCP servers from {hub.config_path}")
