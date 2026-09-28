"""
Unit and Integration Tests for TITAN OS — The $1.0 Billion Enterprise Platform Engine.
Verifies the 4 commercial pillars, $1.0B - $3.2B valuation thresholds, growth milestones,
and founder equity preservation across all epochs.
"""

import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_billion_dollar_engine import (
    get_billion_dollar_engine,
    TitanBillionDollarEngine,
    UNICORN_VALUATION_USD
)


class TestTitanBillionDollarEngine:

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.engine = get_billion_dollar_engine()

    def test_unicorn_threshold_surpassed(self):
        """Must meet or exceed $1.0 Billion USD enterprise valuation."""
        res = self.engine.compute_billion_dollar_consolidation()
        assert res["unicorn_threshold_achieved"] is True
        assert res["conservative_valuation_usd"] >= UNICORN_VALUATION_USD
        assert res["benchmark_status"] == "UNICORN_SCALE_CONFIRMED"
        assert res["founder"] == "Aditya Mehra (Adi)"

    def test_four_commercial_pillars_integrity(self):
        """Verifies that all 4 commercial pillars are active with high gross margin."""
        res = self.engine.compute_billion_dollar_consolidation()
        assert res["total_commercial_pillars"] == 4
        assert res["fully_scaled_arr_usd"] == 320000000.0  # $320M ARR
        assert res["blended_gross_margin_pct"] >= 88.0    # Software gross margins >88%
        assert res["blended_nrr_pct"] >= 130.0            # Top-quartile SaaS retention >130%

    def test_milestone_epochs_and_equity_retention(self):
        """Verifies the progression through 2026, 2027, 2028, 2029 (Unicorn), and 2031 (Decacorn)."""
        milestones = self.engine.milestones
        assert len(milestones) == 5

        # Check Phase 4: $1.0B Unicorn Epoch
        unicorn_phase = milestones[3]
        assert unicorn_phase.target_year == "2029"
        assert unicorn_phase.implied_valuation_usd == 1000000000.0  # Exactly $1.0B USD
        assert unicorn_phase.founder_equity_pct >= 70.0             # Retaining majority founder equity
        assert unicorn_phase.founder_equity_value_usd >= 700000000.0 # $700M+ Founder Net Worth

        # Check Phase 5: $3.2B Decacorn
        decacorn_phase = milestones[4]
        assert decacorn_phase.target_year == "2031"
        assert decacorn_phase.implied_valuation_usd == 3200000000.0 # $3.2B USD
        assert decacorn_phase.founder_equity_value_usd > 2000000000.0 # $2.0B+ Founder Net Worth
