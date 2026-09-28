"""
OMEGA INFINITY (Ω-OS) — PLANETARY WORLD GDP, AGI/ASI LEVELS & POWERS TEST SUITE
Verifies mathematical macroeconomic coherence, 6-level machine intelligence taxonomy,
8 sovereign superpowers, and cryptographic Merkle ledger dispatch.
"""

import os
import sys
import json
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_planetary_gdp_asi_engine import (
    get_planetary_gdp_asi_engine,
    PlanetaryGdpAsiEngine,
    WorldGdpEpoch,
    IntelligenceLevel,
    SovereignPower
)


class TestPlanetaryGdpAsiEngine:

    @pytest.fixture(autouse=True)
    def setup_engine(self):
        self.engine = get_planetary_gdp_asi_engine()

    def test_01_engine_initialization_and_trajectory(self):
        trajectory = self.engine.get_world_gdp_trajectory()
        assert len(trajectory) >= 10, "Expected at least 10 macroeconomic epochs from 1990 to 2060."
        
        years = [e.year for e in trajectory]
        assert 1990 in years
        assert 2026 in years
        assert 2030 in years
        assert 2050 in years
        assert 2060 in years

        # Check chronological order
        assert years == sorted(years)

        # Verify 2026 present baseline
        epoch_2026 = next(e for e in trajectory if e.year == 2026)
        assert epoch_2026.world_gdp_nominal_usd_trillion >= 100.0
        assert epoch_2026.ai_contribution_pct > 0.0
        assert epoch_2026.omega_valuation_usd == 1700000.0

        # Verify 2050 Planetary Titan
        epoch_2050 = next(e for e in trajectory if e.year == 2050)
        assert epoch_2050.world_gdp_nominal_usd_trillion >= 500.0
        assert epoch_2050.ai_contribution_pct >= 75.0
        assert epoch_2050.omega_valuation_usd == 1020000000000.0  # $1.02 Trillion

        # Verify 2060 Solar Singularity Grid
        epoch_2060 = next(e for e in trajectory if e.year == 2060)
        assert epoch_2060.world_gdp_nominal_usd_trillion >= 1000.0  # $1.0 Quadrillion
        assert epoch_2060.omega_valuation_usd == 3600000000000.0  # $3.60 Trillion

    def test_02_intelligence_levels_hierarchy(self):
        levels = self.engine.get_intelligence_levels()
        assert len(levels) == 6, "Expected exactly 6 levels (Level 0 through Level 5)."

        expected_codes = ["LEVEL-0", "LEVEL-1", "LEVEL-2", "LEVEL-3", "LEVEL-4", "LEVEL-5"]
        actual_codes = [lvl.level_code for lvl in levels]
        assert actual_codes == expected_codes

        # Verify autonomy progression
        autonomies = [lvl.autonomy_index_pct for lvl in levels]
        assert autonomies == sorted(autonomies), "Autonomy index must strictly increase across levels."
        assert levels[0].autonomy_index_pct == 5.0
        assert levels[-1].autonomy_index_pct == 100.0

        # Verify Level 3 is OMEGA deployed operational baseline
        level_3 = levels[3]
        assert "DEPLOYED" in level_3.omega_implementation_status
        assert "24 Specialized Agents" in level_3.omega_implementation_status

        # Verify Level 5 (ASI)
        level_5 = levels[5]
        assert "Recursive" in level_5.cognitive_definition or "self-improving" in level_5.cognitive_definition
        assert len(level_5.core_capabilities) >= 3

    def test_03_sovereign_powers_matrix(self):
        powers = self.engine.get_sovereignty_powers()
        assert len(powers) == 8, "Expected 8 sovereign superpowers in the OMEGA powers matrix."

        power_ids = [p.power_id for p in powers]
        expected_ids = [f"POW-{i}" for i in range(1, 9)]
        assert power_ids == expected_ids

        # Verify POW-8 is Constitutional Sovereign Human Alignment to Aditya Mehra
        pow_8 = next(p for p in powers if p.power_id == "POW-8")
        assert "Aditya Mehra" in pow_8.description
        assert "Founder Equity" in pow_8.omega_sovereign_leverage

        # Verify POW-2 Float Yield
        pow_2 = next(p for p in powers if p.power_id == "POW-2")
        assert "Berkshire" in pow_2.name or "Berkshire" in pow_2.description
        assert "float" in pow_2.description.lower()

    def test_04_asi_gdp_simulation(self):
        # Default 2050 simulation
        sim_2050 = self.engine.simulate_asi_gdp_impact(year=2050)
        assert sim_2050["world_gdp_nominal_usd_trillion"] == 550.0
        assert sim_2050["ai_penetration_pct"] == 80.0
        assert sim_2050["ai_economic_value_usd_trillion"] == 440.0
        assert sim_2050["status"] == "PLANETARY ASI SCALE VERIFIED"
        assert sim_2050["founder_equity_pct"] == 85.0
        assert sim_2050["founder_net_worth_usd"] > 800000000000.0  # > $800B

        # Custom simulation: $700T GDP, 25 bps capture, 30x multiple
        sim_custom = self.engine.simulate_asi_gdp_impact(
            year=2055,
            custom_world_gdp_trillion=700.0,
            ai_penetration_pct=85.0,
            omega_gdp_capture_bps=25.0,
            valuation_multiple=30.0
        )
        assert sim_custom["world_gdp_nominal_usd_trillion"] == 700.0
        assert sim_custom["omega_enterprise_valuation_usd"] == (700.0 * 1e12) * (25.0 / 10000.0)
        assert "$1.75 Trillion" in sim_custom["omega_enterprise_valuation_usd_formatted"]

    def test_05_dossier_generation_and_cryptographic_ledger(self):
        dossier = self.engine.generate_asi_gdp_dossier()
        assert "dossier_id" in dossier
        assert dossier["founder"] == "Aditya Mehra (Adi)"
        assert len(dossier["world_gdp_trajectory"]) >= 10
        assert len(dossier["intelligence_levels"]) == 6
        assert len(dossier["sovereignty_powers"]) == 8

        # Verify file existence on disk
        dossier_path = os.path.join(REPO_ROOT, "omega", "data", "planetary_gdp_asi_dossier.json")
        assert os.path.exists(dossier_path)

        with open(dossier_path, "r", encoding="utf-8") as f:
            saved = json.load(f)
        assert saved["dossier_id"] == dossier["dossier_id"]

        # Verify cryptographic ledger event
        ledger_stat = self.engine.kernel.ledger.verify_integrity()
        assert ledger_stat["valid"] is True
        assert ledger_stat["total_blocks"] > 0

    def test_06_macroeconomic_production_coherence(self):
        trajectory = self.engine.get_world_gdp_trajectory()
        for epoch in trajectory:
            # AI economic value must equal world_gdp * ai_contribution_pct / 100
            expected_ai_val = epoch.world_gdp_nominal_usd_trillion * (epoch.ai_contribution_pct / 100.0)
            assert abs(epoch.ai_value_usd_trillion - expected_ai_val) < 0.05
            # OMEGA share of World GDP must not exceed 1.0% in any epoch
            assert epoch.omega_world_gdp_share_pct <= 1.0
