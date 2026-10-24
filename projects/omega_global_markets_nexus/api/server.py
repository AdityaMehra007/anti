"""
FastAPI Enterprise Application for OMEGA Global Markets & EXIM Nexus
Exposes high-performance REST endpoints for all 5 pillars and serves the interactive Cockpit.
"""
import asyncio
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from projects.omega_global_markets_nexus.core.business_empire import (
    GlobalBusinessEmpireCatalog, EnterpriseArchetype
)
from projects.omega_global_markets_nexus.core.stock_market_engine import (
    LimitOrderBook, Order, OrderSide, OrderType, PortfolioRiskOptimizer
)
from projects.omega_global_markets_nexus.core.money_market_engine import (
    TreasuryCashSweepDesk, Basel3LiquidityAuditor, TBillInstrument
)
from projects.omega_global_markets_nexus.core.bond_market_engine import (
    NelsonSiegelCurve, FixedCouponBond, CorporateCreditSpreadAnalyzer
)
from projects.omega_global_markets_nexus.core.global_exim_engine import (
    GlobalEximEngine, TradeContract, Incoterm, LetterOfCreditSpec, ShippingDocuments
)
from projects.omega_global_markets_nexus.core.derivatives_engine import (
    BlackScholesEngine, OptionType, InterestRateSwapContract, FreightForwardAgreementPricer
)
from projects.omega_global_markets_nexus.core.supply_chain_optimizer import (
    MaritimeSupplyChainOptimizer, Chokepoint
)
from projects.omega_global_markets_nexus.core.monte_carlo_stress_engine import (
    MonteCarloStressEngine, StressScenario, EnterpriseBalanceSheet
)
from projects.omega_global_markets_nexus.core.nexus_orchestrator import OmegaNexusOrchestrator
from projects.omega_global_markets_nexus.data_feeds.market_data_service import MarketDataService
from projects.omega_global_markets_nexus.daemon.autonomous_nexus_daemon import NexusAuditLedger

