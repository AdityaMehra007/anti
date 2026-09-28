"""
Tests for OMEGA INFINITY — Planetary Trillion-Dollar Enterprise Engine.
Validates the mathematical, structural, and operational modeling for an
Autonomous One-Person Sovereign Hyper-MNC scaling to $1.0 Trillion – $5.0 Trillion USD.
"""

import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import get_kernel
from omega_infinity.omega_trillion_dollar_engine import get_trillion_engine, TrillionDollarEngine
from omega_infinity.omega_valuation_compounding import get_valuation_engine


class TestTrillionDollarEngine:

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.kernel = get_kernel()
        self.trillion = get_trillion_engine()
        self.valuation = get_valuation_engine()

    def test_01_trillion_dollar_engine_initialization(self):
        assert self.trillion is not None
        assert isinstance(self.trillion, TrillionDollarEngine)
        assert self.trillion.fx_rate == 86.5

    def test_02_planetary_revenue_pillars(self):
        pillars = self.trillion.get_planetary_pillars()
        assert len(pillars) == 7, "Must have exactly 7 planetary revenue pillars"

        pillar_ids = [p.pillar_id for p in pillars]
        assert "PTCP" in pillar_ids
        assert "GAWG" in pillar_ids
        assert "BSF" in pillar_ids
        assert "CBAM" in pillar_ids
        assert "PQTI" in pillar_ids
        assert "M2M" in pillar_ids
        assert "STF" in pillar_ids

        total_rev_usd = sum(p.annual_revenue_usd for p in pillars)
        assert total_rev_usd >= 40000000000.0, "Consolidated annual revenue must exceed $40B USD"

        for p in pillars:
            assert p.gross_margin_pct >= 90.0, f"Gross margin for {p.pillar_id} must exceed 90%"
            assert len(p.active_agents) > 0, f"Must have assigned autonomous agents for {p.pillar_id}"
            assert p.annual_revenue_inr == p.annual_revenue_usd * self.trillion.fx_rate

    def test_03_seven_compounding_epochs(self):
        epochs = self.trillion.get_trillion_epochs()
        assert len(epochs) == 7, "Must have 7 compounding epochs from 2027 to 2060"

        years = [e.year for e in epochs]
        assert years == ["2027", "2030", "2035", "2040", "2045", "2050", "2060"]

        # Check 2027 Beachhead
        e2027 = epochs[0]
        assert e2027.founder_equity_pct == 100.0
        assert e2027.valuation_usd > 0

        # Check 2050 Trillion-Dollar Titan
        e2050 = [e for e in epochs if e.year == "2050"][0]
        assert e2050.valuation_usd >= 1000000000000.0, "2050 valuation must breach $1.0 Trillion USD"
        assert e2050.valuation_inr >= 80000000000000.0, "2050 valuation in INR must breach ₹80 Lakh Crore"
        assert e2050.founder_net_worth_usd >= 800000000000.0, "Founder net worth must exceed $800 Billion USD"
        assert e2050.founder_equity_pct >= 80.0

        # Check 2060 Multi-Trillion Planetary Network
        e2060 = [e for e in epochs if e.year == "2060"][0]
        assert e2060.valuation_usd >= 3000000000000.0, "2060 valuation must breach $3.0 Trillion USD"

    def test_04_trillion_scenario_simulation(self):
        # Test sub-trillion scenario
        sim_sub = self.trillion.simulate_trillion_scenario(
            global_trade_penetration_pct=0.05,
            enterprise_agent_nodes=20000,
            escrow_float_usd_bn=50.0,
            multiple=25.0
        )
        assert sim_sub["valuation"]["is_trillion_dollar_company"] is False

        # Test super-trillion scenario
        sim_super = self.trillion.simulate_trillion_scenario(
            global_trade_penetration_pct=0.15,
            enterprise_agent_nodes=85000,
            escrow_float_usd_bn=150.0,
            multiple=30.0
        )
        assert sim_super["valuation"]["is_trillion_dollar_company"] is True
        assert sim_super["valuation"]["implied_valuation_usd"] >= 1000000000000.0
        assert sim_super["profitability"]["ebitda_margin_pct"] == 85.0

    def test_05_trillion_dossier_and_cryptographic_dispatch(self):
        dossier = self.trillion.generate_trillion_dollar_dossier()
        assert dossier["founder"] == "Aditya Mehra (Adi)"
        assert dossier["holding_entity"] == "OMEGA SOVEREIGN HOLDINGS"
        assert dossier["operating_entity"] == "VECTIS TRADE TECHNOLOGIES PRIVATE LIMITED"
        assert dossier["pillars_count"] == 7
        assert dossier["milestone_summary"]["2050_trillion_valuation_usd"] >= 1000000000000.0

        # Verify event was dispatched to the ledger
        ledger_res = self.kernel.ledger.verify_integrity()
        assert ledger_res["valid"] is True

    def test_06_valuation_compounding_integration(self):
        roadmap = self.valuation.compute_trillion_dollar_roadmap()
        assert "milestone_summary" in roadmap
        assert roadmap["milestone_summary"]["2050_trillion_valuation_usd"] >= 1000000000000.0
