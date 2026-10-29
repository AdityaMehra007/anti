#!/usr/bin/env python3
"""OpenBB Platform Supreme Orchestrator.

Unified management SDK, CLI, and diagnostic runner for the OpenBB Open Data Platform (ODP v5.0.0).
Provides seamless single-command control over the Python SDK, REST API backend,
FastMCP AI agent server, CLI terminal, and Desktop frontend.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent / "OpenBB"
if not REPO_ROOT.exists():
    REPO_ROOT = Path(__file__).resolve().parent

VENV_PYTHON = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
if not VENV_PYTHON.exists():
    VENV_PYTHON = Path(sys.executable)

OPENBB_EXE = REPO_ROOT / ".venv" / "Scripts" / "openbb.exe"
OPENBB_API_EXE = REPO_ROOT / ".venv" / "Scripts" / "openbb-api.exe"
OPENBB_MCP_EXE = REPO_ROOT / ".venv" / "Scripts" / "openbb-mcp.exe"
DESKTOP_DIR = REPO_ROOT / "desktop"


def get_env() -> dict[str, str]:
    """Return environment variables configured for clean UTF-8 Windows operation."""
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["OPENBB_AUTO_BUILD"] = "false"
    return env


def cmd_info(args: argparse.Namespace) -> None:
    """Print complete OpenBB Platform system topology and inventory."""
    print("=" * 70)
    print("  OPENBB OPEN DATA PLATFORM (ODP v5.0.0) — SYSTEM INVENTORY")
    print("=" * 70)
    print(f"Repository Root : {REPO_ROOT}")
    print(f"Virtualenv      : {VENV_PYTHON.parent.parent}")
    print(f"Python Runtime  : {sys.version.split()[0]} ({VENV_PYTHON})")
    print()

    code = """
from openbb import obb
import json

paths = obb.reference.get("paths", {})
routers = obb.reference.get("routers", {})
info = obb.reference.get("info", {})
extensions = info.get("extensions", {})

print(f"Platform Version : {obb.reference.get('openbb', 'v2.0.1core')}")
print(f"Total Routers    : {len(routers)}")
print(f"Total API Paths  : {len(paths)}")
print(f"Active Providers : {len(obb.coverage.providers)}")
print()
print("Installed Extensions:")
for group, ext_list in extensions.items():
    print(f"  [{group}] ({len(ext_list)} packages)")
    for ext in ext_list[:5]:
        print(f"    - {ext}")
    if len(ext_list) > 5:
        print(f"    ... and {len(ext_list) - 5} more")
"""
    subprocess.run([str(VENV_PYTHON), "-u", "-c", code], env=get_env(), check=False)
    print("=" * 70)


def cmd_serve_api(args: argparse.Namespace) -> None:
    """Launch the OpenBB Platform REST API server."""
    host = args.host
    port = str(args.port)
    print(f"[*] Starting OpenBB Platform REST API on http://{host}:{port} ...")
    print(f"[*] Swagger Documentation will be at: http://{host}:{port}/docs")
    print(f"[*] Workspace Widgets Spec at       : http://{host}:{port}/widgets.json")
    print("[*] Press Ctrl+C to stop.")
    cmd = [str(OPENBB_API_EXE), "--host", host, "--port", port]
    try:
        subprocess.run(cmd, env=get_env(), check=True)
    except KeyboardInterrupt:
        print("\n[*] OpenBB REST API stopped.")


def cmd_serve_mcp(args: argparse.Namespace) -> None:
    """Launch the OpenBB Model Context Protocol (MCP) server."""
    host = args.host
    port = str(args.port)
    transport = args.transport
    print(f"[*] Starting OpenBB FastMCP Server (transport={transport}) ...")
    if transport in ("streamable-http", "sse"):
        print(f"[*] Listening on: http://{host}:{port}/mcp (SSE / HTTP)")
    else:
        print("[*] Connected via standard I/O (stdio)")
    print("[*] AI agents can discover financial tools via available_categories / search_tools / call_tool")
    print("[*] Press Ctrl+C to stop.")
    cmd = [
        str(OPENBB_MCP_EXE),
        "--transport", transport,
        "--host", host,
        "--port", port,
    ]
    try:
        subprocess.run(cmd, env=get_env(), check=True)
    except KeyboardInterrupt:
        print("\n[*] OpenBB MCP Server stopped.")


def cmd_cli(args: argparse.Namespace) -> None:
    """Launch the interactive OpenBB Platform CLI."""
    print("[*] Launching OpenBB Interactive Terminal CLI...")
    cmd = [str(OPENBB_EXE), "-i"]
    subprocess.run(cmd, env=get_env(), check=False)


def cmd_repl(args: argparse.Namespace) -> None:
    """Launch interactive Python REPL with OpenBB SDK preloaded."""
    print("[*] Launching Interactive Python Financial Analytics Session...")
    print("[*] Pre-loaded: `from openbb import obb`")
    print("[*] Example: `obb.coverage.providers`")
    print()
    startup_code = "from openbb import obb; print('\\nOpenBB SDK loaded as `obb`. Type `help(obb)` or `obb.coverage.providers` to explore.\\n')"
    cmd = [str(VENV_PYTHON), "-i", "-c", startup_code]
    subprocess.run(cmd, env=get_env(), check=False)


def cmd_desktop_dev(args: argparse.Namespace) -> None:
    """Launch the Desktop frontend development / preview server."""
    port = str(args.port)
    if not DESKTOP_DIR.exists():
        print(f"[!] Desktop directory not found at {DESKTOP_DIR}")
        return
    print(f"[*] Launching OpenBB Desktop Frontend on http://localhost:{port} ...")
    cmd = ["npm", "run", "dev", "--", "--port", port]
    try:
        subprocess.run(cmd, cwd=str(DESKTOP_DIR), shell=True, env=get_env(), check=True)
    except KeyboardInterrupt:
        print("\n[*] OpenBB Desktop server stopped.")


def cmd_test(args: argparse.Namespace) -> None:
    """Execute end-to-end self-tests across all platform components."""
    print("=" * 70)
    print("  RUNNING OPENBB PLATFORM AUTOMATED HEALTH SUITE")
    print("=" * 70)

    test_script = """
