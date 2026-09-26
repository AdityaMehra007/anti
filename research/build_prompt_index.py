#!/usr/bin/env python3
"""
System Prompts Master Indexer & Analyzer
Parses all system prompts in research/system_prompts_leaks, extracts metadata,
detects capabilities/tools/guardrails, and outputs structured JSON and Markdown compendiums.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(r"e:\anti\research\system_prompts_leaks")
OUTPUT_JSON = Path(r"e:\anti\research\SYSTEM_PROMPTS_MASTER_INDEX.json")
OUTPUT_MD = Path(r"e:\anti\research\SYSTEM_PROMPTS_COMPENDIUM.md")

CAPABILITY_PATTERNS = {
    "tool_calling": [r"tool_calls", r"tools\b", r"call_tool", r"functions\b", r"parameters\b", r"tool_choice"],
    "shell_execution": [r"\bbash\b", r"\bpowershell\b", r"\bterminal\b", r"run_command", r"commandline", r"shell\b"],
    "file_editing": [r"replace_file", r"write_to_file", r"edit_file", r"patch", r"create_file", r"file_search", r"view_file"],
    "planning_mode": [r"planning mode", r"implementation_plan", r"plan mode", r"plan_mode", r"task list", r"dag\b"],
    "subagents": [r"subagent", r"invoke_subagent", r"dispatch", r"multi-agent", r"agentic loop"],
    "web_search": [r"search_web", r"web_search", r"google_search", r"bing_search", r"browse_web"],
    "browser_computer_use": [r"computer use", r"control_chrome", r"in-app browser", r"playwright", r"mouse_click", r"screenshot"],
    "voice_audio": [r"voice mode", r"realtime audio", r"text-to-speech", r"audio input", r"voice assistant"],
    "memory_persistence": [r"memory store", r"long-term memory", r"persistent memory", r"user profile"],
    "safety_guardrails": [r"jailbreak", r"forbidden", r"harmful", r"unacceptable", r"never execute", r"safety guard", r"safety policies"]
}

def clean_title(filename_stem):
    title = filename_stem.replace("-", " ").replace("_", " ")
    return " ".join(word.capitalize() if not word.isupper() else word for word in title.split())

def extract_metadata(file_path: Path):
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return None

    rel_path = file_path.relative_to(REPO_ROOT).as_posix()
    parts = rel_path.split("/")
    
    provider = parts[0] if len(parts) > 1 else "Root"
    sub_category = parts[1] if len(parts) > 2 else "Core"
    model_name = clean_title(file_path.stem)
    
    lines = content.splitlines()
    line_count = len(lines)
    char_count = len(content)
    word_count = len(content.split())
    est_tokens = int(char_count / 3.8)  # standard approx token multiplier
    
    # Extract excerpt
    non_empty_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("---")]
    excerpt = " ".join(non_empty_lines[:3])[:300] if non_empty_lines else ""
    if len(excerpt) == 300:
        excerpt += "..."
        
    # Detect capabilities
    content_lower = content.lower()
    capabilities = {}
    for cap_name, patterns in CAPABILITY_PATTERNS.items():
        capabilities[cap_name] = any(re.search(pat, content_lower) for pat in patterns)
        
    # Detect declared tools
    found_tools = re.findall(r"(?:name|tool):\s*[\"']?([a-zA-Z0-9_\-\.]+)", content)
    unique_tools = sorted(list(set(found_tools)))[:10]

    return {
        "id": rel_path.replace("/", "__").replace(".", "_"),
        "rel_path": rel_path,
        "provider": provider,
        "category": sub_category,
        "model_name": model_name,
        "filename": file_path.name,
        "line_count": line_count,
        "char_count": char_count,
        "word_count": word_count,
        "est_tokens": est_tokens,
        "excerpt": excerpt,
        "capabilities": capabilities,
        "detected_tools": unique_tools,
        "has_tools": capabilities["tool_calling"],
        "has_shell": capabilities["shell_execution"],
        "has_planning": capabilities["planning_mode"],
        "has_subagents": capabilities["subagents"],
        "has_safety": capabilities["safety_guardrails"]
    }

def main():
    print(f"Scanning markdown files in {REPO_ROOT}...")
    md_files = list(REPO_ROOT.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files.")
    
    records = []
    for f in md_files:
        meta = extract_metadata(f)
        if meta:
            records.append(meta)
            
    # Sort by provider then model name
    records.sort(key=lambda r: (r["provider"].lower(), r["model_name"].lower()))
    
    # Provider statistics
    provider_stats = {}
    for r in records:
        p = r["provider"]
        if p not in provider_stats:
            provider_stats[p] = {
                "count": 0,
                "total_tokens": 0,
                "tool_calling_count": 0,
                "planning_count": 0,
                "subagent_count": 0,
                "shell_count": 0
            }
        provider_stats[p]["count"] += 1
        provider_stats[p]["total_tokens"] += r["est_tokens"]
        if r["has_tools"]: provider_stats[p]["tool_calling_count"] += 1
        if r["has_planning"]: provider_stats[p]["planning_count"] += 1
        if r["has_subagents"]: provider_stats[p]["subagent_count"] += 1
        if r["has_shell"]: provider_stats[p]["shell_count"] += 1
        
    master_index = {
        "generated_at": datetime.now().isoformat(),
        "total_prompts": len(records),
        "total_estimated_tokens": sum(r["est_tokens"] for r in records),
        "provider_breakdown": provider_stats,
        "prompts": records
    }
    
    # Write JSON
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(master_index, f, indent=2)
    print(f"Successfully wrote {OUTPUT_JSON} ({len(records)} records).")
    
    # Write Markdown Compendium
    lines = [
        "# SYSTEM PROMPTS MASTER COMPENDIUM",
        "",
        f"> **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Total Prompts**: {len(records):,} | **Estimated Total Tokens**: {master_index['total_estimated_tokens']:,}",
        "",
        "## 1. Provider & Ecosystem Overview",
        "",
        "| Provider / Lab | Prompts Count | Est. Tokens | Shell / Bash | Planning Mode | Subagents | Tool Calling |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for p, stats in sorted(provider_stats.items(), key=lambda x: x[1]["count"], reverse=True):
        lines.append(
            f"| **{p}** | {stats['count']} | {stats['total_tokens']:,} | "
            f"{stats['shell_count']} | {stats['planning_count']} | {stats['subagent_count']} | {stats['tool_calling_count']} |"
        )
        
    lines.extend([
        "",
        "---",
        "",
        "## 2. Flagship Systems Deep Inventory",
        ""
    ])
    
    current_prov = None
    for r in records:
        if r["provider"] != current_prov:
            current_prov = r["provider"]
            lines.extend([
                f"\n### {current_prov}\n",
                "| Model / Agent Name | Category | Tokens | Tools | Planning | Subagent | File Path |",
                "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
            ])
        
        tools_badge = "Yes" if r["has_tools"] else "-"
        plan_badge = "Yes" if r["has_planning"] else "-"
        subagent_badge = "Yes" if r["has_subagents"] else "-"
        
        lines.append(
            f"| **{r['model_name']}** | `{r['category']}` | ~{r['est_tokens']:,} | {tools_badge} | {plan_badge} | {subagent_badge} | [`{r['filename']}`](system_prompts_leaks/{r['rel_path']}) |"
        )
        
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"Successfully wrote {OUTPUT_MD}.")

if __name__ == "__main__":
    main()
