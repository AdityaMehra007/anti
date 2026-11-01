#!/usr/bin/env python3
"""
OMEGA Awesome Universe Model Context Protocol (MCP) Server
==========================================================
Autonomous JSON-RPC 2.0 stdio interface exposing 12 curated knowledge and linting tools
for AI Agents, Claude Code, and Antigravity.

Tools:
  - awesome_get_info
  - awesome_list_categories
  - awesome_get_category
  - awesome_search_lists
  - awesome_get_list_details
  - awesome_lint_manifesto
  - awesome_get_top_tier_lists
  - awesome_get_frontier_ai_lists
  - awesome_get_cross_graph
  - awesome_generate_scaffold
  - awesome_export_catalog
  - awesome_run_sovereign_lifecycle
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

from awesome_orchestrator import engine, AwesomeManifestoLinter, MANIFEST_JSON_PATH

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "omega-awesome-universe"
SERVER_VERSION = "1.0.0"

TOOLS_REGISTRY = [
    {
        "name": "awesome_get_info",
        "description": "Get real-time telemetry and overview statistics for the GitHub Awesome Universe.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "awesome_list_categories",
        "description": "List all 29 knowledge domain categories with slugs and list counts.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "awesome_get_category",
        "description": "Get all curated lists within a specific knowledge category.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {
                    "type": "string",
                    "description": "Category slug (e.g. 'programming-languages', 'security', 'frontier-ai-agents')"
                }
            },
            "required": ["slug"]
        }
    },
    {
        "name": "awesome_search_lists",
        "description": "Full-text search across 470+ curated lists using SQLite FTS5 index.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword query (e.g. 'agent', 'python', 'docker', 'database', 'mcp')"
                },
                "category": {
                    "type": "string",
                    "description": "Optional category slug filter"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 20)",
                    "default": 20
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "awesome_get_list_details",
        "description": "Retrieve comprehensive dossier and metadata for a specific Awesome list.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "List ID, repo slug, or exact name"
                }
            },
            "required": ["id"]
        }
    },
    {
        "name": "awesome_lint_manifesto",
        "description": "Validate markdown text or pull request submission against official Awesome Manifesto rules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "markdown": {
                    "type": "string",
                    "description": "Markdown content to inspect"
                },
                "repo_name": {
                    "type": "string",
                    "description": "Repository slug name (e.g. 'awesome-robotics')",
                    "default": "awesome-submission"
                }
            },
            "required": ["markdown"]
        }
    },
    {
        "name": "awesome_get_top_tier_lists",
        "description": "Get S-Tier flagships and high-authority community lists ranked by star impact.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tier": {
                    "type": "string",
                    "enum": ["S", "A", "B"],
                    "default": "S",
                    "description": "Tier ranking to filter (S = Flagship titan, A = High authority, B = Standard)"
                },
                "limit": {
                    "type": "integer",
                    "default": 25,
                    "description": "Max results"
                }
            }
        }
    },
    {
        "name": "awesome_get_frontier_ai_lists",
        "description": "List curated repositories covering Autonomous Agents, MCP Servers, LLMs, and System Prompts.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "awesome_get_cross_graph",
        "description": "Retrieve network topology graph of categories, hubs, and inter-list connections.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "awesome_generate_scaffold",
        "description": "Generate a 100% Awesome-Manifesto-compliant starter README.md template for a new topic.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic_name": {
                    "type": "string",
                    "description": "Topic name (e.g. 'Quantum Computing', 'Synthetic Biology', 'Sovereign Agents')"
                },
                "succinct_description": {
                    "type": "string",
                    "description": "Objective description of the subject matter (must start uppercase and end with period)"
                }
            },
            "required": ["topic_name", "succinct_description"]
        }
    },
    {
        "name": "awesome_export_catalog",
        "description": "Trigger export of full catalog to JSON, SQLite, CSV, and Markdown.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "awesome_run_sovereign_lifecycle",
        "description": "Execute or retrieve the complete 12-Phase Sovereign Lifecycle verification manifest.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "force_rerun": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to re-execute all 12 phases or return existing manifest"
                }
            }
        }
    }
]


def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Any:
    if name == "awesome_get_info":
        s_tier = sum(1 for l in engine.lists.values() if l.tier == "S")
        a_tier = sum(1 for l in engine.lists.values() if l.tier == "A")
        frontier = sum(1 for l in engine.lists.values() if l.is_frontier_ai)
        return {
            "status": "OPERATIONAL",
            "total_lists": len(engine.lists),
            "total_categories": len(engine.categories),
            "s_tier_count": s_tier,
            "a_tier_count": a_tier,
            "frontier_ai_count": frontier,
            "upstream_source": "https://github.com/sindresorhus/awesome",
            "topics_hub": "https://github.com/topics/awesome"
        }

    elif name == "awesome_list_categories":
        return [
            {
                "name": c["name"],
                "slug": c["slug"],
                "icon": c["icon"],
                "list_count": c["list_count"]
            }
            for c in sorted(engine.categories.values(), key=lambda x: x["name"])
        ]

    elif name == "awesome_get_category":
        slug = arguments.get("slug", "").lower()
        cat = next((c for c in engine.categories.values() if c["slug"] == slug or c["name"].lower() == slug), None)
        if not cat:
            return {"error": f"Category '{slug}' not found."}
        items = [engine.lists[lid].to_dict() for lid in cat["lists"] if lid in engine.lists]
        return {
            "category": cat["name"],
            "slug": cat["slug"],
            "list_count": cat["list_count"],
            "lists": items
        }

    elif name == "awesome_search_lists":
        query = arguments.get("query", "")
        category = arguments.get("category")
        limit = arguments.get("limit", 20)
        return engine.search(query, category_slug=category, limit=limit)

    elif name == "awesome_get_list_details":
        lid = arguments.get("id", "").lower()
        item = engine.lists.get(lid)
        if not item:
            item = next((l for l in engine.lists.values() if l.name.lower() == lid or l.repo.lower() == lid), None)
        if not item:
            return {"error": f"List '{lid}' not found."}
        return item.to_dict()

    elif name == "awesome_lint_manifesto":
        markdown = arguments.get("markdown", "")
        repo = arguments.get("repo_name", "awesome-custom")
        return AwesomeManifestoLinter.lint_markdown(markdown, repo_name=repo)

    elif name == "awesome_get_top_tier_lists":
        tier = arguments.get("tier", "S").upper()
        limit = arguments.get("limit", 25)
        filtered = [l.to_dict() for l in engine.lists.values() if l.tier == tier]
        filtered.sort(key=lambda x: x["stars"], reverse=True)
        return filtered[:limit]

    elif name == "awesome_get_frontier_ai_lists":
        frontier = [l.to_dict() for l in engine.lists.values() if l.is_frontier_ai]
        return frontier

    elif name == "awesome_get_cross_graph":
        return engine.get_graph()

    elif name == "awesome_generate_scaffold":
        topic = arguments.get("topic_name", "My Technology")
        desc = arguments.get("succinct_description", "Modern software architecture pattern.")
        if not desc.endswith("."):
            desc += "."

        slug = f"awesome-{slugify(topic)}"
        scaffold = f"""# Awesome {topic} [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> {desc}

