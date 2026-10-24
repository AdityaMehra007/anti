import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from risk_engine import NanoRiskEngine

def test_risk_evaluation_speed_and_approval():
    engine = NanoRiskEngine()
    engine.register_client("ZERODHA-USER-001", 500000.0) # 5 Lakh INR cash
    engine.set_circuit_bands("RELIANCE", 2700.0, 3100.0, 2900.0)

    # Valid buy order
    approved, reason, latency_us = engine.evaluate_order(
        client_id="ZERODHA-USER-001",
        symbol="RELIANCE",
        side="BUY",
        qty=50,
        price_inr=2920.0
    )
    assert approved is True
    assert reason == "RISK_APPROVED"
    assert latency_us < 50.0 # Python interpreter latency, C++ kernel is <0.85us

def test_insufficient_margin_rejection():
    engine = NanoRiskEngine()
    engine.register_client("ZERODHA-USER-002", 10000.0) # 10k INR
    engine.set_circuit_bands("TCS", 3500.0, 4200.0, 3800.0)

    approved, reason, _ = engine.evaluate_order(
        client_id="ZERODHA-USER-002",
        symbol="TCS",
        side="BUY",
        qty=100, # 380,000 INR required
        price_inr=3800.0
    )
    assert approved is False
    assert reason == "ERR_INSUFFICIENT_MARGIN"

def test_circuit_limit_collar_rejection():
    engine = NanoRiskEngine()
    engine.register_client("ZERODHA-USER-003", 1000000.0)
    engine.set_circuit_bands("INFY", 1400.0, 1600.0, 1500.0)

    # Order above upper circuit
    approved, reason, _ = engine.evaluate_order(
        client_id="ZERODHA-USER-003",
        symbol="INFY",
        side="BUY",
        qty=10,
        price_inr=1650.0 # > 1600 upper circuit
    )
    assert approved is False
    assert reason == "ERR_CIRCUIT_LIMIT_BREACHED"
