import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pytest
from reconciler import OmniReconciler

def test_omniledger_reconciliation():
    rec = OmniReconciler()
    rec.ingest_phonepe_event("RRN-1001", 450.0, "SUCCESS")
    rec.ingest_bank_clearing("RRN-1001", 450.0, "SUCCESS")

    rec.ingest_phonepe_event("RRN-1002", 1200.0, "SUCCESS")
    rec.ingest_bank_clearing("RRN-1002", 1200.0, "FAILURE") # Bank timed out

    matched, discrepancies = rec.reconcile_all()
    assert "RRN-1001" in matched
    assert "RRN-1002" in discrepancies
