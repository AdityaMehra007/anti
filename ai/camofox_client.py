"""CamofoxBrowser Python Client - Stealth Headless Browser Interface.

Connects to the camofox-browser REST API (powered by Camoufox C++ anti-fingerprint engine)
for bot-detection bypass, Cloudflare evasion, accessibility snapshots with element refs,
and deterministic AI agent interactions.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class CamofoxError(Exception):
    """Base exception for Camofox API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class CamofoxClient:
    """Zero-dependency client for the camofox-browser REST API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        user_id: str = "omega_agent",
        timeout: float = 60.0,
        auto_start: bool = True,
    ):
        self.base_url = (base_url or os.getenv("CAMOFOX_URL", "http://127.0.0.1:9377")).rstrip("/")
        self.api_key = api_key or os.getenv("CAMOFOX_API_KEY", "")
        self.user_id = user_id
        self.timeout = timeout
        self.auto_start = auto_start
        self._managed_tabs: list[str] = []
        if self.auto_start:
            self.ensure_server()

    def ensure_server(self, max_wait: float = 30.0) -> bool:
        """Check if server is responding; if not, spawn node server.js in external/camofox-browser."""
        try:
            req = urllib.request.Request(f"{self.base_url}/health", headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass

        candidates = [
            Path(r"e:\anti\external\camofox-browser"),
            Path(__file__).resolve().parent.parent / "external" / "camofox-browser",
            Path.cwd() / "external" / "camofox-browser",
        ]
        server_dir = next((c for c in candidates if (c / "server.js").is_file()), None)
        if not server_dir:
            return False

        env = os.environ.copy()
        env["CAMOFOX_BIND_HOST"] = "127.0.0.1"

        try:
            log_path = server_dir / "camofox_daemon.log"
            daemon_log = open(log_path, "a", encoding="utf-8")
            subprocess.Popen(
                ["node", "server.js"],
                cwd=str(server_dir),
                env=env,
                stdout=daemon_log,
                stderr=subprocess.STDOUT,
                shell=True,
            )
        except Exception:
            return False

        start_t = time.time()
        while time.time() - start_t < max_wait:
            time.sleep(1.0)
            try:
                req = urllib.request.Request(f"{self.base_url}/health", headers={"Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=1.5) as resp:
                    if resp.status == 200:
                        return True
            except Exception:
                continue

        return False

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Perform an HTTP request against the Camofox REST server."""
        url = f"{self.base_url}{path}"
        if params:
            query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            if query:
                url = f"{url}?{query}"

        headers = {
            "Accept": "application/json",
            "User-Agent": "CamofoxPythonClient/1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        body_bytes = None
        if data is not None:
            headers["Content-Type"] = "application/json"
            body_bytes = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method.upper())

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                resp_text = resp.read().decode("utf-8")
                if not resp_text:
                    return {}
                return json.loads(resp_text)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            try:
                err_json = json.loads(err_body)
                msg = err_json.get("error") or err_json.get("message") or err_body
            except Exception:
                msg = err_body
            raise CamofoxError(f"HTTP {e.code} on {method} {path}: {msg}", status_code=e.code, response_body=err_body) from e
        except urllib.error.URLError as e:
            raise CamofoxError(f"Failed to connect to Camofox server at {self.base_url}: {e.reason}") from e

    # --- System & Lifecycle ---

    def health(self) -> Dict[str, Any]:
        """Get health and readiness status of the Camofox server."""
        return self._request("GET", "/health")

    def start_browser(self) -> Dict[str, Any]:
        """Explicitly initialize the browser engine."""
        return self._request("POST", "/start")

    def stop_browser(self) -> Dict[str, Any]:
        """Stop running browser instances and flush sessions."""
        return self._request("POST", "/stop")

    # --- Tabs Management ---

    def create_tab(
        self,
        url: Optional[str] = None,
        session_key: str = "default",
        trace: bool = False,
        track_lifecycle: bool = True,
    ) -> Dict[str, Any]:
        """Create a new browser tab, optionally loading an initial URL."""
        payload: Dict[str, Any] = {
            "userId": self.user_id,
            "sessionKey": session_key or "default",
            "trace": trace,
        }
        if url:
            payload["url"] = url

        res = self._request("POST", "/tabs", data=payload)
        tab_id = res.get("tabId")
        if tab_id and track_lifecycle:
            self._managed_tabs.append(tab_id)
        return res

    def list_tabs(self) -> List[Dict[str, Any]]:
        """List active tabs for current user."""
        res = self._request("GET", "/tabs", params={"userId": self.user_id})
        if isinstance(res, list):
            return res
        return res.get("tabs", [])

    def get_tab(self, tab_id: str) -> Dict[str, Any]:
        """Get metadata for a specific tab."""
        return self._request("GET", f"/tabs/{tab_id}", params={"userId": self.user_id})

    def close_tab(self, tab_id: str) -> Dict[str, Any]:
        """Close an open browser tab."""
        res = self._request("DELETE", f"/tabs/{tab_id}", params={"userId": self.user_id})
        if tab_id in self._managed_tabs:
            self._managed_tabs.remove(tab_id)
        return res

    # --- Navigation & Interaction ---

    def navigate(self, tab_id: str, url: str) -> Dict[str, Any]:
        """Navigate to a URL or search macro (e.g. '@google_search query')."""
        return self._request("POST", f"/tabs/{tab_id}/navigate", data={"userId": self.user_id, "url": url})

    def snapshot(
        self,
        tab_id: str,
        max_tokens: Optional[int] = None,
        offset: Optional[int] = None,
        screenshot: bool = False,
    ) -> Dict[str, Any]:
        """Retrieve token-efficient accessibility snapshot with stable element refs (e1, e2, etc.)."""
        params: Dict[str, Any] = {"userId": self.user_id}
        if max_tokens is not None:
            params["maxTokens"] = max_tokens
        if offset is not None:
            params["offset"] = offset
        if screenshot:
            params["screenshot"] = "true"
        return self._request("GET", f"/tabs/{tab_id}/snapshot", params=params)

    def click(self, tab_id: str, ref: Optional[str] = None, selector: Optional[str] = None) -> Dict[str, Any]:
        """Click an element identified by accessibility ref (e.g., 'e12') or CSS selector."""
        payload: Dict[str, Any] = {"userId": self.user_id}
        if ref:
            payload["ref"] = ref
        elif selector:
            payload["selector"] = selector
        else:
            raise ValueError("Must provide either 'ref' or 'selector'")
        return self._request("POST", f"/tabs/{tab_id}/click", data=payload)

    def type(
        self,
        tab_id: str,
        text: str,
        ref: Optional[str] = None,
        selector: Optional[str] = None,
        press_enter: bool = False,
        clear: bool = False,
    ) -> Dict[str, Any]:
        """Type text into an input element."""
        payload: Dict[str, Any] = {
            "userId": self.user_id,
            "text": text,
            "pressEnter": press_enter,
            "clear": clear,
        }
        if ref:
            payload["ref"] = ref
        elif selector:
            payload["selector"] = selector
        return self._request("POST", f"/tabs/{tab_id}/type", data=payload)

    def scroll(self, tab_id: str, direction: str = "down", amount: Optional[int] = None) -> Dict[str, Any]:
        """Scroll the tab page ('up', 'down', 'left', 'right')."""
        payload: Dict[str, Any] = {"userId": self.user_id, "direction": direction}
        if amount is not None:
            payload["amount"] = amount
        return self._request("POST", f"/tabs/{tab_id}/scroll", data=payload)

    def screenshot(self, tab_id: str) -> Dict[str, Any]:
        """Capture page screenshot."""
        return self._request("GET", f"/tabs/{tab_id}/screenshot", params={"userId": self.user_id})

    def evaluate(self, tab_id: str, expression: str) -> Dict[str, Any]:
        """Evaluate arbitrary JavaScript within the page execution context."""
        return self._request("POST", f"/tabs/{tab_id}/evaluate", data={"userId": self.user_id, "expression": expression})

    def extract(self, tab_id: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured data matching a JSON Schema mapped via x-ref properties."""
        return self._request("POST", f"/tabs/{tab_id}/extract", data={"userId": self.user_id, "schema": schema})

    # --- Cookie Management ---

    def import_cookies(self, cookies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Import Netscape or Playwright format cookies into the user session."""
        return self._request("POST", f"/sessions/{self.user_id}/cookies", data={"cookies": cookies})

    # --- Context Manager for Safe Cleanup ---

    def __enter__(self) -> "CamofoxClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        for tab_id in list(self._managed_tabs):
            try:
                self.close_tab(tab_id)
            except Exception:
                pass
        self._managed_tabs.clear()
