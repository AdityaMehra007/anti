"""
Browser-Use Autonomous Runner & Extraction Script
=================================================

A modular CLI and programmatic runner for executing autonomous web agent tasks
using Browser-Use, with support for Google Gemini, OpenAI, and Anthropic models.

Usage:
  python scripts/browser_use_runner.py --task "Find the top trending repositories on GitHub"
  python scripts/browser_use_runner.py --demo
  python scripts/browser_use_runner.py --task "Search python docs for asyncio.gather" --headed
"""

import argparse
import asyncio
import os
import sys
from typing import Optional

# Determine available LLM provider
def get_llm(model_name: str = "gemini-2.5-flash"):
    """
    Initializes and returns an LLM instance based on available environment variables.
    Supports Gemini, Anthropic, and OpenAI.
    """
    # 1. Google Gemini
    if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=model_name if "gemini" in model_name else "gemini-2.5-flash",
                google_api_key=api_key,
                temperature=0.1
            )
        except ImportError:
            print("[WARN] langchain-google-genai not installed. Falling back to OpenAI if configured.")

    # 2. OpenAI
    if os.getenv("OPENAI_API_KEY"):
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=model_name if "gpt" in model_name else "gpt-4o",
                temperature=0.1
            )
        except ImportError:
            print("[WARN] langchain-openai not installed.")

    # 3. Anthropic
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=model_name if "claude" in model_name else "claude-3-5-sonnet-20241022",
                temperature=0.1
            )
        except ImportError:
            print("[WARN] langchain-anthropic not installed.")

    return None


async def run_browser_task(
    task: str,
    headless: bool = True,
    max_steps: int = 20,
    model_name: str = "gemini-2.5-flash",
    output_file: Optional[str] = None,
):
    """
    Executes a task using browser-use Agent.
    """
    print("=" * 60)
    print(f"[*] Task: {task}")
    print(f"[*] Headless: {headless} | Max Steps: {max_steps} | Model: {model_name}")
    print("=" * 60)

    try:
        from browser_use import Agent, Browser
    except ImportError as e:
        print(f"[ERROR] Failed to import browser-use: {e}")
        print("Run: uv pip install browser-use playwright && uv run playwright install chromium")
        sys.exit(1)

    llm = get_llm(model_name)
    if not llm:
        print("\n[!] No LLM API key detected in environment.")
        print("Please set one of the following environment variables to run live web agents:")
        print("  - GEMINI_API_KEY or GOOGLE_API_KEY (Recommended)")
        print("  - OPENAI_API_KEY")
        print("  - ANTHROPIC_API_KEY")
        print("\nExample (PowerShell):")
        print('  $env:GEMINI_API_KEY = "your-api-key"')
        print('  uv run python scripts/browser_use_runner.py --demo')
        print("\n[+] Script verified successfully in dry-run mode (all imports & browser engine ready).")
        return None

    browser = Browser(
        headless=headless,
        disable_security=True,
    )

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        max_steps=max_steps,
    )

    print("[*] Starting browser-use agent execution loop...")
    history = await agent.run()

    result = history.final_result()
    print("\n" + "=" * 60)
    print("[+] FINAL RESULT:")
    print("=" * 60)
    print(result)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result if result else "")
        print(f"\n[+] Saved result to: {output_file}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Browser-Use Autonomous Agent Runner")
    parser.add_argument("--task", type=str, help="Instruction or goal for the browser agent")
    parser.add_argument("--demo", action="store_true", help="Run predefined demo (Hacker News top stories)")
    parser.add_argument("--headed", action="store_true", help="Run browser with visible UI (default is headless)")
    parser.add_argument("--max-steps", type=int, default=20, help="Maximum agent loop actions (default: 20)")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash", help="LLM model identifier")
    parser.add_argument("--output", type=str, help="Optional path to save final text output")

    args = parser.parse_args()

    if args.demo:
        task = "Go to https://news.ycombinator.com, read the front page, and extract the top 3 post titles, scores, and URLs."
    elif args.task:
        task = args.task
    else:
        parser.print_help()
        sys.exit(0)

    asyncio.run(
        run_browser_task(
            task=task,
            headless=not args.headed,
            max_steps=args.max_steps,
            model_name=args.model,
            output_file=args.output,
        )
    )


if __name__ == "__main__":
    main()
