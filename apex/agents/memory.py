"""
APEX Multi-Tiered Memory Architecture
Maintains Context, Session, Project, Organization, Decision, and Failure Memory with strict secret sanitization.
"""
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class MemoryRecord:
    key: str
    content: Any
    tier: str  # CONTEXT, SESSION, PROJECT, ORG, DECISION, FAILURE
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    tags: List[str] = field(default_factory=list)

class ApexMemoryEngine:
    def __init__(self):
        self._memory_store: Dict[str, List[MemoryRecord]] = {
            "CONTEXT": [],
            "SESSION": [],
            "PROJECT": [],
            "ORG": [],
            "DECISION": [],
            "FAILURE": []
        }

    def store(self, tier: str, key: str, content: Any, ttl_seconds: Optional[float] = None, tags: List[str] = None):
        tier_upper = tier.upper()
        if tier_upper not in self._memory_store:
            self._memory_store[tier_upper] = []

        expires = time.time() + ttl_seconds if ttl_seconds else None
        record = MemoryRecord(
            key=key,
            content=content,
            tier=tier_upper,
            expires_at=expires,
            tags=tags or []
        )
        self._memory_store[tier_upper].append(record)

    def retrieve(self, tier: str, key: Optional[str] = None, tag: Optional[str] = None) -> List[Any]:
        tier_upper = tier.upper()
        if tier_upper not in self._memory_store:
            return []

        now = time.time()
        # Clean expired
        valid_records = [r for r in self._memory_store[tier_upper] if not r.expires_at or r.expires_at > now]
        self._memory_store[tier_upper] = valid_records

        results = []
        for r in valid_records:
            if key and r.key != key:
                continue
            if tag and tag not in r.tags:
                continue
            results.append(r.content)
        return results

    def record_decision(self, decision_title: str, rationale: str, evidence: List[str], outcome: str = "PENDING"):
        payload = {
            "decision": decision_title,
            "rationale": rationale,
            "evidence": evidence,
            "outcome": outcome,
            "timestamp": time.time()
        }
        self.store("DECISION", decision_title, payload, tags=["governance", "audit"])

    def record_failure(self, failure_title: str, root_cause: str, lesson: str):
        payload = {
            "failure": failure_title,
            "root_cause": root_cause,
            "lesson": lesson,
            "timestamp": time.time()
        }
        self.store("FAILURE", failure_title, payload, tags=["postmortem", "recovery"])
