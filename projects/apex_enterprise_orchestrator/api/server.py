"""
ApexFlow Enterprise API - Production ASGI Server.
FastAPI REST service providing high-throughput reconciliation, metrics, and interactive dashboard.
"""

import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Header, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel, Field

from projects.apex_enterprise_orchestrator.core.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenException,
)
from projects.apex_enterprise_orchestrator.core.idempotency import IdempotencyLedger
from projects.apex_enterprise_orchestrator.reconciliation.batch_runner import (
    BatchReconciliationEngine,
)
from projects.apex_enterprise_orchestrator.reconciliation.matcher import ThreeWayMatcher
from projects.apex_enterprise_orchestrator.reconciliation.models import (
    GoodsReceipt,
    Invoice,
    MatchVerdict,
    PurchaseOrder,
    ReconciliationResult,
    ToleranceConfig,
)
from projects.apex_enterprise_orchestrator.telemetry.logger import get_structured_logger
from projects.apex_enterprise_orchestrator.telemetry.metrics import MetricsRegistry

# Initialize core services
logger = get_structured_logger("ApexFlowAPI")
metrics = MetricsRegistry()
ledger = IdempotencyLedger()
circuit = CircuitBreaker(failure_threshold=5, recovery_timeout=5.0, name="reconciliation_circuit")
matcher = ThreeWayMatcher()
batch_engine = BatchReconciliationEngine()

app = FastAPI(
    title="ApexFlow Enterprise Orchestrator",
    version="2.4.0",
    description="High-Throughput Distributed Reconciliation, Event-Driven Task Engine, and Enterprise Telemetry.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SingleReconcileRequest(BaseModel):
    purchase_order: Optional[PurchaseOrder] = None
    goods_receipt: Optional[GoodsReceipt] = None
    invoice: Invoice
    tolerance: Optional[ToleranceConfig] = None


class BatchSimulateRequest(BaseModel):
    record_count: int = Field(default=5000, ge=10, le=100000, description="Number of transactions to synthesize")


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>ApexFlow Enterprise Orchestrator</title></head>
        <body style="font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; text-align: center;">
            <h1 style="color: #38bdf8;">ApexFlow Enterprise Orchestrator</h1>
            <p>High-Throughput Distributed Reconciliation & Autonomous Pipeline Engine</p>
            <div style="margin-top: 24px;">
                <a href="/docs" style="color: #38bdf8; margin: 0 16px;">API Swagger Docs</a>
                <a href="/dashboard" style="color: #38bdf8; margin: 0 16px;">Live Mission Control Cockpit</a>
                <a href="/metrics" style="color: #38bdf8; margin: 0 16px;">Prometheus Metrics</a>
            </div>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    snapshot = metrics.get_snapshot()
    return {
        "status": "HEALTHY",
        "service": "ApexFlow Enterprise Orchestrator",
        "version": "2.4.0",
        "uptime_seconds": snapshot["uptime_seconds"],
        "circuit_breaker_state": circuit.state.value,
        "active_counters": snapshot["counters"],
    }


@app.get("/metrics", response_class=PlainTextResponse)
async def prometheus_metrics():
    return metrics.to_prometheus_format()


@app.get("/api/v1/metrics/snapshot")
async def metrics_snapshot():
    return metrics.get_snapshot()


@app.post("/api/v1/reconcile/single", response_model=ReconciliationResult)
async def reconcile_single(
    payload: SingleReconcileRequest,
    x_idempotency_key: Optional[str] = Header(None, alias="X-Idempotency-Key"),
):
    """
    Executes atomic 3-way reconciliation with cryptographic idempotency caching.
    """
    start = time.perf_counter()

    # 1. Idempotency Check
    if x_idempotency_key:
        try:
            is_cached, cached_data = await ledger.check_or_reserve(
                key=x_idempotency_key,
                payload=payload.model_dump(),
            )
            if is_cached and cached_data:
                metrics.increment("idempotency_cache_hits_total")
                return ReconciliationResult(**cached_data)
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
        except RuntimeError as err:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(err))

    # 2. Execution guarded by Circuit Breaker
    async def _execute_match():
        target_matcher = ThreeWayMatcher(payload.tolerance) if payload.tolerance else matcher
        return target_matcher.reconcile(
            po=payload.purchase_order,
            grn=payload.goods_receipt,
            invoice=payload.invoice,
        )

    try:
        result = await circuit.call(_execute_match)
    except CircuitBreakerOpenException as err:
        metrics.increment("circuit_breaker_trips_total")
        if x_idempotency_key:
            await ledger.record_failure(x_idempotency_key)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(err))
    except Exception as err:
        if x_idempotency_key:
            await ledger.record_failure(x_idempotency_key)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

    # 3. Store result in Idempotency Ledger
    if x_idempotency_key:
        await ledger.record_success(x_idempotency_key, result.model_dump())

    # 4. Telemetry Recording
    elapsed_ms = (time.perf_counter() - start) * 1000
    metrics.record_latency(elapsed_ms)
    metrics.increment("reconciliation_requests_total")

    if result.verdict == MatchVerdict.EXACT_MATCH:
        metrics.increment("reconciliation_matches_exact")
    else:
        metrics.increment("reconciliation_discrepancies_total")
        metrics.add_gauge("total_financial_exposure_prevented_inr", result.financial_exposure)

    return result


@app.post("/api/v1/simulate")
async def simulate_high_volume(request: BatchSimulateRequest):
    """
    Simulates high-throughput production load, executing 3-way matching on synthetic streams.
    """
    stream = BatchReconciliationEngine.generate_synthetic_stream(request.record_count)
    report = batch_engine.process_triplets(stream)

    # Update global metrics
    metrics.increment("reconciliation_requests_total", report["total_records"])
    metrics.increment("reconciliation_matches_exact", report["verdict_counts"].get(MatchVerdict.EXACT_MATCH.value, 0))
    metrics.increment(
        "reconciliation_discrepancies_total",
        report["total_records"] - report["verdict_counts"].get(MatchVerdict.EXACT_MATCH.value, 0),
    )
    metrics.add_gauge("total_financial_exposure_prevented_inr", report["total_exposure_prevented"])
    metrics.record_latency(report["average_latency_ms"])

    return report


@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    """Serves the standalone Glassmorphism Mission Control UI."""
    dashboard_path = Path(__file__).parent.parent / "dashboard" / "index.html"
    if not dashboard_path.exists():
        raise HTTPException(status_code=404, detail="Dashboard index.html not found.")
    return HTMLResponse(content=dashboard_path.read_text(encoding="utf-8"))
