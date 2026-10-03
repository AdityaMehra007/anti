"""
Unit tests for Fault-Tolerant Daemon Supervisor (omega_supervisor.py)
"""
import os
import sys
import time
import pytest

from aios.services.omega_supervisor import ServiceConfig, SupervisorManager

def test_service_config_initialization():
    svc = ServiceConfig(
        name="test_service",
        command=[sys.executable, "-c", "import time; time.sleep(0.1)"],
        port=9999,
        auto_restart=True,
        max_restarts=3
    )
    assert svc.name == "test_service"
    assert svc.port == 9999
    assert svc.auto_restart is True
    assert svc.max_restarts == 3
    assert svc.restart_count == 0

def test_supervisor_manager_start_and_status():
    manager = SupervisorManager()
    
    # Add a short-lived test dummy service
    manager.register_service(
        name="dummy_alive",
        command=[sys.executable, "-c", "import time; time.sleep(0.5)"],
        port=9998,
        auto_restart=False
    )
    
    status = manager.get_status()
    assert "dummy_alive" in status
    assert status["dummy_alive"]["running"] is False
    
    # Start service
    manager.start_service("dummy_alive")
    time.sleep(0.1)
    status = manager.get_status()
    assert status["dummy_alive"]["running"] is True
    
    # Stop service
    manager.stop_service("dummy_alive")
    status = manager.get_status()
    assert status["dummy_alive"]["running"] is False

def test_supervisor_manager_all_configured_services():
    manager = SupervisorManager()
    manager.load_default_services()
    status = manager.get_status()
    
    # Expect standard core services defined
    assert "aios_gateway" in status
    assert "tradenexus_api" in status
    assert "plane_webhook_reactor" in status
