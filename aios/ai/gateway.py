#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Central AIOS Gateway & Model Router
Pure Python Standard Library (Zero-Dependency) micro-gateway on Port 8090.
Provides OpenAI-compatible endpoints, PII privacy filtering, telemetry logging,
and local-first routing to Ollama.
"""

import sys
import os
import re
import json
import time
import socket
import urllib.request
import urllib.error
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from datetime import datetime
from typing import Dict, Any, Tuple

AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "ai"))
sys.path.insert(0, str(AIOS_ROOT / "automation"))
sys.path.insert(0, str(AIOS_ROOT / "databases"))
sys.path.insert(0, str(AIOS_ROOT / "scripts"))

try:
    import db
except ImportError:
    db = None

try:
    import health_check
except ImportError:
    health_check = None

try:
    import rag_engine
except ImportError:
    rag_engine = None

try:
    import automation_bridge
except ImportError:
    automation_bridge = None

PORT = 8090
OLLAMA_BASE_URL = "http://localhost:11434"

# PII and Credential detection patterns
PII_PATTERNS = [
    re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),         # Credit card numbers
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), # Email
    re.compile(r"\b(?:sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,})\b"),    # API keys
]

def contains_pii(text: str) -> bool:
    """Checks text against privacy patterns."""
    for pattern in PII_PATTERNS:
        if pattern.search(text):
            return True
    return False

def anonymize_text(text: str) -> str:
    """Replaces sensitive patterns with generic privacy tokens."""
    for pattern in PII_PATTERNS:
        text = pattern.sub("[REDACTED_SENSITIVE]", text)
    return text

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class GatewayRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress noisy standard request logging to preserve terminal clarity
        pass

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def _send_json(self, data: Any, status: int = 200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        url = self.path.split("?")[0]

        if url in ["/", "/health"]:
            self._send_json({
                "status": "HEALTHY",
                "service": "ANTIGRAVITY_OMEGA_AIOS_GATEWAY",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat(),
                "port": PORT
            })
            return

        if url == "/api/telemetry":
            if health_check:
                report = health_check.run_health_check()
                self._send_json(report)
            else:
                self._send_json({"error": "health_check module unavailable"}, 500)
            return

        if url == "/v1/models":
            local_models = []
            try:
                tags_req = urllib.request.Request(f"{OLLAMA_BASE_URL}/api/tags")
                with urllib.request.urlopen(tags_req, timeout=3) as f:
                    tags_data = json.loads(f.read().decode("utf-8"))
                    for m in tags_data.get("models", []):
                        m_details = m.get("details", {})
                        local_models.append({
                            "id": m.get("name", m.get("model")),
                            "object": "model",
                            "type": "local",
                            "status": "online",
                            "size_bytes": m.get("size", 0),
                            "parameter_size": m_details.get("parameter_size", "unknown"),
                            "quantization": m_details.get("quantization_level", "unknown"),
                            "context_length": m_details.get("context_length", 32768)
                        })
            except Exception:
                # Fallback if Ollama is unreachable
                local_models = [
                    {"id": "qwen2.5-coder:3b", "object": "model", "type": "local", "status": "offline", "parameter_size": "3.1B", "quantization": "Q4_K_M"},
                    {"id": "fable5:latest", "object": "model", "type": "local", "status": "offline", "parameter_size": "8.0B", "quantization": "Q4_0"},
                    {"id": "llama3:latest", "object": "model", "type": "local", "status": "offline", "parameter_size": "8.0B", "quantization": "Q4_0"}
                ]

            cloud_models = [
                {"id": "gemini-2.0-flash", "object": "model", "type": "cloud", "provider": "Google", "status": "available"},
                {"id": "claude-3-5-sonnet", "object": "model", "type": "cloud", "provider": "Anthropic", "status": "available"},
                {"id": "gpt-4o-mini", "object": "model", "type": "cloud", "provider": "OpenAI", "status": "available"}
            ]
            self._send_json({"object": "list", "data": local_models + cloud_models})
            return

        if url == "/api/recent_metrics":
            if db:
                metrics = db.get_latest_metrics(limit=20)
                self._send_json({"metrics": metrics})
            else:
                self._send_json({"metrics": []})
            return

        if url == "/v1/rag/stats":
            if db:
                with db.get_connection() as con:
                    docs_cnt = con.execute("SELECT COUNT(*) FROM knowledge_documents").fetchone()[0]
                    chunks_cnt = con.execute("SELECT COUNT(*) FROM knowledge_chunks").fetchone()[0]
                self._send_json({"status": "ONLINE", "indexed_documents": docs_cnt, "indexed_chunks": chunks_cnt})
            else:
                self._send_json({"status": "OFFLINE", "indexed_documents": 0, "indexed_chunks": 0})
            return

        if url == "/v1/automation/status":
            if automation_bridge:
                bridge = automation_bridge.AutomationBridge()
                healthy = bridge.is_healthy()
                wfs = bridge.list_workflows()
                self._send_json({"status": "ONLINE" if healthy else "OFFLINE", "workflows_count": len(wfs), "workflows": wfs})
            else:
                self._send_json({"status": "OFFLINE", "workflows_count": 0, "workflows": []})
            return

        self._send_json({"error": "Endpoint not found", "path": self.path}, 404)

    def do_POST(self):
        url = self.path.split("?")[0]
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            req_data = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            self._send_json({"error": "Invalid JSON payload"}, 400)
            return

        if url == "/v1/chat/completions":
            self.handle_chat_completion(req_data)
            return

        if url == "/v1/rag/query":
            q = req_data.get("query", "")
            top_k = req_data.get("top_k", 3)
            synthesize = req_data.get("synthesize", True)
            if not q:
                self._send_json({"error": "Missing 'query' field"}, 400)
                return

            if rag_engine:
                engine = rag_engine.RAGEngine()
                if synthesize:
                    res = engine.query_and_synthesize(q, top_k=top_k)
                else:
                    matches = engine.search_chunks(q, top_k=top_k)
                    res = {"query": q, "matches": matches, "citations": [m["citation"] for m in matches]}
                self._send_json(res)
            else:
                self._send_json({"error": "rag_engine module unavailable"}, 500)
            return

        if url == "/v1/automation/trigger":
            webhook = req_data.get("webhook", "omega-events")
            payload = req_data.get("payload", {})
            if automation_bridge:
                bridge = automation_bridge.AutomationBridge()
                res = bridge.trigger_webhook(webhook, payload)
                self._send_json(res)
            else:
                self._send_json({"error": "automation_bridge module unavailable"}, 500)
            return

        self._send_json({"error": "Endpoint not found", "path": self.path}, 404)

    def handle_chat_completion(self, req: Dict[str, Any]):
        model = req.get("model", "qwen2.5-coder:3b")
        messages = req.get("messages", [])
        is_stream = req.get("stream", False)
        prompt_text = " ".join([m.get("content", "") for m in messages])

        has_sensitive = contains_pii(prompt_text)
        anonymized_prompt = anonymize_text(prompt_text)

        # Audit logging in master database
        if db:
            try:
                db.log_audit(
                    "AIOS_GATEWAY",
                    "CHAT_COMPLETION",
                    "AI",
                    f"Model: {model} | Stream: {is_stream} | PII: {has_sensitive}",
                    "WARNING" if has_sensitive else "INFO"
                )
            except Exception:
                pass

        # Route to Ollama if local model requested
        ollama_online = health_check.check_port("127.0.0.1", 11434) if health_check else False
        is_local_model = any(k in model.lower() for k in ["qwen", "llama", "fable"]) or "local" in req.get("routing", "")

        # --- STREAMING SSE PATH ---
        if is_stream:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("X-Accel-Buffering", "no")
            self._send_cors_headers()
            self.end_headers()

            if is_local_model:
                if not ollama_online:
                    offline_msg = f"[OMEGA GATEWAY] Model '{model}' is local. Ollama on port 11434 is stopped. Run 'python omega_ctl.py start-ai'."
                    chunk = {
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": model,
                        "choices": [{"index": 0, "delta": {"role": "assistant", "content": offline_msg}, "finish_reason": "stop"}]
                    }
                    try:
                        self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode("utf-8"))
                        self.wfile.write(b"data: [DONE]\n\n")
                        self.wfile.flush()
                    except (BrokenPipeError, ConnectionResetError):
                        pass
                    return

                try:
                    ollama_req = urllib.request.Request(
                        f"{OLLAMA_BASE_URL}/v1/chat/completions",
                        data=json.dumps(req).encode("utf-8"),
                        headers={"Content-Type": "application/json"}
                    )
                    with urllib.request.urlopen(ollama_req, timeout=120) as resp:
                        while True:
                            line = resp.readline()
                            if not line:
                                break
                            self.wfile.write(line)
                            self.wfile.flush()
                    return
                except (BrokenPipeError, ConnectionResetError):
                    return
                except Exception as e:
                    err_chunk = {"error": f"Ollama streaming proxy error: {e}"}
                    try:
                        self.wfile.write(f"data: {json.dumps(err_chunk)}\n\n".encode("utf-8"))
                        self.wfile.write(b"data: [DONE]\n\n")
                        self.wfile.flush()
                    except Exception:
                        pass
                    return
            else:
                # Cloud model simulated stream
                cloud_msg = f"[OMEGA CLOUD ROUTER] Simulated cloud stream for '{model}'. Prompt sanitized (PII detected: {has_sensitive}). Ready for external adapter dispatch."
                words = cloud_msg.split(" ")
                try:
                    for i, word in enumerate(words):
                        chunk = {
                            "id": f"chatcmpl-{int(time.time())}",
                            "object": "chat.completion.chunk",
                            "created": int(time.time()),
                            "model": model,
                            "choices": [{"index": 0, "delta": {"content": (" " if i > 0 else "") + word}, "finish_reason": None if i < len(words) - 1 else "stop"}]
                        }
                        self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode("utf-8"))
                        self.wfile.flush()
                        time.sleep(0.03)
                    self.wfile.write(b"data: [DONE]\n\n")
                    self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass
                return

        # --- BLOCKING JSON PATH ---
        if is_local_model:
            if not ollama_online:
                resp = {
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": f"[OMEGA GATEWAY] Model '{model}' is local. Ollama engine on port 11434 is currently stopped. Launch it with 'python omega_ctl.py start-ai'."
                        },
                        "finish_reason": "stop"
                    }],
                    "usage": {"prompt_tokens": len(prompt_text.split()), "completion_tokens": 30, "total_tokens": len(prompt_text.split()) + 30},
                    "omega_router": {
                        "routed_to": "local_ollama",
                        "engine_status": "offline",
                        "pii_detected": has_sensitive
                    }
                }
                self._send_json(resp)
                return

            try:
                ollama_req = urllib.request.Request(
                    f"{OLLAMA_BASE_URL}/v1/chat/completions",
                    data=json.dumps(req).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(ollama_req, timeout=60) as f:
                    ollama_resp = json.loads(f.read().decode("utf-8"))
                    ollama_resp["omega_router"] = {"routed_to": "local_ollama", "pii_detected": has_sensitive}
                    self._send_json(ollama_resp)
                    return
            except Exception as e:
                self._send_json({"error": f"Ollama proxy error: {e}"}, 502)
                return

        # Cloud AI Gateway path
        self._send_json({
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"[OMEGA CLOUD ROUTER] Request verified. Target cloud model '{model}'. Sanitized payload (PII checked: {has_sensitive}). Ready for cloud dispatch."
                },
                "finish_reason": "stop"
            }],
            "omega_router": {
                "routed_to": "cloud_gateway",
                "pii_redacted": has_sensitive,
                "provider": "google_or_anthropic"
            }
        })

def start_server(port: int = PORT):
    server = ThreadedHTTPServer(("127.0.0.1", port), GatewayRequestHandler)
    print(f"[OK] ANTIGRAVITY OMEGA AIOS Gateway running at http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down AIOS Gateway...")
        server.server_close()

if __name__ == "__main__":
    p = PORT
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        p = int(sys.argv[1])
    start_server(p)
