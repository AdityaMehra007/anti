"""
Unit & Integration Tests for PowerShell Autonomous Orchestrator Suite
=====================================================================
Tests client initialization, AST parser, PSScriptAnalyzer rules, runbooks,
pipeline object streaming, CLI commands, MCP server tools, and the 12-phase
sovereign 'do-everything' lifecycle.
"""

import os
import sys
import json
import pytest
from powershell_orchestrator import (
    PowerShellConfig,
    PowerShellClient,
    PowerShellOrchestrator,
    PowerShellMockEngine,
    PowerShellExecutionResult
)
import powershell_cli
import powershell_mcp_server


@pytest.fixture
def mock_client():
    config = PowerShellConfig(mock_mode=True)
    return PowerShellClient(config)


@pytest.fixture
def mock_orchestrator(mock_client):
    return PowerShellOrchestrator(mock_client)


@pytest.fixture
def live_client():
    config = PowerShellConfig(mock_mode=False)
    return PowerShellClient(config)


# --- 1. Mock Engine Tests ---

def test_mock_engine_telemetry():
    engine = PowerShellMockEngine()
    telemetry = engine.get_telemetry()
    assert telemetry["version"] == "7.5.0"
    assert telemetry["edition"] == "Core"
    assert telemetry["active_runspaces"] == 8
    assert telemetry["total_cmdlets"] >= 1800
    assert telemetry["installed_modules_count"] >= 5
    assert telemetry["registered_runbooks_count"] == 5
    assert telemetry["pipeline_streaming_supported"] is True


def test_mock_engine_ast_parsing():
    engine = PowerShellMockEngine()
    code = """
function Get-ClusterTelemetry {
    [CmdletBinding()]
    param([string]$NodeId, [int]$Retries = 3)
    process {
        Get-Process -Name pwsh
    }
}
"""
    ast = engine.parse_ast(code)
    assert ast.tokens_count > 0
    assert len(ast.functions) == 1
    assert ast.functions[0]["name"] == "Get-ClusterTelemetry"
    assert "NodeId" in ast.parameters
    assert "Retries" in ast.parameters
    assert "Get-Process" in ast.pipeline_calls
    assert ast.has_errors is False


def test_mock_engine_ast_syntax_error():
    engine = PowerShellMockEngine()
    code = "function BadSyntax { [string]$x = 10"  # Missing closing brace
    ast = engine.parse_ast(code)
    assert ast.has_errors is True
    assert len(ast.syntax_errors) > 0


def test_mock_engine_script_analyzer():
    engine = PowerShellMockEngine()
    code = """
$password = "PlainTextSuperSecretPassword!"
Invoke-Expression "Get-Service"
Write-Host "Debug message"
$global:MyVar = 42
"""
    diags = engine.analyze_script(code)
    rules = [d.rule_name for d in diags]
    assert "PSAvoidUsingPlainTextForPassword" in rules
    assert "PSAvoidUsingInvokeExpression" in rules
    assert "PSAvoidUsingWriteHost" in rules
    assert "PSAvoidGlobalVars" in rules


def test_mock_engine_cmdlet_execution():
    engine = PowerShellMockEngine()
    res = engine.execute_mock_command("$PSVersionTable")
    assert res.success is True
    assert res.objects[0]["PSVersion"] == "7.5.0"
    assert res.objects[0]["PSEdition"] == "Core"

    res_proc = engine.execute_mock_command("Get-Process")
    assert res_proc.success is True
    assert len(res_proc.objects) >= 3


# --- 2. Client & Dual-Mode Execution Tests ---

def test_client_init_and_telemetry(mock_client):
    telemetry = mock_client.get_telemetry()
    assert telemetry["version"] is not None
    assert telemetry["operating_mode"] == "SIMULATION"


def test_client_execute_as_json(mock_client):
    res = mock_client.execute("Get-Process", as_json=True)
    assert res.success is True
    assert len(res.objects) > 0


