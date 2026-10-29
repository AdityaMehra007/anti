"""
Unit & Integration Tests for n8n Autonomous Orchestrator Suite
==============================================================
Tests client initialization, node catalog FTS5 search, production workflow DAGs,
workflow execution, inbound webhooks, LangChain AI agent reasoning, CLI commands,
and MCP server tool handlers.
"""

import os
import sys
import json
import pytest
from pathlib import Path

from n8n_orchestrator import (
    N8nConfig,
    N8nClient,
    N8nOrchestrator,
    N8nMockEngine
)
import n8n_cli
import n8n_mcp_server


@pytest.fixture
def mock_client():
    config = N8nConfig(mock_mode=True)
    return N8nClient(config)


@pytest.fixture
def orchestrator(mock_client):
    return N8nOrchestrator(mock_client)


def test_mock_engine_initial_state():
    engine = N8nMockEngine()
    assert engine.version == "1.75.2"
    assert "TypeScript" in engine.framework
    assert engine.active_workers_count == 8
    assert engine.max_concurrency == 32
    assert len(engine.nodes) >= 500
    assert len(engine.workflows) >= 10
    assert len(engine.credentials) >= 4


def test_node_catalog_and_fts5_search(mock_client):
    # Test FTS5 search
    results = mock_client.search_nodes("webhook", limit=5)
    assert len(results) > 0
    assert any("webhook" in (r.get("name", "") + r.get("displayName", "") + r.get("description", "")).lower() for r in results)

    # Test group listing
    transform_nodes = mock_client.list_nodes(group="transform", limit=10)
    assert len(transform_nodes) > 0

    # Test get node details
    details = mock_client.get_node_details("ActionNetwork")
    assert details is not None
    assert details["name"] == "ActionNetwork"


def test_workflow_listing_and_inspection(mock_client):
    wfs = mock_client.list_workflows()
    assert len(wfs) >= 10

    # Inspect specific workflow
    wf = mock_client.get_workflow("ai_agent_researcher") or mock_client.get_workflow(wfs[0]["id"])
    assert wf is not None
    assert "nodes" in wf
    assert len(wf["nodes"]) > 0


def test_workflow_execution(mock_client):
    wfs = mock_client.list_workflows()
    target_wf = wfs[0]["id"]

    input_payload = {"test_metric": 42, "entity": "OMEGA Enterprise"}
    res = mock_client.execute_workflow(target_wf, input_data=input_payload)

    assert res["status"] == "SUCCESS"
    assert "id" in res
    assert res["nodesCount"] > 0
    assert len(res["executedNodes"]) > 0
    assert "resultData" in res["data"]


def test_webhook_trigger(mock_client):
    payload = {"lead_name": "Acme Corp", "status": "QUALIFIED"}
    res = mock_client.trigger_webhook("outreach-dispatch", payload, test_mode=False)

    assert res["status"] == "WEBHOOK_PROCESSED"
    assert res["path"] == "outreach-dispatch"
    assert "executionId" in res
    assert res["executionTimeMs"] >= 0


def test_langchain_ai_agent_reasoning(mock_client):
    res = mock_client.run_ai_agent("Analyze Bangalore GCC market saturation.")

    assert "output" in res
    assert len(res["output"]) > 0
    assert "intermediateSteps" in res
    assert len(res["intermediateSteps"]) >= 2
    assert res["model"] == "gpt-4o-mini"
    assert "thoughts" in res


def test_credentials_vault(mock_client):
    creds = mock_client.list_credentials()
    assert len(creds) >= 4
    for c in creds:
        assert "id" in c
        assert "name" in c
        assert "type" in c
        # Ensure secret data keys are not exposed
        assert "apiKey" not in c
        assert "accessToken" not in c


def test_dropzone_and_workflow_export(mock_client, tmp_path):
    # Test workflow export
    exported = mock_client.export_workflows(dest_dir=str(tmp_path))
    assert len(exported) >= 10
    for p in exported:
        assert Path(p).exists()

    # Test dropzone scanning
    processed = mock_client.scan_dropzone()
    assert isinstance(processed, list)


def test_do_everything_12_phases(orchestrator):
    manifest = orchestrator.do_everything()

    assert manifest["protocol"] == "N8N_SUPREME_AUTONOMOUS_WORKFLOW_V2"
    assert manifest["total_phases_executed"] == 12
    assert len(manifest["phases"]) == 12

    for p in manifest["phases"]:
        assert p["status"] == "PASSED"

    # Verify manifest file exists on disk
    manifest_file = Path("e:/anti/omega/data/n8n_do_everything_manifest.json")
    assert manifest_file.exists()


def test_cli_handlers(mock_client, capsys):
    class DummyArgs:
        group = None
        limit = 5
        query = "webhook"
        active_only = False
        status = None
        command = "info"

    n8n_cli.cmd_info(mock_client, DummyArgs())
    captured = capsys.readouterr()
    assert "N8N ENTERPRISE AUTOMATION & WORKER TELEMETRY" in captured.out

    n8n_cli.cmd_nodes(mock_client, DummyArgs())
    captured = capsys.readouterr()
    assert "Discovered" in captured.out

    n8n_cli.cmd_workflows(mock_client, DummyArgs())
    captured = capsys.readouterr()
    assert "OMEGA Production Workflows" in captured.out


def test_mcp_server_tool_handling():
    # Test telemetry tool
    info = n8n_mcp_server.handle_tool_call("n8n_get_system_info", {})
    assert info["status"] == "ok"
    assert info["nodes_catalog_count"] >= 500

    # Test search nodes
    search_res = n8n_mcp_server.handle_tool_call("n8n_search_nodes", {"query": "slack", "limit": 3})
    assert len(search_res) > 0

    # Test list workflows
    wfs = n8n_mcp_server.handle_tool_call("n8n_list_workflows", {})
    assert len(wfs) >= 10

    # Test AI agent tool
    agent_res = n8n_mcp_server.handle_tool_call("n8n_run_ai_agent", {"prompt": "Quick status probe"})
    assert "output" in agent_res
