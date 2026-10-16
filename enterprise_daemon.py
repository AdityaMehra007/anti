#!/usr/bin/env python3
"""
enterprise_daemon.py - 24/7 Autopilot Background Runner for Aditya Mehra Enterprise
Supports:
  --run-once : Run single cycle and exit
  --daemon   : Run continuously with configurable sleep interval (default: 86400s / 24h, or test mode)
  --interval : Seconds between cycles
"""

import sys
import time
import argparse
from datetime import datetime
from enterprise_engine import OnePersonEnterprise

def main():
    parser = argparse.ArgumentParser(description="Aditya Mehra Autonomous Enterprise Daemon")
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background daemon mode")
    parser.add_argument("--run-once", action="store_true", default=True, help="Run single daily cycle and terminate")
    parser.add_argument("--interval", type=int, default=86400, help="Interval in seconds between runs (default: 86400s)")
    args = parser.parse_args()

    enterprise = OnePersonEnterprise()

    if not args.daemon:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Executing single daily autonomous enterprise cycle...")
        enterprise.run_daily_cycle()
        return

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Aditya Mehra Autonomous Enterprise Daemon (Interval: {args.interval}s)...")
    while True:
        try:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === COMMENCING SCHEDULED ENTERPRISE SWARM DISPATCH ===")
            enterprise.run_daily_cycle()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Cycle complete. Sleeping for {args.interval}s...")
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[!] Enterprise Daemon gracefully terminated by user.")
            break
        except Exception as e:
            print(f"[ERROR] Daemon exception: {e}. Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    main()
