"""Unit and regression tests for CamofoxClient."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch
import pytest

from ai.camofox_client import CamofoxClient, CamofoxError


def test_camofox_client_initialization():
    client = CamofoxClient(base_url="http://127.0.0.1:9377/", api_key="secret123", user_id="agent_x")
    assert client.base_url == "http://127.0.0.1:9377"
    assert client.api_key == "secret123"
    assert client.user_id == "agent_x"


@patch("urllib.request.urlopen")
def test_camofox_client_health(mock_urlopen):
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"status": "healthy", "browser": "ready"}).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    client = CamofoxClient()
    res = client.health()
    assert res["status"] == "healthy"
    assert res["browser"] == "ready"


@patch("urllib.request.urlopen")
def test_camofox_client_create_tab(mock_urlopen):
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"tabId": "tab_42", "url": "https://example.com"}).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    client = CamofoxClient(user_id="test_user")
    res = client.create_tab(url="https://example.com", session_key="s1", trace=True)

    assert res["tabId"] == "tab_42"
    assert "tab_42" in client._managed_tabs


@patch("urllib.request.urlopen")
def test_camofox_client_click_and_type(mock_urlopen):
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"success": True}).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    client = CamofoxClient()
    click_res = client.click("tab_1", ref="e5")
    assert click_res["success"] is True

    type_res = client.type("tab_1", ref="e6", text="Stealth Query", press_enter=True)
    assert type_res["success"] is True


@patch("urllib.request.urlopen")
def test_camofox_client_context_manager_cleanup(mock_urlopen):
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"tabId": "tab_99"}).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    with patch.object(CamofoxClient, "close_tab") as mock_close:
        with CamofoxClient() as client:
            client._managed_tabs.append("tab_99")
            client._managed_tabs.append("tab_100")

        assert mock_close.call_count == 2
        mock_close.assert_any_call("tab_99")
        mock_close.assert_any_call("tab_100")
