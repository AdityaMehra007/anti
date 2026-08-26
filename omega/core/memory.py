import os, uuid, json
from datetime import datetime
from database import OmegaDB

class OmegaMemory:
    '''10-Layer Persistent Memory & Intelligence Engine for Omega Platform.'''
    LAYERS = [
        "GLOBAL", "PROJECT", "AGENT", "TASK", "DECISION",
        "FAILURE", "USER", "KNOWLEDGE", "EXPERIMENT", "EVIDENCE"
    ]

    def __init__(self, db=None):
        self.db = db or OmegaDB()

    def store(self, layer, scope, key_tag, content, confidence=1.0, provenance="OmegaEngine"):
        if layer not in self.LAYERS:
            raise ValueError(f"Invalid layer: {layer}")
        mem_id = f"MEM-{uuid.uuid4().hex[:8]}"
        now = datetime.now().isoformat()
        content_str = json.dumps(content) if isinstance(content, (dict, list)) else str(content)

        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO memories (id, layer, scope, key_tag, content, confidence, provenance, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (mem_id, layer, scope, key_tag, content_str, confidence, provenance, now, now)
            )
            conn.commit()
        return mem_id

    def retrieve(self, layer=None, key_tag=None, limit=10):
        query = "SELECT * FROM memories WHERE 1=1"
        params = []
        if layer:
            query += " AND layer = ?"
            params.append(layer)
        if key_tag:
            query += " AND key_tag LIKE ?"
            params.append(f"%{key_tag}%")
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(query, params).fetchall()
            return [dict(r) for r in rows]
