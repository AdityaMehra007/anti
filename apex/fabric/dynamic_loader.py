"""
APEX V3 - 10,000 Dynamic Agent & Skill Instantiation Engine
Searches and instantiates any specialist from the 10,000 taxonomy matrix on-demand.
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from apex.kernel.agents import SpecialistAgent

WORKSPACE = Path(r"e:\anti")
MATRIX_FILE = WORKSPACE / "apex" / "data" / "apex_10000_master_matrix.json"

class ApexDynamicSpecialistLoader:
    def __init__(self):
        self._matrix: List[Dict[str, Any]] = []
        self._load_matrix()

    def _load_matrix(self):
        if MATRIX_FILE.exists():
            with open(MATRIX_FILE, "r", encoding="utf-8") as f:
                self._matrix = json.load(f)

    def search_specialists(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        q = query.lower()
        results = []
        for agent in self._matrix:
            if q in agent["name"].lower() or q in agent["vertical"].lower() or q in agent["capability"].lower() or q in agent["mission"].lower():
                results.append(agent)
                if len(results) >= limit:
                    break
        return results

    def instantiate_specialist(self, agent_id_or_slug: str) -> Optional[SpecialistAgent]:
        for rec in self._matrix:
            if rec["agent_id"].lower() == agent_id_or_slug.lower() or rec["skill_slug"].lower() == agent_id_or_slug.lower() or rec["name"].lower() == agent_id_or_slug.lower():
                return SpecialistAgent(
                    agent_id=rec["agent_id"],
                    role=rec["name"],
                    system_prompt=rec["mission"],
                    tools_permitted=rec["tools_permitted"],
                    autonomy_level=rec["autonomy_level"],
                    is_dynamic=True
                )
        return None

    @property
    def total_catalog_size(self) -> int:
        return len(self._matrix)
