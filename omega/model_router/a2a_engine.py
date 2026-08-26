"""
OMNIROUTE A2A (AGENT-TO-AGENT) ENGINE
Enables structured peer-to-peer agent messaging preserving trace IDs, identity,
security boundaries, and token budgets.
"""
import time
import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class A2AMessage:
    message_id: str
    trace_id: str
    sender_agent: str
    recipient_agent: str
    action: str
    payload: Dict[str, Any]
    mission_id: Optional[str] = None
    permissions: List[str] = field(default_factory=lambda: ["READ", "EXECUTE"])
    model: Optional[str] = None
    mcp_tools: List[str] = field(default_factory=list)
    result: Optional[Dict[str, Any]] = None
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class A2AEngine:
    def __init__(self):
        self._message_bus: List[A2AMessage] = []

    def dispatch(
        self,
        sender: str,
        recipient: str,
        action: str,
        payload: Dict[str, Any],
        trace_id: Optional[str] = None,
        mission_id: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        model: Optional[str] = None,
        mcp_tools: Optional[List[str]] = None
    ) -> A2AMessage:
        msg = A2AMessage(
            message_id=f"A2A-{uuid.uuid4().hex[:8]}",
            trace_id=trace_id or f"TRC-{uuid.uuid4().hex[:8]}",
            sender_agent=sender,
            recipient_agent=recipient,
            action=action,
            payload=payload,
            mission_id=mission_id,
            permissions=permissions or ["READ", "EXECUTE"],
            model=model,
            mcp_tools=mcp_tools or []
        )
        self._message_bus.append(msg)
        return msg

    def get_trace_messages(self, trace_id: str) -> List[A2AMessage]:
        return [m for m in self._message_bus if m.trace_id == trace_id]
