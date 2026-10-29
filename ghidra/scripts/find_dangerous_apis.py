"""
Ghidra SRE Script: Find Dangerous APIs
=====================================
Scans program symbols and references for dangerous C/Win32 APIs prone to memory corruption
or command injection vulnerabilities.
"""

def run_script(orch, binary_path):
    report = orch.analyze_binary(binary_path)
    flagged = []
    for v in report.vulnerabilities:
        if "API" in v.rule_id:
            flagged.append({
                "api": v.function,
                "severity": v.severity,
                "remedy": v.mitigation_remedy
            })
    return {
        "script": "find_dangerous_apis.py",
        "total_flagged": len(flagged),
        "results": flagged
    }

if __name__ == "__main__":
    import sys
    from ghidra_orchestrator import GhidraOrchestrator
    target = sys.argv[1] if len(sys.argv) > 1 else "ghidra/samples/vulnerable_service.exe"
    print(run_script(GhidraOrchestrator(), target))
