#!/usr/bin/env python3
"""
Airflow Platform Environment Initializer
Generates cryptographic Fernet keys, validates environment configuration, and bootstraps paths.
"""

import base64
import os
from pathlib import Path
import secrets


def generate_fernet_key() -> str:
    """Generates a URL-safe base64-encoded 32-byte key compliant with Fernet specification."""
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()


def main():
    base_dir = Path(__file__).resolve().parent.parent
    env_file = base_dir / ".env"
    env_example = base_dir / ".env.example"

    print("=" * 60)
    print("APACHE AIRFLOW PLATFORM: ENVIRONMENT INITIALIZER")
    print("=" * 60)

    fernet_key = generate_fernet_key()
    print(f"[*] Generated Fresh Fernet Key: {fernet_key}")

    if not env_file.exists() and env_example.exists():
        content = env_example.read_text(encoding="utf-8")
        content = content.replace("46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqBpPo=", fernet_key)
        env_file.write_text(content, encoding="utf-8")
        print(f"[+] Initialized .env from template at: {env_file}")
    elif env_file.exists():
        print(f"[*] Existing .env file found at: {env_file} (leaving untouched)")

    # Ensure required runtime folders exist
    for sub in ["dags", "logs", "plugins", "config"]:
        p = base_dir / sub
        p.mkdir(parents=True, exist_ok=True)
        print(f"[+] Verified directory: {p}")

    print("\n[OK] Initialization complete.")
    print("To launch Airflow:")
    print("  cd airflow_platform")
    print("  docker compose up -d --build")
    print("Web UI will be accessible at: http://localhost:8080 (admin / admin_password)")


if __name__ == "__main__":
    main()
