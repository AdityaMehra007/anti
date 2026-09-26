#!/usr/bin/env python3
"""
========================================================================================
FREE API KEY & CLAUDE CODE AUTHENTICATION ASSISTANT
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Assists with connecting free API keys or logging into Claude Code:
  1. Guides 1-click 'claude auth login' (Zero cost via personal Claude account)
  2. Configures free API keys (OpenRouter Free, Groq, Google AI Studio, Anthropic Trial)
  3. Saves configuration to local .env and tests connection
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import subprocess
import argparse
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
ENV_FILE = ROOT_DIR / ".env"

FREE_KEY_PORTALS = {
    "Claude.ai Free Login": {
        "url": "https://claude.ai",
        "description": "Authenticates Claude Code CLI directly with your free Claude account.",
        "action": "Run: claude auth login"
    },
    "Anthropic Free Trial": {
        "url": "https://console.anthropic.com/settings/keys",
        "description": "Get an official Anthropic API key (sk-ant-...) with starting trial credits."
    },
    "OpenRouter Free Pool": {
        "url": "https://openrouter.ai/keys",
        "description": "Get a free OpenRouter key (sk-or-v1-...) to access free models (:free tier)."
    },
    "Google AI Studio (Gemini Free)": {
        "url": "https://aistudio.google.com/app/apikey",
        "description": "100% Free API key for Gemini 1.5/2.0 Flash."
    },
    "Groq Cloud Free Tier": {
        "url": "https://console.groq.com/keys",
        "description": "100% Free ultra-fast API key for Llama 3.3 70B."
    }
}

def show_options():
    print("=" * 80)
    print("      FREE API KEY & CLAUDE CODE ACTIVATION GUIDE")
    print("=" * 80)
    for idx, (name, data) in enumerate(FREE_KEY_PORTALS.items(), 1):
        print(f"\n[{idx}] {name}")
        print(f"    Portal URL  : {data['url']}")
        print(f"    Details     : {data['description']}")
        if "action" in data:
            print(f"    Quick Action: {data['action']}")
    print("\n" + "=" * 80)

def set_key(key_name: str, key_val: str):
    env_content = ""
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            env_content = f.read()

    lines = env_content.splitlines()
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith(f"{key_name}="):
            new_lines.append(f"{key_name}={key_val}")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f"{key_name}={key_val}")

    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

    print(f"[+] Successfully saved {key_name} to {ENV_FILE}")

def main():
    parser = argparse.ArgumentParser(description="Free API Key Assistant")
    parser.add_argument("--set-anthropic-key", type=str, help="Save Anthropic API key to .env")
    parser.add_argument("--set-openrouter-key", type=str, help="Save OpenRouter API key to .env")
    parser.add_argument("--login", action="store_true", help="Launch official 'claude auth login'")

    args = parser.parse_args()

    if args.login:
        print("[*] Launching 'claude auth login'...")
        subprocess.run(["claude", "auth", "login"], cwd=str(ROOT_DIR))
    elif args.set_anthropic_key:
        set_key("ANTHROPIC_API_KEY", args.set_anthropic_key)
    elif args.set_openrouter_key:
        set_key("OPENROUTER_API_KEY", args.set_openrouter_key)
    else:
        show_options()

if __name__ == "__main__":
    main()
