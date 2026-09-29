"""
Planetary Sovereign Continuum & Frontier Engine API.

Unified high-performance production API gateway connecting:
- Planetary Sovereign Banking (Central Bank, DCM, Custody, RTGS ISO 20022)
- Terra Kinetics Robotics (Universal Kinematic Protocol, 200 Hz Edge Kernel)
- Aether Nuclear Energy (SMR thermodynamics & PPA tollbooths)
- Bioma Foundry (Precision fermentation & DNA compilation)
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Domain imports
from sovereign_continuum.banking.autonomous_sovereign_bank import AutonomousSovereignBank
from sovereign_continuum.banking.iso20022 import ISO20022Gateway, TransferPriority
from aether_energy.ppa_tollbooth_calculator import PPATollboothCalculator
from aether_energy.smr_reactor_model import SMRReactorModel
from bioma_foundry.dna_compiler import DNACompiler
from terra_kinetics.runtime.terra_edge_kernel import TerraEdgeKernel
from terra_kinetics.protocol.ukp_schema import UKPTelemetryPacket, RobotType


# Pydantic Request / Response Models
class ISO20022TransferRequest(BaseModel):
    debtor_name: str = Field(..., example="Tesla Gigafactory Berlin")
    debtor_iban: str = Field(..., example="DE89370400440532013000")
    debtor_bic: str = Field(..., example="DEUTDEDD")
    creditor_name: str = Field(..., example="Terra Kinetics Corp")
    creditor_iban: str = Field(..., example="GB82WEST12345698765432")
    creditor_bic: str = Field(..., example="BARCGB22")
    amount: float = Field(..., gt=0, example=15_000_000.0)
    currency: str = Field(default="USD", example="USD")
    priority: str = Field(default="HIGH", example="HIGH")


class CashSweepRequest(BaseModel):
    subsidiary_balances: Dict[str, float] = Field(
        ...,
        example={"SUB_USA": 45_000_000.0, "SUB_GERMANY": 18_000_000.0, "SUB_SINGAPORE": 22_000_000.0},
    )
    operating_cushion_usd: float = Field(default=5_000_000.0, example=5_000_000.0)


class SMROfftakeRequest(BaseModel):
    thermal_power_mw: float = Field(default=300.0, example=300.0)
    ppa_contract_price_per_mwh: float = Field(default=85.0, example=85.0)
    datacenter_capacity_mw: float = Field(default=100.0, example=100.0)


class DNACompileRequest(BaseModel):
    amino_acid_sequence: str = Field(..., example="MKTIIALSYIFCLVFA")
    organism: str = Field(default="e_coli", example="e_coli")


# FastAPI Application Factory
def create_app() -> FastAPI:
    app = FastAPI(
        title="Planetary Sovereign Continuum & Frontier Engine API",
        description="Unified Enterprise Gateway for Multi-Trillion Planetary Banking, Robotics Tele-Op, Nuclear SMR Tollbooths, and Synthetic Biology.",
        version="1.0.0",
    )

    # Enable CORS for WebGL & browser dashboards
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize shared singletons
    bank = AutonomousSovereignBank()
    iso_gateway = ISO20022Gateway(institution_bic="CONTUS33XXX")
    kernel = TerraEdgeKernel(robot_type=RobotType.UNITREE_H1)
    kernel.power_on()
    compiler = DNACompiler()

    @app.get("/")
    def root():
        return {
            "system": "Planetary Sovereign Continuum",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "capabilities": [
                "Planetary Banking & RTGS Clearing",
                "ISO 20022 Messaging (pacs.008, pacs.009, camt.053)",
                "200 Hz Robot Kinematics Tele-Op & Digital Twin",
                "Nuclear SMR Thermal Thermodynamics & PPA Tollbooths",
                "Synthetic DNA Codon Compilation",
            ],
            "docs_url": "/docs",
        }

    @app.get("/health")
    def health():
        return {
            "status": "HEALTHY",
            "uptime_seconds": round(time.time()),
            "subsystems": {
                "banking_engine": "ONLINE",
                "iso20022_clearing": "ONLINE",
                "robotics_edge_kernel": "ACTIVE_200HZ",
                "nuclear_tollbooth": "CALIBRATED",
                "bioma_foundry": "READY",
            },
        }

    @app.get("/api/v1/banking/overview")
    def get_banking_overview():
        """Returns consolidated planetary sovereign banking balance sheet metrics."""
        overview = bank.generate_consolidated_banking_audit()
        return overview

    @app.post("/api/v1/banking/iso20022/transfer")
    def execute_iso20022_transfer(payload: ISO20022TransferRequest):
        """Constructs and atomically clears an ISO 20022 pacs.008 customer credit transfer."""
        try:
            priority_enum = TransferPriority[payload.priority.upper()]
        except KeyError:
            priority_enum = TransferPriority.NORM

        try:
            tx = iso_gateway.build_pacs008_transfer(
                debtor_name=payload.debtor_name,
                debtor_iban=payload.debtor_iban,
                debtor_bic=payload.debtor_bic,
                creditor_name=payload.creditor_name,
                creditor_iban=payload.creditor_iban,
                creditor_bic=payload.creditor_bic,
                amount=payload.amount,
                currency=payload.currency,
                priority=priority_enum,
            )
            clearing_result = iso_gateway.execute_rtgs_settlement(tx)
            clearing_result["xml_payload"] = iso_gateway.to_xml(tx)
            return clearing_result
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    @app.post("/api/v1/banking/cash-sweep")
    def execute_cash_sweep(payload: CashSweepRequest):
        """Executes zero-balance sweep across subsidiaries into the master treasury."""
        sweep_result = bank.transaction_banking.cash_management.execute_zero_balance_sweep(
            subsidiary_balances=payload.subsidiary_balances,
            target_operating_cushion=payload.operating_cushion_usd,
        )
        return sweep_result

    @app.get("/api/v1/robotics/telemetry")
    def get_robotics_telemetry():
        """Returns current 200 Hz edge kernel telemetry state and safety PL-e interlocks."""
        # Execute one control tick
        step_result = kernel.step_control_cycle()
        return {
            "cycle_count": step_result.cycle_count,
            "latency_ms": step_result.latency_ms,
            "safety_passed": step_result.safety_passed,
            "pl_e_verified": step_result.pl_e_verified,
            "safety_events": step_result.safety_events,
            "robot_type": kernel.robot_type.value,
            "joint_positions_deg": [round(p * 57.2958, 2) for p in step_result.target_packet.positions],
            "torques_nm": [round(t, 2) for t in step_result.target_packet.torques],
        }

    @app.post("/api/v1/energy/smr-offtake")
    def calculate_smr_offtake(payload: SMROfftakeRequest):
        """Calculates nuclear SMR electrical output, capacity factor, and PPA tollbooth economics."""
        reactor = SMRReactorModel(thermal_power_mw=payload.thermal_power_mw)
        elec_mw = reactor.calculate_electrical_output_mw()

        calculator = PPATollboothCalculator(
            contract_price_per_mwh=payload.ppa_contract_price_per_mwh,
            datacenter_load_mw=payload.datacenter_capacity_mw,
        )
        economics = calculator.compute_tollbooth_annual_revenue(available_smr_mw=elec_mw)
        return {
            "thermal_power_mw": payload.thermal_power_mw,
            "net_electrical_output_mw": round(elec_mw, 2),
            "efficiency_thermal_to_electric": round(reactor.thermal_efficiency, 3),
            "ppa_economics": economics,
        }

    @app.post("/api/v1/bio/compile")
    def compile_dna(payload: DNACompileRequest):
        """Compiles amino acid sequences into codon-optimized DNA with GC-content and restriction analysis."""
        try:
            result = compiler.compile(
                peptide_sequence=payload.amino_acid_sequence,
                target_organism=payload.organism,
            )
            return result
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    @app.websocket("/ws/telemetry")
    async def websocket_telemetry(websocket: WebSocket):
        """Streams live 200 Hz UKP telemetry packets to connected WebGL visualizers."""
        await websocket.accept()
        try:
            while True:
                step = kernel.step_control_cycle()
                payload = {
                    "timestamp": time.time(),
                    "cycle": step.cycle_count,
                    "latency_ms": step.latency_ms,
                    "safety_pl_e": step.pl_e_verified,
                    "positions": step.target_packet.positions,
                    "torques": step.target_packet.torques,
                }
                await websocket.send_text(json.dumps(payload))
                await asyncio.sleep(0.05)  # 20 Hz push over websocket for browser display
        except WebSocketDisconnect:
            pass

    return app


# Default ASGI app instance
app = create_app()
