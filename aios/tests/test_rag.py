#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Knowledge Hub & RAG Automated Test Suite
Zero-dependency Python Standard Library test suite verifying:
- Markdown chunking with header and line range preservation
- SQLite indexing into knowledge_documents and knowledge_chunks
- BM25 lexical search ranking and citation formatting
- Gateway /v1/rag/stats and /v1/rag/query endpoints
"""

import sys
import os
import json
import unittest
import urllib.request
import threading
import time
from pathlib import Path

AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "ai"))
sys.path.insert(0, str(AIOS_ROOT / "databases"))

import gateway
from rag_engine import RAGEngine
import db

TEST_PORT = 8097
GATEWAY_URL = f"http://127.0.0.1:{TEST_PORT}"


class TestRAGEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = RAGEngine()
        cls.server = gateway.ThreadedHTTPServer(("127.0.0.1", TEST_PORT), gateway.GatewayRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_01_markdown_chunking(self):
        """Verifies chunker parses headers and assigns valid line ranges."""
        test_doc = AIOS_ROOT / "docs" / "HARDWARE_PROFILE.md"
        chunks = self.engine.chunk_markdown(test_doc)
        self.assertGreater(len(chunks), 0, "Document should yield semantic chunks")
        for c in chunks:
            self.assertIn("header", c)
            self.assertIn("start_line", c)
            self.assertIn("end_line", c)
            self.assertGreaterEqual(c["end_line"], c["start_line"])
            self.assertGreater(len(c["terms"]), 0)

    def test_02_indexing_and_database_persistence(self):
        """Verifies document indexing populates SQLite tables."""
        test_doc = AIOS_ROOT / "docs" / "MODEL_REGISTRY.md"
        cnt = self.engine.index_document(test_doc)
        self.assertGreater(cnt, 0)

        with db.get_connection() as con:
            cur = con.execute("SELECT * FROM knowledge_documents WHERE id = 'doc_model_registry'")
            row = cur.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["chunk_count"], cnt)

    def test_03_search_precision(self):
        """Verifies lexical query returns relevant citations with exact line numbers."""
        hits = self.engine.search_chunks("GTX 960M Maxwell VRAM", top_k=2)
        self.assertGreater(len(hits), 0)
        top_hit = hits[0]
        self.assertIn("citation", top_hit)
        self.assertTrue(top_hit["citation"].startswith("["))
        self.assertIn("#L", top_hit["citation"])
        self.assertGreater(top_hit["score"], 0)

    def test_04_gateway_rag_stats(self):
        """Verifies GET /v1/rag/stats returns online indexing status."""
        req = urllib.request.Request(f"{GATEWAY_URL}/v1/rag/stats")
        with urllib.request.urlopen(req, timeout=5) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertEqual(data.get("status"), "ONLINE")
            self.assertGreater(data.get("indexed_documents", 0), 0)
            self.assertGreater(data.get("indexed_chunks", 0), 0)

    def test_05_gateway_rag_query(self):
        """Verifies POST /v1/rag/query returns citations through Gateway."""
        payload = {
            "query": "SQLite WAL mode",
            "synthesize": False,
            "top_k": 2
        }
        req = urllib.request.Request(
            f"{GATEWAY_URL}/v1/rag/query",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            self.assertEqual(res.status, 200)
            data = json.loads(res.read().decode("utf-8"))
            self.assertIn("citations", data)
            self.assertGreater(len(data["citations"]), 0)


if __name__ == "__main__":
    unittest.main()
