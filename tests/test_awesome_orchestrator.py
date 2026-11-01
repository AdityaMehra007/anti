"""
Tests for OMEGA Awesome Universe Autonomous Orchestrator
========================================================
Comprehensive pytest test suite covering:
1. Curated list ingestion & category normalization
2. S-Tier titans & star impact weighting
3. Frontier AI & Agentic repositories
4. SQLite FTS5 lightning search
5. Awesome Manifesto & PR linter rules
6. Topological cross-category graph
7. Multi-vault export formats
8. 12-Phase Sovereign Lifecycle execution
"""

import pytest
import os
import json
from pathlib import Path
from awesome_orchestrator import (
    AwesomeUniverseEngine,
    AwesomeEntry,
    AwesomeManifestoLinter,
    engine,
    SQLITE_DB_PATH,
    UNIVERSE_JSON_PATH,
    MANIFEST_JSON_PATH
)


def test_universe_initialization():
    """Verify engine successfully parsed upstream Awesome lists."""
    assert len(engine.lists) >= 460
    assert len(engine.categories) >= 28


def test_category_taxonomies():
    """Verify essential knowledge domains are present."""
    required_cats = [
        "Platforms", "Programming Languages", "Front-End Development",
        "Back-End Development", "Computer Science", "Big Data",
        "Security", "Databases", "Frontier AI & Agents"
    ]
    for cat in required_cats:
        assert cat in engine.categories, f"Missing category: {cat}"
        assert engine.categories[cat]["list_count"] > 0


def test_s_tier_flagship_presence():
    """Verify flagship titans are recognized as S-Tier."""
    s_tier_items = [l for l in engine.lists.values() if l.tier == "S"]
    assert len(s_tier_items) >= 10
    names = [l.name.lower() for l in s_tier_items]
    assert any("node" in n for n in names)
    assert any("python" in n for n in names)


def test_frontier_ai_agents():
    """Verify cutting-edge Agentic, MCP, and LLM lists are integrated."""
    frontier_items = [l for l in engine.lists.values() if l.is_frontier_ai]
    assert len(frontier_items) >= 6
    names = [l.name for l in frontier_items]
    assert "Awesome AI Agents" in names
    assert "Awesome MCP Servers" in names
    assert "Awesome LLM" in names
    assert "Awesome ChatGPT Prompts" in names


def test_fts5_search():
    """Test full-text search across various queries."""
    res_py = engine.search("python")
    assert len(res_py) > 0
    assert any("python" in r["name"].lower() or "python" in r["description"].lower() for r in res_py)

    res_agents = engine.search("agents")
    assert len(res_agents) >= 3

    res_mcp = engine.search("mcp")
    assert len(res_mcp) >= 1
    assert any("mcp" in r["name"].lower() or "mcp" in r["description"].lower() for r in res_mcp)


def test_manifesto_linter_compliant_sample():
    """Verify linter gives high score to a compliant list."""
    compliant_md = (
        "# Awesome Robotics [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)\n\n"
        "Autonomous mobile robotics and sensor fusion architectures.\n\n"
        "## Contents\n\n"
        "- [Navigation](#navigation)\n\n"
        "## Navigation\n\n"
        "- [ROS 2](https://github.com/ros2/ros2#readme) - Robot operating system core framework.\n\n"
        "## Contributing\n\n"
        "See contributing.md."
    )
    report = AwesomeManifestoLinter.lint_markdown(compliant_md, repo_name="awesome-robotics")
    assert report["manifesto_score"] >= 80
    assert report["status"] == "COMPLIANT"


def test_manifesto_linter_rule_violations():
    """Verify linter catches common Awesome Manifesto rule breaches."""
    bad_md = (
        "# awesome tool\n\n"
        "The world's best miraculous collection of crazy stuff.\n\n"
        "## Table of Contents\n\n"
        "- [Bad Link](https://github.com/test/lib) - the best ultimate library with no period\n"
        "- [Crypto Token](https://example.com) - buy this cryptocurrency coin now."
    )
    report = AwesomeManifestoLinter.lint_markdown(bad_md, repo_name="not-starting-with-awesome")
    assert report["status"] == "NEEDS_REVISION"
    issues = [i["rule"] for i in report["issues"]]
    assert "REPO_NAME_FORMAT" in issues
    assert "HEADER_TITLE_CASE" in issues
    assert "TOC_NAME_CONVENTION" in issues
    assert "AWESOME_BADGE_MISSING" in issues
    assert "ENTRY_TERMINAL_PERIOD" in issues
    assert "OBJECTIVE_TONE" in issues
    assert "NO_BLOCKCHAIN_SPAM" in issues


def test_cross_category_graph():
    """Verify network topology graph generation."""
    graph = engine.get_graph()
    assert graph["total_nodes"] > 30
    assert graph["total_links"] > 30
    assert any(n["type"] == "category" for n in graph["nodes"])
    assert any(n["type"] == "list" for n in graph["nodes"])


def test_data_vault_exports():
    """Verify data vaults exist and are non-empty."""
    engine.export_all()
    assert UNIVERSE_JSON_PATH.exists()
    assert UNIVERSE_JSON_PATH.stat().st_size > 50000

    assert SQLITE_DB_PATH.exists()
    assert SQLITE_DB_PATH.stat().st_size > 50000


def test_12_phase_sovereign_lifecycle():
    """Verify full 12-phase sovereign lifecycle execution."""
    manifest = engine.do_everything()
    assert manifest["total_phases_executed"] == 12
    assert manifest["overall_status"] == "SOVEREIGN AWESOME UNIVERSE SUITE OPERATIONAL — 100% ATTESTED"
    for phase in manifest["phases"]:
        assert phase["status"] == "PASSED"
        assert phase["elapsed_seconds"] >= 0.0
    assert MANIFEST_JSON_PATH.exists()
