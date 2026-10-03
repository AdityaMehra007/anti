"""
ANTIGRAVITY OMEGA — Fault-Tolerant Daemon Supervisor
Manages, monitors, and auto-restarts all core microservices across the enterprise.
Zero external dependencies (pure Python standard library).
"""

import os
import sys
import time
import json
import logging
import threading
import subprocess
from typing import Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Configure logging
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "supervisor.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("OmegaSupervisor")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class ServiceConfig:
    def __init__(
        self,
        name: str,
        command: List[str],
        port: Optional[int] = None,
        auto_restart: bool = True,
        max_restarts: int = 5,
        cwd: Optional[str] = None
    ):
        self.name = name
        self.command = command
        self.port = port
        self.auto_restart = auto_restart
        self.max_restarts = max_restarts
        self.cwd = cwd or ROOT_DIR
        self.process: Optional[subprocess.Popen] = None
        self.restart_count = 0
        self.last_started: Optional[float] = None
        self.last_exit_code: Optional[int] = None

    def is_running(self) -> bool:
        if self.process is None:
            return False
        return self.process.poll() is None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "port": self.port,
            "running": self.is_running(),
            "pid": self.process.pid if self.is_running() else None,
            "restart_count": self.restart_count,
            "last_started": self.last_started,
            "last_exit_code": self.last_exit_code,
            "auto_restart": self.auto_restart
        }

class SupervisorManager:
    def __init__(self):
        self.services: Dict[str, ServiceConfig] = {}
        self._lock = threading.Lock()
        self._running = True

    def register_service(
        self,
        name: str,
        command: List[str],
        port: Optional[int] = None,
        auto_restart: bool = True,
        max_restarts: int = 5,
        cwd: Optional[str] = None
    ):
        with self._lock:
            self.services[name] = ServiceConfig(
                name=name,
                command=command,
                port=port,
                auto_restart=auto_restart,
                max_restarts=max_restarts,
                cwd=cwd
            )

    def load_default_services(self):
        # 1. AIOS Gateway on port 8090
        gateway_script = os.path.join(ROOT_DIR, "aios", "services", "gateway.py")
        self.register_service(
            name="aios_gateway",
            command=[sys.executable, gateway_script],
            port=8090,
            auto_restart=True,
            max_restarts=5
        )

        # 2. TradeNexus B2B API on port 8000
        tradenexus_script = os.path.join(ROOT_DIR, "GLOBAL-COMPANY-OS", "06_ENGINEERING", "start_server.py")
        self.register_service(
            name="tradenexus_api",
            command=[sys.executable, tradenexus_script],
            port=8000,
            auto_restart=True,
            max_restarts=5
        )

        # 3. Plane Webhook Reactor on port 8092
        plane_reactor_script = os.path.join(ROOT_DIR, "plane", "plane_webhook_reactor.py")
        self.register_service(
            name="plane_webhook_reactor",
            command=[sys.executable, plane_reactor_script, "--port", "8092"],
            port=8092,
            auto_restart=True,
            max_restarts=5
        )

        # 4. Automation Scheduler (Cron & Heartbeat DAGs)
        scheduler_script = os.path.join(ROOT_DIR, "aios", "automation", "scheduler.py")
        self.register_service(
            name="automation_scheduler",
            command=[sys.executable, scheduler_script],
            port=None,
            auto_restart=True,
            max_restarts=5
        )

        # 5. Live Telemetry Relay on port 8096
        telemetry_script = os.path.join(ROOT_DIR, "aios", "services", "live_telemetry_relay.py")
        self.register_service(
            name="live_telemetry_relay",
            command=[sys.executable, telemetry_script, "8096"],
            port=8096,
            auto_restart=True,
            max_restarts=5
        )

    def start_service(self, name: str) -> bool:
        with self._lock:
            svc = self.services.get(name)
            if not svc:
                logger.error(f"Cannot start unknown service: {name}")
                return False

            if svc.is_running():
                logger.info(f"Service {name} is already running (PID: {svc.process.pid})")
                return True

            try:
                log_out = os.path.join(LOG_DIR, f"{name}.log")
                out_fd = open(log_out, "a", encoding="utf-8")
                
                # Use creationflags on Windows for detached console if needed
                creationflags = 0
                if sys.platform == "win32":
                    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

                svc.process = subprocess.Popen(
                    svc.command,
                    cwd=svc.cwd,
                    stdout=out_fd,
                    stderr=subprocess.STDOUT,
                    creationflags=creationflags
                )
                svc.last_started = time.time()
                logger.info(f"Started service '{name}' [PID: {svc.process.pid}] on port {svc.port}")
                return True
            except Exception as e:
                logger.error(f"Failed to start service '{name}': {e}")
                return False

    def stop_service(self, name: str) -> bool:
        with self._lock:
            svc = self.services.get(name)
            if not svc or not svc.is_running():
                return True

            try:
                logger.info(f"Stopping service '{name}' [PID: {svc.process.pid}]...")
                svc.process.terminate()
                try:
                    svc.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    svc.process.kill()
                    svc.process.wait(timeout=1)
                svc.last_exit_code = svc.process.poll()
                svc.process = None
                return True
            except Exception as e:
                logger.error(f"Failed to terminate '{name}': {e}")
                return False

    def restart_service(self, name: str) -> bool:
        self.stop_service(name)
        time.sleep(0.5)
        return self.start_service(name)

    def get_status(self) -> dict:
        with self._lock:
            return {name: svc.to_dict() for name, svc in self.services.items()}

    def start_all(self):
        for name in list(self.services.keys()):
            self.start_service(name)

    def stop_all(self):
        for name in list(self.services.keys()):
            self.stop_service(name)

    def monitor_tick(self):
        with self._lock:
            for name, svc in self.services.items():
                if svc.process is not None and svc.process.poll() is not None:
                    # Process died
                    exit_code = svc.process.poll()
                    svc.last_exit_code = exit_code
                    svc.process = None
                    logger.warning(f"Service '{name}' exited with code {exit_code}")

                    if svc.auto_restart and svc.restart_count < svc.max_restarts:
                        svc.restart_count += 1
                        logger.info(f"Auto-restarting '{name}' (Attempt {svc.restart_count}/{svc.max_restarts})...")
                        # Release lock briefly to start
                        threading.Thread(target=self.start_service, args=(name,), daemon=True).start()
                    elif svc.restart_count >= svc.max_restarts:
                        logger.error(f"Service '{name}' exceeded max restarts ({svc.max_restarts}). Marking stalled.")

    def run_supervisor_loop(self, poll_interval: float = 2.0):
        logger.info("Omega Supervisor monitoring loop active.")
        while self._running:
            self.monitor_tick()
            time.sleep(poll_interval)


