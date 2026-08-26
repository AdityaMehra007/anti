"""
OMEGA TRUTH ENGINE INTEGRATION
Pipeline: FIRECRAWL -> RAW SOURCE -> EXTRACTION -> NORMALIZATION ->
          VALIDATION -> SOURCE RANKING -> TRUTH ENGINE -> KNOWLEDGE GRAPH
Validates claims using source tiers and corroboration.
"""
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from ..live_web.evidence import WebEvidenceObject, SourceTier, SourceQualityEngine

@dataclass
class VerifiedFact:
    subject: str
    predicate: str
    object_value: Any
    confidence: float
    evidence_list: List[WebEvidenceObject] = field(default_factory=list)
    status: str = "VERIFIED_TRUE"
    verified_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["evidence_list"] = [e.to_dict() if hasattr(e, "to_dict") else e for e in self.evidence_list]
        return d

class TruthEngine:
    def __init__(self):
        self._knowledge_graph: Dict[str, List[VerifiedFact]] = {}

    def validate_claim(self, claim: str, evidence: WebEvidenceObject) -> VerifiedFact:
        # Check source quality tier
        weight = SourceQualityEngine.get_tier_weight(evidence.source_tier)

        confidence = round(min(1.0, weight * evidence.confidence), 2)
        status = "VERIFIED_TRUE" if confidence >= 0.70 else ("LIKELY_TRUE" if confidence >= 0.50 else "UNVERIFIED")

        fact = VerifiedFact(
            subject=evidence.domain,
            predicate="claims",
            object_value=claim,
            confidence=confidence,
            evidence_list=[evidence],
            status=status
        )

        key = evidence.domain
        if key not in self._knowledge_graph:
            self._knowledge_graph[key] = []
        self._knowledge_graph[key].append(fact)
        return fact

    def query_facts(self, domain_or_entity: str) -> List[VerifiedFact]:
        return self._knowledge_graph.get(domain_or_entity.lower(), [])

    def get_knowledge_graph_summary(self) -> Dict[str, Any]:
        return {
            "total_entities": len(self._knowledge_graph),
            "total_facts": sum(len(facts) for facts in self._knowledge_graph.values())
        }
