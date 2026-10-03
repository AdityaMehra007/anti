#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Unified Real-Time System Health Monitor
Pure Python Standard Library (Zero-Dependency) using Windows native APIs.
"""

import sys
import os
import json
import socket
import shutil
import ctypes
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Ensure parent directory is in pythonpath
SCRIPT_DIR = Path(__file__).resolve().parent
AIOS_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(AIOS_ROOT / "databases"))

try:
    import db
except ImportError:
    db = None

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

def get_ram_metrics() -> Dict[str, float]:
    """Retrieves physical memory stats via kernel32 GlobalMemoryStatusEx."""
    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    total_gb = stat.ullTotalPhys / (1024 ** 3)
    free_gb = stat.ullAvailPhys / (1024 ** 3)
    used_pct = float(stat.dwMemoryLoad)
    return {
        "total_gb": round(total_gb, 2),
        "free_gb": round(free_gb, 2),
        "used_percent": round(used_pct, 1)
    }

def get_disk_metrics() -> Dict[str, Dict[str, float]]:
    """Retrieves disk usage for drives C: and E:."""
    results = {}
    for drive in ["C:\\", "E:\\"]:
        try:
            total, used, free = shutil.disk_usage(drive)
            results[drive[0]] = {
                "total_gb": round(total / (1024 ** 3), 2),
                "free_gb": round(free / (1024 ** 3), 2),
                "used_percent": round((used / total) * 100, 1)
            }
        except Exception:
            results[drive[0]] = {"total_gb": 0.0, "free_gb": 0.0, "used_percent": 0.0}
    return results

def get_gpu_metrics() -> Optional[Dict[str, Any]]:
    """Queries NVIDIA SMI for Maxwell GTX 960M telemetry."""
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=3
        )
        if res.returncode == 0 and res.stdout.strip():
            parts = [p.strip() for p in res.stdout.strip().split(",")]
            return {
                "name": parts[0],
                "vram_used_mb": float(parts[1]),
                "vram_total_mb": float(parts[2]),
                "gpu_util_percent": float(parts[3]),
                "temp_c": float(parts[4])
            }
    except Exception:
        pass
    return None

def check_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """Tests if a local port is listening."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def run_health_check() -> Dict[str, Any]:
    """Runs a complete system diagnostic pass and returns structured health report."""
    ram = get_ram_metrics()
    disks = get_disk_metrics()
    gpu = get_gpu_metrics()

    ports = {
        "aios_gateway": {"port": 8090, "online": check_port("127.0.0.1", 8090)},
        "ollama": {"port": 11434, "online": check_port("127.0.0.1", 11434)},
        "n8n": {"port": 5678, "online": check_port("127.0.0.1", 5678)},
        "command_ui": {"port": 3000, "online": check_port("127.0.0.1", 3000)},
        "omniroute": {"port": 20128, "online": check_port("127.0.0.1", 20128)},
        "openhands_canvas": {"port": 3001, "online": check_port("127.0.0.1", 3001)},
    }

    # Evaluate health status
    status = "HEALTHY"
    warnings = []

    if ram["free_gb"] < 1.0:
        status = "CRITICAL"
        warnings.append(f"RAM Free is critically low: {ram['free_gb']} GB")
    elif ram["free_gb"] < 2.0:
        status = "WARNING"
        warnings.append(f"RAM Free is low: {ram['free_gb']} GB")

    if disks.get("C", {}).get("free_gb", 100) < 10.0:
        status = "CRITICAL"
        warnings.append(f"Drive C: space critically low: {disks['C']['free_gb']} GB")
    elif disks.get("C", {}).get("free_gb", 100) < 15.0:
        if status != "CRITICAL":
            status = "WARNING"
        warnings.append(f"Drive C: space tight: {disks['C']['free_gb']} GB")

    report = {
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "warnings": warnings,
        "ram": ram,
        "disks": disks,
        "gpu": gpu,
        "services": ports
    }

    # Save to SQLite master database if available
    if db is not None:
        try:
            gpu_vram = gpu["vram_used_mb"] if gpu else None
            db.record_metric(
                cpu=0.0,
                ram_pct=ram["used_percent"],
                ram_free=ram["free_gb"],
                gpu_vram=gpu_vram,
                disk_c=disks.get("C", {}).get("free_gb", 0.0),
                disk_e=disks.get("E", {}).get("free_gb", 0.0),
                status=status
            )
        except Exception as e:
            warnings.append(f"Failed to record metric to SQLite: {e}")

    return report

def format_console_report(r: Dict[str, Any]):
    """Formats and prints colored human-readable health check."""
    status_symbol = {
        "HEALTHY": "[OK] HEALTHY",
        "WARNING": "[!] WARNING",
        "CRITICAL": "[X] CRITICAL"
    }.get(r["status"], "[?] UNKNOWN")

    print("===============================================================================")
    print(f"       ANTIGRAVITY OMEGA :: SYSTEM HEALTH TELEMETRY :: {status_symbol}")
    print("===============================================================================")
    print(f"Timestamp    : {r['timestamp']}")
    print(f"RAM Status   : {r['ram']['free_gb']} GB Free / {r['ram']['total_gb']} GB Total ({r['ram']['used_percent']}% Used)")
    
    c = r['disks'].get('C', {})
    e = r['disks'].get('E', {})
    print(f"Drive C: (Sys): {c.get('free_gb', 0)} GB Free / {c.get('total_gb', 0)} GB Total ({c.get('used_percent', 0)}% Used)")
    print(f"Drive E: (Hub): {e.get('free_gb', 0)} GB Free / {e.get('total_gb', 0)} GB Total ({e.get('used_percent', 0)}% Used)")
    
    if r['gpu']:
        g = r['gpu']
        print(f"GPU ({g['name']}): {g['vram_used_mb']} MB VRAM / {g['vram_total_mb']} MB Total | Util: {g['gpu_util_percent']}% | Temp: {g['temp_c']}C")
    else:
        print("GPU Status   : No discrete NVIDIA GPU telemetry detected")
        
    print("-------------------------------------------------------------------------------")
    print("Core Service Ports:")
    for name, s in r['services'].items():
        state = "[ONLINE]" if s['online'] else "[OFFLINE]"
        print(f"  * {name:<18} (Port {s['port']:<5}) : {state}")
    
    if r['warnings']:
        print("-------------------------------------------------------------------------------")
        print("System Alerts:")
        for w in r['warnings']:
            print(f"  [!] {w}")
    print("===============================================================================\n")

if __name__ == "__main__":
    report = run_health_check()
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        format_console_report(report)
