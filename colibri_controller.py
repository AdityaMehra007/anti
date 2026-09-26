#!/usr/bin/env python3
"""
colibri_controller.py — Unified Colibrì Management Controller for OMEGA / e:\\anti.

Coordinates model downloads, hardware profiling, resource planning, and
server/web dashboard lifecycle management.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COLIBRI_DIR = ROOT / "colibri"
C_DIR = COLIBRI_DIR / "c"
MODELS_DIR = ROOT / "models"

# Recommended open-weights MoE models for consumer hardware
RECOMMENDED_MODELS = {
    "qwen36": {
        "id": "Kreuzzelg/qwen36-35b-a3b-colibri-i4-gs64",
        "description": "Qwen 3.6 35B-A3B colibri int4 gs64 — Pre-converted 23 GB MoE. Ideal balance of size, speed, and intelligence.",
        "size_gb": 23,
        "arch": "qwen36",
        "engine": "qwen36.exe"
    },
    "glm53_flash": {
        "id": "Justvugg/GLM-5.3-Flash-colibri-int4-g64",
        "description": "GLM-5.3 Flash colibri int4 gs64 (Z.ai / Justvugg) — 194 GB frontier MoE.",
        "size_gb": 195,
        "arch": "glm53",
        "engine": "glm53.exe"
    },
    "glm52_i4": {
        "id": "mastouri/GLM-5.2-colibri-int4-g64-with-int8-mtp",
        "description": "GLM-5.2 colibri int4 gs64 with int8 MTP (Z.ai) — 372 GB flagship 744B MoE with speculative decoding.",
        "size_gb": 372,
        "arch": "glm",
        "engine": "colibri.exe"
    }
}


def get_hardware_profile():
    """Detect available CPU, RAM, and drive capacity."""
    profile = {
        "platform": sys.platform,
        "python": sys.version.split()[0],
        "ram_gb": None,
        "disk_free_gb": None,
        "tools_ready": False,
        "engines": []
    }
    
    # Check disk space on drive hosting ROOT
    try:
        usage = shutil.disk_usage(ROOT)
        profile["disk_free_gb"] = round(usage.free / (1024 ** 3), 1)
        profile["disk_total_gb"] = round(usage.total / (1024 ** 3), 1)
    except Exception:
        pass

    # Check RAM
    try:
        import psutil
        profile["ram_gb"] = round(psutil.virtual_memory().total / (1024 ** 3), 1)
    except ImportError:
        # Fallback for Windows
        if sys.platform == "win32":
            try:
                import ctypes
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                profile["ram_gb"] = round(stat.ullTotalPhys / (1024 ** 3), 1)
                profile["ram_avail_gb"] = round(stat.ullAvailPhys / (1024 ** 3), 1)
            except Exception:
                pass

    # Check built engines
    if C_DIR.exists():
        for p in C_DIR.glob("*.exe"):
            profile["engines"].append(p.name)

    compiler = COLIBRI_DIR / "tools" / "w64devkit" / "bin" / "gcc.exe"
    profile["compiler_ready"] = compiler.exists() or shutil.which("gcc") is not None

    return profile


def run_doctor(model_dir=None):
    """Run the official coli doctor diagnostics."""
    cmd = [sys.executable, str(C_DIR / "coli"), "doctor"]
    if model_dir:
        cmd.extend(["--model", str(model_dir)])
    cmd.extend(["--gpu", "none"])
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)


def run_iobench(size_mb=64):
    """Run a high-speed disk I/O benchmark using iobench.exe."""
    exe = C_DIR / "iobench.exe"
    if not exe.exists():
        print(f"iobench.exe not found at {exe}. Compiling...")
        subprocess.run(["make", "-C", str(C_DIR), "iobench.exe"])

    test_file = ROOT / "colibri_disk_test.tmp"
    try:
        print(f"Creating temporary benchmark file ({size_mb} MB) at {test_file}...")
        with open(test_file, "wb") as f:
            f.write(b"\x00" * (size_mb * 1024 * 1024))
        print("Benchmarking sequential streaming throughput...")
        subprocess.run([str(exe), str(test_file), "4", "16", "4", "0"])
    finally:
        if test_file.exists():
            test_file.unlink()


def launch_web(model_dir=None, port=8000):
    """Launch the unified OpenAI-compatible server and web dashboard."""
    cmd = [sys.executable, str(C_DIR / "coli"), "web", "--port", str(port)]
    if model_dir:
        cmd.extend(["--model", str(model_dir)])
    cmd.extend(["--gpu", "none"])
    print(f"Launching Colibrì Web Dashboard on http://127.0.0.1:{port}...")
    subprocess.run(cmd)


def download_model(model_key="olmoe", target_dir=None):
    """Download a model using huggingface_hub."""
    if model_key not in RECOMMENDED_MODELS:
        print(f"Unknown model key '{model_key}'. Options: {list(RECOMMENDED_MODELS.keys())}")
        return

    meta = RECOMMENDED_MODELS[model_key]
    repo_id = meta["id"]
    dest = Path(target_dir) if target_dir else MODELS_DIR / model_key
    dest.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {repo_id} ({meta['size_gb']} GB) to {dest}...")
    try:
        from huggingface_hub import snapshot_download
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
        snapshot_download(repo_id=repo_id, local_dir=str(dest), resume_download=True)
        print(f"Model successfully saved to {dest}")
    except Exception as e:
        print(f"Download failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Colibrì Management Controller for OMEGA")
    sub = parser.add_subparsers(dest="action")

    sub.add_parser("profile", help="Display local hardware profile and engine status")
    
    doc = sub.add_parser("doctor", help="Run Colibrì environment diagnostics")
    doc.add_argument("--model", default=None, help="Model directory to check")

    bench = sub.add_parser("bench", help="Run disk streaming benchmark")
    bench.add_argument("--size-mb", type=int, default=64, help="Benchmark file size in MB")

    web = sub.add_parser("web", help="Launch Web dashboard + OpenAI server")
    web.add_argument("--model", default=None, help="Model directory to load")
    web.add_argument("--port", type=int, default=8000, help="Web dashboard port")

    dl = sub.add_parser("download", help="Download a recommended MoE model")
    dl.add_argument("model", choices=list(RECOMMENDED_MODELS.keys()), default="qwen36", nargs="?")
    dl.add_argument("--dir", default=None, help="Target destination directory")

    args = parser.parse_args()

    if args.action == "profile":
        prof = get_hardware_profile()
        print("\n================ COLIBRÌ HOST PROFILE ================")
        print(f"  Platform         : {prof['platform']}")
        print(f"  Python           : {prof['python']}")
        print(f"  System RAM       : {prof.get('ram_gb')} GB total ({prof.get('ram_avail_gb')} GB available)")
        print(f"  Drive Free Space : {prof.get('disk_free_gb')} GB (Total: {prof.get('disk_total_gb')} GB)")
        print(f"  GCC Toolchain    : {'Ready (w64devkit/gcc)' if prof.get('compiler_ready') else 'Not Found'}")
        print(f"  Available Engines: {', '.join(prof.get('engines', []))}")
        print("======================================================\n")
    elif args.action == "doctor":
        run_doctor(args.model)
    elif args.action == "bench":
        run_iobench(args.size_mb)
    elif args.action == "web":
        launch_web(args.model, args.port)
    elif args.action == "download":
        download_model(args.model, args.dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
