#!/usr/bin/env python3
r"""
OMEGA Master Model Context Protocol (MCP) CLI
==============================================
Command line interface for managing, testing, benchmarking, exporting,
and running the composite Model Context Protocol ecosystem.

Usage:
    python mcp_cli.py list
    python mcp_cli.py test [server_name]
    python mcp_cli.py export [--client claude|cursor|vscode|goose]
    python mcp_cli.py serve [--port 8790]
    python mcp_cli.py composite
"""

import sys
import json
import argparse
from mcp_hub import MCPHub, CompositeMCPServer, serve_cockpit


def main():
    parser = argparse.ArgumentParser(
        description="OMEGA Master Model Context Protocol CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # list
    subparsers.add_parser("list", help="List all registered MCP servers with metadata")

    # test
    test_p = subparsers.add_parser("test", help="Test JSON-RPC 2.0 handshake and tool count")
    test_p.add_argument("server", nargs="?", default=None, help="Optional specific server name to test")
    test_p.add_argument("--timeout", type=float, default=15.0, help="Timeout in seconds per server")

    # export
    exp_p = subparsers.add_parser("export", help="Export config for Claude, Cursor, VS Code, or Goose")
    exp_p.add_argument("--client", choices=["claude", "cursor", "vscode", "goose", "all"], default="all")

    # serve
    srv_p = subparsers.add_parser("serve", help="Launch interactive visual MCP Cockpit server")
    srv_p.add_argument("--port", type=int, default=8790, help="Port to bind (default: 8790)")

    # composite
    subparsers.add_parser("composite", help="Run Composite MCP Multiplexer over stdio")

    args = parser.parse_args()
    hub = MCPHub()

    if args.command == "list":
        servers = hub.list_servers()
        print(f"\n{'NAME':<18} {'CATEGORY':<22} {'TYPE':<8} {'AUTHOR':<20} {'DESCRIPTION'}")
        print("-" * 105)
        for s in servers:
            print(f"{s['name']:<18} {s['category']:<22} {s['type']:<8} {s['author']:<20} {s['description'][:35]}...")
        print(f"\nTotal Registered Servers: {len(servers)}")

    elif args.command == "test":
        if args.server:
            print(f"\nTesting MCP Server: {args.server} (timeout={args.timeout}s)...")
            res = hub.test_server(args.server, timeout=args.timeout)
            print(json.dumps(res, indent=2))
        else:
            print(f"\nRunning Automated Handshake & Tool Audit Across All Servers...")
            res = hub.test_all_servers(timeout=args.timeout)
            print(f"\nAudit Summary:")
            print(f"  Total Servers Tested : {res['total_servers']}")
            print(f"  Passed Handshakes    : {res['passed']}")
            print(f"  Failed / Timeouts    : {res['failed']}")
            print(f"  Verified Tools Count : {res['total_verified_tools']}")
            print("\nDetailed Server Results:")
            for name, details in res["servers"].items():
                status = details.get("status")
                tools = details.get("tools_count", 0)
                lat = details.get("latency_ms", "N/A")
                print(f"  [{status:<4}] {name:<16} : {tools} tools (latency: {lat}ms)")

    elif args.command == "export":
        if args.client == "all":
            for c in ["claude", "cursor", "vscode", "goose"]:
                print(f"\n=== Configuration for {c.upper()} ===")
                print(hub.export_config(c))
        else:
            print(hub.export_config(args.client))

    elif args.command == "serve":
        serve_cockpit(port=args.port)

    elif args.command == "composite":
        composite = CompositeMCPServer(hub)
        composite.run_stdio_loop()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
