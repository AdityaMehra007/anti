"""
OMEGA ∞ Mode H: Antifragile Red-Team & Chaos Engineering Harness
Rigorous stress-testing of Bengaluru's Top Flagship Systems under extreme simulated conditions:
- Multi-bank partition & 95% gateway drop rates (Razorpay HyperMesh)
- High-concurrency duplicate replay assault & Merkle integrity (SovereignLedger)
- Flash crash order book surge & circuit collar rejection (Zerodha NanoTrader)
- Planetary flash-sale stock exhaustion & linearizable lease locking (Flipkart TitanGrid)
- Mass courier blackout & severe urban delivery constraints (Swiggy SwarmPulse)
- Cryptographic proof tampering & forged credential detection (CRED VaultZero ZK)
- Orbital radiation noise & spectral band distortion recovery (Pixxel Aurora)
- Catastrophic grid frequency collapse & substation brownout defense (Ather GridMatrix)
- Split-brain 3-way UPI reconciliation drift isolation (PhonePe OmniLedger)
- API breaking change contract mutation defense (Postman APIMesh)
"""

import sys
import os
import random
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from projects.bangalore_top_500.razorpay_hypermesh.router import HyperMeshRouter
from projects.bangalore_top_500.razorpay_hypermesh.ledger import SovereignLedger
from projects.bangalore_top_500.phonepe_omniledger.reconciler import OmniReconciler
from projects.bangalore_top_500.zerodha_nanotrader.risk_engine import NanoRiskEngine
from projects.bangalore_top_500.flipkart_titangrid.fulfillment_mesh import TitanGridMesh
from projects.bangalore_top_500.swiggy_swarmpulse.swarm_router import SwarmPulseEngine, HyperlocalOrder
from projects.bangalore_top_500.cred_vaultzero.zk_vault import ZkVaultVerifier
from projects.bangalore_top_500.pixxel_aurora.hyperspectral_pipeline import HyperspectralProcessor
from projects.bangalore_top_500.ather_gridmatrix.v2g_telemetry import GridMatrixController
from projects.bangalore_top_500.postman_apimesh.contract_synth import ApiMeshSynthesizer


# ==============================================================================
# CHAOS TEST 1: Razorpay HyperMesh - Multi-Bank Catastrophic Partition Failover
# ==============================================================================
def test_hypermesh_catastrophic_partition_failover():
    router = HyperMeshRouter()
    router.register_gateway("HDFC", "gw_hdfc_01")
    router.register_gateway("ICICI", "gw_icici_01")
    router.register_gateway("SBI", "gw_sbi_01")

    # Prime all gateways with baseline traffic
    for _ in range(20):
        router.gateways["gw_hdfc_01"].record_attempt(True, 40.0)
        router.gateways["gw_icici_01"].record_attempt(True, 50.0)
        router.gateways["gw_sbi_01"].record_attempt(True, 70.0)

    # Initial state: HDFC is fastest preferred
    res1 = router.route_and_execute("TXN-CHAOS-001", 10000.0, preferred_bank="HDFC")
    assert res1["status"] == "ROUTED_SUCCESS"
    assert res1["selected_bank"] == "HDFC"

    # CHAOS INJECTION: 95% packet drop and 900ms latency spike in HDFC and ICICI
    for _ in range(50):
        router.gateways["gw_hdfc_01"].record_attempt(False, 900.0)
        router.gateways["gw_icici_01"].record_attempt(False, 950.0)
        router.gateways["gw_sbi_01"].record_attempt(True, 65.0)

    # Router must failover 100% of traffic to healthy SBI gateway even if user preferred HDFC
    res2 = router.route_and_execute("TXN-CHAOS-002", 10000.0, preferred_bank="HDFC")
    assert res2["status"] == "ROUTED_SUCCESS"
    assert res2["selected_bank"] == "SBI", "HyperMesh failed to switch away from degraded acquiring banks!"

    # CHAOS RECOVERY: ICICI restores ultra-low latency healthy state (flush failure window)
    for _ in range(120):
        router.gateways["gw_icici_01"].record_attempt(True, 20.0)

    # Now selecting optimal route without bank preference routes to recovered peak performer ICICI
    res3 = router.route_and_execute("TXN-CHAOS-003", 10000.0, preferred_bank=None)
    assert res3["status"] == "ROUTED_SUCCESS"
    assert res3["selected_bank"] == "ICICI", "HyperMesh failed to re-balance after bank network recovery!"


