#!/usr/bin/env python3
"""
========================================================================================
CLAUDE CODE BRIDGE & RUNNER FOR ADI CAREER OS
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Integrates the official Claude Code CLI with the ADI CAREER OS workspace:
  - Validates CLAUDE.md context and candidate guardrails.
  - Launches interactive Claude Code sessions.
  - Runs headless / prompt queries via `claude -p "<prompt>"`.
  - Runs Claude Code health diagnostics (`claude doctor`).
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import shutil
import subprocess
import argparse
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
CLAUDE_MD = ROOT_DIR / "CLAUDE.md"

def find_claude_binary() -> str:
    """Finds the claude executable in PATH or user local bin."""
    cmd = shutil.which("claude")
    if cmd:
        return cmd
    
    local_bin = Path(os.environ.get("USERPROFILE", "C:/Users/amehr")) / ".local" / "bin" / "claude.exe"
    if local_bin.exists():
        return str(local_bin)
    
    return "claude"

def run_doctor():
    claude_bin = find_claude_binary()
    print("=" * 70)
    print("  RUNNING CLAUDE CODE DIAGNOSTICS")
    print(f"  Binary: {claude_bin}")
    print("=" * 70)
    subprocess.run([claude_bin, "doctor"], cwd=str(ROOT_DIR))

def run_prompt(prompt: str):
    claude_bin = find_claude_binary()
    print("=" * 70)
    print(f"  RUNNING CLAUDE CODE PROMPT: {prompt}")
    print(f"  Binary: {claude_bin}")
    print("=" * 70)
    res = subprocess.run([claude_bin, "-p", prompt], cwd=str(ROOT_DIR))
    return res.returncode

def launch_interactive():
    claude_bin = find_claude_binary()
    print("=" * 70)
    print("  LAUNCHING CLAUDE CODE INTERACTIVE WORKSPACE")
    print(f"  Working Directory: {ROOT_DIR}")
    print(f"  Instruction File:  {CLAUDE_MD}")
    print("=" * 70)
    subprocess.run([claude_bin], cwd=str(ROOT_DIR))

def run_login():
    claude_bin = find_claude_binary()
    print("=" * 70)
    print("  STARTING CLAUDE CODE AUTHENTICATION")
    print("  Email: adityamehra799@gmail.com")
    print("=" * 70)
    subprocess.run([claude_bin, "auth", "login", "--email", "adityamehra799@gmail.com"], cwd=str(ROOT_DIR))

def main():
    parser = argparse.ArgumentParser(description="Claude Code Bridge for ADI CAREER OS")
    parser.add_argument("-p", "--prompt", type=str, help="Run a non-interactive prompt through Claude Code")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive Claude Code session in terminal")
    parser.add_argument("--doctor", action="store_true", help="Run Claude Code doctor health check")
    parser.add_argument("--login", action="store_true", help="Authenticate Claude Code with personal Claude.ai account")
    parser.add_argument("--check-env", action="store_true", help="Verify Claude Code environment and CLAUDE.md presence")

    args = parser.parse_args()

    claude_bin = find_claude_binary()

    if args.doctor:
        run_doctor()
    elif args.login:
        run_login()
    elif args.prompt:
        run_prompt(args.prompt)
    elif args.interactive:
        launch_interactive()

    else:
        # Default: check environment
        print("=" * 70)
        print("  CLAUDE CODE INTEGRATION STATUS")
        print("=" * 70)
        print(f"Claude Executable : {claude_bin}")
        print(f"CLAUDE.md Context : {'PRESENT' if CLAUDE_MD.exists() else 'MISSING'}")
        print(f"Workspace Root    : {ROOT_DIR}")
        print("\nUsage Commands:")
        print("  python scripts/run_claude_code.py --doctor")
        print("  python scripts/run_claude_code.py --interactive")
        print('  python scripts/run_claude_code.py -p "review career pipeline"')
        print("=" * 70)

if __name__ == "__main__":
    sys.exit(main())
