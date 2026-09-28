"""
OMEGA INFINITY (Ω-OS) — SOVEREIGN ENTERPRISE & HOLDING KERNEL
Enforces OMEGA_CONSTITUTION.md (120 Master Directives) & ADI_OMNI_CODEX.md.
Provides EnterpriseState, Cryptographic Tamper-Evident Ledger, Event Bus,
and Mode Controller (Modes A through M).
"""

import os
import sys
import json
import time
import hashlib
import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Callable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEDGER_DIR = os.path.join(BASE_DIR, "omega", "data")
DEFAULT_LEDGER_PATH = os.path.join(LEDGER_DIR, "omega_infinity_ledger.jsonl")


# ============================================================================
# 1. CONSTITUTIONAL MODES (Section 5)
# ============================================================================

CONSTITUTIONAL_MODES = {
    "A": {"name": "DISCOVERY", "desc": "Environment and capability discovery"},
    "B": {"name": "RESEARCH", "desc": "Deep evidence gathering and cross-checking"},
    "C": {"name": "STRATEGY", "desc": "Converting information into high-leverage decisions"},
    "D": {"name": "BUILD", "desc": "Tangible system construction (Artifact-First)"},
    "E": {"name": "AUTOMATION", "desc": "Process standardization and DAG automation"},
    "F": {"name": "EXECUTION", "desc": "Authorized operational dispatches"},
    "G": {"name": "AUDIT", "desc": "Bottleneck, weakness and compliance inspection"},
    "H": {"name": "RED TEAM", "desc": "Adversarial stress testing and failure probes"},
    "I": {"name": "OPTIMIZATION", "desc": "Economics, latency, and leverage improvement"},
    "J": {"name": "SCALE", "desc": "Repeatable expansion of validated systems"},
    "K": {"name": "MONITOR", "desc": "24/7 observability and anomaly detection"},
    "L": {"name": "LEARNING", "desc": "Converting outcomes into reusable skills and rules"},
    "M": {"name": "CEO", "desc": "Enterprise value creation and capital allocation"}
}


# ============================================================================
# 2. CRYPTOGRAPHIC TAMPER-EVIDENT EVENT LEDGER
# ============================================================================

@dataclass
class LedgerBlock:
    index: int
    timestamp: str
    event_type: str
    actor: str
    payload: Dict[str, Any]
    prev_hash: str
    block_hash: str = ""

    def calculate_hash(self) -> str:
        content = f"{self.index}:{self.timestamp}:{self.event_type}:{self.actor}:{json.dumps(self.payload, sort_keys=True)}:{self.prev_hash}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def seal(self):
        self.block_hash = self.calculate_hash()
        return self


