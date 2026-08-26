"""
OMEGA FIRECRAWL ROUTER
Decides which Firecrawl capability should be used based on query intent and target type.

Routing Matrix:
QUESTION / SEARCH INTENT    -> SEARCH
KNOWN URL                  -> SCRAPE
MULTI-PAGE SITE            -> CRAWL
SITE STRUCTURE / SITEMAP   -> MAP
PDF / DOCUMENT             -> PARSE
INTERACTIVE PAGE / FORM    -> INTERACT (Gated)
STRUCTURED EXTRACTION      -> EXTRACT
DEEP RESEARCH              -> RESEARCH
"""
import re
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .client import FirecrawlClient
from .security import WebContentFirewall

class RouteTarget(str, Enum):
    SEARCH = "SEARCH"
    SCRAPE = "SCRAPE"
    CRAWL = "CRAWL"
    MAP = "MAP"
    PARSE = "PARSE"
    INTERACT = "INTERACT"
    EXTRACT = "EXTRACT"
    RESEARCH = "RESEARCH"

@dataclass
class RoutingDecision:
    target: RouteTarget
    tool_name: str
    reason: str
    parameters: Dict[str, Any]
    risk_level: str

class FirecrawlRouter:
    def __init__(self, client: Optional[FirecrawlClient] = None, firewall: Optional[WebContentFirewall] = None):
        self.client = client or FirecrawlClient()
        self.firewall = firewall or WebContentFirewall()

    def analyze_intent(self, prompt_or_url: str, context: Optional[Dict[str, Any]] = None) -> RoutingDecision:
        ctx = context or {}
        text = prompt_or_url.strip()
        lower_text = text.lower()

        if text.endswith(".pdf") or ".doc" in text or ctx.get("is_document"):
            return RoutingDecision(
                target=RouteTarget.PARSE,
                tool_name="firecrawl_parse",
                reason="Target is a document / PDF file",
                parameters={"url": text},
                risk_level="LOW"
            )

        if (
            "deep research" in lower_text
            or "comprehensive dossier" in lower_text
            or "365-day radar" in lower_text
            or ctx.get("deep_research")
        ):
            return RoutingDecision(
                target=RouteTarget.RESEARCH,
                tool_name="omega_firecrawl_research",
                reason="Request requires multi-step deep research and synthesis",
                parameters={"query": text},
                risk_level="LOW"
            )

        if ctx.get("schema") or "extract json" in lower_text or "schema extraction" in lower_text:
            return RoutingDecision(
                target=RouteTarget.EXTRACT,
                tool_name="firecrawl_extract",
                reason="Extraction schema provided for structured extraction",
                parameters={
                    "urls": ctx.get("urls", [text] if text.startswith("http") else []),
                    "schema": ctx.get("schema", {})
                },
                risk_level="LOW"
            )

        if ctx.get("actions") or "click" in lower_text or "fill form" in lower_text:
            return RoutingDecision(
                target=RouteTarget.INTERACT,
                tool_name="firecrawl_interact",
                reason="Request involves browser UI interaction",
                parameters={"url": ctx.get("url", text), "actions": ctx.get("actions", [])},
                risk_level="HIGH"
            )

        is_url = bool(re.match(r"^https?://", text))
        if is_url:
            if ctx.get("crawl") or "careers" in text or ctx.get("max_depth", 1) > 1:
                return RoutingDecision(
                    target=RouteTarget.CRAWL,
                    tool_name="firecrawl_crawl",
                    reason="Target is a domain / portal requiring multi-page crawl",
                    parameters={"url": text, "limit": ctx.get("limit", 15), "max_depth": ctx.get("max_depth", 2)},
                    risk_level="LOW"
                )
            elif ctx.get("map_site") or "sitemap" in lower_text:
                return RoutingDecision(
                    target=RouteTarget.MAP,
                    tool_name="firecrawl_map",
                    reason="Target requires site hierarchy mapping",
                    parameters={"url": text, "search": ctx.get("search")},
                    risk_level="LOW"
                )
            else:
                return RoutingDecision(
                    target=RouteTarget.SCRAPE,
                    tool_name="firecrawl_scrape",
                    reason="Target is a direct specific URL",
                    parameters={"url": text},
                    risk_level="LOW"
                )

        return RoutingDecision(
            target=RouteTarget.SEARCH,
            tool_name="firecrawl_search",
            reason="Input is a natural language question or discovery query",
            parameters={"query": text, "limit": ctx.get("limit", 10)},
            risk_level="LOW"
        )

    def route_and_execute(self, prompt_or_url: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        decision = self.analyze_intent(prompt_or_url, context)

        if decision.risk_level == "HIGH":
            security_check = self.firewall.check_interaction_allowed(decision.parameters.get("url", ""))
            if not security_check.allowed:
                return {
                    "success": False,
                    "error": f"Security Policy Blocked: {security_check.reason}",
                    "decision": decision.target.value
                }

        if decision.target == RouteTarget.SEARCH:
            raw = self.client.search(decision.parameters["query"], limit=decision.parameters.get("limit", 10))
        elif decision.target == RouteTarget.SCRAPE:
            raw = self.client.scrape(decision.parameters["url"])
        elif decision.target == RouteTarget.CRAWL:
            raw = self.client.crawl(decision.parameters["url"], limit=decision.parameters.get("limit", 15))
        elif decision.target == RouteTarget.MAP:
            raw = self.client.map(decision.parameters["url"], search=decision.parameters.get("search"))
        elif decision.target == RouteTarget.PARSE:
            raw = self.client.parse(decision.parameters["url"])
        elif decision.target == RouteTarget.EXTRACT:
            raw = self.client.extract(decision.parameters["urls"], schema=decision.parameters["schema"])
        elif decision.target == RouteTarget.INTERACT:
            raw = self.client.interact(decision.parameters["url"], actions=decision.parameters["actions"])
        else:
            raw = self.client.search(prompt_or_url)

        sanitized = self.firewall.sanitize_response(raw)
        sanitized["routing_decision"] = {
            "target": decision.target.value,
            "tool_name": decision.tool_name,
            "reason": decision.reason,
            "risk_level": decision.risk_level
        }
        return sanitized
