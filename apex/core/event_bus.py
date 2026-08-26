"""
APEX Core Event Bus with Causation, Correlation, and Priority Routing
"""
import uuid
import time
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class ApexEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    event_type: str = "SYSTEM_EVENT"
    actor: str = "APEX_CORE"
    organization: str = "APEX_ENTERPRISE"
    project_id: Optional[str] = None
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    causation_id: Optional[str] = None
    severity: str = "INFO"  # INFO, WARNING, ERROR, CRITICAL
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class ApexEventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[ApexEvent], Any]]] = {}
        self._history: List[ApexEvent] = []
        self._max_history = 1000

    def subscribe(self, event_type: str, callback: Callable[[ApexEvent], Any]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event: ApexEvent):
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        # Direct subscribers
        if event.event_type in self._subscribers:
            for cb in self._subscribers[event.event_type]:
                try:
                    cb(event)
                except Exception as e:
                    print(f"[EVENT_BUS_ERROR] {event.event_type}: {e}")

        # Wildcard subscribers
        if "*" in self._subscribers:
            for cb in self._subscribers["*"]:
                try:
                    cb(event)
                except Exception as e:
                    print(f"[EVENT_BUS_ERROR] wildcard: {e}")

    def get_history(self, limit: int = 50, event_type: Optional[str] = None) -> List[ApexEvent]:
        if event_type:
            return [e for e in self._history if e.event_type == event_type][-limit:]
        return self._history[-limit:]