class TamperEvidentLedger:
    """
    Append-only SHA-256 chained transaction ledger.
    Every event contains the hash of the preceding event, ensuring tamper evidence.
    """

    def __init__(self, filepath: str = DEFAULT_LEDGER_PATH):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        self.blocks: List[LedgerBlock] = []
        self._load_or_initialize()

    def _load_or_initialize(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            block = LedgerBlock(
                                index=data["index"],
                                timestamp=data["timestamp"],
                                event_type=data["event_type"],
                                actor=data["actor"],
                                payload=data["payload"],
                                prev_hash=data["prev_hash"],
                                block_hash=data["block_hash"]
                            )
                            self.blocks.append(block)
                        except Exception:
                            continue

        if not self.blocks:
            # Genesis Block
            genesis = LedgerBlock(
                index=0,
                timestamp=datetime.datetime.now().isoformat(),
                event_type="GENESIS",
                actor="OMEGA_INFINITY_KERNEL",
                payload={"message": "Sovereign Enterprise Ledger Activated", "directives": 120},
                prev_hash="0" * 64
            ).seal()
            self._append_to_file(genesis)
            self.blocks.append(genesis)

    def _append_to_file(self, block: LedgerBlock):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(block)) + "\n")

    def append(self, event_type: str, actor: str, payload: Dict[str, Any]) -> LedgerBlock:
        prev_hash = self.blocks[-1].block_hash if self.blocks else "0" * 64
        new_index = len(self.blocks)
        block = LedgerBlock(
            index=new_index,
            timestamp=datetime.datetime.now().isoformat(),
            event_type=event_type,
            actor=actor,
            payload=payload,
            prev_hash=prev_hash
        ).seal()
        self.blocks.append(block)
        self._append_to_file(block)
        return block

    def verify_integrity(self) -> Dict[str, Any]:
        """Verifies the entire cryptographic chain."""
        if not self.blocks:
            return {"valid": False, "reason": "Ledger is empty"}

        for i, block in enumerate(self.blocks):
            # Verify recalculation of block_hash
            calculated = block.calculate_hash()
            if calculated != block.block_hash:
                return {
                    "valid": False,
                    "reason": f"Hash mismatch at block {i}",
                    "expected": calculated,
                    "actual": block.block_hash
                }
            # Verify chain linkage
            if i > 0:
                prev = self.blocks[i - 1]
                if block.prev_hash != prev.block_hash:
                    return {
                        "valid": False,
                        "reason": f"Broken chain link at block {i}",
                        "expected_prev": prev.block_hash,
                        "actual_prev": block.prev_hash
                    }

        return {
            "valid": True,
            "total_blocks": len(self.blocks),
            "latest_block_hash": self.blocks[-1].block_hash,
            "genesis_hash": self.blocks[0].block_hash
        }

    def get_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [asdict(b) for b in self.blocks[-limit:]]


# ============================================================================
# 3. SOVEREIGN ENTERPRISE STATE
# ============================================================================

@dataclass
class EnterpriseState:
    holding_name: str = "OMEGA SOVEREIGN HOLDINGS"
    primary_entity: str = "VECTIS TRADE TECHNOLOGIES PRIVATE LIMITED"
    incorporation_jurisdiction: str = "Bengaluru, Karnataka, India"
    founder: str = "Aditya Mehra"
    active_mode: str = "M"  # Default Mode M (CEO)
    capital_reserves_inr: float = 5000000.0  # Projected / Target INR 50L
    monthly_burn_inr: float = 6250.0  # Ultra-minimalist ponytail burn
    runway_months: float = 800.0
    dpiit_recognition: str = "COMPLIANT_READY"
    section_80_iac_eligible: bool = True
    gst_lut_filed: bool = True
    active_ventures: List[Dict[str, Any]] = field(default_factory=lambda: [
        {
            "id": "vectis_trade",
            "name": "VECTIS TRADE",
            "category": "Autonomous Cross-Border Trade & LC Compliance",
            "status": "OPERATIONAL",
            "mrr_inr": 450000.0,
            "arr_inr": 5400000.0
        },
        {
            "id": "omega_intel",
            "name": "OMEGA GLOBAL INTELLIGENCE",
            "category": "Enterprise Market & Network Graph (4.5k MNCs)",
            "status": "ACTIVE",
            "records": 4500
        },
        {
            "id": "omnivanta_foundry",
            "name": "OMNIVANTA AGENTIC SAAS FOUNDRY",
            "category": "Autonomous Micro-SaaS Software Factory",
            "status": "STAGING",
            "ideas_catalog": 500
        }
    ])
    telemetry: Dict[str, Any] = field(default_factory=lambda: {
        "uptime_seconds": 0,
        "total_dispatches": 0,
        "verified_leads_count": 395,
        "target_companies_count": 4500,
        "linkedin_connections_count": 9223,
        "trade_audits_passed": 12,
        "trade_audits_failed": 3,
        "cbam_assessments_completed": 8
    })


# ============================================================================
# 4. OMEGA INFINITY KERNEL
# ============================================================================

