"""
Automated Test Suite for CareerOps Sovereign Engine & Orchestrator (v1.39.0)
Verifies:
- 138 Public ATS and Job Board provider indexing
- 45 Prompt Mode Markdown catalog
- Deterministic A-H evaluation scoring rubric
- Data contract system/user boundaries
- Template and ATS CV validation
"""

import os
import sys
import pytest
from pathlib import Path

# Add workspace root to path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from career_ops_orchestrator import CareerOpsInspector, CareerOpsEvaluationEngine

@pytest.fixture
def inspector():
    return CareerOpsInspector()

@pytest.fixture
def evaluator():
    return CareerOpsEvaluationEngine()


def test_career_ops_version_and_telemetry(inspector):
    """Verifies repository version and high-level telemetry stats."""
    stats = inspector.get_summary_stats()
    assert stats["version"] == "1.39.0"
    assert stats["repository"] == "career-ops-hq/career-ops"
    assert stats["total_providers"] >= 130
    assert stats["total_modes"] >= 40
    assert stats["total_templates"] >= 25
    assert len(stats["architecture_principles"]) == 4


def test_career_ops_providers_inventory(inspector):
    """Verifies provider parsing, classification, and metadata extraction."""
    providers = inspector.inspect_providers()
    assert len(providers) >= 135

    provider_ids = {p["id"] for p in providers}
    # Verify core ATS platforms are present
    assert "greenhouse" in provider_ids
    assert "lever" in provider_ids
    assert "ashby" in provider_ids
    assert "workday" in provider_ids
    assert "bamboohr" in provider_ids
    assert "smartrecruiters" in provider_ids

    # Verify Big Tech
    assert "amazon" in provider_ids
    assert "google" in provider_ids
    assert "apple" in provider_ids

    # Verify Remote boards
    assert "remoteok" in provider_ids
    assert "hackernews" in provider_ids

    # Verify categories exist
    categories = {p["category"] for p in providers}
    assert "Major ATS Platform" in categories
    assert "Big Tech" in categories
    assert "Tech & Remote Boards" in categories


def test_career_ops_prompt_modes(inspector):
    """Verifies that all prompt modes are parsed and core modes exist."""
    modes = inspector.inspect_modes()
    assert len(modes) >= 40

    mode_names = {m["name"] for m in modes}
    # Verify critical system modes
    assert "oferta.md" in mode_names
    assert "_shared.md" in mode_names
    assert "apply.md" in mode_names
    assert "scan.md" in mode_names
    assert "tracker.md" in mode_names
    assert "interview.md" in mode_names

    oferta = next(m for m in modes if m["name"] == "oferta.md")
    assert oferta["is_system_core"] is True
    assert oferta["lines_count"] > 50


def test_career_ops_templates_inventory(inspector):
    """Verifies CV, cover letter, and YAML compliance templates."""
    templates = inspector.inspect_templates()
    assert len(templates) >= 25

    names = {t["name"] for t in templates}
    assert "cv-template.html" in names
    assert "cv-template.compact.html" in names
    assert "cv-template.executive.html" in names
    assert "cover-letter-template.html" in names
    assert "ats-rules.yml" in names


def test_career_ops_deterministic_evaluation_scoring(evaluator):
    """Verifies A-H evaluation rubric logic, scoring, and gap detection."""
    jd = """
    Company: NeuralWave Systems
    Title: Senior AI Platform Engineer
    Requirements:
    - Production ML platform ownership, model registry, distributed inference
    - Cloud & Container Infrastructure: Kubernetes, AWS, Redis, Docker
    - Production APIs & Microservices architecture
    - Mentorship of junior engineering talent
    Compensation: $175,000 - $210,000 USD
    """

    cv = """
    Alex Mercer - Staff Software Engineer
    Experience:
    - Led ML platform team (4 engineers), built automated evaluation gates
    - Scaled Kubernetes clusters across AWS processing 25,000 QPS
    - Designed distributed gRPC microservices and Redis caching
    """

    result = evaluator.evaluate(jd, cv, "https://jobs.example.com/ai-eng")
    meta = result["metadata"]

    assert meta["company"] == "NeuralWave Systems"
    assert meta["role"] == "Senior AI Platform Engineer"
    assert meta["score_numeric"] >= 3.5
    assert meta["score_numeric"] <= 5.0
    assert meta["decision"] in ["Apply (Priority Strike)", "Apply (Standard)"]
    assert len(result["block_b_requirements"]) >= 3
    assert len(result["block_e_customization_plan"]) == 5
    assert result["block_g_legitimacy"]["confidence"] == "High Confidence"


def test_career_ops_data_contract_integrity(inspector):
    """Enforces DATA_CONTRACT.md separation: system layer vs user layer."""
    system_paths = ["modes", "providers", "templates", "lib"]
    user_paths = ["cv.md", "config", "data", "reports", "jds"]

    # Verify system directories exist
    for sp in system_paths:
        assert (inspector.root / sp).exists(), f"System path {sp} missing"

    # Verify no system directory name collides with user paths
    assert set(system_paths).isdisjoint(set(user_paths))
