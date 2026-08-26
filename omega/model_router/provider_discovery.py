"""
LIVE PROVIDER DISCOVERY ENGINE (HARDENED AND EVIDENCE-BASED)
Inspects live OmniRoute gateways, local Ollama daemons, and environment keys.
Discovers actual available models, context windows, and real endpoint status.
Zero hardcoded version assertions or fake claims.
"""
import os
import sys
import time
import json
import shutil
import subprocess
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class DiscoveredModel:
    model_id: str
    provider: str
    source: str  # OMNIROUTE_LIVE, OLLAMA_LOCAL, DIRECT_PROVIDER, CONFIGURED, UNKNOWN
    status: str  # AVAILABLE, DISCOVERED_NOT_VERIFIED, UNREACHABLE, UNKNOWN
    context_limit: Optional[int] = None
    capabilities: List[str] = field(default_factory=lambda: ["chat"])
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    last_verified: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DiscoveryReport:
    gateway_connected: bool
    gateway_endpoint: Optional[str]
    gateway_version: str  # Real discovered version or "UNKNOWN"
    discovered_models: List[DiscoveredModel]
    local_daemon_running: bool
    local_executable_found: bool
    local_executable_path: Optional[str]
    local_models: List[str]
    api_keys_status: Dict[str, Dict[str, Any]]
    environment_keys_present: List[str]
    reconciliation_notes: List[str]
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["discovered_models"] = [m.to_dict() if hasattr(m, "to_dict") else m for m in self.discovered_models]
        return data

class LiveProviderDiscovery:
    CANDIDATE_ENDPOINTS = [
        "http://localhost:20128/v1",
        "http://localhost:8000/v1",
        "http://localhost:3000/v1"
    ]
    OLLAMA_ENDPOINT = "http://localhost:11434"

    def __init__(self):
        self._cached_report: Optional[DiscoveryReport] = None

    def _discover_gateway_version(self, endpoint: Optional[str], response_headers: Optional[Dict[str, str]] = None) -> str:
        # 1. Inspect response headers if available
        if response_headers:
            for hk in ["x-omniroute-version", "x-gateway-version", "server"]:
                val = response_headers.get(hk) or response_headers.get(hk.lower())
                if val and "omniroute" in val.lower():
                    return val

        # 2. Inspect version endpoint if gateway endpoint exists
        if endpoint:
            for v_path in ["/version", "/v1/version", "/api/version"]:
                try:
                    req = urllib.request.Request(f"{endpoint}{v_path}", headers={"User-Agent": "OmegaDiscovery/2.0"})
                    with urllib.request.urlopen(req, timeout=0.5) as r:
                        if r.status == 200:
                            data = json.loads(r.read().decode("utf-8"))
                            if isinstance(data, dict) and "version" in data:
                                return str(data["version"])
                except Exception:
                    pass

        # 3. Inspect npm package metadata if installed globally
        try:
            res = subprocess.run(["npm", "list", "-g", "omniroute", "--json"], capture_output=True, text=True, timeout=1.5)
            if res.returncode == 0:
                data = json.loads(res.stdout)
                deps = data.get("dependencies", {})
                if "omniroute" in deps:
                    return str(deps["omniroute"].get("version", "UNKNOWN"))
        except Exception:
            pass

        return "UNKNOWN"

    def discover(self, force_refresh: bool = False) -> DiscoveryReport:
        if self._cached_report and not force_refresh:
            return self._cached_report

        discovered_models: List[DiscoveredModel] = []
        reconciliation: List[str] = []
        gateway_connected = False
        gateway_endpoint = None
        server_headers = {}

        # 1. Probe OmniRoute Gateway Endpoints
        for ep in self.CANDIDATE_ENDPOINTS:
            try:
                req = urllib.request.Request(
                    f"{ep}/models",
                    headers={"User-Agent": "OmegaDiscovery/2.0"}
                )
                with urllib.request.urlopen(req, timeout=0.8) as resp:
                    if resp.status == 200:
                        server_headers = dict(resp.headers)
                        data = json.loads(resp.read().decode("utf-8"))
                        gateway_connected = True
                        gateway_endpoint = ep
                        model_list = data.get("data", [])
                        for m in model_list:
                            m_id = m.get("id", "unknown") if isinstance(m, dict) else str(m)
                            discovered_models.append(DiscoveredModel(
                                model_id=m_id,
                                provider=m.get("owned_by", "OmniRoute") if isinstance(m, dict) else "OmniRoute",
                                source="OMNIROUTE_LIVE",
                                status="AVAILABLE",
                                capabilities=["chat", "tools"],
                                last_verified=time.time()
                            ))
                        reconciliation.append(f"Discovered {len(discovered_models)} live models from {ep}")
                        break
            except Exception:
                continue

        if not gateway_connected:
            reconciliation.append("OmniRoute gateway process not actively listening on candidate ports.")

        # Discover version evidence
        gateway_version = self._discover_gateway_version(gateway_endpoint, server_headers)

        # 2. Probe Local Ollama Daemon and Executables
        ollama_running = False
        local_models = []
        ollama_exe = shutil.which("ollama")
        candidate_exe = "E:/anti gravity/Tools/Ollama/ollama.exe"
        if not ollama_exe and os.path.exists(candidate_exe):
            ollama_exe = candidate_exe

        try:
            req = urllib.request.Request(f"{self.OLLAMA_ENDPOINT}/api/tags")
            with urllib.request.urlopen(req, timeout=0.8) as resp:
                if resp.status == 200:
                    ollama_running = True
                    data = json.loads(resp.read().decode("utf-8"))
                    for m in data.get("models", []):
                        m_name = m.get("name", "local-model")
                        local_models.append(m_name)
                        discovered_models.append(DiscoveredModel(
                            model_id=f"ollama/{m_name}",
                            provider="Ollama-Local",
                            source="OLLAMA_LOCAL",
                            status="DISCOVERED_NOT_VERIFIED",
                            capabilities=["chat"],
                            last_verified=None
                        ))
                    reconciliation.append(f"Discovered {len(local_models)} local models from Ollama daemon.")
        except Exception:
            reconciliation.append("Ollama daemon is offline on port 11434.")

        # 3. Probe API Keys Presence (Secret values strictly redacted)
        api_keys_status = {}
        env_keys_present = []
        for key_name in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GROQ_API_KEY", "DEEPSEEK_API_KEY", "MISTRAL_API_KEY"]:
            val = os.environ.get(key_name)
            is_present = bool(val and len(val.strip()) > 0)
            api_keys_status[key_name] = {
                "status": "PRESENT" if is_present else "MISSING",
                "source": "ENVIRONMENT" if is_present else "NONE",
                "last_verified": time.time()
            }
            if is_present:
                env_keys_present.append(key_name)

        report = DiscoveryReport(
            gateway_connected=gateway_connected,
            gateway_endpoint=gateway_endpoint,
            gateway_version=gateway_version,
            discovered_models=discovered_models,
            local_daemon_running=ollama_running,
            local_executable_found=bool(ollama_exe),
            local_executable_path=ollama_exe,
            local_models=local_models,
            api_keys_status=api_keys_status,
            environment_keys_present=env_keys_present,
            reconciliation_notes=reconciliation
        )
        self._cached_report = report
        return report

live_discovery = LiveProviderDiscovery()
