r"""
Continuous Autonomous Outreach Engine Sync Daemon
OMEGA Autonomous Mode K (Monitoring) & Mode E (Automation)

Watches:
- e:\anti\linkedin_export\Connections.csv
- Health of local server on port 8080
"""

import os
import sys
import time
import subprocess
import urllib.request
from datetime import datetime

WATCH_FILE = r'e:\anti\linkedin_export\Connections.csv'
GENERATOR_SCRIPT = r'e:\anti\scripts\generate_all_jobs_and_messages.py'
LOG_FILE = r'e:\anti\linkedin_export\sync_log.txt'
SERVER_PORT = 8080
SERVER_URL = f'http://localhost:{SERVER_PORT}/connection_messenger_center.html'

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{ts}] {msg}"
    print(entry, flush=True)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(entry + '\n')
    except Exception:
        pass

def get_file_sig(path):
    if not os.path.exists(path):
        return None
    st = os.stat(path)
    return (st.st_mtime, st.st_size)

def is_server_alive():
    try:
        req = urllib.request.Request(SERVER_URL, method='HEAD')
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False

def ensure_server():
    if not is_server_alive():
        log(f"HTTP Server on port {SERVER_PORT} is down. Spawning local server...")
        try:
            cmd = [sys.executable, "-m", "http.server", str(SERVER_PORT), "--directory", r"e:\anti\linkedin_export"]
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            if is_server_alive():
                log(f"HTTP Server restarted successfully on port {SERVER_PORT}.")
            else:
                log(f"Warning: Server attempted restart on port {SERVER_PORT}, checking again in next cycle.")
        except Exception as e:
            log(f"Error starting HTTP server: {e}")

def run_rebuild():
    log("Change detected or manual sync triggered. Executing rebuild pipeline...")
    start = time.time()
    try:
        res = subprocess.run([sys.executable, GENERATOR_SCRIPT], capture_output=True, text=True, check=True)
        elapsed = time.time() - start
        log(f"Rebuild completed successfully in {elapsed:.2f}s.")
    except subprocess.CalledProcessError as e:
        log(f"Rebuild error: {e.stderr}")

def main():
    log("=== Sovereign Autonomous Sync Daemon Initialized ===")
    log(f"Monitoring: {WATCH_FILE}")
    log(f"Target Server: {SERVER_URL}")

    last_sig = get_file_sig(WATCH_FILE)
    log(f"Initial Connections.csv signature: {last_sig}")

    ensure_server()

    cycle = 0
    while True:
        try:
            cycle += 1
            time.sleep(15)

            # Check File Changes
            curr_sig = get_file_sig(WATCH_FILE)
            if curr_sig != last_sig and curr_sig is not None:
                log(f"Connections.csv was modified! (Old: {last_sig} -> New: {curr_sig})")
                run_rebuild()
                last_sig = curr_sig

            # Health Check every 4 cycles (60s)
            if cycle % 4 == 0:
                ensure_server()

            # Heartbeat every 240 cycles (1 hour)
            if cycle % 240 == 0:
                log(f"Daemon Heartbeat: Operational. Monitored {WATCH_FILE} across {cycle} cycles.")

        except KeyboardInterrupt:
            log("Daemon stopped by user.")
            break
        except Exception as e:
            log(f"Unexpected error in daemon loop: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
