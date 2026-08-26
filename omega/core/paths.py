"""
OMEGA SYSTEM PATHS: PRODUCTION VS SCRATCH SEPARATION
Defines canonical system root vs active development workspace.
"""
import os

# Canonical production repository on E: drive
PRODUCTION_ROOT = r"E:\anti"
PRODUCTION_ALT_ROOT = r"E:\anti gravity"

# Active runtime scratch workspace
SCRATCH_ROOT = r"C:\Users\amehr\.gemini\antigravity\scratch"

# AppData & System Brain
APPDATA_ROOT = r"C:\Users\amehr\.gemini\antigravity"
BRAIN_ROOT = r"C:\Users\amehr\.gemini\antigravity\brain"

def get_canonical_production_path(relative_path: str) -> str:
    return os.path.join(PRODUCTION_ROOT, relative_path)

def get_scratch_path(relative_path: str) -> str:
    return os.path.join(SCRATCH_ROOT, relative_path)

def is_production_path(path: str) -> bool:
    normalized = os.path.normpath(path).lower()
    return normalized.startswith(os.path.normpath(PRODUCTION_ROOT).lower()) or normalized.startswith(os.path.normpath(PRODUCTION_ALT_ROOT).lower())