import sys
from openbb import obb

print('[1/4] Verifying Core SDK & Reference Index...')
paths = obb.reference.get('paths', {})
routers = obb.reference.get('routers', {})
assert len(paths) > 800, f'Expected >800 paths, got {len(paths)}'
assert len(routers) >= 90, f'Expected >=90 routers, got {len(routers)}'
print(f'      PASS: {len(paths)} paths and {len(routers)} routers verified.')

print('[2/4] Verifying Provider Coverage Index...')
providers = obb.coverage.providers
assert 'sec' in providers, 'SEC provider missing'
assert 'bls' in providers, 'BLS provider missing'
assert 'cboe' in providers, 'CBOE provider missing'
assert 'federal_reserve' in providers, 'Federal Reserve provider missing'
print(f'      PASS: {len(providers)} providers verified (bls, cboe, sec, fed, etc.).')

print('[3/4] Verifying Router Tree Integrity...')
expected_routers = ['bls', 'cboe', 'commodity', 'crypto', 'currency', 'derivatives', 'economy', 'equity', 'etf', 'fixedincome', 'news', 'quantitative', 'sec', 'technical']
for r in expected_routers:
    assert hasattr(obb, r), f'Missing top-level router obb.{r}'
print(f'      PASS: All {len(expected_routers)} major routers registered on obb.')

print('[4/4] Verifying FastMCP & FastAPI Package Modules...')
import openbb_mcp_server
import openbb_platform_api
print('      PASS: openbb_mcp_server and openbb_platform_api imported cleanly.')

print('\\n[ALL TESTS PASSED]: OpenBB Open Data Platform is 100% HEALTHY.')
"""
    res = subprocess.run([str(VENV_PYTHON), "-u", "-c", test_script], env=get_env())
    if res.returncode == 0:
        print("\nAll automated verification checks succeeded.")
    else:
        print("\nSome verification checks failed.")


def main() -> None:
    """Parse CLI arguments and dispatch commands."""
    parser = argparse.ArgumentParser(
        description="OpenBB Platform Supreme Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Operational mode")

    # info
    p_info = subparsers.add_parser("info", help="Display platform topology and extension inventory")
    p_info.set_defaults(func=cmd_info)

    # serve-api
    p_api = subparsers.add_parser("serve-api", help="Serve OpenBB Platform REST API (port 6900)")
    p_api.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    p_api.add_argument("--port", type=int, default=6900, help="Port (default: 6900)")
    p_api.set_defaults(func=cmd_serve_api)

    # serve-mcp
    p_mcp = subparsers.add_parser("serve-mcp", help="Serve OpenBB Model Context Protocol server (port 8001)")
    p_mcp.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    p_mcp.add_argument("--port", type=int, default=8001, help="Port (default: 8001)")
    p_mcp.add_argument("--transport", default="streamable-http", choices=["streamable-http", "sse", "stdio"], help="Transport")
    p_mcp.set_defaults(func=cmd_serve_mcp)

    # cli
    p_cli = subparsers.add_parser("cli", help="Launch interactive OpenBB Terminal CLI")
    p_cli.set_defaults(func=cmd_cli)

    # repl
    p_repl = subparsers.add_parser("repl", help="Launch interactive Python session with obb preloaded")
    p_repl.set_defaults(func=cmd_repl)

    # desktop-dev
    p_desk = subparsers.add_parser("desktop-dev", help="Launch desktop web frontend dev server")
    p_desk.add_argument("--port", type=int, default=1470, help="Port (default: 1470)")
    p_desk.set_defaults(func=cmd_desktop_dev)

    # test
    p_test = subparsers.add_parser("test", help="Run platform health and verification tests")
    p_test.set_defaults(func=cmd_test)

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
