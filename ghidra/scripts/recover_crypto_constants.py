"""
Ghidra SRE Script: Recover Cryptographic Constants
==================================================
Identifies cryptographic algorithm signatures in binary image:
- AES Rijndael Substitution Box (S-Box)
- SHA-256 initial hash values
- MD5 initial state words
- RC4 Key Scheduling Algorithm permutations
"""

def run_script(orch, binary_path):
    report = orch.analyze_binary(binary_path)
    crypto_hits = []
    for v in report.vulnerabilities:
        if "CRYPTO" in v.rule_id:
            crypto_hits.append({
                "primitive": v.title,
                "address": f"0x{v.address:08x}",
                "evidence": v.evidence
            })
    return {
        "script": "recover_crypto_constants.py",
        "crypto_algorithms_detected": len(crypto_hits),
        "results": crypto_hits
    }

if __name__ == "__main__":
    import sys
    from ghidra_orchestrator import GhidraOrchestrator
    target = sys.argv[1] if len(sys.argv) > 1 else "ghidra/samples/vulnerable_service.exe"
    print(run_script(GhidraOrchestrator(), target))
