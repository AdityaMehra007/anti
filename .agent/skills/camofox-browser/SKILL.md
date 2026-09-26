---
name: camofox-browser
description: Stealth headless browser server and agent interaction skill powered by Camoufox. Bypasses Cloudflare, bot-detection, and CAPTCHA fingerprinters at the C++ engine level.
metadata:
  origin: Antigravity-Omega
---

# Camofox Browser — Stealth Anti-Detection Engine

## Overview

`camofox-browser` wraps the [Camoufox](https://camoufox.com) hardened Firefox fork with an agentic REST API. It replaces detectable Puppeteer/Playwright scripts with C++ level fingerprint spoofing (spoofing `navigator.hardwareConcurrency`, WebRTC, screen geometry, WebGL, and AudioContext before JavaScript execution).

## When to Use

- When scraping corporate targets or recruiter profiles protected by Cloudflare, Akamai, Datadome, or PerimeterX.
- When querying LinkedIn, Google, Amazon, or job boards without getting blocked or flagged.
- When performing agent navigation requiring token-efficient accessibility snapshots instead of heavy raw HTML.
- When authenticating via Netscape cookie injection (`~/.camofox/cookies/`).

## Architecture & REST Endpoints

The server runs locally by default at `http://localhost:9377`:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | `GET` | Health check & engine status |
| `/tabs` | `POST` | Create a new isolated tab (`{"url": "...", "trace": false}`) |
| `/tabs` | `GET` | List active tabs for a session |
| `/tabs/{tabId}/snapshot` | `POST` | Get accessibility tree with element refs (`e1`, `e2`, etc.) |
| `/tabs/{tabId}/click` | `POST` | Click element by `ref` or CSS `selector` |
| `/tabs/{tabId}/type` | `POST` | Type text into element by `ref` |
| `/tabs/{tabId}/navigate` | `POST` | Navigate to URL or search macro (e.g. `@google_search <term>`) |
| `/tabs/{tabId}/extract` | `POST` | Extract structured data via JSON Schema with `x-ref` |
| `/tabs/{tabId}/screenshot` | `POST` | Capture base64 screenshot |
| `/tabs/{tabId}` | `DELETE` | Close tab and free resources |
| `/sessions/{userId}/cookies` | `POST` | Import cookies for authenticated sessions |

## Python Integration (`ai.camofox_client`)

Use the zero-dependency Python client located at `e:/anti/ai/camofox_client.py`:

```python
from ai.camofox_client import CamofoxClient

with CamofoxClient() as client:
    # 1. Create a stealth tab
    tab = client.create_tab(url="https://example.com")
    tab_id = tab["tabId"]

    # 2. Inspect the accessibility snapshot
    snapshot = client.snapshot(tab_id)
    print("Page snapshot:", snapshot["snapshot"])

    # 3. Deterministically interact via refs
    # client.type(tab_id, ref="e4", text="Query", press_enter=True)
    # client.click(tab_id, ref="e12")
```

## Running the Server

### Standalone (Node.js)
```bash
cd external/camofox-browser
npm start
# Server listens on http://localhost:9377
```

### Windows Docker
```powershell
cd external/camofox-browser
.\build.ps1 up
```
