"""
ARES-FINANCE Terminal Launcher
Starts the FastAPI server and opens the browser.
"""

import sys
import webbrowser
import uvicorn

if __name__ == "__main__":
    port = 8088
    url = f"http://127.0.0.1:{port}"
    print(f"\n=======================================================")
    print(f"  ARES-FINANCE: Sovereign Institutional Terminal")
    print(f"  Web Terminal running at: {url}")
    print(f"  Standalone HTML: apps/ares_financial_terminal/standalone_terminal.html")
    print(f"=======================================================\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    uvicorn.run("apps.ares_financial_terminal.app:app", host="127.0.0.1", port=port, reload=False)