# Initialize App & Services
app = FastAPI(
    title="OMEGA ∞ Global Markets & EXIM Nexus API",
    version="24.0.0",
    description="Institutional API for Global Business Strategy, Stock Quant, Money Markets, Bond Curves, and EXIM Trade Finance."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared in-memory state & engines
market_data = MarketDataService()
orchestrator = OmegaNexusOrchestrator()
order_book = LimitOrderBook(symbol="OMEGA-GLOBAL")
ledger = NexusAuditLedger()

# Seed order book with initial depth
order_book.add_order(Order(order_id="SEED-A1", symbol="OMEGA-GLOBAL", side=OrderSide.SELL, order_type=OrderType.LIMIT, price=125.10, quantity=900))
order_book.add_order(Order(order_id="SEED-A2", symbol="OMEGA-GLOBAL", side=OrderSide.SELL, order_type=OrderType.LIMIT, price=125.20, quantity=1850))
order_book.add_order(Order(order_id="SEED-A3", symbol="OMEGA-GLOBAL", side=OrderSide.SELL, order_type=OrderType.LIMIT, price=125.30, quantity=2400))
order_book.add_order(Order(order_id="SEED-B1", symbol="OMEGA-GLOBAL", side=OrderSide.BUY, order_type=OrderType.LIMIT, price=124.90, quantity=1200))
order_book.add_order(Order(order_id="SEED-B2", symbol="OMEGA-GLOBAL", side=OrderSide.BUY, order_type=OrderType.LIMIT, price=124.80, quantity=2100))
order_book.add_order(Order(order_id="SEED-B3", symbol="OMEGA-GLOBAL", side=OrderSide.BUY, order_type=OrderType.LIMIT, price=124.70, quantity=3500))


# --- Pydantic Request Models ---
class DCFRequest(BaseModel):
    archetype_index: int = 0
    wacc: float = 0.09
    terminal_growth: float = 0.035
    projected_cagr: float = 0.15

class OrderPlacementRequest(BaseModel):
    side: str  # "BUY" or "SELL"
    order_type: str = "LIMIT"  # "LIMIT" or "MARKET"
    price: float
    quantity: int

class CashSweepRequest(BaseModel):
    total_cash_usd: float = 50_000_000.0
    buffer_usd: float = 5_000_000.0

class BondSensitivitiesRequest(BaseModel):
    coupon_pct: float = 5.50
    maturity_years: float = 10.0
    current_ytm_pct: float = 5.0
    yield_shift_bps: float = 100.0

class CustomsDutyRequest(BaseModel):
    hs_code: str = "8471.50.00"
    fob_usd: float = 1_000_000.0
    freight_usd: float = 15_000.0
    insurance_usd: float = 5_000.0
    fx_rate: float = 85.0

class LCAuditRequest(BaseModel):
    lc_amount_usd: float = 1_020_000.0
    tolerance_pct: float = 5.0
    latest_shipment_date: str = "2026-11-15"
    expiry_date: str = "2026-12-31"
    presentation_date: str = "2026-10-21"
    invoice_amount_usd: float = 1_020_000.0
    shipped_date: str = "2026-10-18"
    is_clean_on_board: bool = True
    port_of_loading: str = "Port of Los Angeles"
    port_of_discharge: str = "Nhava Sheva JNPT"

class MacroCycleRequest(BaseModel):
    archetype_index: int = 0
    trade_units: int = 500
    unit_price_usd: float = 40_000.0
    treasury_cash_pool_usd: float = 50_000_000.0
    equity_portfolio_capital_usd: float = 25_000_000.0

class OptionPricingRequest(BaseModel):
    spot: float = 125.0
    strike: float = 125.0
    maturity_years: float = 0.5
    risk_free_rate: float = 0.045
    volatility: float = 0.25
    option_type: str = "CALL"

class ImpliedVolRequest(BaseModel):
    target_price: float = 7.50
    spot: float = 125.0
    strike: float = 125.0
    maturity_years: float = 0.5
    risk_free_rate: float = 0.045
    option_type: str = "CALL"

class IRSRequest(BaseModel):
    notional_usd: float = 50_000_000.0
    tenor_years: int = 5
    fixed_rate_pct: float = 4.25
    floating_sofr_benchmark_pct: float = 5.30

class FFAHedgeRequest(BaseModel):
    spot_freight_teu: float = 2400.0
    forward_locked_rate_teu: float = 2500.0
    volume_teu: int = 200
    settlement_spot_teu: float = 3100.0

class DemurrageRequest(BaseModel):
    teu_containers: int = 150
    port_delay_days: int = 9
    free_days_allowed: int = 5

class DeterministicStressRequest(BaseModel):
    scenario: str = "GFC_2008"  # "STAGFLATION_1970", "GFC_2008", "SUPPLY_2020", "SANCTIONS"
    equities_usd: float = 25_000_000.0
    bonds_usd: float = 16_000_000.0
    cash_usd: float = 18_000_000.0
    trade_usd: float = 13_000_000.0

class MonteCarloRequest(BaseModel):
    num_simulations: int = 2000
    horizon_days: int = 30
    equities_usd: float = 25_000_000.0
    bonds_usd: float = 16_000_000.0
    cash_usd: float = 18_000_000.0
    trade_usd: float = 13_000_000.0


# --- Endpoints ---

@app.get("/", response_class=HTMLResponse)
def serve_cockpit_ui():
    cockpit_path = REPO_ROOT / "projects" / "omega_global_markets_nexus" / "cockpit" / "GLOBAL_MARKETS_EXIM_COMMAND_CENTER.html"
    if cockpit_path.exists():
        return FileResponse(cockpit_path)
    return "<h1>OMEGA Global Markets Cockpit file not found</h1>"

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "OMEGA Global Markets & EXIM Nexus",
        "version": "24.0.0",
        "ledger_metrics": ledger.get_ledger_metrics()
    }

@app.get("/api/market/snapshot")
def get_market_snapshot():
    return market_data.get_unified_market_snapshot()

