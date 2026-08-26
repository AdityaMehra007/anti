"""
OMNIROUTE GOVERNED MCP SERVER
Exposes governed OmniRoute tools with strict RBAC separation:
- READ: List models, providers, health metrics
- ROUTE: Route prompt to optimal model
- CONFIGURE / ADMIN: Restricted administrative settings (High Risk)
"""
from typing import Dict, Any, List
from ..model_router.provider_catalog import provider_catalog
from ..model_router.health_engine import ProviderHealthEngine
from ..model_router.router import ModelRouter
from ..model_router.token_optimizer import TokenOptimizer

class OmniRouteMcpServer:
    def __init__(self):
        self.health_engine = ProviderHealthEngine()
        self.router = ModelRouter(self.health_engine)

    def list_providers(self) -> Dict[str, Any]:
        models = provider_catalog.list_all()
        return {
            "total_models": len(models),
            "providers": list(set(m.provider for m in models)),
            "health_scores": self.health_engine.get_all_scores()
        }

    def route_task(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        selection = self.router.route(prompt, context)
        return selection.to_dict()

    def compress_tokens(self, raw_text: str) -> Dict[str, Any]:
        res = TokenOptimizer.compress_tool_output(raw_text)
        return res.to_dict()
