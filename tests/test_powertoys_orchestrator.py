"""
Unit & Integration Tests for Microsoft PowerToys Autonomous Suite
=================================================================
Tests engine telemetry, module enumeration & toggling, FancyZones coordinate math,
PowerToys Run multi-plugin fuzzy launcher, Awake power management, Keyboard Manager,
Hosts File Editor, Advanced Paste transformations, Workspaces deployment, CIS security audit,
micro-benchmarks, CLI subcommands, MCP server tools, and the 12-phase sovereign lifecycle.
"""

import os
import sys
import json
import pytest

from powertoys_orchestrator import (
    PowerToysConfig,
    PowerToysOrchestrator,
    PowerToysMockEngine
)
import powertoys_cli
import powertoys_mcp_server


@pytest.fixture
def orchestrator():
    config = PowerToysConfig(mock_mode=True)
    return PowerToysOrchestrator(config)


# --- 1. Engine Telemetry & Modules ---

def test_powertoys_telemetry(orchestrator):
    info = orchestrator.get_info()
    assert info["version"] == "0.88.0"
    assert info["runtime"] == ".NET 9.0 (WinUI 3 / WASDK 1.6)"
    assert info["runner_status"] == "RUNNING"
    assert info["total_modules"] >= 20
    assert info["telemetry_opt_in"] is False


def test_powertoys_list_modules(orchestrator):
    modules = orchestrator.list_modules()
    assert len(modules) >= 20
    mod_names = [m["name"] for m in modules]
    assert "FancyZones" in mod_names
    assert "PowerToys Run" in mod_names
    assert "Awake" in mod_names
    assert "Keyboard Manager" in mod_names
    assert "Advanced Paste" in mod_names


def test_powertoys_toggle_module(orchestrator):
    res_disable = orchestrator.toggle_module("Always on Top", enabled=False)
    assert res_disable["new_state"] is False
    res_enable = orchestrator.toggle_module("Always on Top", enabled=True)
    assert res_enable["new_state"] is True


# --- 2. FancyZones Layout Mathematics ---

def test_fancyzones_layout_calculation_fhd(orchestrator):
    layout = orchestrator.calculate_fancyzones("priority-grid-01", (1920, 1080))
    assert layout["layout_id"] == "priority-grid-01"
    assert layout["resolution"] == "1920x1080"
    assert layout["total_zones"] == 3
    assert len(layout["zones"]) == 3
    for z in layout["zones"]:
        assert z["width"] > 0
        assert z["height"] > 0
        assert z["x"] >= 0
        assert z["y"] >= 0


def test_fancyzones_layout_calculation_ultrawide(orchestrator):
    layout = orchestrator.calculate_fancyzones("ultrawide-coder", (5120, 1440))
    assert layout["resolution"] == "5120x1440"
    assert layout["total_zones"] == 4
    # Ensure zones span the display without overlapping out of bounds
    for z in layout["zones"]:
        assert z["x"] + z["width"] <= 5120


# --- 3. PowerToys Run Multi-Plugin Launcher ---

def test_pt_run_calculator_plugin(orchestrator):
    results = orchestrator.query_pt_run("sqrt(256) * 4")
    assert len(results) >= 1
    calc_match = next((r for r in results if r["plugin"] == "CalculatorPlugin"), None)
    assert calc_match is not None
    assert calc_match["action"] == "64.0"


def test_pt_run_unit_converter_plugin(orchestrator):
    results = orchestrator.query_pt_run("100 km to miles")
    assert len(results) >= 1
    unit_match = next((r for r in results if r["plugin"] == "UnitConverterPlugin"), None)
    assert unit_match is not None
    assert "miles" in unit_match["action"]


def test_pt_run_system_commands(orchestrator):
    results = orchestrator.query_pt_run("lock")
    assert len(results) >= 1
    sys_match = next((r for r in results if r["plugin"] == "SystemCommandsPlugin"), None)
    assert sys_match is not None
    assert "Lock" in sys_match["title"]


def test_pt_run_shell_command(orchestrator):
    results = orchestrator.query_pt_run("> ipconfig /all")
    assert len(results) == 1
    assert results[0]["plugin"] == "ShellPlugin"
    assert "ipconfig /all" in results[0]["action"]


# --- 4. Awake Power Management ---

def test_awake_mode_configuration(orchestrator):
    res = orchestrator.set_awake("INDEFINITE", keep_display=True)
    assert res["mode"] == "INDEFINITE"
    assert res["keep_display_on"] is True
    assert res["status"] == "ACTIVE"

    res_timed = orchestrator.set_awake("TIMED", duration_minutes=120, keep_display=False)
    assert res_timed["mode"] == "TIMED"
    assert res_timed["duration_minutes"] == 120
    assert res_timed["keep_display_on"] is False


