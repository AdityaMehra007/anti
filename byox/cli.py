"""
BYOX Unified CLI Command Router
Provides interactive and command-line execution for all 10 core systems.
"""

import sys
import unittest
import argparse
from typing import Optional, List
from byox import __version__

SYSTEMS = [
    "git",
    "redis",
    "shell",
    "regex",
    "neural_net",
    "sqlite",
    "web_server",
    "interpreter",
    "bittorrent",
    "raytracer",
]

def run_all_tests() -> int:
    """Run all automated unit and integration tests across byox."""
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="byox",
        description="Build Your Own X (BYOX) — Rebuilding 10 Core Technologies from Scratch in Pure Python",
    )
    parser.add_argument(
        "--version", "-v", action="version", version=f"BYOX v{__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="subcommand", help="System or action to execute")
    
    # Test runner
    subparsers.add_parser("test", help="Run full automated verification test suite")
    
    # Systems
    for system in SYSTEMS:
        sub = subparsers.add_parser(system, help=f"Execute or inspect {system}")
        sub.add_argument("args", nargs=argparse.REMAINDER, help=f"Arguments forwarded to {system}")
        
    return parser

def main(argv: Optional[List[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
        
    parser = build_parser()
    
    if not argv:
        parser.print_help()
        return 0
        
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 0

    if args.subcommand == "test":
        return run_all_tests()
        
    if args.subcommand in SYSTEMS:
        print(f"[BYOX] Dispatching to {args.subcommand} with args: {getattr(args, 'args', [])}")
        return 0
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
