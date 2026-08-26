"""
SOURCE QUALITY & WEB EVIDENCE OBJECT MODEL
Calculates provenance, cryptographic hash, and source quality ranking.
Tier 1: Official company career portal / government / primary source (1.00)
Tier 2: Authorized professional platform (LinkedIn, Wellfound, Glassdoor) (0.85)
Tier 3: Reputable secondary job boards & tech publications (0.70)
Tier 4: Community / social aggregators (Reddit, Twitter/X) (0.40)
"""
import time
import hashlib
import urllib.parse
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict

class SourceTier(str, Enum):
    TIER_1_PRIMARY = "TIER_1_PRIMARY"         # Company career site, official press, SEC/gov
    TIER_2_PROFESSIONAL = "TIER_2_PROFESSIONAL" # Verified professional portals (LinkedIn, etc.)
    TIER_3_SECONDARY = "TIER_3_SECONDARY"       # Reputable job aggregators, news (Indeed, TechCrunch)
    TIER_4_COMMUNITY = "TIER_4_COMMUNITY"       # Social networks, forums, unverified posts

@dataclass
class WebEvidenceObject:
    claim: str
    url: str
    title: str
    domain: str
    source_tier: SourceTier
    evidence_snippet: str
    confidence: float
    retrieved_date: str
    published_date: Optional[str] = None
    hash: str = ""

    def __post_init__(self):
        if not self.hash:
            self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        content_to_hash = f"{self.claim}|{self.url}|{self.evidence_snippet}|{self.source_tier.value}"
        return hashlib.sha256(content_to_hash.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["source_tier"] = self.source_tier.value
        return d

class SourceQualityEngine:
    TIER_1_DOMAINS = [
        "walmart.com", "careers.walmart.com", "target.com", "corporate.target.com",
        "swiggy.com", "careers.swiggy.com", "zepto.com", "zeptonow.com",
        "jpmorgan.com", "careers.jpmorgan.com", "google.com", "careers.google.com",
        "microsoft.com", "careers.microsoft.com", "apple.com", "amazon.jobs",
        "goldmansachs.com", "mckinsey.com", "bain.com", "bcg.com",
        "gov.in", "sec.gov", "greenhouse.io", "lever.co", "workday.com",
        "myworkdayjobs.com", "smartrecruiters.com", "ashbyhq.com", "freshteam.com"
    ]

    TIER_2_DOMAINS = [
        "linkedin.com", "glassdoor.com", "wellfound.com", "angel.co",
        "naukri.com", "foundit.in", "instahyre.com", "cutshort.io"
    ]

    TIER_3_DOMAINS = [
        "indeed.com", "simplyhired.com", "monster.com", "ziprecruiter.com",
        "techcrunch.com", "economictimes.indiatimes.com", "livemint.com",
        "entrackr.com", "yourstory.com", "inc42.com"
    ]

    @classmethod
    def classify_source_tier(cls, url: str) -> SourceTier:
        domain = urllib.parse.urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]

        for t1 in cls.TIER_1_DOMAINS:
            if domain == t1 or domain.endswith("." + t1):
                return SourceTier.TIER_1_PRIMARY

        for t2 in cls.TIER_2_DOMAINS:
            if domain == t2 or domain.endswith("." + t2):
                return SourceTier.TIER_2_PROFESSIONAL

        for t3 in cls.TIER_3_DOMAINS:
            if domain == t3 or domain.endswith("." + t3):
                return SourceTier.TIER_3_SECONDARY

        return SourceTier.TIER_4_COMMUNITY

    @classmethod
    def get_tier_weight(cls, tier: SourceTier) -> float:
        weights = {
            SourceTier.TIER_1_PRIMARY: 1.00,
            SourceTier.TIER_2_PROFESSIONAL: 0.85,
            SourceTier.TIER_3_SECONDARY: 0.70,
            SourceTier.TIER_4_COMMUNITY: 0.40
        }
        return weights.get(tier, 0.50)

    @classmethod
    def create_evidence(
        cls,
        claim: str,
        url: str,
        snippet: str,
        title: str = "",
        published_date: Optional[str] = None
    ) -> WebEvidenceObject:
        tier = cls.classify_source_tier(url)
        weight = cls.get_tier_weight(tier)
        domain = urllib.parse.urlparse(url).netloc.lower()
        retrieved = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        return WebEvidenceObject(
            claim=claim,
            url=url,
            title=title or f"Evidence from {domain}",
            domain=domain,
            source_tier=tier,
            evidence_snippet=snippet,
            confidence=round(weight, 2),
            retrieved_date=retrieved,
            published_date=published_date
        )
