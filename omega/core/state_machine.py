#!/usr/bin/env python3
"""
========================================================================================
OMEGA ZERO-TRUST ACTION STATE MACHINE (v8.0)
========================================================================================
Enforces strict provenance, transition integrity, and execution status tracking.
========================================================================================
"""

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple


class ActionStage(str, Enum):
    DISCOVERED = "DISCOVERED"
    QUALIFIED = "QUALIFIED"
    RESEARCHED = "RESEARCHED"
    READY = "READY"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    QUEUED = "QUEUED"
    ATTEMPTED = "ATTEMPTED"
    DELIVERED = "DELIVERED"
    REPLIED = "REPLIED"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    ACCEPTED = "ACCEPTED"
    CLOSED = "CLOSED"
    FAILED = "FAILED"
    RETRY = "RETRY"
    ESCALATED = "ESCALATED"
    CANCELLED = "CANCELLED"


class ExecutionStatus(str, Enum):
    PREPARED = "PREPARED"      # Prepared locally; awaiting action or connector
    SIMULATED = "SIMULATED"    # Executed in local sandbox/test mode
    QUEUED = "QUEUED"          # Queued in dispatch pool
    ATTEMPTED = "ATTEMPTED"    # Network call made
    DELIVERED = "DELIVERED"    # Verified delivery confirmation from external API
    FAILED = "FAILED"          # Delivery failure / reject
    VERIFIED = "VERIFIED"      # Multi-source confirmed


class ActionTransitionError(Exception):
    pass


class OmegaStateMachine:
    """Manages lifecycle transitions with zero-trust audit logging."""

    VALID_TRANSITIONS = {
        ActionStage.DISCOVERED: [ActionStage.QUALIFIED, ActionStage.CANCELLED, ActionStage.CLOSED],
        ActionStage.QUALIFIED: [ActionStage.RESEARCHED, ActionStage.READY, ActionStage.CANCELLED, ActionStage.CLOSED],
        ActionStage.RESEARCHED: [ActionStage.READY, ActionStage.CANCELLED, ActionStage.CLOSED],
        ActionStage.READY: [ActionStage.APPROVAL_REQUIRED, ActionStage.QUEUED, ActionStage.CANCELLED],
        ActionStage.APPROVAL_REQUIRED: [ActionStage.QUEUED, ActionStage.CANCELLED, ActionStage.ESCALATED],
        ActionStage.QUEUED: [ActionStage.ATTEMPTED, ActionStage.CANCELLED, ActionStage.ESCALATED],
        ActionStage.ATTEMPTED: [ActionStage.DELIVERED, ActionStage.FAILED, ActionStage.RETRY],
        ActionStage.DELIVERED: [ActionStage.REPLIED, ActionStage.CLOSED, ActionStage.INTERVIEW],
        ActionStage.REPLIED: [ActionStage.INTERVIEW, ActionStage.CLOSED, ActionStage.ESCALATED],
        ActionStage.INTERVIEW: [ActionStage.OFFER, ActionStage.CLOSED, ActionStage.ESCALATED],
        ActionStage.OFFER: [ActionStage.ACCEPTED, ActionStage.CLOSED, ActionStage.ESCALATED],
        ActionStage.ACCEPTED: [ActionStage.CLOSED],
        ActionStage.CLOSED: [ActionStage.DISCOVERED], # Re-open if new opportunity emerges
        ActionStage.FAILED: [ActionStage.RETRY, ActionStage.ESCALATED, ActionStage.CLOSED],
        ActionStage.RETRY: [ActionStage.ATTEMPTED, ActionStage.FAILED, ActionStage.CANCELLED],
        ActionStage.ESCALATED: [ActionStage.QUEUED, ActionStage.CANCELLED, ActionStage.CLOSED],
        ActionStage.CANCELLED: [ActionStage.DISCOVERED]
    }

    @classmethod
    def can_transition(cls, current_stage: ActionStage, target_stage: ActionStage) -> bool:
        return target_stage in cls.VALID_TRANSITIONS.get(current_stage, [])

    @classmethod
    def create_action_record(
        cls,
        action_id: str,
        opportunity_id: str,
        target_name: str,
        company: str,
        action_type: str,
        initial_stage: ActionStage = ActionStage.DISCOVERED,
        execution_status: ExecutionStatus = ExecutionStatus.PREPARED
    ) -> Dict[str, Any]:
        now = datetime.now().isoformat()
        return {
            "action_id": action_id,
            "opportunity_id": opportunity_id,
            "target_name": target_name,
            "company": company,
            "action_type": action_type,
            "current_stage": initial_stage.value,
            "execution_status": execution_status.value,
            "created_at": now,
            "last_updated": now,
            "history": [
                {
                    "timestamp": now,
                    "from_stage": None,
                    "to_stage": initial_stage.value,
                    "execution_status": execution_status.value,
                    "actor": "OmegaOrchestrator",
                    "reason": "Action record initialized",
                    "evidence_hash": hashlib.sha256(f"{action_id}_{now}".encode()).hexdigest()[:16]
                }
            ]
        }

    @classmethod
    def transition(
        cls,
        record: Dict[str, Any],
        target_stage: ActionStage,
        execution_status: Optional[ExecutionStatus] = None,
        actor: str = "User",
        reason: str = "",
        evidence_data: str = ""
    ) -> Dict[str, Any]:
        current = ActionStage(record["current_stage"])
        if not cls.can_transition(current, target_stage):
            raise ActionTransitionError(
                f"Invalid state transition: Cannot advance action {record['action_id']} from {current.value} to {target_stage.value}"
            )
        
        now = datetime.now().isoformat()
        if execution_status is None:
            # Derive default execution status
            if target_stage in [ActionStage.DISCOVERED, ActionStage.QUALIFIED, ActionStage.RESEARCHED, ActionStage.READY, ActionStage.APPROVAL_REQUIRED]:
                execution_status = ExecutionStatus.PREPARED
            elif target_stage == ActionStage.QUEUED:
                execution_status = ExecutionStatus.QUEUED
            elif target_stage == ActionStage.ATTEMPTED:
                execution_status = ExecutionStatus.ATTEMPTED
            elif target_stage == ActionStage.DELIVERED:
                execution_status = ExecutionStatus.DELIVERED
            elif target_stage == ActionStage.FAILED:
                execution_status = ExecutionStatus.FAILED
            else:
                execution_status = ExecutionStatus(record.get("execution_status", ExecutionStatus.PREPARED.value))

        record["current_stage"] = target_stage.value
        record["execution_status"] = execution_status.value
        record["last_updated"] = now
        
        ev_hash = hashlib.sha256(f"{record['action_id']}_{now}_{target_stage.value}_{evidence_data}".encode()).hexdigest()[:16]
        record["history"].append({
            "timestamp": now,
            "from_stage": current.value,
            "to_stage": target_stage.value,
            "execution_status": execution_status.value,
            "actor": actor,
            "reason": reason,
            "evidence_hash": ev_hash
        })
        return record
