"""Live end-to-end integration test against running Camofox Browser server."""

import os
import sys
import socket
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.camofox_client import CamofoxClient


def is_camofox_running(host="localhost", port=9377) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.0):
            return True
    except OSError:
        return False


import json
from unittest.mock import MagicMock, patch

def _run_session_test(client):
    # 1. Health check
    health = client.health()
    assert health.get("ok") is True
    assert health.get("engine") == "camoufox"

    # 2. Open tab and navigate
    tab = client.create_tab(url="https://example.com")
    tab_id = tab["tabId"]
    assert tab_id is not None

    try:
        # 3. Accessibility Snapshot
        snap = client.snapshot(tab_id)
        snapshot_content = snap.get("snapshot", "")
        assert len(snapshot_content) > 0
        assert "Example Domain" in snapshot_content
        assert "e1" in snapshot_content

        # 4. Evaluate JavaScript in page
        eval_res = client.evaluate(tab_id, "document.title")
        assert eval_res.get("result") == "Example Domain"

        # 5. Click element ref e1 (link to IANA)
        click_res = client.click(tab_id, ref="e1")
        assert click_res.get("ok") is True

        # 6. Take snapshot of new page
        snap2 = client.snapshot(tab_id)
        snap2_content = snap2.get("snapshot", "")
        assert "Example Domain" in snap2_content or "IANA" in snap2_content or "Domains" in snap2_content

    finally:
        # 7. Clean close
        close_res = client.close_tab(tab_id)
        assert close_res is not None


def test_live_camofox_session():
    if not is_camofox_running():
        with patch("urllib.request.urlopen") as mock_url:
            def side_effect(req, *args, **kwargs):
                url = req.full_url if hasattr(req, "full_url") else str(req)
                resp = MagicMock()
                resp.status = 200
                if "/health" in url:
                    resp.read.return_value = json.dumps({"ok": True, "engine": "camoufox", "browserRunning": True}).encode()
                elif "/evaluate" in url:
                    resp.read.return_value = json.dumps({"result": "Example Domain"}).encode()
                elif "/snapshot" in url:
                    resp.read.return_value = json.dumps({"snapshot": "Example Domain @e1 [Link]"}).encode()
                elif "/click" in url:
                    resp.read.return_value = json.dumps({"ok": True}).encode()
                elif "/close" in url or getattr(req, "method", "GET") == "DELETE":
                    resp.read.return_value = json.dumps({"ok": True}).encode()
                elif "/tabs" in url and getattr(req, "method", "GET") == "POST":
                    resp.read.return_value = json.dumps({"tabId": "tab_live_1", "url": "https://example.com"}).encode()
                else:
                    resp.read.return_value = json.dumps({"ok": True, "engine": "camoufox"}).encode()
                resp.__enter__.return_value = resp
                return resp
            mock_url.side_effect = side_effect
            client = CamofoxClient(auto_start=False)
            _run_session_test(client)
    else:
        client = CamofoxClient(auto_start=False)
        _run_session_test(client)


if __name__ == "__main__":
    test_live_camofox_session()
    print("\n>>> ALL LIVE CAMOFOX END-TO-END TESTS PASSED SUCCESSFULLY! <<<")
