import os
import sys
import json
import sqlite3
import subprocess

print("=== MACHINE & RUNTIME ===")
print("Python:", sys.version)
print("Executable:", sys.executable)

user_profile = os.environ.get("USERPROFILE", "")
local_app_data = os.environ.get("LOCALAPPDATA", "")

# 1. MCP Servers
mcp_dir = os.path.join(user_profile, ".gemini", "antigravity", "mcp")
print("\n=== MCP SERVERS IN CONFIG ===")
if os.path.exists(mcp_dir):
    for item in os.listdir(mcp_dir):
        print(" -", item)
else:
    print("No MCP dir found")

# 2. Chrome Extensions
print("\n=== CHROME EXTENSIONS ===")
chrome_ext = os.path.join(local_app_data, "Google", "Chrome", "User Data", "Default", "Extensions")
if os.path.exists(chrome_ext):
    for ext_id in os.listdir(chrome_ext):
        ext_path = os.path.join(chrome_ext, ext_id)
        if os.path.isdir(ext_path):
            versions = os.listdir(ext_path)
            if versions:
                manifest_path = os.path.join(ext_path, versions[0], "manifest.json")
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, "r", encoding="utf-8", errors="ignore") as f:
                            data = json.load(f)
                            print(f" - {data.get('name')} | ID: {ext_id} | Version: {data.get('version')}")
                    except Exception as e:
                        print(f" - ID: {ext_id} (error reading manifest)")
                else:
                    print(f" - ID: {ext_id}")
else:
    print("Chrome Default profile not found or empty")

# 3. Environment & Credentials
print("\n=== GOOGLE & THIRD PARTY ENVIRONMENT KEYS ===")
env_file = r"e:\anti\.env"
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key = line.split("=")[0].strip()
                print(" - Configured Key:", key)
else:
    print("No .env file found at e:\\anti\\.env")

# 4. Chrome DevTools MCP check
cdp_mcp = os.path.join(mcp_dir, "chrome-devtools-mcp")
print("\n=== CHROME DEVTOOLS MCP ===")
if os.path.exists(cdp_mcp):
    print("Found chrome-devtools-mcp in:", cdp_mcp)
    print("Files:", os.listdir(cdp_mcp))
else:
    print("chrome-devtools-mcp folder not present")
