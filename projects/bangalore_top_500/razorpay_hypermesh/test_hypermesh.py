import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from router import HyperMeshRouter
from ledger import SovereignLedger

def test_router_healthy_selection():
    router = HyperMeshRouter()
    router.register_gateway("HDFC", "HDFC-GATEWAY-1")
    router.register_gateway("ICICI", "ICICI-GATEWAY-1")

    # Simulate HDFC fast & successful
    for _ in range(10):
        router.gateways["HDFC-GATEWAY-1"].record_attempt(True, 45.0)

    # Simulate ICICI slow & failing
    for _ in range(10):
        router.gateways["ICICI-GATEWAY-1"].record_attempt(False, 600.0)

    res = router.route_and_execute("TXN-101", 5000.0, preferred_bank="HDFC")
    assert res["status"] == "ROUTED_SUCCESS"
    assert res["selected_bank"] == "HDFC"
    assert res["route_latency_ms"] < 5.0

def test_router_failover_on_degraded_bank():
    router = HyperMeshRouter()
    router.register_gateway("AXIS", "AXIS-1")
    router.register_gateway("SBI", "SBI-1")

    for _ in range(20):
        router.gateways["AXIS-1"].record_attempt(False, 900.0) # Axis degraded
        router.gateways["SBI-1"].record_attempt(True, 30.0)   # SBI pristine

    res = router.route_and_execute("TXN-102", 2500.0, preferred_bank="AXIS")
    # Must failover to SBI because Axis is severely degraded
    assert res["status"] == "ROUTED_SUCCESS"
    assert res["selected_bank"] == "SBI"

def test_sovereign_double_entry_integrity():
    ledger = SovereignLedger()
    # Seed clearing account with float
    ledger.accounts["CLEARING_RESERVE"] = 100000000 # 1,000,000 INR
    ledger.accounts["ESCROW_HUB"] = -100000000

    e1 = ledger.record_transfer("ENT-1", "IDEM-1", "CLEARING_RESERVE", "MERCHANT_A", 500000)
    assert ledger.get_balance("MERCHANT_A") == 500000

    # Idempotent replay of same key must return identical entry and not double-credit
    e2 = ledger.record_transfer("ENT-1-DUPE", "IDEM-1", "CLEARING_RESERVE", "MERCHANT_A", 500000)
    assert e2.entry_id == e1.entry_id
    assert ledger.get_balance("MERCHANT_A") == 500000

    # Integrity verification
    assert ledger.verify_integrity() is True
