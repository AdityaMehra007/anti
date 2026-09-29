"""
Test Suite for Terra Kinetics Unified CLI.
"""

import pytest
import subprocess
import sys


def test_cli_help():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Terra Kinetics Unified CLI" in result.stdout
    assert "--frontier" in result.stdout
    assert "--mesh-cycle" in result.stdout


def test_cli_demo():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--demo"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Real-Time 200 Hz Edge Cycle Demonstration" in result.stdout
    assert "Cryptographic Invoice Generated" in result.stdout


def test_cli_pilots():
    for pilot in ["bmw", "dhl"]:
        result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--pilot", pilot], capture_output=True, text=True)
        assert result.returncode == 0
        assert "PASSED [GREEN]" in result.stdout


def test_cli_financial_sim():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--run-sim"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Year 10 Target Implied Valuation" in result.stdout


def test_cli_mesh_cycle():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--mesh-cycle"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Executing Autonomous Executive Agent Mesh Cycle" in result.stdout
    assert "COMPLETED_NOMINAL" in result.stdout


def test_cli_frontier_all():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--frontier", "all"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Year 10 Target Implied Valuation" in result.stdout
    assert "Year 10 Aether Implied Valuation" in result.stdout
    assert "Year 10 Bioma Implied Valuation" in result.stdout


def test_cli_continuum():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--continuum"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Initializing Project Continuum" in result.stdout
    assert "Settled M2M Tx" in result.stdout


def test_cli_atlas():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--atlas"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "GLOBAL ECONOMIC LEDGER" in result.stdout
    assert "United States" in result.stdout
    assert "G7 Bloc" in result.stdout
    assert "BRICS Core" in result.stdout


def test_cli_empire_cycle():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--empire-cycle"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "CONSOLIDATED EMPIRE OPERATIONAL CYCLE" in result.stdout
    assert "Consolidated Gross Revenue" in result.stdout
    assert "Consolidated Enterprise Valuation" in result.stdout


def test_cli_skills_audit():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--skills-audit"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "AUTONOMOUS TRILLION-DOLLAR EMPIRE AGENT SKILLS AUDIT" in result.stdout
    assert "10/10 Verified Clean" in result.stdout


def test_cli_red_team():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--red-team"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "PLANETARY ADVERSARIAL STRESS-TEST PROBES" in result.stdout
    assert "HARDENED_RESILIENT" in result.stdout


def test_cli_banking():
    result = subprocess.run([sys.executable, "-m", "terra_kinetics.cli", "--banking"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "BANK OF THE CONTINUUM" in result.stdout
    assert "CONTUS33XXX" in result.stdout
    assert "SETTLED_REAL_TIME" in result.stdout




