"""
VECTIS TRADE — Master Autonomous Autopilot Controller
Launches the Web Portal, Hot-Folder Watcher Daemon, and Periodic Swarm Monitor concurrently.
"""

import threading
import time
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from vectis_app import run as run_server
from vectis_daemon import start_daemon
from vectis_network_miner import mine_leads
from vectis_agents import AgentHarness
from vectis_parser import generate_sample_dockets

def main():
    print("=============================================================")
    print("  LAUNCHING VECTIS TRADE AUTONOMOUS MASTER AUTOPILOT")
    print("=============================================================")

    # Step 1: Pre-flight lead mining and fixture seeding
    print("[1/4] Mining real network leads...")
    mine_leads()

    print("[2/4] Seeding sample test dockets in inbox...")
    generate_sample_dockets()

    print("[3/4] Executing autonomous 9-agent operations cycle...")
    harness = AgentHarness()
    harness.run_daily_swarm_cycle()

    # Step 2: Launch Daemon in Background Thread
    print("[4/4] Starting Hot-Folder Daemon & Web Portal...")
    daemon_thread = threading.Thread(target=start_daemon, kwargs={"poll_interval": 2}, daemon=True)
    daemon_thread.start()

    # Step 3: Serve Web Portal on Main Thread
    print("\n>>> VECTIS MASTER SYSTEM IS LIVE <<<")
    print(">>> Web Portal: http://localhost:8080")
    print(">>> Hot-Folder Watcher: company/inbox/ -> company/outbox/")
    print("Press Ctrl+C to terminate autopilot.\n")

    run_server(port=8080)

if __name__ == "__main__":
    main()
