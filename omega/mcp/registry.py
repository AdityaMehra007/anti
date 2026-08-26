"""
OMEGA MCP SERVER REGISTRY
Tracks server metadata, version, source, transport, endpoint,
auth, capabilities, tools, permissions, health, risk, cost, rate limits.
"""
import time
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

class ServerHealth(str, Enum):
    CONNECTED = "CONNECTED"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

@dataclass
class McpServerRecord:
    server_name: str
    version: str
    source: str
    transport: str
    endpoint: str
    authentication: str
    capabilities: List[str]
    tools: List[str]
    permissions: List[str]
    health: ServerHealth = ServerHealth.CONNECTED
    risk_level: RiskLevel = RiskLevel.LOW
    cost_per_1k_calls: float = 0.0
    rate_limit_rpm: int = 120
    last_health_check: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["health"] = self.health.value
        data["risk_level"] = self.risk_level.value
        return data

class OmegaMcpRegistry:
    def __init__(self):
        self._servers: Dict[str, McpServerRecord] = {}
        self._register_default_servers()

    def _register_default_servers(self):
        # 1. Firecrawl Live Web Server
        firecrawl_record = McpServerRecord(
            server_name="firecrawl",
            version="3.24.0",
            source="github.com/firecrawl/firecrawl-mcp-server",
            transport="hosted_sse_or_stdio",
            endpoint="https://mcp.firecrawl.dev/v2/mcp",
            authentication="ENV_SECRET_FIRECRAWL_API_KEY",
            capabilities=[
                "search", "scrape", "crawl", "map",
                "parse", "extract", "interact", "batch_scrape"
            ],
            tools=[
                "firecrawl_search", "firecrawl_scrape", "firecrawl_crawl",
                "firecrawl_map", "firecrawl_parse", "firecrawl_extract",
                "firecrawl_interact", "firecrawl_batch_scrape"
            ],
            permissions=[
                "web:read", "web:search", "web:scrape",
                "web:crawl", "web:map", "web:extract"
            ],
            health=ServerHealth.CONNECTED,
            risk_level=RiskLevel.LOW,
            cost_per_1k_calls=1.00,
            rate_limit_rpm=120,
            metadata={"provider": "Mendable / Firecrawl Official", "description": "Governed Live-Web Layer"}
        )
        self.register_server(firecrawl_record)

        # 2. OmniRoute Model Router Gateway
        omniroute_record = McpServerRecord(
            server_name="omniroute",
            version="CONFIGURED_GATEWAY",
            source="github.com/diegosouzapw/OmniRoute",
            transport="openai_compatible_http",
            endpoint="http://localhost:20128/v1",
            authentication="ENV_SECRET_OMNIROUTE_API_KEY",
            capabilities=[
                "model_routing", "provider_fallback", "token_compression",
                "response_caching", "agent_to_agent_a2a", "multi_model_debate"
            ],
            tools=[
                "omniroute_list_providers", "omniroute_route_task",
                "omniroute_compress_tokens", "omniroute_get_health"
            ],
            permissions=["model:route", "model:read", "model:cache", "model:a2a"],
            health=ServerHealth.CONNECTED,
            risk_level=RiskLevel.LOW,
            cost_per_1k_calls=0.50,
            rate_limit_rpm=300,
            metadata={"provider": "OmniRoute Sovereign Router", "description": "Governed Model Gateway"}
        )
        self.register_server(omniroute_record)

    def register_server(self, record: McpServerRecord) -> None:
        self._servers[record.server_name] = record

    def get_server(self, server_name: str) -> Optional[McpServerRecord]:
        return self._servers.get(server_name)

    def list_servers(self) -> List[McpServerRecord]:
        return list(self._servers.values())

    def update_health(self, server_name: str, health: ServerHealth) -> bool:
        if server_name in self._servers:
            self._servers[server_name].health = health
            self._servers[server_name].last_health_check = time.time()
            return True
        return False

    def check_permission(self, server_name: str, requested_permission: str) -> bool:
        srv = self.get_server(server_name)
        if not srv:
            return False
        return requested_permission in srv.permissions

mcp_registry = OmegaMcpRegistry()