# ==============================================================================
# CHAOS TEST 2: SovereignLedger - Concurrency Replay Assault & Merkle Invariance
# ==============================================================================
def test_sovereign_ledger_concurrency_and_replay_assault():
    ledger = SovereignLedger()
    # Zero-sum balanced ledger state for strict double-entry verification
    ledger.accounts["acc_user_prime"] = 500_000_00   # ₹500,000.00
    ledger.accounts["acc_reserve"] = -500_000_00     # Offsetting reserve balance
    ledger.accounts["acc_merchant_alpha"] = 0

    idempotency_attack_key = "IDEMP-ATTACK-BURST-888999"
    amount_paisa = 10_000_00  # ₹10,000.00

    # CHAOS INJECTION: 50 duplicate requests arriving with identical idempotency key
    entries = []
    for i in range(50):
        entry = ledger.record_transfer(
            entry_id=f"tx_attempt_{i}",
            idempotency_key=idempotency_attack_key,
            debit_account="acc_user_prime",
            credit_account="acc_merchant_alpha",
            amount_paisa=amount_paisa
        )
        entries.append(entry)

    # Verify idempotency: exactly ONE real journal entry recorded
    assert len(ledger.entries) == 1, "Ledger allowed duplicate journal entries under replay assault!"
    assert ledger.get_balance("acc_user_prime") == 490_000_00
    assert ledger.get_balance("acc_merchant_alpha") == 10_000_00

    # Every one of the 50 calls returned the identical cryptographic entry
    for e in entries:
        assert e.entry_hash == entries[0].entry_hash

    # Merkle chain validation: zero-financial drift and valid hashes
    assert ledger.verify_integrity() is True

    # Invalid amount rejection
    with pytest.raises(ValueError):
        ledger.record_transfer("tx_invalid", "IDEMP-ERR", "acc_user_prime", "acc_merchant_alpha", -500)


# ==============================================================================
# CHAOS TEST 3: Zerodha NanoTrader - Flash Crash Volatility Burst & Circuit Limit
# ==============================================================================
def test_nanotrader_flash_crash_surge_and_circuit_rejection():
    risk = NanoRiskEngine()
    risk.register_client("TRADER_VIP_01", cash_inr=20000.0)  # ₹20,000
    # Security: RELIANCE with lower limit ₹2,700 and upper limit ₹3,300, LTP ₹3,000
    risk.set_circuit_bands("RELIANCE", lower_inr=2700.0, upper_inr=3300.0, ltp_inr=3000.0)

    # CHAOS INJECTION: Rapid orders submitted in microsecond succession
    # 1. Valid order within circuit limits and margin
    approved1, reason1, lat1 = risk.evaluate_order(
        client_id="TRADER_VIP_01",
        symbol="RELIANCE",
        side="BUY",
        qty=5,
        price_inr=3000.0
    )
    assert approved1 is True
    assert reason1 == "RISK_APPROVED"

    # 2. Flash Crash price breach below circuit band (₹2,500 < lower circuit ₹2,700)
    approved2, reason2, _ = risk.evaluate_order(
        client_id="TRADER_VIP_01",
        symbol="RELIANCE",
        side="BUY",
        qty=1,
        price_inr=2500.0
    )
    assert approved2 is False
    assert reason2 == "ERR_CIRCUIT_LIMIT_BREACHED"

    # 3. Wild surge price breach above circuit band (₹3,600 > upper circuit ₹3,300)
    approved3, reason3, _ = risk.evaluate_order(
        client_id="TRADER_VIP_01",
        symbol="RELIANCE",
        side="SELL",
        qty=1,
        price_inr=3600.0
    )
    assert approved3 is False
    assert reason3 == "ERR_CIRCUIT_LIMIT_BREACHED"

    # 4. Total margin exhaustion: buying ₹30,000 when only ₹5,000 remaining
    approved4, reason4, _ = risk.evaluate_order(
        client_id="TRADER_VIP_01",
        symbol="RELIANCE",
        side="BUY",
        qty=10,
        price_inr=3000.0
    )
    assert approved4 is False
    assert reason4 == "ERR_INSUFFICIENT_MARGIN"


# ==============================================================================
# CHAOS TEST 4: Flipkart TitanGrid - Planetary Flash-Sale Stock Depletion Mesh
# ==============================================================================
def test_titangrid_flash_sale_inventory_exhaustion():
    mesh = TitanGridMesh()
    sku = "IPHONE-16-PRO-MAX-1TB"
    mesh.add_stock(sku, "HUB-BLR-NORTH", "560001", qty=6)
    mesh.add_stock(sku, "HUB-BLR-SOUTH", "560100", qty=4)

    # CHAOS INJECTION: Flash-sale burst of 15 order reservations
    successful_reservations = []
    failed_reservations = []

    for i in range(15):
        hub_assigned = mesh.reserve_inventory_linearizable(
            order_id=f"BBD_ORDER_{i:03d}",
            sku=sku,
            customer_pin="560001",
            qty=1
        )
        if hub_assigned:
            successful_reservations.append((i, hub_assigned))
        else:
            failed_reservations.append(i)

    # Exactly 10 items should have been reserved across both hubs
    assert len(successful_reservations) == 10
    assert len(failed_reservations) == 5

    # First 6 should have gone to HUB-BLR-NORTH (regional affinity)
    north_count = sum(1 for _, h in successful_reservations if h == "HUB-BLR-NORTH")
    south_count = sum(1 for _, h in successful_reservations if h == "HUB-BLR-SOUTH")
    assert north_count == 6
    assert south_count == 4


