"""
prompts_chat_mcp_server.py — Model Context Protocol (MCP) Server for prompts.chat
================================================================================
Stdio-based JSON-RPC MCP server exposing the 2,627 prompts.chat library to
Antigravity, Claude Code, Cursor, and any MCP-compliant AI client.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any, Dict, List, Optional

from prompts_chat_engine import (
    QualityScorer,
    VariableExtractor,
    get_engine,
)

SERVER_NAME = "prompts-chat"
SERVER_VERSION = "1.0.0"

TOOLS = [
    {
        "name": "search_prompts",
        "description": "Search 2,627+ battle-tested persona and system prompts from prompts.chat by keyword, category, or developer flag.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword or phrase (e.g. 'linux terminal', 'python', 'interviewer')"},
                "category": {"type": "string", "description": "Optional category filter (e.g. 'Software & Coding', 'Business & Strategy', 'Writing & Editorial')"},
                "for_devs": {"type": "boolean", "description": "Filter strictly for developer-oriented prompts"},
                "limit": {"type": "integer", "description": "Max number of results to return (default: 10, max: 50)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_prompt",
        "description": "Get the complete prompt text, variable schema, and archetype metadata for a specific act or slug.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "act_or_slug": {"type": "string", "description": "The exact Act name (e.g. 'Linux Terminal') or slug (e.g. 'linux-terminal')"}
            },
            "required": ["act_or_slug"]
        }
    },
    {
        "name": "fill_prompt",
        "description": "Interpolate parameterized variables into a prompt template.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "act_or_slug": {"type": "string", "description": "The Act name or slug"},
                "variables": {
                    "type": "object",
                    "description": "Key-value dictionary of variable substitutions",
                    "additionalProperties": {"type": "string"}
                }
            },
            "required": ["act_or_slug", "variables"]
        }
    },
    {
        "name": "improve_prompt",
        "description": "Analyze an existing prompt and augment it with role grounding, strict negative constraints, and structured output formatting.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The prompt text to improve"}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "analyze_prompt_quality",
        "description": "Audit a prompt's completeness, constraint density, and formatting rules, returning a 0-100 score and recommendations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The prompt text to analyze"}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "random_prompt",
        "description": "Fetch a random high-quality prompt from the library, optionally filtered by category or developer flag.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Optional category filter"},
                "for_devs": {"type": "boolean", "description": "Filter for developer prompts"}
            }
        }
    },
    {
        "name": "get_prompts_chat_stats",
        "description": "Get census and distribution statistics for the 2,627 prompt library.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "search_skills",
        "description": "Search across the 3,841+ installed agent skills in the repository by name or capability description.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword (e.g. 'tdd', 'career', 'database', 'docker')"},
                "limit": {"type": "integer", "description": "Maximum results to return (default: 10)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_skill",
        "description": "Retrieve full instruction set, SKILL.md, and file manifest for an installed agent skill.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The exact skill name or directory slug"}
            },
            "required": ["name"]
        }
    }
]


def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    engine = get_engine()

    if name == "search_prompts":
        query = arguments.get("query", "")
        category = arguments.get("category")
        for_devs = arguments.get("for_devs")
        limit = min(50, max(1, int(arguments.get("limit", 10))))

        records, total = engine.search(query=query, category=category, for_devs=for_devs, limit=limit)
        results = [
            {
                "id": r.id,
                "slug": r.slug,
                "act": r.act,
                "category": r.category,
                "for_devs": r.for_devs,
                "quality_score": r.quality_score,
                "variables": [v.to_dict() for v in r.variables],
                "preview": r.prompt[:250] + ("..." if len(r.prompt) > 250 else "")
            }
            for r in records
        ]
        return {
            "total_matches": total,
            "returned_count": len(results),
            "results": results
        }

    elif name == "get_prompt":
        act_or_slug = arguments.get("act_or_slug", "")
        record = engine.get_by_act(act_or_slug) or engine.get_by_slug(act_or_slug)
        if not record:
            return {"error": f"Prompt not found for '{act_or_slug}'"}
        return record.to_dict()

    elif name == "fill_prompt":
        act_or_slug = arguments.get("act_or_slug", "")
        variables = arguments.get("variables", {})
        record = engine.get_by_act(act_or_slug) or engine.get_by_slug(act_or_slug)
        if not record:
            return {"error": f"Prompt not found for '{act_or_slug}'"}

        filled = VariableExtractor.interpolate(record.prompt, variables)
        return {
            "act": record.act,
            "original_prompt": record.prompt,
            "filled_prompt": filled,
            "variables_applied": variables
        }

    elif name == "improve_prompt":
        prompt_text = arguments.get("prompt", "").strip()
        score, positives = QualityScorer.score(prompt_text)

        # Standard prompt engineering transformation rules
        improved = prompt_text
        if not re.search(r"i want you to act as|you are an? expert", improved, re.I):
            improved = f"You are an expert specialist. {improved}"
        if not re.search(r"do not|avoid|never|only reply", improved, re.I):
            improved += "\n\nOperating Constraints:\n- Do not include unsolicited preamble or postamble.\n- Only output the exact requested content.\n- Adhere strictly to the required format."
        if not re.search(r"markdown|code block|bullet points|json", improved, re.I):
            improved += "\n\nOutput Format:\n- Format your response using clean GitHub-flavored markdown."

        new_score, new_positives = QualityScorer.score(improved)
        return {
            "original_score": score,
            "improved_score": new_score,
            "improvements_made": list(set(new_positives) - set(positives)),
            "improved_prompt": improved
        }

    elif name == "analyze_prompt_quality":
        prompt_text = arguments.get("prompt", "")
        score, positives = QualityScorer.score(prompt_text)
        recommendations = []
        if score < 50:
            recommendations.append("Add explicit role definition (e.g. 'I want you to act as...')")
            recommendations.append("Add clear negative constraints (e.g. 'Do not write explanations, only output...')")
        if "Output structure specification" not in positives:
            recommendations.append("Specify expected output format (JSON, markdown table, code block)")
        if "Immediate priming sequence" not in positives:
            recommendations.append("Provide the initial seed input or first interaction sequence")

        return {
            "quality_score": score,
            "strengths": positives,
            "recommendations": recommendations,
            "char_count": len(prompt_text),
            "word_count": len(prompt_text.split())
        }

    elif name == "random_prompt":
        category = arguments.get("category")
        for_devs = arguments.get("for_devs")
        record = engine.get_random(for_devs=for_devs, category=category)
        if not record:
            return {"error": "No prompt found matching criteria"}
        return record.to_dict()

    elif name == "get_prompts_chat_stats":
        return engine.get_stats()

    elif name == "search_skills":
        query = arguments.get("query", "")
        limit = min(50, max(1, int(arguments.get("limit", 10))))
        skills = engine.search_skills(query, limit=limit)
        return {
            "query": query,
            "total_returned": len(skills),
            "skills": skills
        }

    elif name == "get_skill":
        skill_name = arguments.get("name", "")
        skill_data = engine.get_skill(skill_name)
        if not skill_data:
            return {"error": f"Skill '{skill_name}' not found"}
        return skill_data

    else:
        return {"error": f"Unknown tool: {name}"}


def main():
    """Runs the MCP server over stdio reading JSON-RPC messages."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": SERVER_NA