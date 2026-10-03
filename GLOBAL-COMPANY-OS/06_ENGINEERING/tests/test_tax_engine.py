import pytest
import os
import sys

finance_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "11_FINANCE"))
sys.path.insert(0, finance_dir)
from tax_engine import TaxEngine

def test_tax_engine_intrastate():
    res = TaxEngine.compute_invoice_taxes(25000.0, is_interstate=False)
    assert res["taxable_value"] == 25000.0
    assert res["cgst"] == 2250.0
    assert res["sgst"] == 2250.0
    assert res["igst"] == 0.0
    assert res["total_invoice"] == 29500.0

def test_tax_engine_interstate():
    res = TaxEngine.compute_invoice_taxes(50000.0, is_interstate=True)
    assert res["taxable_value"] == 50000.0
    assert res["igst"] == 9000.0
    assert res["cgst"] == 0.0
    assert res["sgst"] == 0.0
    assert res["total_invoice"] == 59000.0

def test_tax_engine_margins():
    res = TaxEngine.compute_net_burn_and_profit(100000.0, 11400.0)
    assert res["gross_revenue"] == 100000.0
    assert res["direct_costs"] == 11400.0
    assert res["gross_profit"] == 88600.0
    assert res["gross_margin_pct"] == 88.6