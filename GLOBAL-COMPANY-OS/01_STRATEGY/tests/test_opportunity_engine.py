#!/usr/bin/env python3
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from opportunity_engine import OpportunityEngine

def test_generate_500_opportunities():
    opps = OpportunityEngine.generate_500_opportunities()
    assert len(opps) == 500
    assert opps[0]["id"] == "OPP-001"
    assert "TradeNexus" in opps[0]["title"]

def test_score_opportunity():
    opps = OpportunityEngine.generate_500_opportunities()
    winner = opps[0]
    score = OpportunityEngine.score_opportunity(winner)
    assert score > 90.0
    assert score <= 100.0
