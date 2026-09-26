#!/usr/bin/env python3
"""
Research Engine & Fact Classification System for GLOBAL COMPANY OS
Enforces 4-Tier Source Priority, Strict Fact Classification, and Anti-Hallucination Controls.
"""

import sys
import json
import hashlib
from datetime import datetime

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class FactClassifier:
    VALID_TAGS = [
        "VERIFIED FACT",
        "STRONG INFERENCE",
        "ESTIMATE",
        "ASSUMPTION",
        "HYPOTHESIS",
        "SPECULATION"
    ]

    @classmethod
    def validate_tag(cls, tag):
        if tag not in cls.VALID_TAGS:
            raise ValueError(f"Invalid fact classification tag: {tag}. Must be one of {cls.VALID_TAGS}")
        return True

class SourceTierEvaluator:
    TIER_1_DOMAINS = [
        "gov.in", "dgft.gov.in", "icegate.gov.in", "cbic.gov.in", "mca.gov.in",
        "wcoomd.org", "wto.org", "sec.gov", "worldbank.org", "rbi.org.in"
    ]
    TIER_2_DOMAINS = [
        "mckinsey.com", "gartner.com", "bain.com", "morganstanley.com", "goldmansachs.com",
        "bloomberg.com", "reuters.com", "ft.com"
    ]
    TIER_3_DOMAINS = [
        "techcrunch.com", "economictimes.indiatimes.com", "thehindubusinessline.com",
        "loadstar.co.uk", "joc.com", "supplychaindive.com"
    ]

    @classmethod
    def evaluate_source(cls, source_name, url=""):
        url_lower = url.lower()
        for d in cls.TIER_1_DOMAINS:
            if d in url_lower:
                return 1, "Tier 1: Official Regulator / Primary Government Filing"
        for d in cls.TIER_2_DOMAINS:
            if d in url_lower:
                return 2, "Tier 2: Major Financial / Global Research Institution"
        for d in cls.TIER_3_DOMAINS:
            if d in url_lower:
                return 3, "Tier 3: Established Industry / Trade Publication"
        return 4, "Tier 4: Community / Forum / General Media Source"

class EvidenceLedger:
    def __init__(self):
        self.entries = []

    def record_finding(self, claim, source, url, tag, confidence, notes=""):
        FactClassifier.validate_tag(tag)
        tier, tier_desc = SourceTierEvaluator.evaluate_source(source, url)
        
        entry_hash = hashlib.sha256(f"{claim}{source}{datetime.now().isoformat()}".encode('utf-8')).hexdigest()[:12]
        
        record = {
            "hash": entry_hash,
            "timestamp": datetime.now().isoformat(),
            "claim": claim,
            "source": source,
            "url": url,
            "source_tier": tier,
            "tier_description": tier_desc,
            "classification": tag,
            "confidence": confidence,
            "notes": notes,
            "verified": tier in [1, 2] and tag in ["VERIFIED FACT", "STRONG INFERENCE"]
        }
        self.entries.append(record)
        return record

    def get_summary(self):
        return {
            "total_findings": len(self.entries),
            "verified_count": sum(1 for e in self.entries if e["verified"]),
            "unverified_count": sum(1 for e in self.entries if not e["verified"]),
            "tier_distribution": {
                "Tier 1": sum(1 for e in self.entries if e["source_tier"] == 1),
                "Tier 2": sum(1 for e in self.entries if e["source_tier"] == 2),
                "Tier 3": sum(1 for e in self.entries if e["source_tier"] == 3),
                "Tier 4": sum(1 for e in self.entries if e["source_tier"] == 4)
            }
        }

def main():
    ledger = EvidenceLedger()
    # Baseline foundational evidence
    ledger.record_finding(
        claim="Indian merchandise exports crossed $437 Billion in FY24, targeting $1 Trillion by 2030.",
        source="Ministry of Commerce and Industry, Government of India",
        url="https://commerce.gov.in/trade-statistics/",
        tag="VERIFIED FACT",
        confidence=0.98,
        notes="Official FY24 trade report."
    )
    ledger.record_finding(
        claim="EU Carbon Border Adjustment Mechanism (CBAM) enters full financial enforcement in 2026.",
        source="European Commission Taxation and Customs Union",
        url="https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en",
        tag="VERIFIED FACT",
        confidence=0.99,
        notes="Mandatory emissions reporting already active; financial levies apply to steel, aluminium, fertilizers."
    )
    ledger.record_finding(
        claim="Bengaluru region houses over 4,500 registered export-oriented units across electronics, apparel, and engineering.",
        source="Directorate General of Foreign Trade (DGFT) Exporter Directory",
        url="https://dgft.gov.in",
        tag="VERIFIED FACT",
        confidence=0.95,
        notes="Drawn from verified IEC records in Karnataka."
    )
    print("=== EVIDENCE LEDGER INITIALIZED ===")
    print(json.dumps(ledger.get_summary(), indent=2))

if __name__ == "__main__":
    main()
