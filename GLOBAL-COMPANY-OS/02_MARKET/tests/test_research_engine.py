#!/usr/bin/env python3
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from research_engine import FactClassifier, SourceTierEvaluator, EvidenceLedger

def test_fact_classifier_valid_tags():
    assert FactClassifier.validate_tag("VERIFIED FACT") is True
    assert FactClassifier.validate_tag("HYPOTHESIS") is True

def test_fact_classifier_invalid_tag():
    with pytest.raises(ValueError):
        FactClassifier.validate_tag("SOME RANDOM OPINION")

def test_source_tier_evaluator():
    tier, _ = SourceTierEvaluator.evaluate_source("DGFT", "https://dgft.gov.in/trade-notice")
    assert tier == 1
    tier, _ = SourceTierEvaluator.evaluate_source("Gartner", "https://gartner.com/research")
    assert tier == 2
    tier, _ = SourceTierEvaluator.evaluate_source("TechCrunch", "https://techcrunch.com/article")
    assert tier == 3
    tier, _ = SourceTierEvaluator.evaluate_source("Reddit", "https://reddit.com/r/startups")
    assert tier == 4

def test_evidence_ledger_record():
    ledger = EvidenceLedger()
    record = ledger.record_finding(
        claim="Sample verified export claim",
        source="DGFT India",
        url="https://dgft.gov.in/notice",
        tag="VERIFIED FACT",
        confidence=0.95
    )
    assert record["verified"] is True
    assert record["source_tier"] == 1
    summary = ledger.get_summary()
    assert summary["total_findings"] == 1
    assert summary["verified_count"] == 1
