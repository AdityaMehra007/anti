"""
Tests for OMEGA GitHub Marketplace Autonomous Orchestrator
==========================================================
Comprehensive pytest test suite covering:
1. Marketplace catalog ingestion & category normalization
2. Actions vs Apps classification & metadata verification
3. S-Tier titans & verified creator attestation
4. SQLite FTS5 lightning search with category filters
5. Automated production workflow synthesis (Python, Node, Docker)
6. Static AST workflow security auditing (permissions, mutable tags, script injection)
7. Cross-dependency & pipeline topology graph
8. Multi-vault data exports (JSON, SQLite, CSV, Markdown, Graph)
9. 12-Phase Sovereign Lifecycle execution & manifest attestation
"""

import pytest
import os
import json
from pathlib import Path
from github_marketplace_orchestrator import (
    GitHubMarketplaceEngine,
    MarketplaceItem,
    WorkflowSynthesizer,
    WorkflowSecurityAuditor,
    engine,
    SQLITE_DB_PATH,
    MARKETPLACE_JSON_PATH,
    CATEGORIES_JSON_PATH,
    GRAPH_JSON_PATH,
    EXPORT_CSV_PATH,
    EXPORT_MD_PATH,
    MANIFEST_JSON_PATH
)


def test_marketplace_initialization():
    """Verify engine successfully assembled 360+ verified catalog items and 19 categories."""
    assert len(engine.items) >= 360
    assert len(engine.categories) >= 18
    assert engine.items["actions-checkout"].name == "Checkout"


def test_category_taxonomies():
    """Verify essential knowledge and operational domains are present."""
    required_cats = [
        "continuous-integration", "deployment", "security",
        "testing", "code-quality", "code-review", "dependency-management",
        "monitoring", "publishing", "utilities"
    ]
    for cat in required_cats:
        assert cat in engine.categories, f"Missing category: {cat}"
        assert engine.categories[cat]["item_count"] > 0
        assert engine.categories[cat]["action_count"] > 0


def test_actions_and_apps_classification():
    """Verify Actions and Apps are accurately distinguished and partitioned."""
    actions = [it for it in engine.items.values() if it.type == "action"]
    apps = [it for it in engine.items.values() if it.type == "app"]

    assert len(actions) >= 200
    assert len(apps) >= 100
    assert len(actions) + len(apps) == len(engine.items)


def test_s_tier_flagship_titans():
    """Verify flagship developer titans are indexed with verified badges and S-tier ratings."""
    s_tier_items = [it for it in engine.items.values() if it.tier == "S"]
    assert len(s_tier_items) >= 25

    flagship_ids = [
        "actions-checkout", "actions-setup-node", "actions-setup-python",
        "docker-build-push-action", "github-codeql-action", "app-dependabot"
    ]
    for fid in flagship_ids:
        assert fid in engine.items, f"Missing flagship: {fid}"
        item = engine.items[fid]
        assert item.tier == "S"
        assert item.verified_creator is True
        assert item.stars >= 1000


def test_sqlite_fts5_search():
    """Verify SQLite FTS5 search delivers sub-millisecond keyword and category filtering."""
    # 1. Search for 'docker'
    docker_results = engine.search(query="docker", limit=10)
    assert len(docker_results) >= 2
    assert any("docker" in r["name"].lower() or "docker" in r["description"].lower() for r in docker_results)

    # 2. Category filtered search
    sec_results = engine.search(query="scan", category="security", limit=10)
    assert len(sec_results) >= 1
    for r in sec_results:
        assert r["category"] == "security"

    # 3. Verified creator filter
    verified_results = engine.search(query="actions", verified_only=True, limit=10)
    assert len(verified_results) >= 1
    for r in verified_results:
        assert r["verified_creator"] == 1


