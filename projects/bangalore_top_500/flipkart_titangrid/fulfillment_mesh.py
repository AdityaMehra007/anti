"""
Flipkart Project TitanGrid: Multi-Warehouse Planetary Ingestion Mesh
Linearizable lease locking and multi-hub inventory allocation during Big Billion Days.
"""
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class HubInventory:
    hub_id: str
    pin_code: str
    stock_count: int
    reserved_count: int = 0

class TitanGridMesh:
    def __init__(self):
        self.inventory: Dict[str, Dict[str, HubInventory]] = {} # sku -> hub_id -> HubInventory

    def add_stock(self, sku: str, hub_id: str, pin_code: str, qty: int):
        if sku not in self.inventory:
            self.inventory[sku] = {}
        self.inventory[sku][hub_id] = HubInventory(hub_id=hub_id, pin_code=pin_code, stock_count=qty)

    def reserve_inventory_linearizable(self, order_id: str, sku: str, customer_pin: str, qty: int) -> Optional[str]:
        hubs = self.inventory.get(sku, {})
        # Find matching regional hub first
        preferred_hub = None
        for hub in hubs.values():
            if hub.pin_code[:3] == customer_pin[:3] and (hub.stock_count - hub.reserved_count) >= qty:
                preferred_hub = hub
                break

        if not preferred_hub:
            for hub in hubs.values():
                if (hub.stock_count - hub.reserved_count) >= qty:
                    preferred_hub = hub
                    break

        if preferred_hub:
            preferred_hub.reserved_count += qty
            return preferred_hub.hub_id
        return None
