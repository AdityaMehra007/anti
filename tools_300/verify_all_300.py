#!/usr/bin/env python3
"""
Antigravity 300 Tools Verification Test Suite
Executes all 300 tools synchronously in test mode, validates JSON outputs and status codes.
"""

import os
import sys
import json
import time
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(BASE_DIR, "manifest.json")

def verify_all():
    if not os.path.exists(MANIFEST_PATH):
        print(f"Error: Manifest not found at {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(1)
        
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    tools = manifest.get("tools", [])
    total = len(tools)
    
    print(f"\n=======================================================")
    print(f"  STARTING FULL TEST SUITE VERIFICATION OF {total} TOOLS")
    print(f"=======================================================\n")
    
    passed = 0
    failed = 0
    start_total_time = time.time()
    
    results_summary = []
    
    for idx, tool in enumerate(tools, 1):
        rel_path = tool["relative_path"]
        full_path = os.path.join(BASE_DIR, rel_path)
        tool_id = tool["tool_id"]
        slug = tool["slug"]
        
        t0 = time.time()
        res = subprocess.run([sys.executable, full_path, "--test"], capture_output=True, text=True)
        dur_ms = round((time.time() - t0) * 1000, 2)
        
        is_success = False
        error_msg = ""
        
        if res.returncode == 0:
            try:
                data = json.loads(res.stdout)
                if data.get("status") == "SUCCESS" and "results" in data:
                    is_success = True
                else:
                    error_msg = f"Unexpected payload: {res.stdout[:100]}"
            except Exception as e:
                error_msg = f"JSON Parse error: {str(e)}"
        else:
            error_msg = f"Exit code {res.returncode}: {res.stderr[:100]}"
            
        if is_success:
            passed += 1
            status_str = "PASS"
        else:
            failed += 1
            status_str = "FAIL"
            
        results_summary.append({
            "tool_id": tool_id,
            "slug": slug,
            "domain_id": tool["domain_id"],
            "status": status_str,
            "duration_ms": dur_ms,
            "error": error_msg if not is_success else None
        })
        
        if idx % 30 == 0 or idx == total or not is_success:
            print(f"[{idx:>3}/{total}] Tool #{tool_id:03d} ({slug:<32}) ... {status_str} ({dur_ms:>5.1f}ms)")
            
    total_elapsed = round(time.time() - start_total_time, 2)
    
    print("\n=======================================================")
    print(f"  VERIFICATION RUN COMPLETE")
    print(f"  Total Tools Tested: {total}")
    print(f"  Passed:             {passed}")
    print(f"  Failed:             {failed}")
    print(f"  Success Rate:       {round((passed/total)*100, 2)}%")
    print(f"  Total Execution:    {total_elapsed}s")
    print("=======================================================\n")
    
    # Save verification report
    report_path = os.path.join(BASE_DIR, "verification_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_tools": total,
            "passed": passed,
            "failed": failed,
            "success_rate_percent": round((passed/total)*100, 2),
            "total_execution_seconds": total_elapsed,
            "results": results_summary
        }, f, indent=2)
        
    return failed == 0

if __name__ == "__main__":
    success = verify_all()
    sys.exit(0 if success else 1)