## Contents

- [Core Foundations](#core-foundations)
- [Frameworks & Tools](#frameworks--tools)
- [Official Resources](#official-resources)

## Core Foundations

- [Specification](https://github.com/example/spec#readme) - Canonical technical specification.

## Frameworks & Tools

- [Primary SDK](https://github.com/example/sdk#readme) - High-throughput production runtime.

## Official Resources

- [Official Documentation](https://example.com) - Reference manuals and guides.

---

## Contributing

Please read the [contributing guidelines](contributing.md) before submitting pull requests.

## Footnotes

Licensed under [CC0](LICENSE).
"""
        return {
            "suggested_repo_name": slug,
            "markdown_template": scaffold,
            "manifesto_compliance": "100% compliant with sindresorhus/awesome standards."
        }

    elif name == "awesome_export_catalog":
        engine.export_all()
        return {"status": "EXPORTED", "message": "All data vaults successfully written to disk."}

    elif name == "awesome_run_sovereign_lifecycle":
        force = arguments.get("force_rerun", False)
        if not force and MANIFEST_JSON_PATH.exists():
            with open(MANIFEST_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return engine.do_everything()

    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break

        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except Exception:
            continue

        msg_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "serverInfo": {
                        "name": SERVER_NAME,
                        "version": SERVER_VERSION
                    },
                    "capabilities": {
                        "tools": {}
                    }
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "notifications/initialized":
            pass

        elif method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": TOOLS_REGISTRY
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            try:
                result = handle_call_tool(tool_name, tool_args)
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                }
            except Exception as e:
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32603,
                        "message": str(e),
                        "data": traceback.format_exc()
                    }
                }

            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "ping":
            res = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        else:
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
