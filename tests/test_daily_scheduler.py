"""Tests for the DailyScheduler module."""
import os
import pytest
from omnimoney.daily_scheduler import DailyScheduler


def test_scheduler_initialization(tmp_path):
    reports_dir = str(tmp_path / "daily_reports")
    scheduler = DailyScheduler(reports_dir=reports_dir)
    assert os.path.exists(reports_dir)
    assert scheduler.engine is not None
    assert scheduler.sales is not None


def test_run_daily_cycle(tmp_path):
    reports_dir = str(tmp_path / "daily_reports")
    scheduler = DailyScheduler(reports_dir=reports_dir)
    result = scheduler.run_daily_cycle()

    assert result["status"] == "SUCCESS"
    assert "date" in result
    assert result["prospects_mined"] >= 0

    # Verify generated files exist
    assert os.path.exists(result["brief_file"])
    assert os.path.exists(result["hit_list_file"])
    assert os.path.exists(result["scripts_file"])

    with open(result["hit_list_file"], "r", encoding="utf-8") as f:
        hit_list_text = f.read()
        assert "PROSPECT HIT LIST" in hit_list_text

    with open(result["scripts_file"], "r", encoding="utf-8") as f:
        scripts_text = f.read()
        assert "READY-TO-SEND OUTREACH SCRIPTS" in scripts_text
