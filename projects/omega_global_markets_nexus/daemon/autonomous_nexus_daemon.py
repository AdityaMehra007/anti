"""
Autonomous OMEGA Nexus Daemon & Immutable Audit Ledger
Maintains an automated 24/7 background operating loop, records macro cycle executions,
manages cash sweeps, audits cross-border shipments, and logs telemetry to SQLite.
"""
import json
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from projects.omega_global_markets_nexus.core.nexus_orchestrator import OmegaNexusOrchestrator
from projects.omega_global_markets_nexus.data_feeds.market_data_service import MarketDataService


class NexusAuditLedger:
    """SQLite-backed immutable audit trail for all global market operations and trade events."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_dir = Path(__file__).resolve().parent
            self.db_path = str(db_dir / "nexus_ledger.db")
        else:
            self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS macro_cycles (
                    cycle_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    business_archetype TEXT NOT NULL,
                    annual_fcf_bn REAL NOT NULL,
                    enterprise_value_bn REAL NOT NULL,
                    exim_trade_volume_usd REAL NOT NULL,
                    exim_settlement_status TEXT NOT NULL,
                    money_market_yield_pct REAL NOT NULL,
                    basel3_lcr_pct REAL NOT NULL,
                    bond_10y_yield_pct REAL NOT NULL,
                    curve_state TEXT NOT NULL,
                    stock_portfolio_sharpe REAL NOT NULL,
                    verdict TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trade_events (
                    trade_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    contract_id TEXT NOT NULL,
                    cif_value_usd REAL NOT NULL,
                    hs_code TEXT NOT NULL,
                    landed_cost_local REAL NOT NULL,
                    ucp600_status TEXT NOT NULL,
                    sanctions_cleared INTEGER NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cash_sweeps (
                    sweep_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    total_cash_usd REAL NOT NULL,
                    buffer_cash_usd REAL NOT NULL,
                    sofr_repo_usd REAL NOT NULL,
                    tbills_30d_usd REAL NOT NULL,
                    cp_90d_usd REAL NOT NULL,
                    blended_yield_pct REAL NOT NULL,
                    annual_interest_usd REAL NOT NULL
                )
            """)
            conn.commit()

    def record_macro_cycle(self, report_dict: Dict[str, Any]) -> str:
        cycle_id = f"CYC-{int(time.time() * 1000)}"
        now_iso = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO macro_cycles VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                cycle_id,
                now_iso,
                report_dict["business_archetype"],
                report_dict["annual_fcf_generated_bn"],
                report_dict["enterprise_value_bn"],
                report_dict["exim_trade_volume_usd"],
                report_dict["exim_settlement_status"],
                report_dict["money_market_blended_yield_pct"],
                report_dict["basel3_lcr_pct"],
                report_dict["bond_10y_yield_pct"],
                report_dict["curve_inversion_status"],
                report_dict["stock_portfolio_sharpe"],
                report_dict["nexus_macro_verdict"]
            ))
            conn.commit()
        return cycle_id

    def record_cash_sweep(self, sweep_res: Dict[str, Any]) -> str:
        sweep_id = f"SWP-{int(time.time() * 1000)}"
        now_iso = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cash_sweeps VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                sweep_id,
                now_iso,
                sweep_res["total_cash_usd"],
                sweep_res["overnight_operational_cash"],
                sweep_res["swept_to_sofr_repo"],
                sweep_res["swept_to_30d_tbills"],
                sweep_res["swept_to_90d_cp"],
                sweep_res["weighted_blended_yield_pct"],
                sweep_res["annualized_interest_income_usd"]
            ))
            conn.commit()
        return sweep_id

    def get_latest_cycles(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM macro_cycles ORDER BY timestamp DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_ledger_metrics(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) as total_cycles FROM macro_cycles")
            total_cycles = cursor.fetchone()["total_cycles"]
            cursor.execute("SELECT count(*) as total_sweeps, coalesce(sum(annual_interest_usd), 0) as total_interest FROM cash_sweeps")
            sweep_row = cursor.fetchone()
            return {
                "total_macro_cycles_recorded": total_cycles,
                "total_sweeps_executed": sweep_row["total_sweeps"],
                "total_annual_interest_captured_usd": sweep_row["total_interest"]
            }


class AutonomousNexusDaemon:
    """Continuous automated execution daemon running market surveillance and autonomous rebalancing."""

    def __init__(self, db_path: Optional[str] = None):
        self.orchestrator = OmegaNexusOrchestrator()
        self.market_data = MarketDataService()
        self.ledger = NexusAuditLedger(db_path=db_path)

    def execute_single_cycle(self, archetype_idx: int = 0) -> Dict[str, Any]:
        report = self.orchestrator.run_full_macro_cycle(
            archetype_index=archetype_idx,
            trade_units=500,
            unit_price_usd=40_000.0,
            treasury_cash_pool_usd=50_000_000.0,
            equity_portfolio_capital_usd=25_000_000.0
        )
        report_data = report.__dict__
        cycle_id = self.ledger.record_macro_cycle(report_data)
        report_data["cycle_id"] = cycle_id
        return report_data

    def run_daemon_loop(self, iterations: int = 3, interval_seconds: float = 1.0) -> List[Dict[str, Any]]:
        results = []
        for i in range(iterations):
            arch_idx = i % 5
            cycle_result = self.execute_single_cycle(archetype_idx=arch_idx)
            results.append(cycle_result)
            if i < iterations - 1:
                time.sleep(interval_seconds)
        return results
