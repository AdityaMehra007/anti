"""
IMMUTABLE TRANSACTION LEDGER
Records all significant actions, trace IDs, agent IDs, tool calls, results, and reconciliation.
"""
import time
import hashlib
from typing import Dict, Any, List
from dataclasses import dataclass, asdict, field

@dataclass
class LedgerTransaction:
    transaction_id: str
    trace_id: str
    agent_id: str
    tool_or_model: str
    environment: str  # LIVE, SANDBOX, SIMULATED
    authorization_status: str
    input_summary: str
    output_summary: str
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    entry_hash: str = ""

    def __post_init__(self):
        if not self.entry_hash:
            raw = f"{self.transaction_id}|{self.trace_id}|{self.agent_id}|{self.input_summary}|{self.timestamp}"
            self.entry_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class ImmutableTransactionLedger:
    def __init__(self):
        self._entries: List[LedgerTransaction] = []

    def record(
        self,
        trace_id: str,
        agent_id: str,
        tool_or_model: str,
        env: str,
        auth_status: str,
        input_sum: str,
        output_sum: str
    ) -> LedgerTransaction:
        tx_id = f"TX-{len(self._entries)+1:06d}"
        tx = LedgerTransaction(
            transaction_id=tx_id,
            trace_id=trace_id,
            agent_id=agent_id,
            tool_or_model=tool_or_model,
            environment=env,
            authorization_status=auth_status,
            input_summary=input_sum,
            output_summary=output_sum
        )
        self._entries.append(tx)
        return tx

    def list_transactions(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self._entries[-limit:]]

    def verify_integrity(self) -> bool:
        for t in self._entries:
            raw = f"{t.transaction_id}|{t.trace_id}|{t.agent_id}|{t.input_summary}|{t.timestamp}"
            expected = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if t.entry_hash != expected:
                return False
        return True
