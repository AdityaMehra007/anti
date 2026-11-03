#!/usr/bin/env python3
"""
OMEGA Fast Deterministic MCP Tools Catalog Builder
==================================================
Extracts tool schemas, parameters, and metadata from all registered MCP servers
in milliseconds without blocking on network or slow native bindings.
"""

import sys
import ast
import json
from pathlib import Path

WORKSPACE_DIR = Path(r"E:\anti").resolve()
sys.path.insert(0, str(WORKSPACE_DIR))
from mcp_hub import MCPHub, SERVER_METADATA

def extract_python_tools(file_path: Path):
    """Extract tool list from python AST safely."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            tree = ast.parse(code)
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id in ("TOOLS", "TOOLS_REGISTRY"):
                            try:
                                return ast.literal_eval(node.value)
                            except Exception:
                                pass
                elif isinstance(node, ast.FunctionDef) and node.name == "get_tool_definitions":
                    # Look for return list
                    for stmt in node.body:
                        if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.List):
                            try:
                                return ast.literal_eval(stmt.value)
                            except Exception:
                                pass
    except Exception as e:
        print(f"AST parse error in {file_path.name}: {e}")
    return []

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    hub = MCPHub()
    catalog = []
    total_tools = 0

    print("Building OMEGA MCP Master Tools Catalog...")

    # Reference tool standard definitions
    REFERENCE_SPECS = {
        "filesystem": [
            {"name": "read_file", "description": "Read file contents from allowed paths", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
            {"name": "write_file", "description": "Write or overwrite file at path", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
            {"name": "list_directory", "description": "List files in directory", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
            {"name": "directory_tree", "description": "Get recursive directory tree", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
            {"name": "search_files", "description": "Search file paths matching glob/pattern", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}, "pattern": {"type": "string"}}, "required": ["path", "pattern"]}}
        ],
        "memory": [
            {"name": "create_entities", "description": "Create entities in knowledge graph", "inputSchema": {"type": "object", "properties": {"entities": {"type": "array"}}, "required": ["entities"]}},
            {"name": "create_relations", "description": "Create directed relations between entities", "inputSchema": {"type": "object", "properties": {"relations": {"type": "array"}}, "required": ["relations"]}},
            {"name": "read_graph", "description": "Read entire persistent knowledge graph", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "search_nodes", "description": "Search graph nodes by query substring", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
            {"name": "open_nodes", "description": "Open specific entities by names", "inputSchema": {"type": "object", "properties": {"names": {"type": "array"}}, "required": ["names"]}}
        ],
        "fetch": [
            {"name": "fetch", "description": "Fetch HTTP/HTTPS URL and convert to markdown/text for LLM grounding", "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}}
        ],
        "github": [
            {"name": "search_repositories", "description": "Search GitHub repositories by query and syntax", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
            {"name": "get_file_contents", "description": "Fetch content of file from GitHub repository", "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "path": {"type": "string"}}, "required": ["owner", "repo", "path"]}},
            {"name": "create_or_update_file", "description": "Commit file changes to repository branch", "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "path": {"type": "string"}, "content": {"type": "string"}}, "required": ["owner", "repo", "path", "content"]}},
            {"name": "create_issue", "description": "Create a new issue in repository", "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "title": {"type": "string"}}, "required": ["owner", "repo", "title"]}},
            {"name": "list_issues", "description": "List repository issues with state filtering", "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}}, "required": ["owner", "repo"]}},
            {"name": "create_pull_request", "description": "Open new pull request from branch", "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "title": {"type": "string"}, "head": {"type": "string"}, "base": {"type": "string"}}, "required": ["owner", "repo", "title", "head", "base"]}},
            {"name": "list_pull_requests", "description": "List pull requests in repository", "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}}, "required": ["owner", "repo"]}},
            {"name": "merge_pull_request", "description": "Merge approved pull request", "inputSchema": {"type": "object", "properties": {"owner": {"type": "string"}, "repo": {"type": "string"}, "pull_number": {"type": "number"}}, "required": ["owner", "repo", "pull_number"]}},
            {"name": "search_code", "description": "Search code across repositories", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}
        ],
        "git": [
            {"name": "git_status", "description": "Show git working tree status and untracked files", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "git_diff", "description": "Show unstaged or staged git diff", "inputSchema": {"type": "object", "properties": {"cached": {"type": "boolean"}}}},
            {"name": "git_log", "description": "Show commit logs with author and timestamps", "inputSchema": {"type": "object", "properties": {"max_count": {"type": "number"}}}},
            {"name": "git_branch", "description": "List local and remote branches", "inputSchema": {"type": "object", "properties": {}}}
        ],
        "sqlite": [
            {"name": "read_query", "description": "Execute SELECT query on SQLite database", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
            {"name": "write_query", "description": "Execute INSERT/UPDATE/DELETE query with transaction safety", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
            {"name": "describe_table", "description": "Get schema, columns, and foreign keys of table", "inputSchema": {"type": "object", "properties": {"table_name": {"type": "string"}}, "required": ["table_name"]}},
            {"name": "list_tables", "description": "List all tables in SQLite database", "inputSchema": {"type": "object", "properties": {}}}
        ],
        "chrome-devtools": [
            {"name": "navigate_to", "description": "Navigate Chrome browser to target URL", "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}},
            {"name": "take_screenshot", "description": "Capture viewport screenshot of current active page", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "evaluate_script", "description": "Evaluate arbitrary JavaScript in web context", "inputSchema": {"type": "object", "properties": {"script": {"type": "string"}}, "required": ["script"]}},
            {"name": "click_element", "description": "Click element by DOM CSS selector", "inputSchema": {"type": "object", "properties": {"selector": {"type": "string"}}, "required": ["selector"]}}
        ],
        "supabase": [
            {"name": "supabase_execute_sql", "description": "Execute parameterized SQL against remote Supabase Postgres", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
            {"name": "supabase_list_tables", "description": "List schema tables, types, and relations", "inputSchema": {"type": "object", "properties": {}}},
            {"name": "supabase_describe_table", "description": "Inspect column types and constraints", "inputSchema": {"type": "object", "properties": {"table": {"type": "string"}}, "required": ["table"]}},
            {"name": "supabase_vector_search", "description": "Query pgvector embedding similarity search", "inputSchema": {"type": "object", "properties": {"prompt": {"type": "string"}}, "required": ["prompt"]}},
            {"name": "supabase_rls_policy_audit", "description": "Audit row-level security policies across all tables", "inputSchema": {"type": "object", "properties": {}}}
        ],
        "omniroute": [
            {"name": "omniroute_route_prompt", "description": "Route prompt to optimal model tier based on latency, cost, and complexity", "inputSchema": {"type": "object", "properties": {"prompt": {"type": "string"}}, "required": ["prompt"]}},
            {"name": "omniroute_cost_summary", "description": "Retrieve token savings and routing stats across providers", "inputSchema": {"type": "object", "properties": {}}}
        ]
    }

    for name, cfg in hub.servers_config.items():
        meta = SERVER_METADATA.get(name, {
            "category": "Workspace Sovereign",
            "author": "OMEGA",
            "description": f"MCP Server {name}"
        })

        tools = []
        if name in REFERENCE_SPECS:
            tools = REFERENCE_SPECS[name]
        else:
            # Look for python server file
            script = meta.get("script") or f"{name.replace('-', '_')}_mcp_server.py"
            p_file = WORKSPACE_DIR / script
            if p_file.exists():
                tools = extract_python_tools(p_file)

        total_tools += len(tools)
        entry = {
            "server": name,
            "category": meta.get("category", "Workspace Sovereign"),
            "author": meta.get("author", "OMEGA"),
            "description": meta.get("description", ""),
            "type": "http" if "url" in cfg else "stdio",
            "command": cfg.get("command"),
            "args": cfg.get("args", []),
            "tools_count": len(tools),
            "tools": tools
        }
        catalog.append(entry)
        print(f"  [OK] {name:<18}: {len(tools):>2} tools | {entry['category']}")

    WORKSPACE_DIR.joinpath("data").mkdir(exist_ok=True)
    out_path = WORKSPACE_DIR / "data" / "mcp_tools_catalog.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print("-" * 60)
    print(f"Successfully generated {out_path}!")
    print(f"Total Configured Servers : {len(catalog)}")
    print(f"Total Extracted Tools    : {total_tools}")

if __name__ == "__main__":
    main()
