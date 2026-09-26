"""
supabase_client.py
Production-grade Supabase client wrapper for Python.
Supports local Docker Compose stacks, Supabase CLI instances, and Supabase Cloud.
Resilient: operates with or without the official `supabase` PyPI package using standard library HTTP.
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, List, Optional

# Default configuration
DEFAULT_URL = os.getenv("SUPABASE_URL", "http://localhost:8000")
DEFAULT_KEY = os.getenv(
    "SUPABASE_ANON_KEY",
    # Standard local development anon key
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE2MDAwMDAwMDAsImV4cCI6MjAwMDAwMDAwMH0.M1m5sK_4-yHk9jN7X0wK3pQ8g7h9r3v2y1t0q8p9o6w"
)
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

class SupabaseRestClient:
    """Lightweight REST & PostgREST client for Supabase without external dependencies."""

    def __init__(self, url: str = DEFAULT_URL, key: str = DEFAULT_KEY):
        self.url = url.rstrip("/")
        self.key = key
        self.rest_url = f"{self.url}/rest/v1"
        self.auth_url = f"{self.url}/auth/v1"
        self.storage_url = f"{self.url}/storage/v1"

    def _headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Antigravity-Supabase-Client/1.0"
        }
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def _request(self, method: str, endpoint: str, data: Optional[Any] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 10) -> Dict[str, Any]:
        url = endpoint if endpoint.startswith("http") else f"{self.url}/{endpoint.lstrip('/')}"
        req_headers = self._headers(headers)
        req_data = None
        if data is not None:
            req_data = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read().decode("utf-8")
                return {
                    "status_code": response.status,
                    "data": json.loads(content) if content else None,
                    "ok": True
                }
        except urllib.error.HTTPError as e:
            err_content = e.read().decode("utf-8")
            try:
                err_data = json.loads(err_content)
            except Exception:
                err_data = {"raw": err_content}
            return {
                "status_code": e.code,
                "error": err_data,
                "ok": False
            }
        except Exception as e:
            return {
                "status_code": 0,
                "error": str(e),
                "ok": False
            }

    # PostgREST CRUD Operations
    def select(self, table: str, select: str = "*", filters: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        query_params = {"select": select}
        if filters:
            query_params.update(filters)
        url = f"{self.rest_url}/{table}?{urllib.parse.urlencode(query_params)}"
        return self._request("GET", url)

    def insert(self, table: str, records: Any, upsert: bool = False) -> Dict[str, Any]:
        headers = {"Prefer": "return=representation"}
        if upsert:
            headers["Prefer"] += ",resolution=merge-duplicates"
        url = f"{self.rest_url}/{table}"
        return self._request("POST", url, data=records, headers=headers)

    def update(self, table: str, match_column: str, match_value: str, values: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Prefer": "return=representation"}
        url = f"{self.rest_url}/{table}?{match_column}=eq.{urllib.parse.quote(str(match_value))}"
        return self._request("PATCH", url, data=values, headers=headers)

    def delete(self, table: str, match_column: str, match_value: str) -> Dict[str, Any]:
        url = f"{self.rest_url}/{table}?{match_column}=eq.{urllib.parse.quote(str(match_value))}"
        return self._request("DELETE", url)

    def rpc(self, function_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.rest_url}/rpc/{function_name}"
        return self._request("POST", url, data=params or {})

    # Auth Operations
    def sign_up(self, email: str, password: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {"email": email, "password": password}
        if metadata:
            payload["data"] = metadata
        return self._request("POST", f"{self.auth_url}/signup", data=payload)

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        payload = {"email": email, "password": password}
        return self._request("POST", f"{self.auth_url}/token?grant_type=password", data=payload)

    # Health Check
    def health_check(self) -> Dict[str, Any]:
        result = {
            "gateway": False,
            "rest": False,
            "auth": False,
            "details": {}
        }
        # Check PostgREST root
        res_rest = self._request("GET", f"{self.rest_url}/", timeout=3)
        result["rest"] = res_rest["status_code"] in (200, 401, 404)
        result["details"]["rest"] = res_rest

        # Check Auth health/root
        res_auth = self._request("GET", f"{self.auth_url}/health", timeout=3)
        result["auth"] = res_auth["status_code"] in (200, 401)
        result["details"]["auth"] = res_auth

        result["gateway"] = result["rest"] or result["auth"]
        return result


def get_client(url: Optional[str] = None, key: Optional[str] = None) -> SupabaseRestClient:
    """Return a configured Supabase client."""
    target_url = url or os.getenv("SUPABASE_URL", DEFAULT_URL)
    target_key = key or os.getenv("SUPABASE_ANON_KEY", DEFAULT_KEY)
    return SupabaseRestClient(url=target_url, key=target_key)


def get_client_config() -> Dict[str, str]:
    """Return active client configuration settings."""
    return {
        "url": os.getenv("SUPABASE_URL", DEFAULT_URL),
        "key_prefix": DEFAULT_KEY[:10] + "..." if DEFAULT_KEY else "none",
        "has_service_key": bool(SERVICE_KEY)
    }


if __name__ == "__main__":
    client = get_client()
    print("[*] Active Supabase Configuration:")
    print(json.dumps(get_client_config(), indent=2))
    print("[*] Probing local endpoint health...")
    health = client.health_check()
    print("[*] Gateway reachable:", health["gateway"])
    print("[*] PostgREST reachable:", health["rest"])
    print("[*] Auth reachable:", health["auth"])