def test_client_list_modules_and_gallery(mock_client):
    modules = mock_client.list_modules()
    assert len(modules) >= 5
    names = [m.get("Name") or m.get("name") for m in modules]
    assert "Microsoft.PowerShell.Management" in names

    gallery = mock_client.find_gallery_module(keyword="Az")
    assert len(gallery) >= 1
    assert gallery[0]["name"] == "Az"


def test_client_list_runspaces(mock_client):
    runspaces = mock_client.list_runspaces()
    assert len(runspaces) == 8
    assert all(r["state"] == "Opened" for r in runspaces)


# --- 3. Enterprise Runbooks Tests ---

def test_runbook_cis_hardening(mock_client):
    res = mock_client.execute_runbook("cis_hardening")
    assert res["success"] is True
    assert "result_data" in res
    data = res["result_data"]
    assert "ComplianceScore" in data or "PassedChecks" in data or "Status" in data


def test_runbook_cloud_recon(mock_client):
    res = mock_client.execute_runbook("cloud_recon")
    assert res["success"] is True
    data = res["result_data"]
    assert "Runbook" in data
    assert data["Runbook"] == "Cloud_Infra_Recon"


def test_runbook_active_directory(mock_client):
    res = mock_client.execute_runbook("ad_audit")
    assert res["success"] is True
    data = res["result_data"]
    assert "Verdict" in data or "DirectoryHealthScore" in data


def test_runbook_network_diagnostic(mock_client):
    res = mock_client.execute_runbook("network_diag")
    assert res["success"] is True
    data = res["result_data"]
    assert "OverallNetworkHealth" in data or "Probes" in data


def test_runbook_service_watchdog(mock_client):
    res = mock_client.execute_runbook("self_healing")
    assert res["success"] is True
    data = res["result_data"]
    assert "Status" in data or "Services" in data


# --- 4. Orchestrator High-Level & Benchmark Tests ---

def test_orchestrator_pipeline_benchmark(mock_orchestrator):
    bench = mock_orchestrator.benchmark_pipeline(iterations=3)
    assert bench["iterations"] == 3
    assert bench["objects_per_run"] == 1000
    assert bench["average_latency_ms"] > 0
    assert bench["throughput_objects_per_sec"] > 0


def test_orchestrator_do_everything_lifecycle(mock_orchestrator):
    manifest = mock_orchestrator.do_everything()
    assert manifest["execution_id"].startswith("PWSH-SOVEREIGN-")
    assert manifest["total_phases_executed"] == 12
    assert "100% ATTESTED" in manifest["overall_status"]
    assert len(manifest["phases"]) == 12

    # Verify manifest file exists on disk
    manifest_file = os.path.join("omega", "data", "powershell_do_everything_manifest.json")
    assert os.path.exists(manifest_file)
    with open(manifest_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["execution_id"] == manifest["execution_id"]


# --- 5. MCP Server Tool Dispatcher Tests ---

def test_mcp_tools_list():
    assert len(powershell_mcp_server.TOOLS) == 12
    tool_names = [t["name"] for t in powershell_mcp_server.TOOLS]
    assert "powershell_get_telemetry" in tool_names
    assert "powershell_execute_command" in tool_names
    assert "powershell_analyze_ast" in tool_names
    assert "powershell_script_analyzer" in tool_names
    assert "powershell_do_everything" in tool_names


def test_mcp_handle_call_tool():
    telemetry = powershell_mcp_server.handle_call_tool("powershell_get_telemetry", {})
    assert telemetry["version"] is not None

    ast_res = powershell_mcp_server.handle_call_tool("powershell_analyze_ast", {"script_content": "Get-Process"})
    assert ast_res["tokens_count"] > 0

    runbooks = powershell_mcp_server.handle_call_tool("powershell_list_runbooks", {})
    assert len(runbooks) == 5
