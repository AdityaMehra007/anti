#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Knowledge Hub & Semantic RAG Engine
Pure Python Standard Library (Zero-Dependency) local document indexing,
lexical/BM25 retrieval, chunk line tracking, and grounded cited synthesis.
"""

import sys
import os
import re
import math
import json
import hashlib
import urllib.request
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "databases"))
sys.path.insert(0, str(AIOS_ROOT / "scripts"))

try:
    import db
except ImportError:
    db = None

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
GATEWAY_URL = os.environ.get("GATEWAY_URL", "http://127.0.0.1:8090")

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "with",
    "by", "of", "from", "as", "is", "was", "are", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "this", "that", "these", "those"
}


def tokenize(text: str) -> List[str]:
    """Extracts alphanumeric words, lowercased and stripped of stopwords."""
    words = re.findall(r"\b[A-Za-z0-9_]{2,}\b", text.lower())
    return [w for w in words if w not in STOPWORDS]


class RAGEngine:
    def __init__(self):
        pass

    def chunk_markdown(self, file_path: Path) -> List[Dict[str, Any]]:
        """Splits markdown file into coherent chunks preserving line numbers and headers."""
        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        chunks = []
        current_header = file_path.stem.replace("_", " ").title()
        current_lines = []
        chunk_start = 1

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            # If line is a markdown heading (# Header)
            if stripped.startswith("#") and len(stripped.split()) > 1:
                # Flush previous chunk if non-empty
                if current_lines:
                    chunk_text = "".join(current_lines).strip()
                    if len(chunk_text) > 30:
                        chunks.append({
                            "header": current_header,
                            "start_line": chunk_start,
                            "end_line": idx - 1,
                            "content": chunk_text,
                            "terms": " ".join(tokenize(chunk_text))
                        })
                    current_lines = []
                current_header = stripped.lstrip("#").strip()
                chunk_start = idx

            current_lines.append(line)

            # Cap chunk at 50 lines if no headers encountered
            if len(current_lines) >= 50:
                chunk_text = "".join(current_lines).strip()
                if len(chunk_text) > 30:
                    chunks.append({
                        "header": current_header,
                        "start_line": chunk_start,
                        "end_line": idx,
                        "content": chunk_text,
                        "terms": " ".join(tokenize(chunk_text))
                    })
                current_lines = []
                chunk_start = idx + 1

        # Flush final chunk
        if current_lines:
            chunk_text = "".join(current_lines).strip()
            if len(chunk_text) > 30:
                chunks.append({
                    "header": current_header,
                    "start_line": chunk_start,
                    "end_line": len(lines),
                    "content": chunk_text,
                    "terms": " ".join(tokenize(chunk_text))
                })

        return chunks

    def index_document(self, file_path: Path, category: str = "DOCS") -> int:
        """Indexes a single markdown file into master.db."""
        if not db or not file_path.exists():
            return 0

        raw_bytes = file_path.read_bytes()
        content_hash = hashlib.sha256(raw_bytes).hexdigest()
        doc_id = f"doc_{file_path.stem.lower()}"
        chunks = self.chunk_markdown(file_path)

        with db.get_connection() as con:
            # Check if unchanged
            cur = con.execute("SELECT content_hash FROM knowledge_documents WHERE id = ?", (doc_id,))
            row = cur.fetchone()
            if row and row["content_hash"] == content_hash:
                return len(chunks)  # Already up to date

            # Upsert document entry
            con.execute(
                """
                INSERT INTO knowledge_documents (id, file_path, title, category, content_hash, chunk_count, embedded_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(id) DO UPDATE SET
                    content_hash = excluded.content_hash,
                    chunk_count = excluded.chunk_count,
                    embedded_at = CURRENT_TIMESTAMP
                """,
                (doc_id, str(file_path), file_path.stem.replace("_", " ").title(), category, content_hash, len(chunks))
            )

            # Clear old chunks
            con.execute("DELETE FROM knowledge_chunks WHERE doc_id = ?", (doc_id,))

            # Insert new chunks
            for idx, c in enumerate(chunks):
                con.execute(
                    """
                    INSERT INTO knowledge_chunks (doc_id, file_path, chunk_index, header, start_line, end_line, content, terms)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (doc_id, str(file_path), idx, c["header"], c["start_line"], c["end_line"], c["content"], c["terms"])
                )
            con.commit()

        return len(chunks)

    def index_directory(self, dir_path: Path) -> Dict[str, int]:
        """Indexes all markdown files in the specified directory."""
        results = {}
        if not dir_path.exists():
            return results

        for p in dir_path.glob("*.md"):
            cnt = self.index_document(p)
            results[p.name] = cnt

        if db:
            db.log_audit("RAG_ENGINE", "INDEX_DIRECTORY", "KNOWLEDGE", f"Indexed {len(results)} files in {dir_path}", "INFO")
        return results

    def search_chunks(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Performs lexical BM25-style search over all indexed knowledge chunks."""
        if not db:
            return []

        query_terms = tokenize(query)
        if not query_terms:
            return []

        with db.get_connection() as con:
            cur = con.execute("SELECT * FROM knowledge_chunks")
            all_chunks = [dict(row) for row in cur.fetchall()]

        if not all_chunks:
            return []

        total_chunks = len(all_chunks)
        # Compute term document frequencies (DF)
        df: Dict[str, int] = {}
        for q in query_terms:
            df[q] = sum(1 for c in all_chunks if f" {q} " in f" {c['terms']} ")

        scored_chunks = []
        for c in all_chunks:
            chunk_tokens = c["terms"].split()
            doc_len = len(chunk_tokens)
            if doc_len == 0:
                continue

            score = 0.0
            for q in query_terms:
                if q in chunk_tokens:
                    tf = chunk_tokens.count(q) / doc_len
                    idf = math.log((total_chunks - df[q] + 0.5) / (df[q] + 0.5) + 1.0)
                    score += tf * idf

            if score > 0:
                file_name = Path(c["file_path"]).name
                scored_chunks.append({
                    "score": round(score, 4),
                    "file_name": file_name,
                    "file_path": c["file_path"],
                    "header": c["header"],
                    "start_line": c["start_line"],
                    "end_line": c["end_line"],
                    "citation": f"[{file_name}#L{c['start_line']}-L{c['end_line']}]",
                    "content": c["content"]
                })

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks[:top_k]

    def query_and_synthesize(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Retrieves cited context and invokes local model to answer with ground truth."""
        matches = self.search_chunks(query, top_k=top_k)
        if not matches:
            return {
                "query": query,
                "answer": "No relevant local documents matched the query.",
                "citations": []
            }

        # Build grounded context
        context_blocks = []
        citations = []
        for m in matches:
            citations.append(m["citation"])
            context_blocks.append(f"--- SOURCE: {m['citation']} ({m['header']}) ---\n{m['content']}")

        full_context = "\n\n".join(context_blocks)
        system_prompt = (
            "You are the ANTIGRAVITY OMEGA Knowledge Assistant. Answer the user query using ONLY "
            "the provided verified context. Every claim you make must cite the exact source marker "
            "(e.g. [FILENAME#Lxx-Lyy]). If the context does not contain the answer, explicitly state that."
        )
        user_message = f"CONTEXT:\n{full_context}\n\nQUESTION:\n{query}"

        # Request completion from local gateway
        try:
            req_data = {
                "model": "qwen2.5-coder:3b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "stream": False
            }
            req = urllib.request.Request(
                f"{GATEWAY_URL}/v1/chat/completions",
                data=json.dumps(req_data).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                answer = data["choices"][0]["message"]["content"]
        except Exception as e:
            answer = f"[GATEWAY ERROR] Could not invoke local AI for synthesis: {e}\n\nRelevant Context:\n{full_context}"

        return {
            "query": query,
            "answer": answer,
            "citations": citations,
            "matches": matches
        }


if __name__ == "__main__":
    engine = RAGEngine()
    docs_path = AIOS_ROOT / "docs"
    print(f"[*] Indexing all markdown documents in {docs_path}...")
    res = engine.index_directory(docs_path)
    print(f"[OK] Indexed {len(res)} files with total chunks: {sum(res.values())}")
    for fname, cnt in res.items():
        print(f"  * {fname:<30}: {cnt} chunks")

    # Sample query test
    test_q = "What is the primary local AI model and what hardware does it use?"
    print(f"\n[*] Testing Search Query: '{test_q}'")
    hits = engine.search_chunks(test_q, top_k=2)
    for h in hits:
        print(f"  -> Score: {h['score']} | Citation: {h['citation']} ({h['header']})")
