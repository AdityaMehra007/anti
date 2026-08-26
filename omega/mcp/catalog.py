"""
FIRECRAWL TOOL CATALOG
Defines formal schemas and capabilities for Firecrawl tools.
"""
from typing import Dict, Any

FIRECRAWL_TOOL_CATALOG: Dict[str, Dict[str, Any]] = {
    "firecrawl_search": {
        "name": "firecrawl_search",
        "description": "Searches the live web using Firecrawl and returns clean, LLM-ready markdown results with URLs and snippets.",
        "risk_level": "LOW",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query string."},
                "limit": {"type": "integer", "description": "Maximum number of search results.", "default": 10},
                "sources": {"type": "array", "items": {"type": "string"}, "description": "Domains to prioritize."}
            },
            "required": ["query"]
        }
    },
    "firecrawl_scrape": {
        "name": "firecrawl_scrape",
        "description": "Scrapes a single URL and converts it into clean markdown, extracting metadata, titles, and structured sections.",
        "risk_level": "LOW",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target web page URL to scrape."},
                "formats": {"type": "array", "items": {"type": "string"}, "default": ["markdown"]},
                "onlyMainContent": {"type": "boolean", "default": True}
            },
            "required": ["url"]
        }
    },
    "firecrawl_crawl": {
        "name": "firecrawl_crawl",
        "description": "Crawls a domain or career portal section recursively up to max depth.",
        "risk_level": "LOW",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Base URL to begin crawling."},
                "limit": {"type": "integer", "default": 15},
                "maxDepth": {"type": "integer", "default": 2},
                "includePaths": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["url"]
        }
    },
    "firecrawl_map": {
        "name": "firecrawl_map",
        "description": "Discovers and maps the hierarchy of URLs within a company domain.",
        "risk_level": "LOW",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Domain root URL."},
                "search": {"type": "string", "description": "Keyword to filter routes (e.g. 'careers')."}
            },
            "required": ["url"]
        }
    },
    "firecrawl_parse": {
        "name": "firecrawl_parse",
        "description": "Parses PDF documents, reports, or job specifications into structured clean text.",
        "risk_level": "LOW",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL or path to PDF/document."}
            },
            "required": ["url"]
        }
    },
    "firecrawl_extract": {
        "name": "firecrawl_extract",
        "description": "Extracts structured JSON data conforming to a specified schema from one or more URLs.",
        "risk_level": "LOW",
        "parameters": {
            "type": "object",
            "properties": {
                "urls": {"type": "array", "items": {"type": "string"}},
                "schema": {"type": "object"},
                "prompt": {"type": "string"}
            },
            "required": ["urls", "schema"]
        }
    },
    "firecrawl_interact": {
        "name": "firecrawl_interact",
        "description": "Executes interactive browser actions (click, scroll, type). HIGH RISK - requires approval.",
        "risk_level": "HIGH",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "actions": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["url", "actions"]
        }
    }
}

def get_tool_schema(tool_name: str) -> Dict[str, Any]:
    return FIRECRAWL_TOOL_CATALOG.get(tool_name, {})
