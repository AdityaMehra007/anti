#!/usr/bin/env python3
"""
System Prompts Intelligence CLI (prompt_cli.py)
Interactive command-line tool for querying, inspecting, searching,
and comparing 423 production AI system prompts.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from difflib import unified_diff

INDEX_PATH = Path(r"e:\anti\research\SYSTEM_PROMPTS_MASTER_INDEX.json")
REPO_ROOT = Path(r"e:\anti\research\system_prompts_leaks")

def load_index():
    if not INDEX_PATH.exists():
        print(f"Error: Index file not found at {INDEX_PATH}")
        sys.exit(1)
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def cmd_list(args, data):
    prompts = data["prompts"]
    if args.provider:
        prompts = [p for p in prompts if p["provider"].lower() == args.provider.lower()]
    if args.has_tools:
        prompts = [p for p in prompts if p["has_tools"]]
    if args.has_planning:
        prompts = [p for p in prompts if p["has_planning"]]
    if args.has_subagents:
        prompts = [p for p in prompts if p["has_subagents"]]
        
    print(f"\n--- Found {len(prompts)} System Prompts ---\n")
    print(f"{'ID / Path':<65} | {'Tokens':<8} | {'Tools':<5} | {'Plan':<5}")
    print("-" * 90)
    for p in prompts[:args.limit]:
        t_badge = "YES" if p["has_tools"] else "-"
        pl_badge = "YES" if p["has_planning"] else "-"
        print(f"{p['rel_path']:<65} | ~{p['est_tokens']:<7} | {t_badge:<5} | {pl_badge:<5}")
    if len(prompts) > args.limit:
        print(f"\n... and {len(prompts) - args.limit} more. Use --limit to display more.")

def cmd_search(args, data):
    query = args.query.lower()
    results = []
    
    for p in data["prompts"]:
        if args.provider and p["provider"].lower() != args.provider.lower():
            continue
            
        full_file = REPO_ROOT / p["rel_path"]
        content = ""
        if full_file.exists() and args.deep:
            try:
                content = full_file.read_text(encoding="utf-8", errors="replace").lower()
            except:
                pass
                
        matches_meta = (
            query in p["model_name"].lower() or 
            query in p["category"].lower() or 
            query in p["excerpt"].lower() or 
            any(query in t.lower() for t in p["detected_tools"])
        )
        matches_deep = query in content if args.deep else False
        
        if matches_meta or matches_deep:
            results.append(p)
            
    print(f"\n--- Search results for '{args.query}' ({len(results)} found) ---\n")
    for r in results[:args.limit]:
        print(f"[{r['provider']}] {r['model_name']} (~{r['est_tokens']:,} tokens)")
        print(f"  Path: {r['rel_path']}")
        if r['detected_tools']:
            print(f"  Tools: {', '.join(r['detected_tools'])}")
        print(f"  Excerpt: {r['excerpt'][:120]}...\n")

def cmd_show(args, data):
    target = args.id_or_path.replace("\\", "/")
    matched = None
    for p in data["prompts"]:
        if target.lower() in p["rel_path"].lower() or target.lower() in p["id"].lower():
            matched = p
            break
            
    if not matched:
        print(f"Prompt matching '{args.id_or_path}' not found.")
        return
        
    full_path = REPO_ROOT / matched["rel_path"]
    if not full_path.exists():
        print(f"File not found on disk: {full_path}")
        return
        
    print("=" * 80)
    print(f"Model: {matched['model_name']} | Provider: {matched['provider']} | Category: {matched['category']}")
    print(f"Tokens: ~{matched['est_tokens']:,} | Lines: {matched['line_count']} | Path: {matched['rel_path']}")
    print(f"Tools Detected: {', '.join(matched['detected_tools']) or 'None'}")
    print("=" * 80)
    print()
    content = full_path.read_text(encoding="utf-8", errors="replace")
    if args.lines and args.lines > 0:
        lines = content.splitlines()[:args.lines]
        print("\n".join(lines))
        if len(lines) < matched['line_count']:
            print(f"\n... [Truncated at {args.lines} lines. Omit --lines to see full prompt]")
    else:
        print(content)

def cmd_compare(args, data):
    def find_prompt(term):
        term = term.replace("\\", "/").lower()
        for p in data["prompts"]:
            if term in p["rel_path"].lower() or term in p["id"].lower():
                return p
        return None
        
    p1 = find_prompt(args.prompt1)
    p2 = find_prompt(args.prompt2)
    
    if not p1:
        print(f"Error: Prompt 1 '{args.prompt1}' not found.")
        return
    if not p2:
        print(f"Error: Prompt 2 '{args.prompt2}' not found.")
        return
        
    print("\n" + "=" * 80)
    print("SYSTEM PROMPT ARCHITECTURAL COMPARISON")
    print("=" * 80)
    print(f"{'Metric / Feature':<25} | {'Prompt 1':<25} | {'Prompt 2':<25}")
    print("-" * 80)
    print(f"{'Model Name':<25} | {p1['model_name']:<25} | {p2['model_name']:<25}")
    print(f"{'Provider':<25} | {p1['provider']:<25} | {p2['provider']:<25}")
    print(f"{'Estimated Tokens':<25} | {p1['est_tokens']:<25} | {p2['est_tokens']:<25}")
    print(f"{'Total Lines':<25} | {p1['line_count']:<25} | {p2['line_count']:<25}")
    print(f"{'Tool Calling':<25} | {str(p1['has_tools']):<25} | {str(p2['has_tools']):<25}")
    print(f"{'Planning Mode':<25} | {str(p1['has_planning']):<25} | {str(p2['has_planning']):<25}")
    print(f"{'Subagents':<25} | {str(p1['has_subagents']):<25} | {str(p2['has_subagents']):<25}")
    print(f"{'Shell Execution':<25} | {str(p1['has_shell']):<25} | {str(p2['has_shell']):<25}")
    print(f"{'Safety Guardrails':<25} | {str(p1['has_safety']):<25} | {str(p2['has_safety']):<25}")
    print("-" * 80)
    print(f"P1 Tools: {', '.join(p1['detected_tools']) or 'None'}")
    print(f"P2 Tools: {', '.join(p2['detected_tools']) or 'None'}")
    print("=" * 80 + "\n")

def cmd_tools(args, data):
    all_tools = {}
    for p in data["prompts"]:
        if args.provider and p["provider"].lower() != args.provider.lower():
            continue
        for t in p["detected_tools"]:
            if t not in all_tools:
                all_tools[t] = []
            all_tools[t].append(f"{p['provider']}/{p['model_name']}")
            
    print(f"\n--- Extracted Tool Signatures ({len(all_tools)} unique tools) ---\n")
    for t, origins in sorted(all_tools.items(), key=lambda x: len(x[1]), reverse=True)[:args.limit]:
        print(f"• {t:<25} (Used in {len(origins)} prompts: {', '.join(origins[:3])})")

def main():
    parser = argparse.ArgumentParser(description="System Prompts Intelligence CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")
    
    # List
    p_list = subparsers.add_parser("list", help="List system prompts")
    p_list.add_argument("--provider", "-p", help="Filter by provider")
    p_list.add_argument("--has-tools", action="store_true", help="Only prompts with tool calling")
    p_list.add_argument("--has-planning", action="store_true", help="Only prompts with planning mode")
    p_list.add_argument("--has-subagents", action="store_true", help="Only prompts with subagents")
    p_list.add_argument("--limit", "-n", type=int, default=30, help="Max results to show")
    
    # Search
    p_search = subparsers.add_parser("search", help="Search system prompts")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--provider", "-p", help="Filter by provider")
    p_search.add_argument("--deep", "-d", action="store_true", help="Search full text file contents")
    p_search.add_argument("--limit", "-n", type=int, default=20, help="Max results to show")
    
    # Show
    p_show = subparsers.add_parser("show", help="View full system prompt")
    p_show.add_argument("id_or_path", help="Prompt ID, filename, or relative path")
    p_show.add_argument("--lines", "-l", type=int, default=0, help="Number of lines to show (0 for all)")
    
    # Compare
    p_comp = subparsers.add_parser("compare", help="Compare two system prompts")
    p_comp.add_argument("prompt1", help="First prompt path or keyword")
    p_comp.add_argument("prompt2", help="Second prompt path or keyword")
    
    # Tools
    p_tools = subparsers.add_parser("tools", help="Inspect detected tools")
    p_tools.add_argument("--provider", "-p", help="Filter by provider")
    p_tools.add_argument("--limit", "-n", type=int, default=40, help="Max tools to show")
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    data = load_index()
    
    if args.command == "list":
        cmd_list(args, data)
    elif args.command == "search":
        cmd_search(args, data)
    elif args.command == "show":
        cmd_show(args, data)
    elif args.command == "compare":
        cmd_compare(args, data)
    elif args.command == "tools":
        cmd_tools(args, data)

if __name__ == "__main__":
    main()
