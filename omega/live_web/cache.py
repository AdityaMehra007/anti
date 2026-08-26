"""
WEB INTELLIGENCE CACHE
Provides TTL-governed in-memory & file-backed caching with freshness tracking.
Stores LAST_CHECKED, NEXT_CHECK, and content hash metadata.
"""
import time
import hashlib
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class CacheEntry:
    key: str
    data: Any
    created_at: float
    expires_at: float
    content_hash: str
    last_checked: str
    next_check: str
    hit_count: int = 0

class WebIntelligenceCache:
    def __init__(self, default_ttl_seconds: int = 3600):
        self.default_ttl = default_ttl_seconds
        self._cache: Dict[str, CacheEntry] = {}

    def _hash_key(self, key: str) -> str:
        return hashlib.md5(key.encode("utf-8")).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if not entry:
            return None
        now = time.time()
        if now > entry.expires_at:
            del self._cache[key]
            return None
        entry.hit_count += 1
        return entry.data

    def set(self, key: str, data: Any, ttl_seconds: Optional[int] = None) -> CacheEntry:
        ttl = ttl_seconds or self.default_ttl
        now = time.time()
        expires = now + ttl
        content_hash = hashlib.sha256(str(data).encode("utf-8")).hexdigest()[:16]

        last_chk = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
        next_chk = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(expires))

        entry = CacheEntry(
            key=key,
            data=data,
            created_at=now,
            expires_at=expires,
            content_hash=content_hash,
            last_checked=last_chk,
            next_check=next_chk
        )
        self._cache[key] = entry
        return entry

    def clear(self):
        self._cache.clear()

    def stats(self) -> Dict[str, Any]:
        return {
            "total_cached_items": len(self._cache),
            "keys": list(self._cache.keys())[:10]
        }
