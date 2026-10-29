"""
Unit Tests for NSA Ghidra Autonomous SRE Engine & Orchestrator
=============================================================
Verifies multi-format binary dissection, Sleigh disassembly, P-Code microcode generation,
pseudo-C decompilation, vulnerability detection, ROP gadget identification, and
the master 12-phase sovereign lifecycle.
"""

import os
import sys
import json
import unittest

from ghidra_orchestrator import (
    GhidraConfig,
    GhidraOrchestrator,
    BinaryDissector
)


class TestGhidraOrchestrator(unittest.TestCase):
    """Test suite for NSA Ghidra Autonomous SRE Suite."""

    @classmethod
    def setUpClass(cls):
        cls.orchestrator = GhidraOrchestrator()
        cls.sample_binary = os.path.abspath("ghidra/samples/vulnerable_service.exe")
        if not os.path.exists(cls.sample_binary):
            cls.orchestrator.do_everything(cls.sample_binary)

    def test_01_get_info_telemetry(self):
        """Verifies Ghidra engine version and supported ISAs."""
        info = self.orchestrator.get_info()
        self.assertIn("Ghidra", info["name"])
        self.assertEqual(info["version"], "11.1.2_PUBLIC")
        self.assertGreaterEqual(len(info["supported_processors"]), 5)
        self.assertEqual(info["pcode_operations_count"], 78)

    def test_02_binary_dissection(self):
        """Verifies PE32+ header dissection, sections, and mitigations."""
        report = self.orchestrator.analyze_binary(self.sample_binary)
        self.assertEqual(report.metadata.format, "PE32+")
        self.assertEqual(report.metadata.architecture, "x86_64")
        self.assertGreaterEqual(len(report.sections), 4)
        self.assertIn(".text", [s.name for s in report.sections])
        self.assertIn(".rdata", [s.name for s in report.sections])
        self.assertIn("sha256", report.metadata.hashes)

    def test_03_shannon_entropy(self):
        """Verifies Shannon entropy calculation on binary."""
        with open(self.sample_binary, "rb") as f:
            data = f.read()
        ent = BinaryDissector.calculate_entropy(data)
        self.assertGreater(ent, 0.0)
        self.assertLessEqual(ent, 8.0)

    def test_04_sleigh_disassembly(self):
        """Verifies Sleigh instruction decoding and P-Code generation."""
        instructions = self.orchestrator.disassemble(self.sample_binary, count=10)
        self.assertGreaterEqual(len(instructions), 5)
        first_instr = instructions[0]
        self.assertTrue(hasattr(first_instr, "mnemonic"))
        self.assertTrue(hasattr(first_instr, "pcode_ops"))

    def test_05_pcode_microcode_generation(self):
        """Verifies Ghidra P-Code micro-operation synthesis."""
        pcode = self.orchestrator.get_pcode(self.sample_binary, count=15)
        self.assertGreaterEqual(len(pcode), 5)
        self.assertIn("pcode_mnemonic", pcode[0])

    def test_06_decompiler_pseudo_c(self):
        """Verifies pseudo-C decompilation and variable recovery."""
        decomp = self.orchestrator.decompile_function(self.sample_binary, "main")
        self.assertEqual(decomp.name, "main")
        self.assertIn("int main", decomp.pseudo_c_code)
        self.assertIn("return 0;", decomp.pseudo_c_code)
        self.assertIn("uVar1", decomp.recovered_types)

    def test_07_strings_and_iocs(self):
        """Verifies string extraction and IOC categorization."""
        strings = self.orchestrator.extract_strings(self.sample_binary)
        self.assertGreaterEqual(len(strings), 5)
        categories = {s.category for s in strings}
        self.assertTrue("URL" in categories or "API_Name" in categories or "General" in categories)

    def test_08_vulnerability_and_rop_audit(self):
        """Verifies dangerous API flagging and ROP gadget extraction."""
        audit = self.orchestrator.audit_vulnerabilities(self.sample_binary)
        self.assertGreaterEqual(audit["findings_count"], 1)
        self.assertGreaterEqual(audit["rop_gadgets_count"], 1)

    def test_09_script_execution(self):
        """Verifies execution of Ghidra SRE analysis scripts."""
        res = self.orchestrator.run_script("ghidra/scripts/find_dangerous_apis.py", self.sample_binary)
        self.assertEqual(res["status"], "SUCCESS")

    def test_10_sovereign_12_phase_lifecycle(self):
        """Verifies the master 12-phase sovereign lifecycle produces valid manifest."""
        manifest = self.orchestrator.do_everything(self.sample_binary)
        self.assertEqual(manifest["total_phases_executed"], 12)
        self.assertIn("SOVEREIGN GHIDRA", manifest["overall_status"])
        for p in manifest["phases"]:
            self.assertEqual(p["status"], "PASSED")


if __name__ == "__main__":
    unittest.main()
