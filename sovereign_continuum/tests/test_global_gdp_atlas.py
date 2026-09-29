"""
Unit Tests for Global GDP Atlas and Planetary Balance Sheet.
"""

import pytest
from sovereign_continuum.global_gdp_atlas import GlobalGdpAtlas


def test_global_gdp_aggregates_and_shares():
    atlas = GlobalGdpAtlas()
    top_20_nominal = sum(c.nominal_gdp_t for c in atlas.TOP_20_ECONOMIES)
    
    # Top 20 economies make up over 80% of world nominal GDP
    share_of_world = (top_20_nominal / atlas.TOTAL_GLOBAL_GDP_NOMINAL_T) * 100.0
    assert share_of_world > 80.0
    assert atlas.TOTAL_GLOBAL_GDP_NOMINAL_T == 108.5
    assert atlas.TOTAL_GLOBAL_GDP_PPP_T == 185.0


def test_sector_decomposition_sums_to_100():
    atlas = GlobalGdpAtlas()
    total_pct = sum(s.share_of_global_gdp_pct for s in atlas.GLOBAL_SECTORS)
    assert pytest.approx(total_pct, 0.1) == 100.0

    total_value = sum(s.annual_gdp_t for s in atlas.GLOBAL_SECTORS)
    assert pytest.approx(total_value, 0.5) == atlas.TOTAL_GLOBAL_GDP_NOMINAL_T


def test_global_debt_pyramid():
    atlas = GlobalGdpAtlas()
    total_debt = sum(atlas.GLOBAL_DEBT_STACK.values())
    assert total_debt == atlas.TOTAL_GLOBAL_DEBT_T
    assert atlas.GLOBAL_DEBT_STACK["Sovereign / Government Debt"] == 94.0


def test_bloc_comparison():
    atlas = GlobalGdpAtlas()
    blocs = atlas.get_bloc_comparison()
    g7 = blocs["G7_Bloc"]
    brics = blocs["BRICS_Bloc_Core"]

    assert g7["nominal_gdp_t"] > 45.0  # G7 nominal > $45T
    assert brics["ppp_gdp_t"] > 50.0   # BRICS PPP > $50T
    assert g7["share_world_nominal_pct"] > 40.0