def test_workflow_synthesizer_python():
    """Verify production Python workflow synthesizer enforces least privilege and SHA pinning."""
    yaml_code = WorkflowSynthesizer.synthesize("python", {"pin_sha": True, "security_scan": True, "cache": True})
    assert "name: CI - Python Suite" in yaml_code
    assert "permissions:" in yaml_code
    assert "contents: read" in yaml_code
    assert "concurrency:" in yaml_code
    assert "cancel-in-progress: true" in yaml_code
    assert "actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11" in yaml_code
    assert "aquasecurity/trivy-action" in yaml_code


def test_workflow_synthesizer_docker():
    """Verify Docker container packaging workflow synthesizer produces multi-platform build steps."""
    yaml_code = WorkflowSynthesizer.synthesize("docker", {"pin_sha": True})
    assert "Build & Publish Container Image" in yaml_code
    assert "packages: write" in yaml_code
    assert "docker/setup-buildx-action" in yaml_code
    assert "docker/login-action" in yaml_code
    assert "docker/build-push-action" in yaml_code


def test_workflow_security_auditor_hardened():
    """Verify a properly hardened workflow receives a perfect or near-perfect security score."""
    hardened_yaml = """
name: Production Hardened CI
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.7
      - run: echo "Secure execution"
"""
    report = WorkflowSecurityAuditor.audit_yaml(hardened_yaml)
    assert report["security_score"] == 100
    assert report["risk_level"] == "LOW"
    assert report["is_compliant"] is True
    assert report["findings_count"] == 0


def test_workflow_security_auditor_vulnerable():
    """Verify auditor catches mutable tags, missing permissions, and script injection risks."""
    vulnerable_yaml = """
name: Insecure Pipeline
on: [push, pull_request_target]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo ${{ github.event.issue.title }}
"""
    report = WorkflowSecurityAuditor.audit_yaml(vulnerable_yaml)
    assert report["security_score"] < 60
    assert report["risk_level"] in ["HIGH", "CRITICAL"]
    assert report["is_compliant"] is False

    rules = [f["rule"] for f in report["findings"]]
    assert "MISSING_EXPLICIT_PERMISSIONS" in rules
    assert "UNPINNED_ACTION_TAG" in rules
    assert "DANGEROUS_PULL_REQUEST_TARGET" in rules
    assert "POTENTIAL_SCRIPT_INJECTION" in rules
    assert "MISSING_JOB_TIMEOUT" in rules


def test_cross_category_graph():
    """Verify topological sequence graph links actions into cohesive pipelines."""
    assert len(engine.graph_edges) >= 15
    sample_edge = engine.graph_edges[0]
    assert "source" in sample_edge
    assert "target" in sample_edge
    assert sample_edge["source"] in engine.items
    assert sample_edge["target"] in engine.items


def test_data_vault_exports():
    """Verify all vault export files exist and contain valid structures."""
    engine.export_all()

    assert SQLITE_DB_PATH.exists() and SQLITE_DB_PATH.stat().st_size > 100000
    assert MARKETPLACE_JSON_PATH.exists() and MARKETPLACE_JSON_PATH.stat().st_size > 100000
    assert CATEGORIES_JSON_PATH.exists() and CATEGORIES_JSON_PATH.stat().st_size > 1000
    assert GRAPH_JSON_PATH.exists() and GRAPH_JSON_PATH.stat().st_size > 10000
    assert EXPORT_CSV_PATH.exists() and EXPORT_CSV_PATH.stat().st_size > 10000
    assert EXPORT_MD_PATH.exists() and EXPORT_MD_PATH.stat().st_size > 2000


def test_12_phase_sovereign_lifecycle():
    """Verify execution of full 12-phase sovereign lifecycle and manifest attestation."""
    manifest = engine.do_everything()

    assert manifest["status"] == "PASSED"
    assert manifest["total_phases_executed"] == 12
    assert manifest["total_phases"] == 12
    assert len(manifest["phases"]) == 12

    for p in manifest["phases"]:
        assert p["status"] == "PASSED"
        assert p["elapsed_seconds"] >= 0
        assert "evidence" in p

    assert MANIFEST_JSON_PATH.exists()
