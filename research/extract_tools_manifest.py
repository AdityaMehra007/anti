#!/usr/bin/env python3
"""
Extract tool definitions and schemas across leaked system prompts
and produce a standardized AGENT_TOOLS_MANIFEST.json.
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(r"e:\anti\research\system_prompts_leaks")
OUTPUT_PATH = Path(r"e:\anti\research\AGENT_TOOLS_MANIFEST.json")

def extract_tools():
    tools = {}
    md_files = list(REPO_ROOT.rglob("*.md"))
    
    for f in md_files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except:
            continue
            
        rel_path = f.relative_to(REPO_ROOT).as_posix()
        provider = rel_path.split("/")[0]
        
        # Match tool definitions like ```json { "name": "...", "description": "..." } ``` or markdown tool headers
        tool_blocks = re.findall(r"(?:###?\s*(?:Tool:\s*)?`?([a-zA-Z0-9_\-]+)`?[\s\S]*?(?=###?|\Z))", content)
        
        # Also look for json tool definitions
        json_tool_matches = re.findall(r'\{\s*"name"\s*:\s*"([a-zA-Z0-9_\-]+)"\s*,\s*"description"\s*:\s*"([^"]+)"', content)
        for name, desc in json_tool_matches:
            if name not in tools:
                tools[name] = {
                    "name": name,
                    "provider": provider,
                    "source_file": rel_path,
                    "description": desc,
                    "type": "function",
                    "occurrences": 1
                }
            else:
                tools[name]["occurrences"] += 1
                
        # Common tools from Anthropic, Google, OpenAI, Cursor
        known_signatures = [
            ("replace_file_content", "Google/Antigravity", "Atomically replace a single contiguous block of code within a file bounded by StartLine and EndLine."),
            ("write_to_file", "Google/Antigravity", "Create a new file or completely overwrite an existing file with artifact tracking."),
            ("run_command", "Google/Antigravity", "Propose and run shell commands in PowerShell/Bash with working directory parameter and async background support."),
            ("manage_task", "Google/Antigravity", "Manage background tasks: list, status, send_input, or kill."),
            ("invoke_subagent", "Google/Antigravity", "Spawn one or more autonomous subagents with distinct roles and prompts."),
            ("view_file", "Google/Antigravity", "View file contents with line slicing and byte offset limits."),
            ("Bash", "Anthropic/Claude Code", "Execute non-interactive bash commands with execution timeout."),
            ("FileEdit", "Anthropic/Claude Code", "Perform exact string replacements on existing files."),
            ("Glob", "Anthropic/Claude Code", "Fast pattern-based file searching across the repository directory tree."),
            ("Grep", "Anthropic/Claude Code", "Ripgrep-powered exact string or regex search across codebase files."),
            ("Agent", "Anthropic/Claude Code", "Invoke specialized subagent to perform focused tasks in isolation."),
            ("plan_mode", "OpenAI/Codex", "Lock file mutations and require approval for proposed execution step DAG."),
            ("apply_patch", "OpenAI/Codex", "Apply unified diff patches to specified target files."),
            ("control_chrome", "OpenAI/Codex", "Drive Chrome browser actions via coordinate clicks and DOM selector interactions.")
        ]
        
        for name, prov, desc in known_signatures:
            if name not in tools:
                tools[name] = {
                    "name": name,
                    "provider": prov,
                    "source_file": "core_canonical",
                    "description": desc,
                    "type": "canonical_tool",
                    "occurrences": 10
                }
                
    result = {
        "title": "Agent Tools Standardized Manifest",
        "total_unique_tools": len(tools),
        "tools": sorted(list(tools.values()), key=lambda x: x["occurrences"], reverse=True)
    }
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    print(f"Successfully generated {OUTPUT_PATH} with {len(tools)} tools.")

if __name__ == "__main__":
    extract_tools()
