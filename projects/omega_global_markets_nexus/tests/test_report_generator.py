"""
Unit Tests for Executive Dossier & Report Generator
"""
import pytest
from pathlib import Path
from projects.omega_global_markets_nexus.reports.report_generator import generate_executive_dossier


def test_dossier_generation(tmp_path):
    res = generate_executive_dossier(output_dir=str(tmp_path))
    assert res["status"] == "DOSSIER_GENERATED"
    assert "cycle_id" in res
    assert Path(res["markdown_report_path"]).exists()

    content = Path(res["markdown_report_path"]).read_text(encoding="utf-8")
    assert "OMEGA" in content
    assert "Business Archetype In Focus" in content
    assert "SOFR Overnight Fixing" in content
