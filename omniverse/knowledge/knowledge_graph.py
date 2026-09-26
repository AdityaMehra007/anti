"""
ANTIGRAVITY OMNIVERSE: UNIVERSAL KNOWLEDGE GRAPH ENGINE
=======================================================
Implements the global entity-relationship knowledge graph supporting
17 first-class entities, 18 typed relations, confidence scoring, and graph traversal.
"""
import sqlite3
import json
import time
from typing import Dict, Any, List, Optional, Set
from pathlib import Path

class UniversalKnowledgeGraph:
    """Relational graph engine backed by SQLite WAL with edge confidence scores."""

    VALID_ENTITIES = {
        "Company", "Person", "Product", "Technology", "Country", "City",
        "Industry", "Market", "Dataset", "Organization", "Regulation",
        "Patent", "ResearchPaper", "Project", "Software", "API", "EconomicIndicator"
    }

    VALID_RELATIONS = {
        "OWNS", "BUILDS", "COMPETES_WITH", "PARTNERS_WITH", "ACQUIRED",
        "INVESTED_IN", "USES", "DEPENDS_ON", "LOCATED_IN", "SERVES",
        "EMPLOYS", "FUNDED_BY", "RELATED_TO", "DERIVED_FROM", "CITES",
        "MEASURES", "CAUSES", "CORRELATES_WITH"
    }

    def __init__(self, db_path: str = "data/omniverse_graph.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS graph_nodes (
                    id TEXT PRIMARY KEY,
                    entity_type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    properties TEXT,
                    created_at REAL NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS graph_edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    properties TEXT,
                    created_at REAL NOT NULL,
                    FOREIGN KEY(source_id) REFERENCES graph_nodes(id),
                    FOREIGN KEY(target_id) REFERENCES graph_nodes(id)
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_edge_src ON graph_edges(source_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_edge_tgt ON graph_edges(target_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_edge_rel ON graph_edges(relation);")
            conn.commit()

    def add_node(self, node_id: str, entity_type: str, name: str, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if entity_type not in self.VALID_ENTITIES:
            raise ValueError(f"Invalid entity type '{entity_type}'. Must be one of {self.VALID_ENTITIES}")
        
        now = time.time()
        props_str = json.dumps(properties or {})
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO graph_nodes (id, entity_type, name, properties, created_at) VALUES (?, ?, ?, ?, ?)",
                (node_id, entity_type, name, props_str, now)
            )
            conn.commit()
        return {"id": node_id, "entity_type": entity_type, "name": name, "properties": properties or {}}

    def add_edge(self, source_id: str, relation: str, target_id: str, confidence: float = 1.0, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if relation not in self.VALID_RELATIONS:
            raise ValueError(f"Invalid relation '{relation}'. Must be one of {self.VALID_RELATIONS}")
        
        conf = max(0.0, min(1.0, float(confidence)))
        now = time.time()
        props_str = json.dumps(properties or {})
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO graph_edges (source_id, relation, target_id, confidence, properties, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (source_id, relation, target_id, conf, props_str, now)
            )
            conn.commit()
        return {"source": source_id, "relation": relation, "target": target_id, "confidence": conf}

    def get_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("""
                SELECT e.relation, e.target_id, n.name, n.entity_type, e.confidence
                FROM graph_edges e
                JOIN graph_nodes n ON e.target_id = n.id
                WHERE e.source_id = ?
            """, (node_id,))
            rows = cur.fetchall()
            return [{"relation": r[0], "target_id": r[1], "target_name": r[2], "target_type": r[3], "confidence": r[4]} for r in rows]

    def count_nodes_and_edges(self) -> Dict[str, int]:
        with sqlite3.connect(self.db_path) as conn:
            nodes_count = conn.execute("SELECT COUNT(*) FROM graph_nodes").fetchone()[0]
            edges_count = conn.execute("SELECT COUNT(*) FROM graph_edges").fetchone()[0]
            return {"nodes": nodes_count, "edges": edges_count}
