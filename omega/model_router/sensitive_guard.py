"""
SENSITIVE DATA & PRIVACY ROUTING GUARD
Enforces data classifications: PUBLIC, INTERNAL, CONFIDENTIAL, SENSITIVE.
Strictly gates sensitive payloads to verified local models or blocks them.
"""
from enum import Enum
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass
from .provider_discovery import live_discovery

class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    SENSITIVE = "SENSITIVE"

@dataclass
class PolicyVerdict:
    allowed: bool
    classification: DataClassification
    target_route: str  # LOCAL_PRIVATE, ENTERPRISE_CLOUD, BLOCKED, QUEUE
    reason: str

class SensitiveDataGuard:
    @classmethod
    def evaluate_payload(
        cls,
        task_text: str,
        explicit_class: Optional[DataClassification] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PolicyVerdict:
        meta = metadata or {}
        data_class = explicit_class

        if not data_class:
            lower = task_text.lower()
            if any(k in lower for k in ["private key", "password", "ssn", "credentials", "secret_token", "salary_negotiation_secret"]):
                data_class = DataClassification.SENSITIVE
            elif any(k in lower for k in ["confidential", "internal roadmap", "unreleased"]):
                data_class = DataClassification.CONFIDENTIAL
            elif any(k in lower for k in ["internal", "employee notes"]):
                data_class = DataClassification.INTERNAL
            else:
                data_class = DataClassification.PUBLIC

        # Gating Policy for SENSITIVE and CONFIDENTIAL
        if data_class in [DataClassification.SENSITIVE, DataClassification.CONFIDENTIAL]:
            discovery = live_discovery.discover()
            if discovery.local_daemon_running and discovery.local_models:
                return PolicyVerdict(
                    allowed=True,
                    classification=data_class,
                    target_route="LOCAL_PRIVATE",
                    reason=f"Sensitive payload approved for local private model: {discovery.local_models[0]}"
                )
            else:
                return PolicyVerdict(
                    allowed=False,
                    classification=data_class,
                    target_route="BLOCKED",
                    reason="SENSITIVE_DATA_BLOCKED: Local private inference daemon (Ollama) is offline on port 11434. Cloud routing prohibited for sensitive payloads."
                )

        return PolicyVerdict(
            allowed=True,
            classification=data_class,
            target_route="ENTERPRISE_CLOUD",
            reason="Public / Internal task approved for governed OmniRoute gateway."
        )
