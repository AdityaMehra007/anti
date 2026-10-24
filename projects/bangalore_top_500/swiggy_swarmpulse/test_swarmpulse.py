import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from swarm_router import SwarmPulseEngine, HyperlocalOrder

def test_swarmpulse_optimal_batching():
    engine = SwarmPulseEngine()
    # Koramangala Darkstore coordinates
    ds_lat, ds_lng = 12.9352, 77.6245

    # Register 2 riders nearby
    engine.register_rider("RIDER-A", 12.9355, 77.6248) # 50m away
    engine.register_rider("RIDER-B", 12.9450, 77.6350) # 1.5km away

    orders = [
        HyperlocalOrder("ORD-1", "DS-KOR-1", 12.9360, 77.6250),
        HyperlocalOrder("ORD-2", "DS-KOR-1", 12.9365, 77.6255),
        HyperlocalOrder("ORD-3", "DS-KOR-1", 12.9370, 77.6260),
    ]

    assignments = engine.find_optimal_batch(ds_lat, ds_lng, orders)
    # Rider A is closest, should take multiple orders in batch
    assert "RIDER-A" in assignments
    assert len(assignments["RIDER-A"]) == 3