class SupervisorHTTPHandler(BaseHTTPRequestHandler):
    manager: Optional[SupervisorManager] = None

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/status" or path == "/":
            status = self.manager.get_status() if self.manager else {}
            payload = json.dumps({"status": "ok", "services": status}, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        if path in ("/start", "/stop", "/restart"):
            service_name = params.get("name", [None])[0]
            if not service_name:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Missing service name parameter"}')
                return

            success = False
            if path == "/start":
                success = self.manager.start_service(service_name)
            elif path == "/stop":
                success = self.manager.stop_service(service_name)
            elif path == "/restart":
                success = self.manager.restart_service(service_name)

            payload = json.dumps({"status": "ok" if success else "failed", "service": service_name}).encode("utf-8")
            self.send_response(200 if success else 500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'{"error": "Not found"}')

    def log_message(self, format, *args):
        # Mute standard noisy HTTP log lines to stdout
        pass


def run_supervisor_server(port: int = 8095):
    manager = SupervisorManager()
    manager.load_default_services()

    SupervisorHTTPHandler.manager = manager
    server = HTTPServer(("0.0.0.0", port), SupervisorHTTPHandler)
    logger.info(f"Omega Supervisor HTTP API listening on http://localhost:{port}")

    # Start monitoring thread
    monitor_thread = threading.Thread(target=manager.run_supervisor_loop, daemon=True)
    monitor_thread.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal. Stopping all services...")
        manager._running = False
        manager.stop_all()
        server.server_close()
        logger.info("Supervisor shut down cleanly.")

if __name__ == "__main__":
    port = 8095
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_supervisor_server(port)