# ==============================================================================
# CHAOS TEST 5: Swiggy SwarmPulse - Monsoon Courier Blackout & Capacity Caps
# ==============================================================================
def test_swarmpulse_monsoon_courier_blackout():
    engine = SwarmPulseEngine()

    # Register 10 delivery fleet riders across Koramangala
    for i in range(10):
        engine.register_rider(f"rider_{i:02d}", lat=12.935 + (i * 0.001), lng=77.620 + (i * 0.001))

    # CHAOS INJECTION: Severe flash rainstorm knocks 8 riders offline
    for i in range(8):
        engine.riders[f"rider_{i:02d}"].is_available = False

    # Surge of 10 hyperlocal quick-commerce orders from DarkStore Koramangala
    orders = [
        HyperlocalOrder(
            order_id=f"instamart_order_{j}",
            darkstore_id="DS_KORAMANGALA_01",
            customer_lat=12.936 + (j * 0.002),
            customer_lng=77.621 + (j * 0.002)
        )
        for j in range(10)
    ]

    assignments = engine.find_optimal_batch(
        darkstore_lat=12.9352,
        darkstore_lng=77.6245,
        orders=orders
    )

    # Only 2 riders are active. Max capacity per rider is 3. Total assigned <= 6.
    total_assigned_orders = sum(len(order_list) for order_list in assignments.values())
    assert total_assigned_orders == 6, f"SwarmPulse violated capacity caps: assigned {total_assigned_orders}"

    for r_id, assigned_list in assignments.items():
        assert len(assigned_list) <= 3, f"Rider {r_id} overloaded beyond max capacity 3!"
        assert engine.riders[r_id].is_available is True


# ==============================================================================
# CHAOS TEST 6: CRED VaultZero - Cryptographic Tampering & Forgery Resistance
# ==============================================================================
def test_vaultzero_zk_signature_tampering_and_forgery():
    zk = ZkVaultVerifier("CRED_SOVEREIGN_ENCLAVE_KEY_CHAOS")

    # Legitimate credit evaluation
    legit_token_premium = zk.create_credit_commitment("USER_CHETAN_790", credit_score=810, annual_income_lakhs=45.0)
    legit_token_standard = zk.create_credit_commitment("USER_PRIYA_760", credit_score=765, annual_income_lakhs=28.0)

    # Valid proof verifications
    assert zk.verify_proof("USER_CHETAN_790", legit_token_premium, claimed_tier="PREMIUM") is True
    assert zk.verify_proof("USER_PRIYA_760", legit_token_standard, claimed_tier="STANDARD") is True

    # CHAOS INJECTION 1: Bitflip attack - mutate 1 character in the SHA256 hex proof
    tampered_token = ("0" if legit_token_premium[0] != "0" else "1") + legit_token_premium[1:]
    assert zk.verify_proof("USER_CHETAN_790", tampered_token, claimed_tier="PREMIUM") is False

    # CHAOS INJECTION 2: Identity hijacking - use Chetan's proof for Rahul
    assert zk.verify_proof("USER_ATTACKER_999", legit_token_premium, claimed_tier="PREMIUM") is False

    # CHAOS INJECTION 3: Privilege escalation - claim PREMIUM tier using STANDARD proof
    assert zk.verify_proof("USER_PRIYA_760", legit_token_standard, claimed_tier="PREMIUM") is False


# ==============================================================================
# CHAOS TEST 7: Pixxel Aurora - Orbital Radiation Noise & Methane Plume Isolation
# ==============================================================================
def test_pixxel_aurora_radiation_bitflip_and_spectral_noise():
    processor = HyperspectralProcessor(num_bands=300)

    # Baseline 300 spectral bands (atmosphere background)
    baseline = [0.85] * 300
    # True methane plume: sharp absorption drop in SWIR bands 210-240 (~0.40)
    raw_plume = [0.85] * 300
    for b in range(210, 240):
        raw_plume[b] = 0.45  # absorption dip ~0.40

    # CHAOS INJECTION: Inject random space radiation noise across all spectral channels (+/- 0.04)
    random.seed(42)
    noisy_plume = [val + random.uniform(-0.04, 0.04) for val in raw_plume]

    # Process noisy signature
    res = processor.detect_methane_plume(noisy_plume, baseline)
    assert res["methane_detected"] is True
    assert res["confidence_score"] > 0.85

    # False positive test: pure random noise without genuine SWIR absorption
    noisy_background = [val + random.uniform(-0.06, 0.06) for val in baseline]
    false_res = processor.detect_methane_plume(noisy_background, baseline)
    assert false_res["methane_detected"] is False


