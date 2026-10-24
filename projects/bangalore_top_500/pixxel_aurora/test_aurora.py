import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from hyperspectral_pipeline import HyperspectralProcessor

def test_pixxel_methane_plume_detection():
    proc = HyperspectralProcessor(300)
    baseline = [1.0] * 300
    spectral = [1.0] * 300

    # Simulate strong methane absorption in SWIR bands
    for b in range(210, 240):
        spectral[b] = 0.75 # 25% absorption dip

    res = proc.detect_methane_plume(spectral, baseline)
    assert res["methane_detected"] is True
    assert res["confidence_score"] > 0.8
