"""
Ghidra SRE Script: Entropy & Packer Detector
============================================
Performs section-by-section Shannon entropy mapping to distinguish native compiled code
from compressed, packed (UPX, Themida, VMProtect), or encrypted binary blocks.
"""

def run_script(orch, binary_path):
    report = orch.analyze_binary(binary_path)
    sections_entropy = [
        {
            "section": s.name,
            "entropy": s.entropy,
            "is_packed": s.is_suspicious_or_packed,
            "flags": s.characteristics_flags
        }
        for s in report.sections
    ]
    return {
        "script": "entropy_packer_detector.py",
        "overall_entropy": report.overall_entropy,
        "packer_verdict": report.packer_detection["verdict"],
        "sections": sections_entropy
    }

if __name__ == "__main__":
    import sys
    from ghidra_orchestrator import GhidraOrchestrator
    target = sys.argv[1] if len(sys.argv) > 1 else "ghidra/samples/vulnerable_service.exe"
    print(run_script(GhidraOrchestrator(), target))
