import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from contract_synth import ApiMeshSynthesizer

def test_api_mesh_contract_evolution():
    mesh = ApiMeshSynthesizer()
    mesh.register_endpoint("/v1/payments", "POST", ["amount", "currency"], schema_version=1)

    # Non-breaking update: same required params
    is_breaking, diff = mesh.check_breaking_changes("/v1/payments", "POST", ["amount", "currency"])
    assert is_breaking is False
    assert len(diff) == 0

    # Breaking update: added new mandatory parameter "merchant_id"
    is_breaking_new, diff_new = mesh.check_breaking_changes("/v1/payments", "POST", ["amount", "currency", "merchant_id"])
    assert is_breaking_new is True
    assert "merchant_id" in diff_new