# ==============================================================================
# CHAOS TEST 8: Ather GridMatrix - Severe Grid Frequency Collapse & Brownout
# ==============================================================================
def test_ather_gridmatrix_catastrophic_frequency_collapse():
    controller = GridMatrixController(substation_capacity_kw=100.0)

    # Register 4 charging pods with 25kW capacity each (Total = 100 kW demand)
    for i in range(4):
        pod_id = f"POD_ATHER_{i}"
        controller.register_pod(pod_id, max_kw=25.0)
        controller.pods[pod_id].connected_vehicle_id = f"ATHER_450X_{i}"
        controller.pods[pod_id].battery_soc_pct = 50.0  # normal SoC

    # Nominal grid frequency (50.0 Hz)
    controller.optimize_load(grid_frequency_hz=50.0)
    total_nominal_kw = sum(p.current_kw for p in controller.pods.values())
    # Under 50Hz, boost = 0.9, each pod = 25 * 1.0 * 0.9 = 22.5 kW -> total = 90 kW <= 100 kW
    assert total_nominal_kw <= controller.capacity_kw

    # CHAOS INJECTION: Severe frequency collapse to 48.2 Hz (< 49.8 Hz critical brownout)
    controller.optimize_load(grid_frequency_hz=48.2)
    total_emergency_kw = sum(p.current_kw for p in controller.pods.values())

    # Throttling by scale_factor=0.5 must occur to prevent transformer failure
    # Each pod: 25.0 * 0.5 * 0.9 = 11.25 kW -> total = 45.0 kW
    assert total_emergency_kw <= 50.0, f"GridMatrix failed to shed load: {total_emergency_kw} kW"
    assert total_emergency_kw < total_nominal_kw


# ==============================================================================
# CHAOS TEST 9: PhonePe OmniLedger - 3-Way UPI Split-Brain Drift Isolation
# ==============================================================================
def test_omniledger_upi_split_brain_drift():
    reconciler = OmniReconciler()

    # Ingest 100 synchronized transactions
    for i in range(100):
        rrn = f"UPI_RRN_{i:06d}"
        reconciler.ingest_phonepe_event(rrn, amount_inr=500.0, status="SUCCESS")
        reconciler.ingest_bank_clearing(rrn, amount_inr=500.0, status="SUCCESS")
        reconciler.records[rrn].merchant_status = "CREDITED"

    # CHAOS INJECTION: 10 split-brain network partition anomalies
    for j in range(100, 110):
        rrn_chaos = f"UPI_RRN_CHAOS_{j}"
        reconciler.ingest_phonepe_event(rrn_chaos, amount_inr=1500.0, status="TIMEOUT")
        reconciler.ingest_bank_clearing(rrn_chaos, amount_inr=1500.0, status="SUCCESS")
        reconciler.records[rrn_chaos].merchant_status = "PENDING"

    matched, discrepancies = reconciler.reconcile_all()

    assert len(matched) == 100
    assert len(discrepancies) == 10
    assert "UPI_RRN_CHAOS_105" in discrepancies


# ==============================================================================
# CHAOS TEST 10: Postman APIMesh - Breaking Schema Mutation Shield
# ==============================================================================
def test_apimesh_breaking_schema_divergence():
    synth = ApiMeshSynthesizer()
    synth.register_endpoint(
        path="/v1/payments/instant-settle",
        method="POST",
        required_params=["merchant_id", "amount_paisa", "token"],
        schema_version=1
    )

    # Backward compatible update (non-breaking): same required parameters
    is_breaking_1, added_1 = synth.check_breaking_changes(
        path="/v1/payments/instant-settle",
        method="POST",
        new_required_params=["merchant_id", "amount_paisa", "token"]
    )
    assert is_breaking_1 is False
    assert len(added_1) == 0

    # CHAOS INJECTION: Upstream developer introduces breaking change: newly added required parameter
    is_breaking_2, added_2 = synth.check_breaking_changes(
        path="/v1/payments/instant-settle",
        method="POST",
        new_required_params=["merchant_id", "amount_paisa", "token", "kyc_regulatory_aadhaar_hash"]
    )
    assert is_breaking_2 is True
    assert "kyc_regulatory_aadhaar_hash" in added_2
