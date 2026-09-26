---
name: browser-use
description: Autonomous web automation and interaction skill using Browser-Use, enabling agents to navigate, extract structured data, click, fill forms, and operate web interfaces via LLM vision and DOM grounding.
metadata:
  origin: workspace
---

# Browser-Use — Autonomous AI Browser Agent

## When to Use

- When an agent needs to dynamically navigate websites, search engines, web apps, or portals that require JavaScript rendering and complex interactions.
- When performing multi-step workflows across web applications (e.g. searching, filtering, paginating, filling forms).
- When standard HTTP scraping (`read_url_content`, curl, requests) fails due to client-side hydration, SPAs, anti-bot challenges, or authenticated session states.
- When extracting structured data from unstructured or dynamic websites.
- For browser-in-the-loop task completion where visual cues (buttons, icons, dynamic menus) guide the agent's actions.

---

## Architecture & How It Works

Browser-Use pairs an LLM (Gemini, Claude, GPT, or local models) with Playwright / Chromium via two primary perception layers:

1. **DOM Tree Extraction**: Extracts interactive and semantically meaningful DOM elements (buttons, inputs, links, dropdowns), labeling each element with a unique index.
2. **Visual Grounding**: Takes viewport screenshots with bounding boxes or element tags, allowing vision-capable models to understand layout, spatial relationships, and visual affordances.
3. **Agent Action Loop**:
   - `Navigate(url)`
   - `Click(index)`
   - `Input_text(index, text)`
   - `Scroll_at(x, y)` / `Scroll_down()`
   - `Switch_tab(tab_id)` / `New_tab(url)`
   - `Extract_content(goal)`
   - `Done(result)`

---

## Prerequisites & Installation

To run `browser-use` in this workspace:

```bash
# Ensure virtual environment exists
uv venv .venv

# Install browser-use and dependencies
uv pip install browser-use playwright langchain-google-genai langchain-openai

# Install Playwright browser engine (Chromium)
uv run playwright install chromium
```

---

## Safety First & Blast Radius Guardrails

Browser agents have direct agency in real browsers. Always observe these strict safety protocols:

1. **Read-Only by Default**:
   - Never execute mutating transactions (payments, purchases, deleting records, sending mass messages) unless explicitly authorized.
   - For sensitive workflows, run against staging/mock test environments.
2. **Credential Protection**:
   - Never hardcode credentials or secrets in scripts. Use `.env` or system environment variables.
   - Never store or log sensitive user credentials, session cookies, or PII into public artifacts or unmasked logs.
3. **Loop & Step Budgeting**:
   - Always enforce a maximum step limit (e.g. `max_steps=20` or `max_steps=30`) to prevent infinite looping, excessive token consumption, or runaway navigation.
4. **Domain Sandboxing**:
   - Where possible, constrain navigation to authorized domain boundaries or specific URL patterns to prevent unintended redirections.

---

## Python API Usage

### 1. Minimal Quickstart (Gemini)

```python
import asyncio
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

async def run():
    agent = Agent(
        task="Go to https://news.ycombinator.com and extract the top 3 story titles and URLs.",
        llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
    )
    history = await agent.run()
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(run())
```

### 2. Structured Output & Custom Controller

```python
import asyncio
from pydantic import BaseModel, Field
from typing import List
from browser_use import Agent, Controller
from langchain_google_genai import ChatGoogleGenerativeAI

class NewsItem(BaseModel):
    title: str
    url: str
    points: int = 0

class NewsReport(BaseModel):
    items: List[NewsItem] = Field(description="Top news items extracted from the page")

controller = Controller(output_model=NewsReport)

async def run():
    agent = Agent(
        task="Extract the top 5 articles with their titles, links, and points from Hacker News",
        llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
        controller=controller,
        max_steps=15,
    )
    history = await agent.run()
    report = history.extracted_content()
    print(report)

if __name__ == "__main__":
    asyncio.run(run())
```

### 3. Reusing Existing Chrome Profile / Persistent Sessions

To operate with authenticated sessions (e.g., existing Google / GitHub login):

```python
from browser_use import Agent, Browser, BrowserConfig

browser = Browser(
    config=BrowserConfig(
        chrome_instance_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        # Or specify custom user_data_dir for isolated profile persistence
        user_data_dir="./.chrome-profile"
    )
)

agent = Agent(
    task="Navigate to internal portal and download the weekly report",
    llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
    browser=browser
)
```

---

## CLI & Script Execution

Use the repository runner script:

```bash
# Run a general browser task
uv run python scripts/browser_use_runner.py --task "Search Google for latest Next.js 16 release notes and summarize key features"

# Run in headful mode (watch the browser live)
uv run python scripts/browser_use_runner.py --task "Check weather in Tokyo" --headed

# Run with maximum step constraint
uv run python scripts/browser_use_runner.py --task "Find documentation for Pydantic v2 migration" --max-steps 10
```

---

## Troubleshooting & Best Practices

- **Timeout / Slow Loading**: If a site uses heavy client-side rendering, configure wait delays or increase step budgets.
- **Bot Detection / Cloudflare**: Run with `--headed` or attach to a real Chrome user profile (`user_data_dir`).
- **Token Efficiency**: Use fast, vision-optimized models like `gemini-2.5-flash` or `claude-3-5-sonnet` for rapid perception and low latency.
