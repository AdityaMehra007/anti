#!/usr/bin/env python3
"""
Antigravity 300 Tools Master CLI Orchestrator
Allows listing, searching, inspecting, and executing any of the 300 tools across 10 domains.
"""

import os
import sys
import json
import argparse
import subprocess
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(BASE_DIR, "manifest.json")

def load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        print(f"Error: Manifest file not found at {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def list_tools(domain=None, search=None):
    manifest = load_manifest()
    tools = manifest.get("tools", [])
    
    filtered = []
    for t in tools:
        if domain and domain.lower() not in t["domain_id"].lower() and domain.lower() not in t["category"].lower():
            continue
        if search:
            query = search.lower()
            if query not in t["name"].lower() and query not in t["slug"].lower() and query not in t["description"].lower() and query not in str(t["tool_id"]):
                continue
        filtered.append(t)
        
    print(f"\n{'='*95}")
    print(f"  ANTIGRAVITY 300 TOOLS REPOSITORY ({len(filtered)} / {len(tools)} matching)")
    print(f"{'='*95}")
    print(f"{'ID':<6} | {'DOMAIN':<14} | {'SLUG':<35} | {'NAME'}")
    print(f"{'-'*6}-+-{'-'*14}-+-{'-'*35}-+-{'-'*34}")
    
    for t in filtered:
        print(f"{t['tool_id']:<6} | {t['domain_id']:<14} | {t['slug']:<35} | {t['name'][:34]}")
        
    print(f"{'='*95}\n")

def find_tool(identifier):
    manifest = load_manifest()
    tools = manifest.get("tools", [])
    
    # Try by numeric ID
    if str(identifier).isdigit():
        target_id = int(identifier)
        for t in tools:
            if t["tool_id"] == target_id:
                return t
                
    # Try by slug or id_str
    ident_str = str(identifier).strip().lower()
    for t in tools:
        if t["slug"].lower() == ident_str or t["id_str"].lower() == ident_str:
            return t
            
    # Try partial slug match
    for t in tools:
        if ident_str in t["slug"].lower():
            return t
            
    return None

def run_tool(identifier, params=None, is_test=False):
    tool = find_tool(identifier)
    if not tool:
        print(f"Error: Tool '{identifier}' not found in manifest.", file=sys.stderr)
        sys.exit(1)
        
    rel_path = tool["relative_path"]
    full_path = os.path.join(BASE_DIR, rel_path)
    
    if not os.path.exists(full_path):
        print(f"Error: Tool script not found at {full_path}", file=sys.stderr)
        sys.exit(1)
        
    cmd = [sys.executable, full_path]
    if is_test:
        cmd.append("--test")
    elif params:
        cmd.extend(["--params", json.dumps(params)])
        
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Execution failed with code {result.returncode}:\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)
    else:
        print(result.stdout)

def main():
    parser = argparse.ArgumentParser(description="Antigravity 300 Tools Master CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_p = subparsers.add_parser("list", help="List available tools")
    list_p.add_argument("--domain", "-d", help="Filter by domain ID (exim, b2b_sales, events, analytics, genai, growth, finance, devops, talent, market_intel)")
    list_p.add_argument("--search", "-s", help="Search by keyword or ID")
    
    # Run command
    run_p = subparsers.add_parser("run", help="Execute a specific tool")
    run_p.add_argument("tool", help="Tool ID (1-300), slug, or identifier")
    run_p.add_argument("--params", "-p", type=str, default=None, help="JSON string of parameter inputs")
    run_p.add_argument("--test", "-t", action="store_true", help="Execute in test mode with preset parameters")
    
    # Domains command
    subparsers.add_parser("domains", help="List all 10 domains and their tool count")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_tools(domain=args.domain, search=args.search)
    elif args.command == "run":
        parsed_params = None
        if args.params:
            try:
                parsed_params = json.loads(args.params)
            except Exception as e:
                print(f"Invalid JSON string passed to --params: {e}", file=sys.stderr)
                sys.exit(1)
        run_tool(args.tool, params=parsed_params, is_test=args.test)
    elif args.command == "domains":
        manifest = load_manifest()
        domain_counts = {}
        for t in manifest.get("tools", []):
            d = t["category"]
            domain_counts[d] = domain_counts.get(d, 0) + 1
        print("\nEnterprise Domains:")
        for dom, cnt in domain_counts.items():
            print(f" - {dom}: {cnt} Tools")
        print(f"\nTotal: {manifest.get('total_tools')} Tools\n")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
