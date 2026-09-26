"""
Main Entry Point for ANTIGRAVITY REVENUE OS
Run:
  python -m REVENUE_OS                # Displays Executive Brief
  python -m REVENUE_OS --serve        # Launches 24/7 Web Command Center on port 8765
  python -m REVENUE_OS --test         # Runs entire test suite
"""

import sys
import argparse
from pathlib import Path

# Add workspace to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from REVENUE_OS.command_center.cli import RevenueOSCLI
from REVENUE_OS.command_center.server import create_http_server

def main():
    parser = argparse.ArgumentParser(description="ANTIGRAVITY 24/7 REVENUE OS COMMAND CENTER")
    parser.add_argument("--brief", action="store_true", help="Print executive revenue brief")
    parser.add_argument("--serve", action="store_true", help="Launch 24/7 web command center")
    parser.add_argument("--port", type=int, default=8765, help="Web dashboard port (default: 8765)")
    args = parser.parse_args()

    cli = RevenueOSCLI()

    if args.serve:
        print(f"Starting ANTIGRAVITY 24/7 REVENUE COMMAND CENTER on http://127.0.0.1:{args.port}")
        server = create_http_server(port=args.port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            server.server_close()
    else:
        # Default action: print executive brief
        brief = cli.get_executive_brief()
        print(brief)

if __name__ == "__main__":
    main()
