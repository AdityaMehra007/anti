import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from v2g_telemetry import GridMatrixController

def test_gridmatrix_dynamic_throttling():
    controller = GridMatrixController(substation_capacity_kw=100.0)
    controller.register_pod("POD-1", 50.0)
    controller.register_pod("POD-2", 50.0)

    controller.pods["POD-1"].connected_vehicle_id = "ATHER-450X-1"
    controller.pods["POD-1"].battery_soc_pct = 20.0 # Low battery

    controller.pods["POD-2"].connected_vehicle_id = "ATHER-RIZTA-1"
    controller.pods["POD-2"].battery_soc_pct = 85.0 # High battery

    # Nominal grid frequency 50.0 Hz
    controller.optimize_load(grid_frequency_hz=50.0)
    assert controller.pods["POD-1"].current_kw > controller.pods["POD-2"].current_kw

    # Under-frequency grid stress (49.5 Hz) -> Must throttle total power
    controller.optimize_load(grid_frequency_hz=49.5)
    total_kw = controller.pods["POD-1"].current_kw + controller.pods["POD-2"].current_kw
    assert total_kw <= 60.0
