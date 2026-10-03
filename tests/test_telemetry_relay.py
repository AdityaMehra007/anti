"""
Unit tests for Live Telemetry Relay daemon (aios/services/live_telemetry_relay.py)
"""
import json
import pytest
from aios.services.live_telemetry_relay import collect_system_telemetry, format_sse_event

def test_collect_system_telemetry():
    telemetry = collect_system_telemetry()
    assert isinstance(telemetry, dict)
    assert "timestamp" in telemetry
    assert "cpu_count" in telemetry
    assert "memory" in telemetry
    assert "disk_e" in telemetry
    assert "status" in telemetry
    assert telemetry["status"] == "HEALTHY"

def test_format_sse_event():
    payload = {"status": "ok", "ping": "pong"}
    sse_text = format_sse_event(payload, event="ping_event")
    assert sse_text.startswith("event: ping_event\n")
    assert "data: {\"status\": \"ok\", \"ping\": \"pong\"}\n\n" in sse_text
