#!/usr/bin/env python3
"""
TradeNexus Production Server Launcher
Runs FastAPI backend serving the REST API and the Interactive Web UI.
"""

import os
import sys
import uvicorn

if __name__ == "__main__":
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "06_ENGINEERING"))
    sys.path.insert(0, src_dir)
    uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=False, log_level="info")