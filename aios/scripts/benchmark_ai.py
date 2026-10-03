#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Repeatable Local AI Benchmark Harness
Measures Tokens Per Second (TPS), Time to First Token (TTFT),
VRAM consumption on GTX 960M, and records benchmarks to SQLite master.db.
Zero-Dependency (Pure Python Standard Library).
"""

import sys
import os
import time
import json
import urllib.request
import urllib.error
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "databases"))
sys.path.insert(0, str(AIOS_ROOT / "scripts"))

try:
    import db
except ImportError:
    db = None

try:
    import health_check
except ImportError:
    health_check = None

OLLAMA_URL = "http://127.0.0.1:11434"

def get_vram_used_mb() -> float:
    """Queries NVIDIA SMI for discrete GTX 960M VRAM usage."""
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=3
        )
        if res.returncode == 0 and res.stdout.strip():
            return float(res.stdout.strip().split("\n")[0])
    except Exception:
        pass
    return 0.0

def run_benchmark(model: str = "qwen2.5-coder:3b") -> Optional[Dict[str, Any]]:
    """Runs a standardized generation benchmark against the local Ollama instance."""
    print("===============================================================================")
    print(f"       ANTIGRAVITY OMEGA :: LOCAL AI BENCHMARK :: {model}")
    print("===============================================================================")

    # 1. Check Ollama connectivity
    if not health_check or not health_check.check_port("127.0.0.1", 11434):
        print(f"[!] Ollama is not active on {OLLAMA_URL}.")
        print("    Attempting to launch Ollama via omega_ctl.py start-ai...")
        subprocess.run([sys.executable, str(AIOS_ROOT / "scripts" / "omega_ctl.py"), "start-ai"])
        time.sleep(3)
        if not health_check.check_port("127.0.0.1", 11434):
            print("[ERROR] Could not start Ollama. Aborting benchmark.")
            return None

    # 2. Check model availability
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            available = [m["name"] for m in data.get("models", [])]
            print(f"[*] Available local models: {', '.join(available)}")
            if model not in available and f"{model}:latest" not in available:
                # Find best fallback
                matching = [m for m in available if "qwen" in m or "llama" in m]
                if matching:
                    model = matching[0]
                    print(f"[*] Using installed model: {model}")
                else:
                    print(f"[ERROR] Model '{model}' not found in Ollama repository.")
                    return None
    except Exception as e:
        print(f"[ERROR] Failed to query Ollama tags: {e}")
        return None

    vram_before = get_vram_used_mb()
    print(f"[*] GPU VRAM before model load: {vram_before} MB")

    # 3. Standard coding task prompt
    prompt = (
        "Write an efficient Python implementation of the Quicksort algorithm with Dutch National Flag 3-way partitioning. "
        "Include docstrings and type annotations."
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 512,
            "temperature": 0.2
        }
    }

    print(f"[*] Dispatching test prompt ({len(prompt.split())} words) to {model}...")
    t0 = time.time()
    
    try:
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw_resp = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[ERROR] Inference request failed: {e}")
        return None

    t_total = time.time() - t0
    vram_during = get_vram_used_mb()

    # Ollama returns nanosecond metrics: eval_count, eval_duration, prompt_eval_duration
    eval_count = raw_resp.get("eval_count", 0)
    eval_duration_ns = raw_resp.get("eval_duration", 1)
    prompt_eval_duration_ns = raw_resp.get("prompt_eval_duration", 0)

    tps = round(eval_count / (eval_duration_ns / 1e9), 2) if eval_duration_ns > 0 else 0.0
    ttft_ms = round(prompt_eval_duration_ns / 1e6, 2)
    vram_delta = max(0.0, vram_during - vram_before)

    print("\n-------------------------------------------------------------------------------")
    print("Benchmark Telemetry Results:")
    print(f"  * Target Model          : {model}")
    print(f"  * Generated Tokens      : {eval_count} tokens")
    print(f"  * Total Wall Time       : {t_total:.2f} seconds")
    print(f"  * Time To First Token   : {ttft_ms:.1f} ms")
    print(f"  * Token Velocity (TPS)  : {tps} tokens/sec")
    print(f"  * Peak VRAM Consumed    : {vram_during} MB (Delta: +{vram_delta} MB)")
    print("-------------------------------------------------------------------------------")

    # Record benchmark in SQLite database
    if db:
        try:
            details = json.dumps({
                "model": model,
                "eval_tokens": eval_count,
                "tps": tps,
                "ttft_ms": ttft_ms,
                "vram_mb": vram_during,
                "vram_delta_mb": vram_delta
            })
            db.log_audit("BENCHMARK", "RUN_BENCHMARK", "AI_INFERENCE", details, "INFO")
            print("[OK] Benchmark receipt permanently recorded in SQLite master.db.")
        except Exception as e:
            print(f"[!] Could not record to audit log: {e}")

    print("===============================================================================\n")
    return {
        "model": model,
        "eval_count": eval_count,
        "tps": tps,
        "ttft_ms": ttft_ms,
        "vram_during_mb": vram_during,
        "vram_delta_mb": vram_delta,
        "response_sample": raw_resp.get("response", "")[:120] + "..."
    }

if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5-coder:3b"
    res = run_benchmark(m)
    if res:
        sys.exit(0)
    else:
        sys.exit(1)
