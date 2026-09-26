#!/usr/bin/env python3
"""
OMEGA ∞ AUTOMATED VERIFICATION SUITE
Verifies:
1. Constitutional integrity (all 120 sections present and non-empty).
2. Agent contracts for all 9 Executive Departments (Section 12 compliance).
3. Presence of all 6 core OMEGA SKILL.md files.
4. Command interpreter parsing for all 15 commands.
5. Section 107 reporting structure compliance (all 15 mandatory headers).
6. Section 77 High-Impact Approval System.
7. Observability daemon health check.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import os
import unittest
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from omega.core.omega_infinity_runtime import (
    OmegaCommandInterpreter,
    OmegaReportGenerator,
    HighImpactApprovalGate,
    OmegaInfinityRuntime
)
from omega.core.omega_monitor import OmegaMonitor

class TestOmegaInfinityArchitecture(unittest.TestCase):

    def setUp(self):
        self.constitution_path = os.path.join(BASE_DIR, "OMEGA_CONSTITUTION.md")

    def test_01_constitution_completeness(self):
        """Verify OMEGA_CONSTITUTION.md exists and contains all 120 sections (0 to 119)."""
        self.assertTrue(os.path.exists(self.constitution_path), "OMEGA_CONSTITUTION.md not found")
        with open(self.constitution_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertGreater(len(content), 15000, "Constitution is suspiciously short")

        # Verify all 120 numbered sections: # 0. through # 119.
        for section_num in range(120):
            pattern = rf"^# {section_num}\. "
            match = re.search(pattern, content, re.MULTILINE)
            self.assertIsNotNone(match, f"Missing Constitution Section: # {section_num}.")

    def test_02_executive_agents_contracts(self):
        """Verify all 9 executive agents exist and adhere to Section 12 Agent Contract."""
        agents = [
            "omega-executive-director.md",
            "omega-strategy.md",
            "omega-research.md",
            "omega-product.md",
            "omega-engineering.md",
            "omega-business.md",
            "omega-finance.md",
            "omega-security-redteam.md",
            "omega-governance.md"
        ]
        mandatory_contract_sections = [
            "MISSION",
            "INPUTS",
            "OUTPUTS",
            "TOOLS",
            "CONSTRAINTS",
            "SUCCESS CRITERIA",
            "FAILURE CONDITIONS",
            "ESCALATION RULES",
            "VERIFICATION METHOD"
        ]

        agents_dir = os.path.join(BASE_DIR, ".agents", "agents")
        for agent_file in agents:
            path = os.path.join(agents_dir, agent_file)
            self.assertTrue(os.path.exists(path), f"Agent contract missing: {agent_file}")
            with open(path, "r", encoding="utf-8") as f:
                agent_content = f.read()

            for sec in mandatory_contract_sections:
                self.assertIn(sec, agent_content, f"Agent {agent_file} is missing contract section: {sec}")

    def test_03_core_skills_presence(self):
        """Verify all 6 core OMEGA SKILL.md files exist and contain frontmatter."""
        skills = [
            "omega-operating-system",
            "omega-red-team",
            "omega-zero-to-one",
            "omega-reality-audit",
            "omega-automation-engine",
            "omega-capital-allocation"
        ]
        skills_dir = os.path.join(BASE_DIR, ".agents", "skills")
        for skill in skills:
            skill_path = os.path.join(skills_dir, skill, "SKILL.md")
            self.assertTrue(os.path.exists(skill_path), f"Skill missing: {skill}/SKILL.md")
            with open(skill_path, "r", encoding="utf-8") as f:
                skill_content = f.read()
            self.assertTrue(skill_content.startswith("---"), f"Skill {skill} missing YAML frontmatter")

    def test_04_command_interpreter_15_commands(self):
        """Verify that all 15 canonical commands parse into valid operating modes."""
        interpreter = OmegaCommandInterpreter()
        for cmd in OmegaCommandInterpreter.VALID_COMMANDS:
            res = interpreter.parse_command(cmd)
            self.assertEqual(res["command"], cmd)
            self.assertIn(res["active_mode_code"], OmegaCommandInterpreter.OPERATING_MODES)

    def test_05_section_107_reporting_structure(self):
        """Verify generated reports contain all 15 mandatory Section 107 headers."""
        reporter = OmegaReportGenerator()
        cmd_info = {
            "command": "FULL POWER",
            "active_mode_code": "M",
            "active_mode_name": "CEO"
        }
        report = reporter.generate_report(cmd_info, {})
        for header in OmegaReportGenerator.SECTION_HEADERS:
            self.assertIn(f"## {header}", report, f"Report missing mandatory header: ## {header}")

    def test_06_high_impact_approval_gate(self):
        """Verify Section 77 High-Impact Approval System blocks unauthorized actions."""
        # 1. Financial transfer must require human approval
        fin_check = HighImpactApprovalGate.check_authorization("FINANCIAL_TRANSFER", {"amount": 5000})
        self.assertFalse(fin_check["authorized"])
        self.assertTrue(fin_check["requires_human_approval"])

        # 2. Destructive delete must require human approval
        del_check = HighImpactApprovalGate.check_authorization("DESTRUCTIVE_DELETE", {"target": "data.db"})
        self.assertFalse(del_check["authorized"])
        self.assertTrue(del_check["requires_human_approval"])

        # 3. Read/Research action is authorized
        read_check = HighImpactApprovalGate.check_authorization("DATA_QUERY", {"query": "SELECT 1"})
        self.assertTrue(read_check["authorized"])
        self.assertFalse(read_check["requires_human_approval"])

    def test_07_monitor_health_check(self):
        """Verify Observability daemon health check runs clean."""
        monitor = OmegaMonitor()
        status = monitor.perform_health_check()
        self.assertIn(status["status"], ["HEALTHY", "DEGRADED"])
        self.assertTrue(status["checks"]["constitution"]["healthy"])
        self.assertTrue(status["checks"]["filesystem_writable"]["healthy"])


if __name__ == "__main__":
    unittest.main()
