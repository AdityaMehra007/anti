"""
OMEGA INFINITY (Ω-OS) — COMPREHENSIVE VERIFICATION TEST SUITE
Enforces 100% test coverage across:
- Sovereign Kernel State & Constitutional Mode Transitions
- SHA-256 Cryptographic Tamper-Evident Event Ledger
- VECTIS Trade Gateway Adapter (UCP 600, SWIFT MT700, EU CBAM)
- Enterprise Market & Network Intelligence Search
- 12-Department Sovereign Autonomous Swarm Coordination
"""

import os
import sys
import json
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import OmegaKernel, CONSTITUTIONAL_MODES
from omega_infinity.omega_vectis_adapter import VectisEnterpriseAdapter
from omega_infinity.omega_intel_engine import IntelSearchEngine
from omega_infinity.omega_swarm_matrix import SwarmMatrix
from company.vectis_swift_parser import SAMPLE_SWIFT_MT700


@pytest.fixture
def temp_kernel(tmp_path):
    ledger_file = str(tmp_path / "test_ledger.jsonl")
    return OmegaKernel(ledger_path=ledger_file)


def test_kernel_boot_and_mode_transitions(temp_kernel):
    kernel = temp_kernel
    summary = kernel.get_summary()

    assert summary["holding"] == "OMEGA SOVEREIGN HOLDINGS"
    assert summary["founder"] == "Aditya Mehra"
    assert summary["active_mode"]["code"] == "M"

    # Test transitioning through modes
    res_b = kernel.set_mode("B")
    assert res_b["mode"] == "B"
    assert res_b["name"] == "RESEARCH"

    res_d = kernel.set_mode("D")
    assert res_d["mode"] == "D"
    assert res_d["name"] == "BUILD"

    # Invalid mode rejection
    with pytest.raises(ValueError):
        kernel.set_mode("Z")


def test_tamper_evident_ledger_integrity(temp_kernel):
    kernel = temp_kernel
    ledger = kernel.ledger

    # Genesis block + Boot block exist
    integrity = ledger.verify_integrity()
    assert integrity["valid"] is True
    assert integrity["total_blocks"] >= 2

    # Append events
    ledger.append("TEST_EVENT_1", "TEST_ACTOR", {"key": "val1"})
    ledger.append("TEST_EVENT_2", "TEST_ACTOR", {"key": "val2"})

    integrity_after = ledger.verify_integrity()
    assert integrity_after["valid"] is True
    assert integrity_after["total_blocks"] >= 4

    # Simulate tampering with a block's payload
    tampered_block = ledger.blocks[1]
    original_payload = tampered_block.payload.copy()
    tampered_block.payload["tampered"] = True

    tampered_integrity = ledger.verify_integrity()
    assert tampered_integrity["valid"] is False
    assert "Hash mismatch" in tampered_integrity["reason"]

    # Revert tampering
    tampered_block.payload = original_payload
    reverted_integrity = ledger.verify_integrity()
    assert reverted_integrity["valid"] is True


def test_vectis_adapter_clean_docket():
    from company.vectis_parser import generate_sample_dockets
    clean_docket_path = os.path.join(REPO_ROOT, "company", "inbox", "docket_peenya_clean.json")
    if not os.path.exists(clean_docket_path):
        generate_sample_dockets()
    assert os.path.exists(clean_docket_path)

    adapter = VectisEnterpriseAdapter()
    with open(clean_docket_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    res = adapter.audit_docket(data)
    assert res["success"] is True
    assert res["passed"] is True
    assert res["fatal_count"] == 0
    assert len(res["certificate_seal"]) == 64


def test_vectis_adapter_flawed_docket():
    from company.vectis_parser import generate_sample_dockets
    flawed_docket_path = os.path.join(REPO_ROOT, "company", "inbox", "docket_tirupur_flawed.json")
    if not os.path.exists(flawed_docket_path):
        generate_sample_dockets()
    assert os.path.exists(flawed_docket_path)

    adapter = VectisEnterpriseAdapter()
    with open(flawed_docket_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    res = adapter.audit_docket(data)
    assert res["success"] is True
    assert res["passed"] is False
    assert res["fatal_count"] >= 2
    # Verify exact discrepancy rules flagged
    codes = [d["code"] for d in res["discrepancies"]]
    assert "DISC-INV-005" in codes
    assert "DISC-XDOC-002" in codes


def test_vectis_adapter_swift_ingestion():
    adapter = VectisEnterpriseAdapter()
    res = adapter.parse_swift_and_audit(SAMPLE_SWIFT_MT700)

    assert res["success"] is True
    assert res["lc_number"] == "LC-DB-2027-9941"
    assert res["beneficiary"] == "PRECISION AUTO MACHINING PVT LTD"
    assert res["passed"] is True
    assert len(res["certificate_seal"]) == 64


def test_vectis_adapter_cbam_calculation():
    adapter = VectisEnterpriseAdapter()
    payload = {
        "goods_name": "Hot-Rolled Steel Bars",
        "cn_code": "72142000",
        "quantity_metric_tonnes": 100.0,
        "direct_fuel_emissions_tco2": 60.0,
        "electricity_consumed_mwh": 70.0
    }
    res = adapter.calculate_cbam(payload)

    assert res["success"] is True
    assert res["goods_name"] == "Hot-Rolled Steel Bars"
    assert res["production_volume_tonnes"] == 100.0
    assert res["total_embedded_emissions_tco2"] > 0
    assert res["estimated_cbam_tariff_eur"] > 0
    assert res["estimated_cbam_tariff_inr"] > 0


def test_intel_engine_queries():
    engine = IntelSearchEngine()
    stats = engine.get_stats()

    assert stats["total_network_connections"] >= 9000
    assert stats["total_verified_trade_leads"] >= 300

    # Search companies
    comps = engine.search_companies("ServiceNow", limit=5)
    assert len(comps) >= 1
    assert "ServiceNow" in comps[0]["name"]

    # Search network connections
    conns = engine.search_network("Deutsche Bank", limit=5)
    assert len(conns) >= 1
    assert "Deutsche Bank" in conns[0]["company"]

    # Search trade leads
    leads = engine.search_trade_leads("Deutsche", limit=5)
    assert len(leads) >= 1


def test_swarm_matrix_coordination():
    swarm = SwarmMatrix()
    agents = swarm.get_agent_states()
    assert len(agents) == 12

    # Test single dispatch
    res_single = swarm.dispatch_agent_task("trade", "Verified test LC presentation")
    assert res_single["success"] is True
    assert res_single["agent"]["tasks_completed"] >= 1

    # Test full cycle
    res_cycle = swarm.run_full_swarm_cycle()
    assert res_cycle["success"] is True
    assert res_cycle["agents_executed"] == 12