@app.get("/api/business/archetypes")
def get_business_archetypes():
    catalog = GlobalBusinessEmpireCatalog.get_tier_one_archetypes()
    output = []
    for arch in catalog:
        dcf = arch.calculate_dcf_valuation()
        output.append({
            "name": arch.name,
            "category": arch.category.value,
            "benchmark_peers": arch.benchmark_peers,
            "description": arch.description,
            "moat_score": arch.moat.composite_score,
            "pricing_power": arch.pricing_power_index,
            "financials": arch.financials.__dict__,
            "annual_fcf_bn": arch.financials.free_cash_flow_usd_bn,
            "implied_enterprise_value_bn": dcf["enterprise_value_bn"],
            "implied_multiple": dcf["implied_fcf_multiple"]
        })
    return output

@app.post("/api/business/dcf")
def compute_custom_dcf(req: DCFRequest):
    catalog = GlobalBusinessEmpireCatalog.get_tier_one_archetypes()
    if req.archetype_index < 0 or req.archetype_index >= len(catalog):
        raise HTTPException(status_code=400, detail="Invalid archetype index")
    arch = catalog[req.archetype_index]
    return arch.calculate_dcf_valuation(
        wacc=req.wacc,
        terminal_growth=req.terminal_growth,
        projected_5yr_cagr=req.projected_cagr
    )

@app.get("/api/stock/orderbook")
def get_order_book_depth():
    return order_book.get_order_book_depth()

@app.post("/api/stock/order")
def place_order(req: OrderPlacementRequest):
    side = OrderSide.BUY if req.side.upper() == "BUY" else OrderSide.SELL
    order_type = OrderType.LIMIT if req.order_type.upper() == "LIMIT" else OrderType.MARKET
    order = Order(
        order_id=f"ORD-{int(time.time() * 1000)}",
        symbol="OMEGA-GLOBAL",
        side=side,
        order_type=order_type,
        price=req.price,
        quantity=req.quantity
    )
    fills = order_book.add_order(order)
    return {
        "order_id": order.order_id,
        "remaining_quantity": order.remaining_quantity,
        "filled_quantity": order.filled_quantity,
        "fills": [f.__dict__ for f in fills],
        "depth": order_book.get_order_book_depth()
    }

@app.post("/api/money/sweep")
def simulate_cash_sweep(req: CashSweepRequest):
    res = TreasuryCashSweepDesk.execute_sweep(
        total_cash_usd=req.total_cash_usd,
        overnight_buffer_target_usd=req.buffer_usd
    )
    ledger.record_cash_sweep(res)
    return res

@app.get("/api/bond/curve")
def get_yield_curve(beta0: float = 0.048, beta1: float = -0.012, beta2: float = 0.015, tau: float = 2.5):
    curve = NelsonSiegelCurve(beta_0=beta0, beta_1=beta1, beta_2=beta2, tau=tau)
    ladder = curve.generate_tenor_ladder()
    inversion = curve.check_curve_inversion()
    return {
        "parameters": {"beta0": beta0, "beta1": beta1, "beta2": beta2, "tau": tau},
        "ladder": ladder,
        "inversion_check": inversion
    }

@app.post("/api/bond/price-impact")
def compute_bond_price_impact(req: BondSensitivitiesRequest):
    bond = FixedCouponBond(
        cusip="US-BND-API",
        issuer="Apex Sovereign Corp",
        par_value=1_000.0,
        coupon_rate_pct=req.coupon_pct,
        maturity_years=req.maturity_years,
        frequency=2
    )
    sensitivities = bond.calculate_duration_convexity(req.current_ytm_pct)
    impact = bond.estimate_price_impact(req.current_ytm_pct, req.yield_shift_bps)
    return {
        "sensitivities": sensitivities,
        "impact": impact
    }

@app.post("/api/exim/tariff")
def calculate_customs_landed_cost(req: CustomsDutyRequest):
    engine = GlobalEximEngine(fx_rate_to_local=req.fx_rate)
    contract = TradeContract(
        contract_id="CNT-API-REQ",
        exporter_name="Apex Global Technologies",
        exporter_country="United States",
        importer_name="Indo Tech Ltd",
        importer_country="India",
        hs_code=req.hs_code,
        incoterm=Incoterm.CIF,
        cargo_quantity_units=1,
        unit_price_usd=req.fob_usd,
        freight_usd=req.freight_usd,
        marine_insurance_usd=req.insurance_usd
    )
    landed = engine.compute_customs_landed_cost(contract)
    return landed.__dict__

