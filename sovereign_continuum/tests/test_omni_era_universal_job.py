"""
Unit tests for the Omni-Era Universal Job Engine.
Verifies the execution of THE OMNI-ERA UNIVERSAL MASTER PROMPT.
"""

import os
import json
import pytest
from omni_era_universal_job import OmniEraUniversalJobEngine


def test_omni_era_job_initialization():
    engine = OmniEraUniversalJobEngine()
    assert len(engine.departments) == 12
    assert "DEPT-BIO-TRANSCENDENCE" in engine.departments
    assert "DEPT-ETERNAL-VIGIL" in engine.departments
    assert engine.generator.problem_graph.total_count() >= 12


def test_master_prompt_integrity():
    engine = OmniEraUniversalJobEngine()
    prompt_info = engine.load_master_prompt()
    assert prompt_info["status"] == "VALIDATED_AND_ACTIVE"
    assert prompt_info["line_count"] > 100
    assert prompt_info["byte_size"] > 5000


def test_execute_omni_job():
    engine = OmniEraUniversalJobEngine()
    ledger = engine.execute_omni_job()

    assert ledger["job_id"] == "Ω-MASTER-JOB-001"
    assert ledger["summary_metrics"]["departments_active"] == 12
    assert ledger["summary_metrics"]["universal_flourishing_index_phi"] > 99.0
    assert ledger["summary_metrics"]["net_suffering_index_s"] < 1.0
    assert len(ledger["era_flourishing_metrics"]) == 7

    # Verify JSON persistence
    assert os.path.exists("OMNI_ERA_JOB_EXECUTION_LEDGER.json")
    with open("OMNI_ERA_JOB_EXECUTION_LEDGER.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["job_codename"] == "PROJECT PAN-SENTIENT OMNI-GENESIS"
    assert len(data["master_departments"]) == 12
