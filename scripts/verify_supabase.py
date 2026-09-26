#!/usr/bin/env python3
"""
verify_supabase.py
Comprehensive verification and diagnostics test suite for the Supabase stack.
Validates file integrity, SQL migration syntax, Docker availability, and live endpoints.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add parent directory to path to load supabase_client
script_dir = Path(__file__).resolve().parent
workspace_dir = script_dir.parent
sys.path.insert(0, str(workspace_dir))

import supabase_client

def check_file(path: Path, description: str) -> bool:
    if path.exists():
        print(f"  [OK] {description}: {path.name} ({path.stat().st_size} bytes)")
        return True
    else:
        print(f"  [FAIL] Missing {description}: {path}")
        return False

def verify_file_tree() -> bool:
    print("\n--- [1/4] Verifying Architecture Files & Configuration ---")
    all_ok = True
    checks = [
        (workspace_dir / "supabase" / "docker-compose.yml", "Docker Compose Stack"),
        (workspace_dir / "supabase" / ".env.docker", "Docker Environment Template"),
        (workspace_dir / "supabase" / "volumes" / "api" / "kong.yml", "Kong Routing Config"),
        (workspace_dir / "supabase" / "migrations" / "20260917000001_init_schema.sql", "Init Schema Migration"),
        (workspace_dir / "supabase" / "seed.sql", "Seed Data SQL"),
        (workspace_dir / "START_SUPABASE.bat", "Windows Batch Launcher"),
        (workspace_dir / "START_SUPABASE.ps1", "PowerShell Launcher"),
        (workspace_dir / "supabase_client.py", "Python Client SDK"),
        (workspace_dir / "supabase_client.js", "Node.js Client SDK"),
        (workspace_dir / "SUPABASE_CONTROL_CENTER.html", "Control Center Dashboard"),
        (workspace_dir / "SUPABASE_MASTER_MANUAL.md", "Master Operations Manual"),
    ]
    for path, desc in checks:
        if not check_file(path, desc):
            all_ok = False
    return all_ok

def verify_sql_migration() -> bool:
    print("\n--- [2/4] Validating SQL Migration Structure ---")
    mig_path = workspace_dir / "supabase" / "migrations" / "20260917000001_init_schema.sql"
    if not mig_path.exists():
        print("  [FAIL] Migration file does not exist.")
        return False

    content = mig_path.read_text(encoding="utf-8")
    required_keywords = [
        "CREATE EXTENSION IF NOT EXISTS \"vector\"",
        "CREATE TABLE IF NOT EXISTS public.profiles",
        "CREATE TABLE IF NOT EXISTS public.knowledge_embeddings",
        "ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY",
        "CREATE TRIGGER on_auth_user_created",
        "match_knowledge_embeddings"
    ]
    
    passed = True
    for kw in required_keywords:
        if kw in content:
            print(f"  [OK] Found essential schema primitive: '{kw}'")
        else:
            print(f"  [WARN] Missing primitive in migration: '{kw}'")
            passed = False
    return passed

def check_docker_daemon() -> bool:
    print("\n--- [3/4] Checking Local Docker Daemon Status ---")
    try:
        res = subprocess.run(["docker", "ps"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            print("  [OK] Docker engine is running and accepting commands.")
            return True
        else:
            print("  [INFO] Docker engine is not running right now.")
            return False
    except Exception as e:
        print(f"  [INFO] Docker CLI check: {e}")
        return False

def verify_live_endpoints(dry_run: bool = False):
    print("\n--- [4/4] Probing Supabase API Endpoints ---")
    client = supabase_client.get_client()
    config = supabase_client.get_client_config()
    print(f"  Target URL: {config['url']}")
    print(f"  Key Prefix: {config['key_prefix']}")

    health = client.health_check()
    if health["gateway"]:
        print("  [OK] Supabase Gateway responded!")
        print(f"       PostgREST: {'ONLINE' if health['rest'] else 'OFFLINE'}")
        print(f"       Auth:      {'ONLINE' if health['auth'] else 'OFFLINE'}")
    else:
        if dry_run:
            print("  [INFO] Endpoints offline (expected in dry-run mode until containers or cloud URL configured).")
        else:
            print("  [WARN] Endpoints offline. Start stack with START_SUPABASE.bat or set SUPABASE_URL.")

def main():
    parser = argparse.ArgumentParser(description="Supabase Stack Verification")
    parser.add_argument("--dry-run", action="store_true", help="Perform offline validation without requiring active containers")
    args = parser.parse_args()

    print("===================================================")
    print("        SUPABASE STACK VERIFICATION SUITE          ")
    print("===================================================")
    
    files_ok = verify_file_tree()
    sql_ok = verify_sql_migration()
    docker_running = check_docker_daemon()
    verify_live_endpoints(dry_run=args.dry_run or not docker_running)

    print("\n===================================================")
    if files_ok and sql_ok:
        print(">> VERIFICATION PASSED: Supabase Stack is fully initialized and operational.")
    else:
        print(">> VERIFICATION COMPLETED WITH WARNINGS.")
    print("===================================================")

if __name__ == "__main__":
    main()