@app.post("/api/exim/lc-audit")
def audit_lc_presentation(req: LCAuditRequest):
    engine = GlobalEximEngine()
    lc = LetterOfCreditSpec(
        lc_reference="LC-API-AUDIT",
        issuing_bank="Standard Chartered Bank",
        applicant="Applicant Enterprise Ltd",
        beneficiary="Beneficiary Corp",
        credit_amount_usd=req.lc_amount_usd,
        tolerance_pct=req.tolerance_pct,
        expiry_date=req.expiry_date,
        latest_shipment_date=req.latest_shipment_date,
        port_of_loading=req.port_of_loading,
        port_of_discharge=req.port_of_discharge
    )
    docs = ShippingDocuments(
        doc_reference="DOC-API-AUDIT",
        invoice_number="INV-API-001",
        invoice_amount_usd=req.invoice_amount_usd,
        invoice_beneficiary="Beneficiary Corp",
        invoice_applicant="Applicant Enterprise Ltd",
        bill_of_lading_no="BOL-MAERSK-1122",
        shipped_on_board_date=req.shipped_date,
        bol_port_of_loading=req.port_of_loading,
        bol_port_of_discharge=req.port_of_discharge,
        is_clean_on_board=req.is_clean_on_board
    )
    return engine.audit_ucp600_presentation(lc, docs, presentation_date=req.presentation_date)

@app.post("/api/macro/cycle")
def execute_macro_cycle(req: MacroCycleRequest):
    report = orchestrator.run_full_macro_cycle(
        archetype_index=req.archetype_index,
        trade_units=req.trade_units,
        unit_price_usd=req.unit_price_usd,
        treasury_cash_pool_usd=req.treasury_cash_pool_usd,
        equity_portfolio_capital_usd=req.equity_portfolio_capital_usd
    )
    rep_dict = report.__dict__
    cycle_id = ledger.record_macro_cycle(rep_dict)
    rep_dict["cycle_id"] = cycle_id
    return rep_dict

@app.get("/api/ledger/history")
def get_ledger_history(limit: int = 10):
    return {
        "metrics": ledger.get_ledger_metrics(),
        "recent_cycles": ledger.get_latest_cycles(limit=limit)
    }

# --- Multi-Asset Derivatives Endpoints ---

@app.post("/api/derivatives/option-price")
def price_option(req: OptionPricingRequest):
    op_type = OptionType.CALL if req.option_type.upper() == "CALL" else OptionType.PUT
    greeks = BlackScholesEngine.price_option(
        spot=req.spot,
        strike=req.strike,
        maturity_years=req.maturity_years,
        risk_free_rate=req.risk_free_rate,
        volatility=req.volatility,
        dividend_yield=0.0,
        option_type=op_type
    )
    return greeks.__dict__

@app.post("/api/derivatives/implied-vol")
def solve_implied_vol(req: ImpliedVolRequest):
    op_type = OptionType.CALL if req.option_type.upper() == "CALL" else OptionType.PUT
    iv = BlackScholesEngine.solve_implied_volatility(
        target_price=req.target_price,
        spot=req.spot,
        strike=req.strike,
        maturity_years=req.maturity_years,
        risk_free_rate=req.risk_free_rate,
        option_type=op_type
    )
    return {
        "target_price": req.target_price,
        "solved_implied_volatility": iv,
        "solved_implied_volatility_pct": round(iv * 100.0, 2)
    }

@app.post("/api/derivatives/irs-valuation")
def value_interest_rate_swap(req: IRSRequest):
    swap = InterestRateSwapContract(
        notional_usd=req.notional_usd,
        tenor_years=req.tenor_years,
        fixed_rate_pct=req.fixed_rate_pct,
        floating_sofr_benchmark_pct=req.floating_sofr_benchmark_pct
    )
    # Default discount curve map
    curve_map = {1: 0.045, 2: 0.044, 3: 0.043, 4: 0.043, 5: 0.044}
    return swap.calculate_swap_valuation(curve_map)

