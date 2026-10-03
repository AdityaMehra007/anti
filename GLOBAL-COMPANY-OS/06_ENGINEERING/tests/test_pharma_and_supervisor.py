import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "25_AUTOMATIONS")))

from src.pharma_fda_connector import PharmaFDAConnector
from sovereign_operations_supervisor import SovereignOperationsSupervisor

def test_pharma_fda_connector():
    items = [
        {"item_id": "DRL-01", "product_name": "Omeprazole Delayed-Release Capsules", "hs_code": "30049099"}
    ]
    rep = PharmaFDAConnector.audit_pharma_export(
        docket_id="DOC-DRL-USA-01",
        exporter_name="Dr. Reddy's Laboratories Limited",
        destination_country="USA",
        items=items
    )
    assert rep.docket_id == "DOC-DRL-USA-01"
    assert rep.overall_status == "PHARMA_CLEARED_READY_FOR_FLIGHT"
    assert rep.fda_prior_notice_token.startswith("FDA-PN-2027-")
    assert len(rep.cold_chain_validation_hash) == 64

def test_sovereign_supervisor_health_cycle():
    res = SovereignOperationsSupervisor.run_health_cycle()
    assert res["monitored_conglomerates"] == 7
    assert res["active_contracted_arr_inr"] == 10500000
    assert res["supervision_status"] == "AUTONOMOUS_NORMAL"
