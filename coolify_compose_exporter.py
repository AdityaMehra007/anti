"""
Coolify Template Compose Exporter
=================================
Extracts, decodes, and variable-interpolates Docker Compose stacks directly from
Coolify's 352+ service templates catalog.
Generates fully functional, standalone docker-compose.yml and .env files ready
for immediate local Docker Desktop or remote server deployment.
"""

from __future__ import annotations

import os
import re
import json
import base64
import secrets
from typing import Any, Dict, Optional, Tuple


class CoolifyComposeExporter:
    """
    Decodes and processes base64 Docker Compose templates from Coolify.
    Automatically generates required secrets, hashes, and service variables.
    """
    def __init__(self, catalog_path: Optional[str] = None):
        default_path = os.path.join(os.path.dirname(__file__), "coolify", "templates", "service-templates-latest.json")
        self.catalog_path = catalog_path or default_path
        self.templates: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.catalog_path):
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                self.templates = json.load(f)

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        return self.templates.get(template_id)

    def export(
        self,
        template_id: str,
        domain: str = "localhost",
        custom_env: Optional[Dict[str, str]] = None
    ) -> Tuple[str, Dict[str, str]]:
        """
        Export a decoded and populated docker-compose YAML and its generated .env dictionary.
        """
        tpl = self.get_template(template_id)
        if not tpl or "compose" not in tpl:
            raise ValueError(f"Template '{template_id}' not found or does not contain compose data.")

        # Decode base64 compose
        raw_compose = base64.b64decode(tpl["compose"]).decode("utf-8")

        # Find all environment variable references ${VAR} or ${VAR:-default}
        env_vars: Dict[str, str] = custom_env.copy() if custom_env else {}

        # Scan for magic Coolify placeholders
        placeholders = re.findall(r"\$\{([A-Za-z0-9_]+)(?::-[^}]*)?\}", raw_compose)
        for var in set(placeholders):
            if var not in env_vars:
                if "PASSWORD" in var or "SECRET" in var or "KEY" in var or "SALT" in var:
                    env_vars[var] = secrets.token_urlsafe(24)
                elif "USER" in var:
                    env_vars[var] = "admin"
                elif "EMAIL" in var:
                    env_vars[var] = f"admin@{domain}"
                elif "URL" in var or "FQDN" in var:
                    env_vars[var] = f"http://{domain}"
                elif "PORT" in var:
                    env_vars[var] = str(tpl.get("port", "8080"))
                else:
                    env_vars[var] = "value"

        # Also support SERVICE_URL_ placeholders without ${}
        raw_placeholders = re.findall(r"(SERVICE_URL_[A-Za-z0-9_]+)", raw_compose)
        for var in set(raw_placeholders):
            if var not in env_vars:
                port = tpl.get("port", "80")
                env_vars[var] = f"http://{template_id}.{domain}:{port}"

        return raw_compose, env_vars

    def save_stack(self, template_id: str, target_dir: str, domain: str = "localhost") -> Dict[str, str]:
        """
        Save the docker-compose.yml and .env files to target directory.
        """
        compose_content, env_dict = self.export(template_id, domain)
        os.makedirs(target_dir, exist_ok=True)

        compose_path = os.path.join(target_dir, "docker-compose.yml")
        env_path = os.path.join(target_dir, ".env")

        with open(compose_path, "w", encoding="utf-8") as f:
            f.write(compose_content)

        with open(env_path, "w", encoding="utf-8") as f:
            for k, v in sorted(env_dict.items()):
                f.write(f"{k}={v}\n")

        return {
            "compose_path": compose_path,
            "env_path": env_path,
            "template_id": template_id,
            "total_vars": str(len(env_dict))
        }
