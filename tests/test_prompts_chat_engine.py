"""
tests/test_prompts_chat_engine.py — Unit Test Suite for prompts.chat Deep Engine
==============================================================================
Validates parsing, SQLite FTS5 search, variable interpolation, quality scoring,
MCP server tools, and REST API endpoints.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from prompts_chat_engine import (
    ArchetypeClassifier,
    PromptsChatEngine,
    PromptVariable,
    QualityScorer,
    VariableExtractor,
    get_engine,
    slugify,
)
import prompts_chat_mcp_server as mcp_server


@pytest.fixture(scope="module")
def engine() -> PromptsChatEngine:
    eng = get_engine()
    if eng.count() == 0:
        eng.sync()
    return eng


def test_database_census(engine: PromptsChatEngine):
    """Verify all 2,627 prompts are ingested and indexed."""
    count = engine.count()
    assert count >= 2600, f"Expected at least 2600 prompts, got {count}"

    stats = engine.get_stats()
    assert stats["total_prompts"] == count
    assert stats["developer_prompts"] >= 180
    assert stats["average_quality"] > 40
    assert stats["unique_contributors"] > 1000
    assert "Software & Coding" in stats["categories"]


def test_variable_extraction():
    """Verify variable extraction patterns (${Name:Default}, ${Name}, [Name])."""
    text1 = "Act as an interviewer for ${Position:Software Developer} at ${Company:Acme Corp}."
    vars1 = VariableExtractor.extract(text1)
    assert len(vars1) == 2
    assert vars1[0].name == "Position"
    assert vars1[0].default_value == "Software Developer"
    assert vars1[1].name == "Company"
    assert vars1[1].default_value == "Acme Corp"

    text2 = "Translate [SOURCE_TEXT] into ${Target_Language:French}."
    vars2 = VariableExtractor.extract(text2)
    names = [v.name for v in vars2]
    assert "SOURCE_TEXT" in names
    assert "Target_Language" in names


def test_variable_interpolation():
    """Verify template interpolation with custom values."""
    template = "I will be the candidate for ${Position:Software Developer} at [Company]."
    values = {"Position": "Chief AI Architect", "Company": "Anthropic"}
    filled = VariableExtractor.interpolate(template, values)
    assert "Chief AI Architect" in filled
    assert "Anthropic" in filled
    assert "${Position" not in filled
    assert "[Company]" not in filled


def test_variable_interpolation_default_fallback():
    """Verify fallback to defaults if value is missing."""
    template = "Interview for ${Position:Staff Engineer}."
    filled = VariableExtractor.interpolate(template, {})
    assert "Staff Engineer" in filled
    assert "${Position" not in filled


def test_quality_scorer():
    """Verify prompt quality scoring rules and positive markers."""
    weak_prompt = "Tell me about dogs"
    score_weak, strengths_weak = QualityScorer.score(weak_prompt)
    assert score_weak < 40

    strong_prompt = (
        "I want you to act as a Linux Terminal. I will type commands and you will reply "
        "with what the terminal should show. Only reply with the terminal output inside "
        "one unique code block, and nothing else. Do not write explanations. "
        "My first command is pwd"
    )
    score_strong, strengths_strong = QualityScorer.score(strong_prompt)
    assert score_strong >= 70
    assert "Explicit role grounding" in strengths_strong
    assert "Strict negative boundaries" in strengths_strong
    assert "Output structure specification" in strengths_strong


def test_archetype_classification():
    """Verify categorization and Universal Job Archetype assignment."""
    cat, arch, skills = ArchetypeClassifier.classify(
        "Linux Terminal",
        "I want you to act as a linux terminal. Run bash commands."
    )
    assert cat == "Software & Coding"
    assert arch == "SOFTWARE_ENGINEER_BACKEND"
    assert "backend-patterns" in skills

    cat2, arch2, skills2 = ArchetypeClassifier.classify(
        "Job Interviewer",
        "Act as an interviewer for a role."
    )
    assert cat2 == "Business & Strategy"
    assert arch2 == "TECHNICAL_RECRUITER"


def test_search_fts_and_relevance(engine: PromptsChatEngine):
    """Verify FTS5 full-text search capability."""
    records, total = engine.search("linux terminal")
    assert total > 0
    assert any("linux" in r.act.lower() or "linux" in r.prompt.lower() for r in records)


def test_search_filters(engine: PromptsChatEngine):
    """Verify category and developer filters."""
    dev_records, dev_total = engine.search(query="", for_devs=True, limit=10)
    assert dev_total > 0
    assert all(r.for_devs for r in dev_records)

    cat_records, cat_total = engine.search(query="", category="Writing & Editorial", limit=10)
    assert cat_total > 0
    assert all(r.category == "Writing & Editorial" for r in cat_records)


def test_get_by_act_and_slug(engine: PromptsChatEngine):
    """Verify prompt lookup by Act name and slug."""
    record = engine.get_by_act("Linux Terminal")
    assert record is not None
    assert record.act == "Linux Terminal"
    assert record.slug == "linux-terminal"

    by_slug = engine.get_by_slug("linux-terminal")
    assert by_slug is not None
    assert by_slug.id == record.id


def test_get_random(engine: PromptsChatEngine):
    """Verify random prompt retrieval."""
    p1 = engine.get_random()
    assert p1 is not None
    assert p1.act

    p_dev = engine.get_random(for_devs=True)
    assert p_dev is not None
    assert p_dev.for_devs is True


def test_mcp_search_prompts():
    """Verify MCP search_prompts tool handler."""
    res = mcp_server.handle_call_tool("search_prompts", {"query": "python", "limit": 5})
    assert "results" in res
    assert len(res["results"]) <= 5
    assert res["total_matches"] > 0


def test_mcp_get_and_fill_prompt():
    """Verify MCP get_prompt and fill_prompt tool handlers."""
    get_res = mcp_server.handle_call_tool("get_prompt", {"act_or_slug": "Job Interviewer"})
    assert get_res.get("act") == "Job Interviewer"

    fill_res = mcp_server.handle_call_tool("fill_prompt", {
        "act_or_slug": "Job Interviewer",
        "variables": {"Position": "Lead Site Reliability Engineer"}
    })
    assert "Lead Site Reliability Engineer" in fill_res.get("filled_prompt", "")


def test_mcp_improve_prompt():
    """Verify MCP improve_prompt tool handler."""
    res = mcp_server.handle_call_tool("improve_prompt", {"prompt": "Write a python script"})
    assert res["improved_score"] > res["original_score"]
    assert "Operating Constraints:" in res["improved_prompt"]


def test_mcp_analyze_prompt_quality():
    """Verify MCP analyze_prompt_quality tool handler."""
    res = mcp_server.handle_call_tool("analyze_prompt_quality", {"prompt": "Help me code"})
    assert "quality_score" in res
    assert "recommendations" in res
    assert len(res["recommendations"]) > 0


def test_mcp_stats_tool():
    """Verify MCP get_prompts_chat_stats tool handler."""
    stats = mcp_server.handle_call_tool("get_prompts_chat_stats", {})
    assert stats["total_prompts"] >= 2600


def test_book_chapters_engine(engine: PromptsChatEngine):
    """Verify book chapters retrieval from prompt engineering guide."""
    chapters = engine.get_book_chapters()
    assert len(chapters) == 31
    assert any(c["slug"] == "01-understanding-ai-models" for c in chapters)

    ch = engine.get_book_chapter("01-understanding-ai-models")
    assert ch is not None
    assert "Large Language Models" in ch["content"]
    assert ch["word_count"] > 100


def test_multilingual_book(engine: PromptsChatEngine):
    """Verify multilingual book translations and chapters."""
    langs = engine.get_book_languages()
    assert len(langs) >= 15
    codes = [l["code"] for l in langs]
    assert "en" in codes
    assert "es" in codes
    assert "tr" in codes

    ch_es = engine.get_book_chapter("01-understanding-ai-models", lang="es")
    assert ch_es is not None
    assert len(ch_es["content"]) > 100


def test_search_skills_and_get_skill(engine: PromptsChatEngine):
    """Verify search and retrieval across 3,841+ installed agent skills."""
    skills = engine.search_skills("tdd")
    assert len(skills) > 0
    assert any("tdd" in s["name"].lower() for s in skills)

    skill = engine.get_skill("tdd")
    assert skill is not None
    assert "SKILL.md" in skill["files"]
    assert "tdd" in skill["content"].lower()


def test_mcp_skills_tools():
    """Verify MCP tools search_skills and get_skill."""
    search_res = mcp_server.handle_call_tool("search_skills", {"query": "prompts-chat"})
    assert search_res["total_returned"] > 0

    get_res = mcp_server.handle_call_tool("get_skill", {"name": "prompts-chat"})
    assert get_res["name"] == "prompts-chat"
    assert "SKILL.md" in get_res["files"]


def test_export_enriched_json(engine: PromptsChatEngine, tmp_path: Path):
    """Verify exporting all prompts with variables and scoring to JSON."""
    test_out = tmp_path / "test_enriched.json"
    exported_path = engine.export_enriched_json(test_out)
    assert exported_path.exists()

    data = json.loads(exported_path.read_text(encoding="utf-8"))
    assert len(data) >= 2600
    assert "variables" in data[0]
    assert "quality_score" in data[0]


def test_http_api_endpoints():
    """Verify built-in REST API and Cockpit HTTP server responses."""
    import socketserver
    import threading
    import time
    import urllib.request
    from prompts_chat_cli import PromptsChatHttpHandler

    socketserver.TCPServer.allow_reuse_address = True
    port = 9989
    httpd = socketserver.TCPServer(("127.0.0.1", port), PromptsChatHttpHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.3)

    try:
        # 1. UI Root endpoint
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as resp:
            assert resp.status == 200
            content = resp.read().decode("utf-8")
            assert "prompts.chat" in content

        # 2. Stats endpoint
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/stats") as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode("utf-8"))
            assert data["total_prompts"] >= 2600

        # 2b. Book endpoints
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/book-languages") as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode("utf-8"))
            assert len(data["languages"]) >= 15

        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/book") as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode("utf-8"))
           