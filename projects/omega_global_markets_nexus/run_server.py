"""
Launch Entry Point for OMEGA Global Markets & EXIM Nexus API Server
Runs Uvicorn server on http://localhost:8800 with auto-reload.
"""
import sys
import uvicorn
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

def main():
    print("=" * 80)
    print("🏛️  STARTING OMEGA GLOBAL MARKETS & EXIM NEXUS SERVER")
    print("=" * 80)
    print("🌐 Endpoint:       http://localhost:8800")
    print("📑 Swagger Docs:   http://localhost:8800/docs")
    print("📊 HTML Cockpit:   http://localhost:8800/")
    print("=" * 80)
    uvicorn.run(
        "projects.omega_global_markets_nexus.api.server:app",
        host="127.0.0.1",
        port=8800,
        log_level="info"
    )

if __name__ == "__main__":
    main()
