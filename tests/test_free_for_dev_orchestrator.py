"""
Tests for OMEGA Free-For-Dev Autonomous Developer Cloud & Zero-Dollar Stack Orchestrator
========================================================================================
Tests category extraction, quota parsing, no-credit-card filtering, zero-dollar stack
synthesis, architecture feasibility audit, and 12-phase sovereign lifecycle.
"""

import pytest
import os
import json
from pathlib import Path
from free_for_dev_orchestrator import (
    FreeForDevOrchestrator,
    FreeService,
    CATALOG_JSON_PATH,
    SQLITE_DB_PATH,
    MANIFEST_JSON_PATH
)


@pytest.fixture
def orchestrator():
    return FreeForDevOrchestrator()


def test_free_for_dev_initialization(orchestrator):
    """Verify engine loaded upstream free-for-dev catalog."""
    assert len(orchestrator.services) >= 1300
    assert len(orchestrator.categories) >= 50


def test_flagship_and_no_card_services(orchestrator):
    """Verify flagship providers and no-credit-card filtering."""
    no_card = [s for s in orchestrator.services.values() if not s.requires_credit_card]
    assert len(no_card) >= 1000
    names = [s.name.lower() for s in orchestrator.services.values()]
    assert any("cloudflare" in n for n in names)
    assert any("github" in n for n in names)
    assert any("supabase" in n for n in names)


def test_zero_dollar_stack_synthesis(orchestrator):
    """Verify automated stack synthesis produces viable architectures."""
    stack = orchestrator.architect_zero_dollar_stack(archetype="saas_mvp")
    assert "services" in stack
    assert len(stack["services"]) >= 3
    assert stack["estimated_commercial_monthly_value_usd"] > 0


def test_free_for_dev_search(orchestrator):
    """Verify search capability."""
    res = orchestrator.search_services("database")
    assert len(res) > 0


def test_free_for_dev_12_phase_lifecycle(orchestrator):
    """Verify 12-phase lifecycle execution."""
    manifest = orchestrator.do_everything()
    assert manifest["total_phases_executed"] == 12
    assert "SOVEREIGN FREE-FOR-DEV SUITE OPERATIONAL" in manifest["overall_status"]
    assert MANIFEST_JSON_PATH.exists()
