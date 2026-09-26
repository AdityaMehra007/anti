import os, json
from datetime import datetime

class EventSystem:
    """Reactive Event Bus for Triggering Specialized Agents."""
    def __init__(self, workspace=r"e:\anti"):
        self.workspace = workspace
        self.listeners = {}

    def subscribe(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def publish(self, event_name, payload):
        event_record = {
            "event": event_name,
            "payload": payload,
            "timestamp": datetime.now().isoformat()
        }
        # In this synchronous architecture, dispatch to registered callbacks
        if event_name in self.listeners:
            for cb in self.listeners[event_name]:
                try: cb(payload)
                except Exception: pass
        return event_record
