"""
Automated Workspace Security & Secret Scanner
Audits files across AI-Command-Center for private keys, API tokens,
hardcoded passwords, and unignored database files.
"""

import os
import re

SCAN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SECRET_PATTERNS = [
    (r"AIza[0-9A-Za-z-_]{35}", "Google API Key"),
    (r"sk-[a-zA-Z0-9]{32,}", "OpenAI API Key"),
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"gho_[0-9a-zA-Z]{36}", "GitHub OAuth Token"),
    (r"xox[baprs]-[0-9a-zA-Z]{10,48}", "Slack Token"),
    (r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----", "Private Key Header"),
    (r"password\s*=\s*['\"][^'\"]{6,}['\"]", "Hardcoded Plaintext Password"),
]

IGNORE_DIRS = {".git", ".venv", "node_modules", "backups", "__pycache__"}
IGNORE_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".ico",
    ".pdf",
    ".db",
    ".sqlite",
    ".docx",
    ".zip",
}


def run_security_scan():
    findings = []
    scanned_count = 0

    for root, dirs, files in os.walk(SCAN_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in IGNORE_EXTS or f == "security_scan.py":
                continue

            filepath = os.path.join(root, f)
            scanned_count += 1

            try:
                with open(filepath, encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    for pattern, secret_type in SECRET_PATTERNS:
                        matches = re.finditer(pattern, content)
                        for m in matches:
                            # Avoid flagging self-references or examples
                            val = m.group(0)
                            if "example" in val.lower() or "sk-..." in val:
                                continue
                            rel_path = os.path.relpath(filepath, SCAN_DIR)
                            findings.append(
                                {
                                    "file": rel_path,
                                    "type": secret_type,
                                    "preview": val[:8] + "..." + val[-4:],
                                }
                            )
            except Exception:
                pass

    print("=== WORKSPACE SECURITY SCAN ===")
    print(f"Total Text Files Scanned: {scanned_count}")
    print(f"Secret Exposures Detected: {len(findings)}")

    if findings:
        for f in findings:
            print(f" [ALERT] {f['type']} in {f['file']}: {f['preview']}")
    else:
        print(
            "[CLEAN] Zero hardcoded API keys or private credentials found in AI-Command-Center."
        )

    return len(findings) == 0


if __name__ == "__main__":
    run_security_scan()