# --- 5. Keyboard Manager ---

def test_keyboard_manager_remaps(orchestrator):
    remaps = orchestrator.get_keyboard_remaps()
    assert "key_remaps" in remaps
    assert "global_shortcuts" in remaps
    assert remaps["conflicts_detected"] == 0

    add_res = orchestrator.add_key_remap("F12", "F11")
    assert add_res["status"] == "APPLIED"
    assert add_res["original_key"] == "F12"
    assert add_res["remapped_to"] == "F11"


# --- 6. Hosts File Editor ---

def test_hosts_file_parsing_and_addition(orchestrator):
    records = orchestrator.get_hosts()
    assert len(records) >= 1
    assert any(r["ip_address"] == "127.0.0.1" for r in records)

    add_res = orchestrator.add_hosts("127.0.0.1", "test.vault.internal", "Unit test record")
    assert add_res["status"] == "ADDED"
    assert add_res["hostname"] == "test.vault.internal"


# --- 7. Advanced Paste AI Transformation ---

def test_advanced_paste_plain_text(orchestrator):
    html = "<h1>Title</h1><p>Hello <b>World</b></p>"
    res = orchestrator.transform_paste(html, "plain_text")
    assert res["status"] == "SUCCESS"
    assert "<" not in res["output_text"]
    assert "Title" in res["output_text"]


def test_advanced_paste_case_conversions(orchestrator):
    snake = "user_account_identifier"
    res = orchestrator.transform_paste(snake, "snake_to_camel")
    assert res["output_text"] == "userAccountIdentifier"

    camel = "userAccountIdentifier"
    res2 = orchestrator.transform_paste(camel, "camel_to_snake")
    assert res2["output_text"] == "user_account_identifier"


def test_advanced_paste_redact_pii(orchestrator):
    sensitive = "Contact ceo@company.com with token sk_live_948aef89b39d10e82c892301923849102"
    res = orchestrator.transform_paste(sensitive, "redact_pii")
    assert "[EMAIL_REDACTED]" in res["output_text"]
    assert "[SECRET_KEY_REDACTED]" in res["output_text"]


# --- 8. Text Extractor & Workspaces ---

def test_text_extractor_ocr(orchestrator):
    ocr = orchestrator.extract_ocr((50, 50, 500, 300))
    assert ocr["confidence_score"] > 0.95
    assert ocr["recognized_word_count"] > 10


def test_workspaces_launch(orchestrator):
    ws = orchestrator.launch_workspace("Full-Stack Dev")
    assert ws["workspace_name"] == "Full-Stack Dev"
    assert ws["total_applications_launched"] >= 2
    assert all(a["status"] == "DISPATCHED_TO_ZONE" for a in ws["applications"])


# --- 9. Security Audit & Benchmarking ---

def test_security_audit(orchestrator):
    audit = orchestrator.audit_security()
    assert audit["compliance_score"] >= 80.0
    assert audit["status"] == "COMPLIANT"
    assert audit["total_checks"] == 5


def test_benchmarking(orchestrator):
    bench = orchestrator.benchmark(iterations=100)
    assert bench["fancyzones_snapping"]["operations_per_sec"] > 1000
    assert bench["pt_run_fuzzy_search"]["queries_per_sec"] > 500
    assert bench["overall_status"] == "HIGH_PERFORMANCE_OPTIMAL"


# --- 10. CLI Integration ---

def test_powertoys_cli_info(capsys):
    ret = powertoys_cli.main(["info"])
    assert ret == 0
    out = capsys.readouterr().out
    assert "0.88.0" in out


def test_powertoys_cli_run_launcher(capsys):
    ret = powertoys_cli.main(["run-launcher", "sqrt(144) + 10"])
    assert ret == 0
    out = capsys.readouterr().out
    assert "22.0" in out


# --- 11. MCP Protocol Tool Handler ---

def test_powertoys_mcp_tools():
    assert len(powertoys_mcp_server.TOOLS) == 16
    tool_names = [t["name"] for t in powertoys_mcp_server.TOOLS]
    assert "powertoys_get_status" in tool_names
    assert "powertoys_calculate_fancyzones" in tool_names
    assert "powertoys_query_pt_run" in tool_names
    assert "powertoys_do_everything" in tool_names

    status_res = powertoys_mcp_server.handle_tool_call("powertoys_get_status", {})
    assert status_res["version"] == "0.88.0"


# --- 12. Full 12-Phase Sovereign Attestation ---

def test_powertoys_do_everything_manifest(orchestrator):
    manifest = orchestrator.do_everything()
    assert manifest["total_phases_executed"] == 12
    assert "100% ATTESTED" in manifest["overall_status"]
    assert len(manifest["phases"]) == 12
    assert all(p["status"] == "PASSED" for p in manifest["phases"])
