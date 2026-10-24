"""
ApexFlow Enterprise Core - Idempotency Ledger.
Guarantees exactly-once execution semantics for financial, procurement, and agentic workflows.
"""

import asyncio
import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


class IdempotencyStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class IdempotencyRecord:
    key: str
    payload_hash: str
    status: IdempotencyStatus
    response_json: Optional[str]
    created_at: float
    expires_at: float


class IdempotencyLedger:
    """
    ACID-compliant Idempotency Ledger with SQLite backing and in-memory fast-path.
    
    Protects distributed financial and reconciliation endpoints from:
    1. Double processing during network timeouts.
    2. Concurrent duplicate submissions with identical payloads.
    3. Payload mutation under the same idempotency key (tamper detection).
    """

    def __init__(self, db_path: Optional[str] = None, default_ttl_seconds: int = 86400):
        self.default_ttl = default_ttl_seconds
        self.db_path = db_path or ":memory:"
        self._lock: Optional[asyncio.Lock] = None
        if self.db_path == ":memory:":
            self._conn = sqlite3.connect("file:idempotency_mem?mode=memory&cache=shared", uri=True, check_same_thread=False)
        else:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()

    @property
    def lock(self) -> asyncio.Lock:
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    def _init_db(self) -> None:
        with self._conn:
            self._conn.execute("PRAGMA journal_mode = WAL;")
            self._conn.execute("PRAGMA synchronous = NORMAL;")
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS idempotency_ledger (
                    idempotency_key TEXT PRIMARY KEY,
                    payload_hash TEXT NOT NULL,
                    status TEXT NOT NULL,
                    response_json TEXT,
                    created_at REAL NOT NULL,
                    expires_at REAL NOT NULL
                );
            """)
            self._conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_expires_at 
                ON idempotency_ledger (expires_at);
            """)

    @staticmethod
    def compute_hash(payload: Any) -> str:
        """Computes deterministic SHA-256 digest of serialized payload."""
        if isinstance(payload, bytes):
            serialized = payload
        elif isinstance(payload, str):
            serialized = payload.encode("utf-8")
        else:
            serialized = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    async def check_or_reserve(
        self,
        key: str,
        payload: Any,
        ttl_seconds: Optional[int] = None,
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        payload_hash = self.compute_hash(payload)
        now = time.time()
        ttl = ttl_seconds or self.default_ttl
        expires_at = now + ttl

        async with self.lock:
            cursor = self._conn.cursor()
            cursor.execute(
                "SELECT payload_hash, status, response_json, expires_at FROM idempotency_ledger WHERE idempotency_key = ?",
                (key,)
            )
            row = cursor.fetchone()

            if row:
                cached_hash, status, response_json, row_expires_at = row
                
                # Check expiry
                if now > row_expires_at:
                    self._conn.execute("DELETE FROM idempotency_ledger WHERE idempotency_key = ?", (key,))
                    self._conn.commit()
                else:
                    if cached_hash != payload_hash:
                        raise ValueError(
                            f"Idempotency key '{key}' was previously used with a different payload hash."
                        )
                    if status == IdempotencyStatus.PENDING.value:
                        raise RuntimeError(
                            f"Request with key '{key}' is already in-flight (PENDING state)."
                        )
                    if status == IdempotencyStatus.COMPLETED.value:
                        return True, json.loads(response_json) if response_json else {}

            # Not found or expired -> reserve as PENDING
            self._conn.execute(
                """
                INSERT OR REPLACE INTO idempotency_ledger 
                (idempotency_key, payload_hash, status, response_json, created_at, expires_at)
                VALUES (?, ?, ?, NULL, ?, ?)
                """,
                (key, payload_hash, IdempotencyStatus.PENDING.value, now, expires_at)
            )
            self._conn.commit()
            return False, None

    async def record_success(self, key: str, response: Any) -> None:
        """Marks key as COMPLETED and stores serialized response."""
        response_json = json.dumps(response, default=str)
        async with self.lock:
            self._conn.execute(
                """
                UPDATE idempotency_ledger 
                SET status = ?, response_json = ? 
                WHERE idempotency_key = ?
                """,
                (IdempotencyStatus.COMPLETED.value, response_json, key)
            )
            self._conn.commit()

    async def record_failure(self, key: str) -> None:
        """Cleans up or marks key as FAILED so client can retry with fresh attempt."""
        async with self.lock:
            self._conn.execute(
                "DELETE FROM idempotency_ledger WHERE idempotency_key = ?",
                (key,)
            )
            self._conn.commit()