@app.post("/api/derivatives/ffa-hedge")
def calculate_ffa_hedge(req: FFAHedgeRequest):
    return FreightForwardAgreementPricer.price_ffa_hedge(
        spot_freight_usd_teu=req.spot_freight_teu,
        forward_contract_rate_usd_teu=req.forward_locked_rate_teu,
        contracted_teu_volume=req.volume_teu,
        settlement_spot_freight_usd_teu=req.settlement_spot_teu
    )

# --- Maritime Supply Chain & Logistics Endpoints ---

@app.get("/api/logistics/routes")
def get_maritime_corridors():
    catalog = MaritimeSupplyChainOptimizer.get_corridor_catalog()
    return {
        route_id: {
            "origin": spec.origin_port,
            "destination": spec.destination_port,
            "distance_nm": spec.distance_nautical_miles,
            "transit_days": spec.transit_days,
            "bunker_fuel_cost_usd": spec.total_bunker_fuel_cost_usd,
            "canal_tolls_usd": spec.canal_tolls_usd,
            "total_voyage_cost_usd": spec.total_voyage_cost_usd,
            "chokepoints": [c.value for c in spec.primary_chokepoints]
        }
        for route_id, spec in catalog.items()
    }

@app.get("/api/logistics/chokepoint-disruption")
def simulate_chokepoint_disruption(chokepoint: str = "Suez Canal / Red Sea"):
    return MaritimeSupplyChainOptimizer.simulate_chokepoint_blockade(Chokepoint.SUEZ_CANAL)

@app.post("/api/logistics/demurrage")
def calculate_demurrage(req: DemurrageRequest):
    return MaritimeSupplyChainOptimizer.compute_demurrage_and_detention(
        teu_containers=req.teu_containers,
        port_delay_days=req.port_delay_days,
        free_days_allowed=req.free_days_allowed
    )

# --- Macro Stress-Testing & Monte Carlo Endpoints ---

@app.post("/api/stress/deterministic")
def run_deterministic_stress(req: DeterministicStressRequest):
    sheet = EnterpriseBalanceSheet(
        equities_portfolio_usd=req.equities_usd,
        bond_portfolio_usd=req.bonds_usd,
        money_market_cash_usd=req.cash_usd,
        exim_trade_receivables_usd=req.trade_usd
    )
    scen_map = {
        "STAGFLATION_1970": StressScenario.GREAT_STAGFLATION_1970S,
        "GFC_2008": StressScenario.GFC_2008_LIQUIDITY_CRUNCH,
        "SUPPLY_2020": StressScenario.SUPPLY_CHAIN_FRACTURE_2020,
        "SANCTIONS": StressScenario.SOVEREIGN_SANCTIONS_CHOKEPOINT
    }
    selected_scen = scen_map.get(req.scenario, StressScenario.GFC_2008_LIQUIDITY_CRUNCH)
    res = MonteCarloStressEngine.run_deterministic_shock(sheet, selected_scen)
    return res.__dict__

@app.post("/api/stress/monte-carlo")
def run_monte_carlo_simulation(req: MonteCarloRequest):
    sheet = EnterpriseBalanceSheet(
        equities_portfolio_usd=req.equities_usd,
        bond_portfolio_usd=req.bonds_usd,
        money_market_cash_usd=req.cash_usd,
        exim_trade_receivables_usd=req.trade_usd
    )
    return MonteCarloStressEngine.run_stochastic_monte_carlo(
        sheet=sheet,
        num_simulations=req.num_simulations,
        horizon_days=req.horizon_days
    )

# --- WebSocket Streaming Endpoint ---

@app.websocket("/ws/market-stream")
async def websocket_market_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            snapshot = market_data.get_unified_market_snapshot()
            await websocket.send_json({
                "type": "MARKET_TICK_STREAM",
                "timestamp": snapshot["timestamp"],
                "data": snapshot
            })
            await asyncio.sleep(2.0)
    except WebSocketDisconnect:
        pass
    except Exception:
        await websocket.close()
