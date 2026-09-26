import os
import sys
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from omega_dispatch_console import OmegaDispatchConsole

def test_console_initialization():
    console = OmegaDispatchConsole()
    assert len(console.jobs) >= 60
    assert console.get_job("BLR-JOB-001") is not None
    assert console.get_job("BLR-JOB-001")["company"] == "Accenture India"

def test_filter_by_tier():
    console = OmegaDispatchConsole()
    tier_s = console.filter_by_tier("Tier S")
    tier_a = console.filter_by_tier("Tier A")
    tier_b = console.filter_by_tier("Tier B")
    assert len(tier_s) > 0
    assert len(tier_a) > 0
    assert len(tier_b) > 0
    assert len(tier_s) + len(tier_a) + len(tier_b) == len(console.jobs)

def test_get_job_summary():
    console = OmegaDispatchConsole()
    job = console.get_job("BLR-JOB-011") # Puma India
    assert job is not None
    assert "Puma" in job["company"]
    summary = console.render_job_card(job)
    assert "BLR-JOB-011" in summary
    assert "Puma" in summary
    assert "Cover Letter" in summary or "Application" in summary
