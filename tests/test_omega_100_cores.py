"""
Unit and Integration Tests for OMEGA INFINITY — 100-Core Sovereign Centurion Engine
Verifies that all 100 cores are instantiated, partitioned across 10 divisions,
validated for unique IDs, and that the ₹100 Crore enterprise financial model passes.
"""

import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_100_cores_engine import get_centurion_engine, Centurion100Engine, AutonomousCore


class TestOmega100CoresEngine:

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.engine = get_centurion_engine()

    def test_exact_100_cores_instantiated(self):
        """Must register exactly 100 distinct autonomous cores."""
        assert self.engine.get_total_core_count() == 100
        assert len(self.engine.cores) == 100

    def test_unique_sequential_core_ids(self):
        """Core IDs must run sequentially from CORE-001 through CORE-100 without duplicates."""
        core_ids = list(self.engine.cores.keys())
        assert len(core_ids) == len(set(core_ids)), "Core IDs must be strictly unique"

        for i in range(1, 101):
            expected_id = f"CORE-{i:03d}"
            assert expected_id in self.engine.cores, f"Missing {expected_id}"

    def test_10_divisions_with_10_cores_each(self):
        """Must have exactly 10 divisions, and each division must contain exactly 10 cores."""
        divisions = self.engine.get_division_breakdown()
        assert len(divisions) == 10, "Must have exactly 10 divisions"

        for div_id, div_data in divisions.items():
            assert div_data["core_count"] == 10, f"Division {div_id} must have exactly 10 cores"
            assert div_data["total_economic_value_crores"] > 0, f"Division {div_id} must have positive value"
            assert len(div_data["cores"]) == 10

    def test_100_crore_master_balance_sheet(self):
        """Consolidated annual run-rate must meet or exceed the ₹100 Crore milestone."""
        sheet = self.engine.compute_100_crore_master_balance_sheet()

        assert sheet["status"] == "SOVEREIGN_100_CRORE_MILESTONE_UNLOCKED"
        assert sheet["founder"] == "Aditya Mehra (Adi)"
        assert sheet["founder_equity_pct"] == 100.0
        assert sheet["total_autonomous_cores"] == 100
        assert sheet["target_achieved"] is True

        # Check values
        assert sheet["consolidated_annual_run_rate_crores"] >= 100.0, "Run rate must be >= 100 Cr"
        assert sheet["consolidated_annual_run_rate_usd"] > 10000000.0  # > $10M USD
        assert sheet["implied_enterprise_valuation_crores"] > 500.0    # > ₹500 Cr enterprise valuation
        assert sheet["surplus_over_100_crore_target_crores"] >= 0.0

    def test_full_centurion_diagnostic_sweep(self):
        """Diagnostic sweep across all 100 cores must achieve 100% operational status with zero errors."""
        sweep = self.engine.run_full_centurion_diagnostic_sweep()

        assert sweep["sweep_status"] == "ALL_100_CORES_OPERATIONAL"
        assert sweep["total_cores_audited"] == 100
        assert sweep["healthy_cores"] == 100
        assert sweep["failed_cores"] == 0
        assert sweep["constitutional_integrity_pct"] == 100.0

    def test_individual_core_telemetry_fidelity(self):
        """Inspect key milestone cores across different divisions."""
        # Core 011: Dark Store Velocity (380s -> 223s)
        c11 = self.engine.cores["CORE-011"]
        assert c11.code_name == "Velocity-380"
        assert c11.verified_kpis["cycle_time_sec"] == 223
        assert c11.verified_kpis["baseline_sec"] == 380

        # Core 012: CM2 Margin (+₹28.40)
        c12 = self.engine.cores["CORE-012"]
        assert c12.code_name == "Margin-CM2"
        assert c12.verified_kpis["cm2_surplus_inr"] == 28.40
        assert c12.verified_kpis["hubs_monitored"] == 14

        # Core 021: Cross-Border EXIM 40% BCD
        c21 = self.engine.cores["CORE-021"]
        assert c21.code_name == "Nexus-EXIM"
        assert c21.verified_kpis["hs_classification_accuracy"] == 99.8

        # Core 061: Aero India 2025 Protocol
        c61 = self.engine.cores["CORE-061"]
        assert c61.code_name == "Aero-Protocol"
        assert c61.verified_kpis["attendee_flow_daily"] == 15000

        # Core 071: GCC Radar (12,380 entities)
        c71 = self.engine.cores["CORE-071"]
        assert c71.code_name == "GCC-Radar"
        assert c71.verified_kpis["gcc_entities_tracked"] == 12380

        # Core 100: Planetary ASI Sovereign Compounding
        c100 = self.engine.cores["CORE-100"]
        assert c100.code_name == "Planetary-ASI"
        assert c100.verified_kpis["founder_equity_pct"] == 100.0
