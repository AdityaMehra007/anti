"""
APEX Immutable Audit Logging Engine
Answers: WHO | WHAT | WHEN | WHY | WITH WHICH DATA | USING WHICH TOOL | UNDER WHICH POLICY | WITH WHAT RESULT
"""
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field

@dataclass
class AuditRecord:
    timestamp: float = field(default_factory=time.time)
    actor: str = "AGENT"
    action: str = "EXECUTE_TOOL"
    reason: str = "Goal execution step"
    tool: str = "none"
    data_scope: str = "workspace"
    policy_evaluated: str = "A3_DEFAULT"
    status: str = "SUCCESS"
    result_summary: str = ""
    correlation_id: str = "unknown"

class ApexAuditLogger:
    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or Path(r"e:\anti\apex\artifacts\audit_trail.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.in_memory_logs: List[AuditRecord] = []

    def log(self, actor: str, action: str, reason: str, tool: str, policy: str, status: str, result_summary: str, correlation_id: str = "unknown"):
        record = AuditRecord(
            actor=actor,
            action=action,
            reason=reason,
            tool=tool,
            policy_evaluated=policy,
            status=status,
            result_summary=result_summary,
            correlation_id=correlation_id
        )
        self.in_memory_logs.append(record)
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(record)) + "\n")
        except Exception as e:
            print(f"[AUDIT_WRITE_ERROR] {e}")

    def get_recent_records(self, limit: int = 50) -> List[AuditRecord]:
        return self.in_memory_logs[-limit:]
