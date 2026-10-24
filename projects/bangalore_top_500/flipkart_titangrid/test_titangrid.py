import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from fulfillment_mesh import TitanGridMesh

def test_titangrid_regional_allocation():
    mesh = TitanGridMesh()
    sku = "IPHONE-16-PRO"
    # Whitefield Hub (560066) and Hebbal Hub (560024)
    mesh.add_stock(sku, "HUB-WHITEFIELD", "560066", 50)
    mesh.add_stock(sku, "HUB-HEBBAL", "560024", 20)

    # Order for customer in Whitefield (560066)
    allocated_hub = mesh.reserve_inventory_linearizable("ORD-BBD-1", sku, "560066", 1)
    assert allocated_hub == "HUB-WHITEFIELD"

    # Deplete Whitefield
    mesh.reserve_inventory_linearizable("ORD-BBD-2", sku, "560066", 49)
    # Next order must failover to Hebbal
    next_hub = mesh.reserve_inventory_linearizable("ORD-BBD-3", sku, "560066", 1)
    assert next_hub == "HUB-HEBBAL"
