#!/usr/bin/env python3
"""
SQLFluff Automation & Quality Gateway Runner
Enforces SQL standards, dialect validation, auto-fixing, and CI auditing.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def resolve_sqlfluff_cmd():
    """Locate sqlfluff executable or uv fallback."""
    if shutil.which("sqlfluff"):
        return ["sqlfluff"]
    if shutil.which("uv"):
        return ["uv", "tool", "run", "sqlfluff"]
    # Try python -m sqlfluff
    try:
        res = subprocess.run(
            [sys.executable, "-m", "sqlfluff", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0:
            return [sys.executable, "-m", "sqlfluff"]
    except Exception:
        pass

    sys.stderr.write(
        "Error: Neither 'sqlfluff' nor 'uv' was found in PATH.\n"
        "Install via: pip install sqlfluff  OR  uv tool install sqlfluff\n"
    )
    sys.exit(1)


def run_sqlfluff(action: str, paths: list[str], extra_args: list[str] = None):
    """Execute SQLFluff command with appropriate options."""
    base_cmd = resolve_sqlfluff_cmd()
    cmd = base_cmd + [action] + (extra_args or []) + paths
    print(f"[*] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="SQLFluff Runner for Antigravity Omega Relational Schemas"
    )
    parser.add_argument(
        "action",
        nargs="?",
        default="lint",
        choices=["lint", "fix", "format", "rules", "dialects", "version"],
        help="Action to perform (default: lint)",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["aios/databases/"],
        help="Target SQL files or directories (default: aios/databases/)",
    )
    parser.add_argument(
        "--dialect",
        default=None,
        help="Override dialect specified in .sqlfluff (e.g., sqlite, postgres, mysql)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args, unknown = parser.parse_known_args()

    extra_args = []
    if args.dialect:
        extra_args.extend(["--dialect", args.dialect])
    if args.verbose:
        extra_args.append("-v")
    if unknown:
        extra_args.extend(unknown)

    # For version, rules, dialects - no target paths needed
    if args.action in ("version", "rules", "dialects"):
        base_cmd = resolve_sqlfluff_cmd()
        cmd = base_cmd + [f"--{args.action}" if args.action == "version" else args.action]
        ret = subprocess.run(cmd).returncode
        sys.exit(ret)

    target_paths = args.paths
    ret = run_sqlfluff(args.action, target_paths, extra_args)
    sys.exit(ret)


if __name__ == "__main__":
    main()
