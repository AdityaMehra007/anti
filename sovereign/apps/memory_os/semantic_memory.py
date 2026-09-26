import os, sys, json
from datetime import datetime

# Add sovereign/core to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "core")))
from memory import SovereignMemory

class SemanticMemoryOS:
    '''Semantic Multi-Layer Memory Layer with Compaction & Freshness Scoring.'''
    def __init__(self):
        self.mem = SovereignMemory()

    def record_decision(self, project_name, decision_title, rationale, alternatives=None):
        content = {
            "decision": decision_title,
            "rationale": rationale,
            "alternatives_considered": alternatives or [],
            "timestamp": datetime.now().isoformat()
        }
        return self.mem.store(
            layer="DECISION",
            scope=project_name,
            key_tag=f"DECISION_{decision_title.replace(' ', '_')}",
            content=content,
            confidence=1.0,
            provenance="SemanticMemoryOS"
        )

    def search_knowledge(self, keyword, limit=10):
        return self.mem.retrieve(key_tag=keyword, limit=limit)
