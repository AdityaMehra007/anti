"""
Unit & Integration Tests for OMEGA Global Markets & EXIM Nexus FastAPI Server
"""
import pytest
from fastapi.testclient import TestClient
from projects.omega_global_markets_nexus.api.server import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_get_market_snapshot():
    response = client.get("/api/market/snapshot")
    assert response.status_code == 200
    data = response.json()
    assert "equities" in data
    assert "money_market" in data
    assert "yield_ladder" in data
    assert "fx_rates" in data


def test_get_business_archetypes():
    response = client.get("/api/business/archetypes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    assert data[0]["moat_score"] > 80.0


def test_dcf_endpoint():
    payload = {
        "archetype_index": 0,
        "wacc": 0.09,
        "terminal_growth": 0.035,
        "projected_cagr": 0.15
    }
    response = client.post("/api/business/dcf", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["enterprise_value_bn"] > 100.0


def test_stock_orderbook_and_order_placement():
    # 1. Fetch depth
    res = client.get("/api/stock/orderbook")
    assert res.status_code == 200
    depth = res.json()
    assert depth["best_bid"] is not None
    assert depth["best_ask"] is not None

    # 2. Place limit buy order
    order_payload = {
        "side": "BUY",
        "order_type": "LIMIT",
        "price": 125.00,
        "quantity": 200
    }
    res_order = client.post("/api/stock/order", json=order_payload)
    assert res_order.status_code == 200
    order_data = res_order.json()
    assert "order_id" in order_data
    assert "depth" in order_data


def test_money_sweep_endpoint():
    payload = {
        "total_cash_usd": 30_000_000.0,
        "buffer_usd": 5_000_000.0
    }
    response = client.post("/api/money/sweep", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["overnight_operational_cash"] == 5_000_000.0
    assert data["weighted_blended_yield_pct"] > 3.0


def test_bond_curve_and_price_impact():
    res_curve = client.get("/api/bond/curve")
    assert res_curve.status_code == 200
    curve_data = res_curve.json()
    assert "ladder" in curve_data

    payload_impact = {
        "coupon_pct": 5.5,
        "maturity_years": 10.0,
        "current_ytm_pct": 5.0,
        "yield_shift_bps": 50.0
    }
    res_impact = client.post("/api/bond/price-impact", json=payload_impact)
    assert res_impact.status_code == 200
    impact_data = res_impact.json()
    assert "sensitivities" in impact_data


def test_exim_customs_and_lc_audit():
    res_tariff = client.post("/api/exim/tariff", json={
        "hs_code": "8471.50.00",
        "fob_usd": 500_000.0,
        "freight_usd": 10_000.0,
        "insurance_usd": 2_000.0,
        "fx_rate": 85.0
    })
    assert res_tariff.status_code == 200
    assert res_tariff.json()["total_landed_cost"] > 0

    res_lc = client.post("/api/exim/lc-audit", json={
        "lc_amount_usd": 512_000.0,
        "tolerance_pct": 5.0,
        "latest_shipment_date": "2026-11-15",
        "expiry_date": "2026-12-31",
        "presentation_date": "2026-10-21",
        "invoice_amount_usd": 512_000.0,
        "shipped_date": "2026-10-18",
        "is_clean_on_board": True,
        "port_of_loading": "Port of Los Angeles",
        "port_of_discharge": "Nhava Sheva JNPT"
    })
    assert res_lc.status_code == 200
    assert res_lc.json()["is_compliant"] is True


def test_macro_cycle_and_ledger():
    res_cycle = client.post("/api/macro/cycle", json={
        "archetype_index": 0,
        "trade_units": 200,
        "unit_price_usd": 35_000.0,
        "treasury_cash_pool_usd": 40_000_000.0,
        "equity_portfolio_capital_usd": 20_000_000.0
    })
    assert res_cycle.status_code == 200
    cycle_data = res_cycle.json()
    assert "cycle_id" in cycle_data
    assert "nexus_macro_verdict" in cycle_data

    res_ledger = client.get("/api/ledger/history")
    assert res_ledger.status_code == 200
    assert res_ledger.json()["metrics"]["total_macro_cycles_recorded"] > 0


def test_derivatives_endpoints():
    res_opt = client.post("/api/derivatives/option-price", json={
        "spot": 125.0,
        "strike": 125.0,
        "maturity_years": 0.5,
        "risk_free_rate": 0.045,
        "volatility": 0.25,
        "option_type": "CALL"
    })
    assert res_opt.status_code == 200
    assert res_opt.json()["price"] > 0
    assert res_opt.json()["delta"] > 0

    res_iv = client.post("/api/derivatives/implied-vol", json={
        "target_price": 9.50,
        "spot": 125.0,
        "strike": 125.0,
        "maturity_years": 0.5,
        "risk_free_rate": 0.045,
        "option_type": "CALL"
    })
    assert res_iv.status_code == 200
    assert res_iv.json()["solved_implied_volatility"] > 0

    res_irs = client.post("/api/derivatives/irs-valuation", json={
        "notional_usd": 25_000_000.0,
        "tenor_years": 5,
        "fixed_rate_pct": 4.50,
        "floating_sofr_benchmark_pct": 5.30
    })
    assert res_irs.status_code == 200
    assert "par_swap_rate_pct" in res_irs.json()

    res_ffa = client.post("/api/derivatives/ffa-hedge", json={
        "spot_freight_teu": 2400.0,
        "forward_locked_rate_teu": 2500.0,
        "volume_teu": 100,
        "settlement_spot_teu": 3000.0
    })
    assert res_ffa.status_code == 200
    assert res_ffa.json()["ffa_hedging_pnl_usd"] == 50_000.0


def test_logistics_endpoints():
    res_routes = client.get("/api/logistics/routes")
    assert res_routes.status_code == 200
    assert "ASIA_EUROPE_SUEZ" in res_routes.json()

    res_disrupt = client.get("/api/logistics/chokepoint-disruption")
    assert res_disrupt.status_code == 200
    assert res_disrupt.json()["status"] == "DISRUPTED_REROUTING_REQUIRED"

    res_demurrage = client.post("/api/logistics/demurrage", json={
        "teu_containers": 50,
        "port_delay_days": 8,
        "free_days_allowed": 5
    })
    assert res_demurrage.status_code == 200
    assert res_demurrage.json()["chargeable_days"] == 3


def test_stress_endpoints():
    res_det = client.post("/api/stress/deterministic", json={
        "scenario": "GFC_2008",
        "equities_usd": 25_000_000.0,
        "bonds_usd": 16_000_000.0,
        "cash_usd": 18_000_000.0,
        "trade_usd": 13_000_000.0
    })
    assert res_det.status_code == 200
    assert res_det.json()["dollar_loss_usd"] > 0

    res_mc = client.post("/api/stress/monte-carlo", json={
        "num_simulations": 300,
        "horizon_days": 30,
        "equities_usd": 25_000_000.0,
        "bonds_usd": 16_000_000.0,
        "cash_usd": 18_000_000.0,
        "trade_usd": 13_000_000.0
    })
    assert res_mc.status_code == 200
    assert res_mc.json()["mc_var_99_usd"] > 0
