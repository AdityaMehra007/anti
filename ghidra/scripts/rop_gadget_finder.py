"""
Ghidra SRE Script: ROP Gadget Finder
====================================
Disassembles executable segments to identify Return-Oriented Programming (ROP) gadgets
for exploit payload analysis and defense verification.
"""

def run_script(orch, binary_path):
    report = orch.analyze_binary(binary_path)
    return {
        "script": "rop_gadget_finder.py",
        "total_gadgets_found": len(report.rop_gadgets),
        "gadgets": [
            {
                "address": f"0x{g.address:08x}",
                "instructions": " ; ".join(g.instructions),
                "type": g.classification
            }
            for g in report.rop_gadgets
        ]
    }

if __name__ == "__main__":
    import sys
    from ghidra_orchestrator import GhidraOrchestrator
    target = sys.argv[1] if len(sys.argv) > 1 else "ghidra/samples/vulnerable_service.exe"
    print(run_script(GhidraOrchestrator(), target))
