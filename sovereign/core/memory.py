import os, uuid, json
from datetime import datetime
from database import SovereignDB

class SovereignMemory:
    '''10-Layer Persistent Memory Engine for Sovereign Platform.'''
    LAYERS = [
        "GLOBAL", "PROJECT", "AGENT", "SESSION", "DECISION",
        "ARCHITECTURE", "USER_PREFERENCE", "FAILURE", "KNOWLEDGE", "EVIDENCE"
    ]

    def __init__(self, db=None):
        if isinstance(db, str):
            self.memory_dir = db
            self.db = SovereignDB()
        else:
            self.db = db or SovereignDB()

    def store(self, layer, scope, key_tag, content, confidence=1.0, provenance="SYSTEM"):
        if layer not in self.LAYERS:
            raise ValueError(f"Invalid memory layer: {layer}. Allowed: {self.LAYERS}")
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

    def record_lesson(self, what_happened, why, what_worked, what_failed, what_should_change):
        lesson = {
            "what_happened": what_happened,
            "why": why,
            "what_worked": what_worked,
            "what_failed": what_failed,
            "what_should_change": what_should_change
        }
        return self.store(
            layer="KNOWLEDGE",
            scope="OPERATIONS",
            key_tag="LESSON_LEARNED",
            content=lesson
        )

    def retrieve(self, layer=None, scope=None, key_tag=None, limit=20):
        query = "SELECT * FROM memories WHERE 1=1"
        params = []
        if layer:
            query += " AND layer = ?"
            params.append(layer)
        if scope:
            query += " AND scope = ?"
            params.append(scope)
        if key_tag:
            query += " AND key_tag LIKE ?"
            params.append(f"%{key_tag}%")
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(query, params).fetchall()
            return [dict(r) for r in rows]
