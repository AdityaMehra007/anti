"""
OMEGA PROVIDER CATALOG (MEASURED & ESTIMATED METADATA)
Prioritizes live discovered models and marks fallback templates as ESTIMATED.
"""
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from .provider_discovery import live_discovery, DiscoveredModel

class ProviderCategory(str, Enum):
    FRONTIER_QUALITY = "FRONTIER_QUALITY"
    FAST = "FAST"
    LOW_COST_FREE = "LOW_COST_FREE"
    LOCAL = "LOCAL"
    SPECIALIZED = "SPECIALIZED"

@dataclass
class ModelSpec:
    model_id: str
    provider: str
    category: ProviderCategory
    context_window: int
    status: str  # DISCOVERED, ESTIMATED_TEMPLATE, UNREACHABLE
    cost_per_1m_input: float
    cost_per_1m_output: float
    cost_source: str  # DISCOVERED_PRICE, CONFIGURED_PRICE, UNKNOWN
    supports_vision: bool = False
    supports_tools: bool = True
    is_free_tier: bool = False
    verified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["category"] = self.category.value
        return d

class ProviderCatalog:
    def __init__(self):
        self._templates: Dict[str, ModelSpec] = {}
        self._populate_fallback_templates()

    def _populate_fallback_templates(self):
        templates = [
            ("claude-3-7-sonnet-20250219", "Anthropic", ProviderCategory.FRONTIER_QUALITY, 200000, 3.00, 15.00, False),
            ("gpt-4o", "OpenAI", ProviderCategory.FRONTIER_QUALITY, 128000, 2.50, 10.00, True),
            ("gemini-2.5-pro", "Google", ProviderCategory.FRONTIER_QUALITY, 1000000, 1.25, 5.00, True),
            ("deepseek-r1", "DeepSeek", ProviderCategory.FRONTIER_QUALITY, 64000, 0.55, 2.19, False),
            ("gemini-2.5-flash", "Google", ProviderCategory.FAST, 1000000, 0.075, 0.30, True),
            ("groq/llama-3.3-70b-versatile", "Groq", ProviderCategory.FAST, 128000, 0.59, 0.79, False),
            ("gpt-4o-mini", "OpenAI", ProviderCategory.FAST, 128000, 0.15, 0.60, True),
            ("cerebras/llama3.1-8b", "Cerebras", ProviderCategory.LOW_COST_FREE, 8192, 0.00, 0.00, False),
            ("ollama/qwen2.5:14b", "Ollama-Local", ProviderCategory.LOCAL, 32768, 0.00, 0.00, False)
        ]
        for mid, prov, cat, ctx, in_p, out_p, vis in templates:
            self._templates[mid] = ModelSpec(
                model_id=mid,
                provider=prov,
                category=cat,
                context_window=ctx,
                status="ESTIMATED_TEMPLATE",
                cost_per_1m_input=in_p,
                cost_per_1m_output=out_p,
                cost_source="CONFIGURED_PRICE",
                supports_vision=vis,
                verified=False
            )

    def list_all(self) -> List[ModelSpec]:
        # Combine live discovered models + fallback templates
        res = list(self._templates.values())
        report = live_discovery.discover()
        for d in report.discovered_models:
            if d.model_id not in self._templates:
                res.append(ModelSpec(
                    model_id=d.model_id,
                    provider=d.provider,
                    category=ProviderCategory.FAST,
                    context_window=d.context_limit or 32768,
                    status="DISCOVERED",
                    cost_per_1m_input=0.0,
                    cost_per_1m_output=0.0,
                    cost_source="UNKNOWN",
                    verified=True
                ))
        return res

    def get_model(self, model_id: str) -> Optional[ModelSpec]:
        for m in self.list_all():
            if m.model_id == model_id:
                return m
        return None

    def list_by_category(self, category: ProviderCategory) -> List[ModelSpec]:
        return [m for m in self.list_all() if m.category == category]

provider_catalog = ProviderCatalog()
