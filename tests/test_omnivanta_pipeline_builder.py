import os
import sys
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from omnivanta_pipeline_builder import (
    OmniVantaPipelineBuilder,
    ClientProspect,
    ProposalGenerator
)

@pytest.fixture
def sample_prospects():
    return [
        ClientProspect(
            company_id="PROSPECT-001",
            company_name="Apex Event Productions Pvt Ltd",
            industry="Experiential Marketing & Events",
            location="Bengaluru, Karnataka",
            estimated_annual_vendor_spend_inr=50000000.0, # 5 Cr spend
            contact_name="Rajesh Kumar",
            contact_title="Chief Operating Officer",
            contact_email="rajesh@apexevents.in",
            typical_leakage_pct=10.0
        ),
        ClientProspect(
            company_id="PROSPECT-002",
            company_name="Silicon Fleet & Warehousing LLP",
            industry="Commercial Logistics & Fleet",
            location="Bengaluru, Karnataka",
            estimated_annual_vendor_spend_inr=20000000.0, # 2 Cr spend
            contact_name="Priya Sharma",
            contact_title="Head of Procurement",
            contact_email="priya@siliconfleet.com",
            typical_leakage_pct=8.0
        )
    ]

def test_pipeline_builder_initialization(sample_prospects):
    builder = OmniVantaPipelineBuilder(sample_prospects)
    assert len(builder.prospects) == 2
    assert builder.total_pipeline_spend_inr() == 70000000.0

def test_estimated_recovery_calculation(sample_prospects):
    builder = OmniVantaPipelineBuilder(sample_prospects)
    est_recovery = builder.calculate_total_recoverable_capital_inr()
    # 50M * 10% = 5M, 20M * 8% = 1.6M => Total 6.6M INR
    assert est_recovery == 6600000.0

def test_contingency_pipeline_revenue(sample_prospects):
    builder = OmniVantaPipelineBuilder(sample_prospects)
    # Total recovery: 6.6M INR. Contingency fee @ 20% = 1.32M INR
    assert builder.calculate_total_contingency_revenue_inr(fee_pct=20.0) == 1320000.0

def test_proposal_generation(sample_prospects):
    p = sample_prospects[0]
    gen = ProposalGenerator(fee_pct=20.0)
    proposal = gen.generate_proposal(p)
    assert p.company_name in proposal
    assert "INR 50,000,000.00" in proposal
    assert "INR 5,000,000.00" in proposal
    assert "20.0% Success-Based Contingency Fee" in proposal
    assert "Zero Out-of-Pocket Expense" in proposal

def test_pipeline_export_json(sample_prospects, tmp_path):
    builder = OmniVantaPipelineBuilder(sample_prospects)
    export_path = tmp_path / "prospects.json"
    builder.export_json(str(export_path))
    assert export_path.exists()
    assert "Apex Event Productions Pvt Ltd" in export_path.read_text(encoding="utf-8")
