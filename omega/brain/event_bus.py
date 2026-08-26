"""
OMEGA EVENT BUS
Pub/Sub system supporting 10 core event types:
PAGE_DISCOVERED, PAGE_SCRAPED, JOB_FOUND, JOB_CHANGED, JOB_EXPIRED,
COMPANY_CHANGED, CONTACT_FOUND, RESEARCH_COMPLETED, SOURCE_FAILED, SOURCE_CHANGED
"""
import time
from enum import Enum
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field, asdict

class EventType(str, Enum):
    PAGE_DISCOVERED = "PAGE_DISCOVERED"
    PAGE_SCRAPED = "PAGE_SCRAPED"
    JOB_FOUND = "JOB_FOUND"
    JOB_CHANGED = "JOB_CHANGED"
    JOB_EXPIRED = "JOB_EXPIRED"
    COMPANY_CHANGED = "COMPANY_CHANGED"
    CONTACT_FOUND = "CONTACT_FOUND"
    RESEARCH_COMPLETED = "RESEARCH_COMPLETED"
    SOURCE_FAILED = "SOURCE_FAILED"
    SOURCE_CHANGED = "SOURCE_CHANGED"

@dataclass
class OmegaEvent:
    event_type: EventType
    payload: Dict[str, Any]
    source: str = "firecrawl_mcp"
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["event_type"] = self.event_type.value
        return d

class OmegaEventBus:
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable[[OmegaEvent], None]]] = {
            t: [] for t in EventType
        }
        self._history: List[OmegaEvent] = []

    def subscribe(self, event_type: EventType, handler: Callable[[OmegaEvent], None]):
        self._subscribers[event_type].append(handler)

    def publish(self, event: OmegaEvent):
        self._history.append(event)
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                pass

    def get_history(self, limit: int = 50) -> List[OmegaEvent]:
        return self._history[-limit:]

# Global event bus instance
event_bus = OmegaEventBus()
