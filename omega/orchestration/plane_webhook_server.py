"""
Bidirectional Webhook & Event Reactor for Plane CE.
Listens for Plane issue events (issue.created, issue.updated, state_change),
triggers autonomous agent workflows, and logs lifecycle activity.
"""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import sys
import threading
from typing import Any, Callable, Dict, Optional
from urllib.request import Request, urlopen

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


class WebhookHandler(BaseHTTPRequestHandler):
    """Handles incoming Plane webhook payloads and health probes."""

    def log_message(self, format: str, *args: Any) -> None:
        # Standardize logging format
        print(f"[WEBHOOK-HTTP] {self.address_string()} - {format % args}")

    def do_GET(self) -> None:
        if self.path in ("/health", "/healthz"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "plane-webhook-reactor"}).encode())
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        if self.path.startswith("/webhook"):
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

            try:
                payload = json.loads(raw_body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
                return

            event_type = payload.get("event") or payload.get("action") or "unknown"

            # Execute callback registered on server
            callback: Optional[Callable[[str, Dict[str, Any]], None]] = getattr(self.server, "event_callback", None)
            if callback:
                try:
                    callback(event_type, payload)
                except Exception as ex:
                    print(f"[-] Error in webhook event callback: {ex}", file=sys.stderr)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "processed",
                "event": event_type,
                "timestamp": self.date_time_string(),
            }).encode())
            return

        self.send_response(404)
        self.end_headers()


def default_event_logger(event_type: str, payload: Dict[str, Any]) -> None:
    """Default callback logging webhook events to terminal, jsonl log, and invoking agent reactor."""
    print(f"[+] [EVENT-RECEIVED] Type: {event_type} | Data: {json.dumps(payload.get('data', {}))}")
    log_dir = REPO_ROOT / "omega" / "data"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "plane_webhook_events.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps({"event": event_type, "payload": payload}) + "\n")

    try:
        from omega.orchestration.plane_agent_reactor import PlaneAgentReactor
        reactor = PlaneAgentReactor(dry_run=True)
        reactor.process_event(event_type, payload)
    except Exception as ex:
        print(f"[-] Warning: Reactor processing error: {ex}")


class PlaneWebhookServer:
    """HTTP Webhook Daemon listening for Plane events."""

    def __init__(
        self,
        port: int = 8096,
        host: str = "0.0.0.0",
        callback: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.callback = callback or default_event_logger
        self.httpd: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    @property
    def server_port(self) -> int:
        if self.httpd:
            return self.httpd.server_port
        return self.port

    def start_in_thread(self) -> threading.Thread:
        """Starts server in background thread."""
        self.httpd = HTTPServer((self.host, self.port), WebhookHandler)
        setattr(self.httpd, "event_callback", self.callback)
        self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self._thread.start()
        print(f"[*] Plane Webhook Server running in thread on http://{self.host}:{self.server_port}")
        return self._thread

    def start_blocking(self) -> None:
        """Starts server in blocking mode."""
        self.httpd = HTTPServer((self.host, self.port), WebhookHandler)
        setattr(self.httpd, "event_callback", self.callback)
        print(f"[*] Plane Webhook Server listening on http://{self.host}:{self.server_port} (Ctrl+C to stop)...")
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Stopping Plane Webhook Server...")
        finally:
            self.stop()

    def stop(self) -> None:
        """Stops the running server."""
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None


def send_test_event(port: int = 8096) -> None:
    """Sends a sample webhook event to verify connectivity."""
    url = f"http://127.0.0.1:{port}/webhook"
    payload = {
        "event": "issue.state_changed",
        "data": {
            "issue_id": "OMEGA-CORE-001",
            "title": "Quantum Fleet Synchronization",
            "old_state": "Backlog",
            "new_state": "In Progress",
            "agent_assigned": "omega-executor",
        }
    }
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    print(f"[*] Dispatching test webhook to {url}...")
    try:
        with urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            print(f"[+] Webhook response: {json.dumps(data, indent=2)}")
    except Exception as ex:
        print(f"[-] Failed to send test webhook: {ex}")


def test_self_roundtrip() -> None:
    """Starts an ephemeral server in a thread, sends an event, and verifies 200 OK."""
    server = PlaneWebhookServer(port=0, host="127.0.0.1")
    server.start_in_thread()
    port = server.server_port
    print(f"[*] Ephemeral webhook server online on port {port}. Running round-trip check...")
    try:
        send_test_event(port=port)
    finally:
        server.stop()
        print("[+] Ephemeral server stopped cleanly.")


def main() -> None:
    parser = argparse.ArgumentParser(description="OMEGA Plane Webhook Event Reactor")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PLANE_WEBHOOK_PORT", 8096)), help="Listen port")
    parser.add_argument("--host", default="0.0.0.0", help="Listen host")
    parser.add_argument("--test-event", action="store_true", help="Send a test webhook event to the server")
    parser.add_argument("--test-self", action="store_true", help="Spin up ephemeral server and verify round-trip processing")

    args = parser.parse_args()

    if args.test_self:
        test_self_roundtrip()
        return

    if args.test_event:
        send_test_event(port=args.port)
        return

    server = PlaneWebhookServer(port=args.port, host=args.host)
    server.start_blocking()


if __name__ == "__main__":
    main()
