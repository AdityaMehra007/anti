"""
Unit tests for Plane Autonomous Worker execution loop (plane_autonomous_worker.py)
"""
import pytest
from omega.orchestration.plane_autonomous_worker import PlaneAutonomousWorker

def test_autonomous_worker_task_detection():
    worker = PlaneAutonomousWorker(dry_run=True)
    
    # Non-agent task
    issue_regular = {
        "id": "iss-001",
        "name": "Design button layout",
        "description_raw": "Make it blue"
    }
    assert worker.should_execute_task(issue_regular) is False

    # Autonomous bot task
    issue_auto = {
        "id": "iss-002",
        "name": "[AUTONOMOUS] Run unit test suite and verify linter",
        "description_raw": "Task: run verification and report"
    }
    assert worker.should_execute_task(issue_auto) is True

def test_autonomous_worker_execute_and_report():
    worker = PlaneAutonomousWorker(dry_run=True)
    issue = {
        "id": "iss-105",
        "project_id": "CORE",
        "name": "[AUTONOMOUS] Health check and system verification",
        "description_raw": "Execute system diagnostic and return evidence."
    }
    
    res = worker.process_autonomous_issue(issue, workspace_slug="omega")
    assert res["status"] == "completed"
    assert res["issue_id"] == "iss-105"
    assert "execution_summary" in res
    assert "exit_code" in res