class OmegaKernel:
    """
    Central Nervous System for the Sovereign Enterprise.
    Coordinates State, Ledger, Event Routing, and Autonomous Modes.
    """

    def __init__(self, ledger_path: str = DEFAULT_LEDGER_PATH):
        self.start_time = time.time()
        self.ledger = TamperEvidentLedger(ledger_path)
        self.state = EnterpriseState()
        self.listeners: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self.registered_engines: Dict[str, Any] = {}

        # Log system boot
        self.ledger.append(
            event_type="KERNEL_BOOT",
            actor="OMEGA_INFINITY_KERNEL",
            payload={
                "version": "OMEGA-∞-SOVEREIGN-1.0",
                "founder": self.state.founder,
                "mode": self.state.active_mode,
                "status": "SYSTEM_OPTIMAL"
            }
        )

    def register_engine(self, engine_id: str, engine_instance: Any):
        self.registered_engines[engine_id] = engine_instance
        self.ledger.append(
            event_type="ENGINE_REGISTERED",
            actor="OMEGA_INFINITY_KERNEL",
            payload={"engine_id": engine_id, "type": str(type(engine_instance))}
        )

    def set_mode(self, mode_code: str) -> Dict[str, Any]:
        mode_code = mode_code.upper()
        if mode_code not in CONSTITUTIONAL_MODES:
            raise ValueError(f"Invalid constitutional mode '{mode_code}'. Valid modes: {list(CONSTITUTIONAL_MODES.keys())}")

        old_mode = self.state.active_mode
        self.state.active_mode = mode_code
        mode_info = CONSTITUTIONAL_MODES[mode_code]

        self.ledger.append(
            event_type="MODE_TRANSITION",
            actor="FOUNDER_COMMAND",
            payload={
                "previous_mode": old_mode,
                "new_mode": mode_code,
                "name": mode_info["name"],
                "desc": mode_info["desc"]
            }
        )
        return {
            "success": True,
            "mode": mode_code,
            "name": mode_info["name"],
            "description": mode_info["desc"],
            "timestamp": datetime.datetime.now().isoformat()
        }

    def dispatch_event(self, event_name: str, actor: str, data: Dict[str, Any]) -> LedgerBlock:
        self.state.telemetry["total_dispatches"] += 1
        block = self.ledger.append(
            event_type=event_name,
            actor=actor,
            payload=data
        )
        # Notify subscribers
        for callback in self.listeners.get(event_name, []):
            try:
                callback(data)
            except Exception as e:
                print(f"[EVENT ERROR] Error delivering event {event_name}: {e}")
        return block

    def subscribe(self, event_name: str, callback: Callable[[Dict[str, Any]], None]):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def get_summary(self) -> Dict[str, Any]:
        self.state.telemetry["uptime_seconds"] = int(time.time() - self.start_time)
        return {
            "holding": self.state.holding_name,
            "primary_entity": self.state.primary_entity,
            "founder": self.state.founder,
            "active_mode": {
                "code": self.state.active_mode,
                "name": CONSTITUTIONAL_MODES[self.state.active_mode]["name"],
                "desc": CONSTITUTIONAL_MODES[self.state.active_mode]["desc"]
            },
            "financials": {
                "capital_reserves_inr": self.state.capital_reserves_inr,
                "monthly_burn_inr": self.state.monthly_burn_inr,
                "runway_months": self.state.runway_months,
                "dpiit_status": self.state.dpiit_recognition
            },
            "ventures": self.state.active_ventures,
            "telemetry": self.state.telemetry,
            "ledger_status": self.ledger.verify_integrity(),
            "timestamp": datetime.datetime.now().isoformat()
        }


# Global singleton instance for easy import across processes
_KERNEL_INSTANCE: Optional[OmegaKernel] = None

def get_kernel() -> OmegaKernel:
    global _KERNEL_INSTANCE
    if _KERNEL_INSTANCE is None:
        _KERNEL_INSTANCE = OmegaKernel()
    return _KERNEL_INSTANCE
