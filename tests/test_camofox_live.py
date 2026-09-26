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


@pytest.mark.skipif(not is_camofox_running(), reason="Camofox server not running on localhost:9377")
def test_live_camofox_session():
    print("[1] Connecting to Camofox Server...")
    client = CamofoxClient()

    # 1. Health check
    health = client.health()
    print(f"Server health: ok={health.get('ok')}, engine={health.get('engine')}, browserRunning={health.get('browserRunning')}")
    assert health.get("ok") is True
    assert health.get("engine") == "camoufox"

    # 2. Open tab and navigate
    print("[2] Creating tab at https://example.com...")
    tab = client.create_tab(url="https://example.com")
    tab_id = tab["tabId"]
    print(f"Created tab: {tab_id}")

    try:
        # 3. Accessibility Snapshot
        print("[3] Taking accessibility snapshot...")
        snap = client.snapshot(tab_id)
        snapshot_content = snap.get("snapshot", "")
        print(f"Snapshot received (len={len(snapshot_content)} chars):")
        print("--- SNAPSHOT SNIPPET ---")
        print("\n".join(snapshot_content.splitlines()[:10]))
        print("------------------------")
        assert len(snapshot_content) > 0
        assert "Example Domain" in snapshot_content
        assert "e1" in snapshot_content

        # 4. Evaluate JavaScript in page
        print("[4] Evaluating JavaScript in page context...")
        eval_res = client.evaluate(tab_id, "document.title")
        print(f"Page title via JS evaluation: {eval_res}")
        assert eval_res.get("result") == "Example Domain"

        # 5. Click element ref e1 (link to IANA)
        print("[5] Clicking element ref 'e1'...")
        click_res = client.click(tab_id, ref="e1")
        print(f"Click response: {click_res}")
        assert click_res.get("ok") is True

        # 6. Take snapshot of new page
        print("[6] Taking snapshot of navigated page...")
        snap2 = client.snapshot(tab_id)
        snap2_content = snap2.get("snapshot", "")
        print(f"Navigated snapshot received (len={len(snap2_content)} chars)")
        print("--- NAVIGATED SNIPPET ---")
        print("\n".join(snap2_content.splitlines()[:8]))
        print("------------------------")
        assert "IANA" in snap2_content or "Domains" in snap2_content

    finally:
        # 7. Clean close
        print(f"[7] Closing tab {tab_id}...")
        close_res = client.close_tab(tab_id)
        print("Tab closed successfully.")


if __name__ == "__main__":
    test_live_camofox_session()
    print("\n>>> ALL LIVE CAMOFOX END-TO-END TESTS PASSED SUCCESSFULLY! <<<")
