#!/usr/bin/env python3
"""
tests/test_career_command_center.py — Verification of Command Center HUD & Packaging
=====================================================================================
Tests:
  1. Career Command Center HTML document structure and essential elements.
  2. Integration of interview defense, offer calculator, and telemetry sections.
  3. Master export bundle archive verification including new assets.
"""

import pytest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def test_career_command_center_html_exists():
    hud_path = REPO_ROOT / "apps" / "job_application_studio" / "career_command_center.html"
    assert hud_path.exists(), "career_command_center.html must exist"
    content = hud_path.read_text(encoding="utf-8")
    
    # Must contain candidate profile elements
    assert "Aditya Mehra" in content
    assert "AERO India 2025" in content
    assert "Instawork" in content
    assert "99.2%" in content

    # Must contain functional tabs
    assert "tab-conquest" in content
    assert "tab-interview" in content
    assert "tab-negotiator" in content
    assert "tab-telemetry" in content

    # Must contain interactive calculator logic
    assert "calculateCounter" in content
    assert "loadInterviewBrief" in content

def test_master_bundle_contains_phase6_assets():
    bundle_path = REPO_ROOT / "applications_generated" / "ADITYA_MEHRA_GLOBAL_APPLICATIONS_BUNDLE.zip"
    assert bundle_path.exists(), "Master bundle zip must exist"
    assert bundle_path.stat().st_size > 1_000_000, "Bundle must be substantial"

    with zipfile.ZipFile(bundle_path, "r") as zf:
        namelist = zf.namelist()
        
        # Check portals
        assert "portals/career_command_center.html" in namelist or any("career_command_center.html" in n for n in namelist)
        assert "portals/bangalore_current_month_jobs.html" in namelist or any("bangalore_current_month_jobs.html" in n for n in namelist)
        
        # Check interview prep files
        interview_preps = [n for n in namelist if "interview_prep" in n]
        assert len(interview_preps) >= 3, f"Expected at least 3 interview prep packs, found {len(interview_preps)}"
