"""
OMEGA CONTROL PLANE - Event Bus
Typed Pub-Sub Event Bus connecting all subsystems with event persistence.
"""
import time
from typing import Dict, Any, Callable, List
from pathlib import Path
import sys

WORKSPACE = Path(r"e:\anti")
sys.path.insert(0, str(WORKSPACE))

from apex.control_plane.data_core import OmegaMasterDataCore

class OmegaEventBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OmegaEventBus, cls).__new__(cls)
            cls._instance.subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
            cls._instance.data_core = OmegaMasterDataCore()
        return cls._instance

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event_type: str, source: str, payload: Dict[str, Any]) -> int:
        # 1. Persist to Master Core
        eid = self.data_core.record_event(event_type, source, payload)
        
        # 2. Dispatch to subscribers
        event_obj = {
            "event_id": eid,
            "event_type": event_type,
            "source": source,
            "payload": payload,
            "timestamp": time.time()
        }
        handlers = self.subscribers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event_obj)
            except Exception as e:
                print(f"[EVENT_BUS_ERROR] Handler failed for {event_type}: {e}")

        return eid

if __name__ == "__main__":
    bus = OmegaEventBus()
    bus.subscribe("TEST_EVENT", lambda e: print("[EVENT_BUS_HANDLER] Received:", e["event_type"], e["source"]))
    bus.publish("TEST_EVENT", "UNIT_TEST", {"hello": "world"})
