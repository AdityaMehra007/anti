"""
OMEGA INFINITY (Ω-OS) — ENTERPRISE MARKET & NETWORK INTELLIGENCE ENGINE
Indexes and provides high-speed search across:
1. Target Enterprise Matrix (4,500 deduplicated MNC & growth companies)
2. Verified LinkedIn Network Graph (9,223 executive connections)
3. Mined VECTIS Trade Leads (395 verified trade & supply chain decision makers)
"""

import os
import sys
import csv
import json
from typing import Dict, Any, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

COMPANIES_CSV = os.path.join(REPO_ROOT, "data", "Master_4500_Unique_Companies_Deduplicated.csv")
CONNECTIONS_CSV = os.path.join(REPO_ROOT, "linkedin_export", "Connections.csv")
LEADS_JSON = os.path.join(REPO_ROOT, "company", "leads", "master_verified_leads.json")


class IntelSearchEngine:
    """
    In-memory search and query engine for corporate targets and network relationships.
    """

    def __init__(self):
        self.companies: List[Dict[str, Any]] = []
        self.connections: List[Dict[str, Any]] = []
        self.trade_leads: List[Dict[str, Any]] = []
        self.loaded = False
        self._load_datasets()

    def _load_datasets(self):
        # 1. Load Companies
        if os.path.exists(COMPANIES_CSV):
            try:
                with open(COMPANIES_CSV, "r", encoding="utf-8", errors="replace") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get("Company Name"):
                            self.companies.append({
                                "id": row.get("Unique ID", ""),
                                "name": row.get("Company Name", "").strip(),
                                "sector": row.get("Industry Sector", "").strip(),
                                "target_role": row.get("Target BBA IB Role", "").strip(),
                                "location": row.get("Bangalore Hub Location", "").strip()
                            })
            except Exception as e:
                print(f"[INTEL] Warning: Could not parse {COMPANIES_CSV}: {e}")

        # 2. Load LinkedIn Connections
        if os.path.exists(CONNECTIONS_CSV):
            try:
                with open(CONNECTIONS_CSV, "r", encoding="utf-8", errors="replace") as f:
                    # Skip top note lines until header
                    lines = f.readlines()
                    header_idx = -1
                    for idx, line in enumerate(lines[:10]):
                        if "First Name" in line and "Last Name" in line:
                            header_idx = idx
                            break
                    if header_idx != -1:
                        reader = csv.DictReader(lines[header_idx:])
                        for row in reader:
                            fname = row.get("First Name", "").strip()
                            lname = row.get("Last Name", "").strip()
                            comp = row.get("Company", "").strip()
                            pos = row.get("Position", "").strip()
                            if fname or lname or comp:
                                self.connections.append({
                                    "name": f"{fname} {lname}".strip(),
                                    "company": comp,
                                    "position": pos,
                                    "url": row.get("URL", "").strip(),
                                    "connected_on": row.get("Connected On", "").strip()
                                })
            except Exception as e:
                print(f"[INTEL] Warning: Could not parse {CONNECTIONS_CSV}: {e}")

        # 3. Load Trade Leads
        if os.path.exists(LEADS_JSON):
            try:
                with open(LEADS_JSON, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.trade_leads = data
                    elif isinstance(data, dict) and "leads" in data:
                        self.trade_leads = data["leads"]
            except Exception as e:
                print(f"[INTEL] Warning: Could not parse {LEADS_JSON}: {e}")

        self.loaded = True

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_target_companies": len(self.companies),
            "total_network_connections": len(self.connections),
            "total_verified_trade_leads": len(self.trade_leads),
            "sectors_indexed": len(set(c["sector"] for c in self.companies if c.get("sector")))
        }

    def search_companies(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        if not q:
            return self.companies[:limit]

        results = []
        for c in self.companies:
            if (q in c["name"].lower() or
                q in c["sector"].lower() or
                q in c["location"].lower() or
                q in c["target_role"].lower()):
                results.append(c)
                if len(results) >= limit:
                    break
        return results

    def search_network(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        if not q:
            return self.connections[:limit]

        results = []
        for conn in self.connections:
            if (q in conn["name"].lower() or
                q in conn["company"].lower() or
                q in conn["position"].lower()):
                results.append(conn)
                if len(results) >= limit:
                    break
        return results

    def search_trade_leads(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        if not q:
            return self.trade_leads[:limit]

        results = []
        for lead in self.trade_leads:
            name = str(lead.get("name", "")).lower()
            comp = str(lead.get("company", "")).lower()
            pos = str(lead.get("position", "")).lower()
            if q in name or q in comp or q in pos:
                results.append(lead)
                if len(results) >= limit:
                    break
        return results
