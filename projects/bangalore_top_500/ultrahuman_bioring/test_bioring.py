import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from biomarker_engine import MetabolicSynthesizer

def test_ultrahuman_metabolic_scoring():
    synth = MetabolicSynthesizer()
    # High recovery state
    res = synth.compute_metabolic_score(glucose_mg_dl=92.0, hrv_ms=75.0, skin_temp_delta_c=-0.1)
    assert res["status"] == "OPTIMAL"
    assert res["metabolic_score"] >= 85.0

    # High glucose spike & elevated temperature (stress/illness)
    stressed = synth.compute_metabolic_score(glucose_mg_dl=165.0, hrv_ms=25.0, skin_temp_delta_c=1.2)
    assert stressed["status"] == "RECOVERY_NEEDED"
    assert stressed["metabolic_score"] < 60.0
