#!/usr/bin/env python3
"""
Infisical Autonomous MCP (Model Context Protocol) Server
========================================================
Exposes Infisical SecretOps capabilities, Zero-Knowledge secrets management,
secret leak scanning, dynamic leased credentials, internal PKI X.509 cert issuance,
and tamper-evident audit ledger to AI agents via standard JSON-RPC stdio protocol.

Supported tools:
- infisical_get_telemetry
- infisical_list_projects
- infisical_list_secrets
- infisical_get_secret
- infisical_set_secret
- infisical_rollback_secret
- infisical_scan_workspace
- infisical_scan_snippet
- infisical_create_dynamic_lease
- infisical_revoke_dynamic_lease
- infisical_list_dynamic_leases
- infisical_issue_certificate
- infisical_revoke_certificate
- infisical_sync_cloud_integration
- infisical_create_access_request
- infisical_approve_access_request
- infisical_verify_audit_chain
- infisical_run_sovereign_lifecycle
"""

import sys
import json
import logging
from typing import Any, Dict

from infisical_orchestrator import InfisicalClient, InfisicalOrchestrator

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("infisical_mcp")

client = InfisicalClient()
orchestrator = InfisicalOrchestrator(client)

TOOLS = [
    {
        "name": "infisical_get_telemetry",
        "description": "Get real-time Infisical cluster health, cryptographic algorithms, secret counts, active dynamic leases, and audit blockchain integrity.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "infisical_list_projects",
        "description": "List all registered Infisical projects and environments.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "infisical_list_secrets",
        "description": "List secrets in a specific project and environment (values masked unless reveal is true).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string", "description": "Project ID"},
                "environment": {"type": "string", "description": "Target environment (dev, staging, production)"},
                "path": {"type": "string", "default": "/", "description": "Secret folder path"},
                "reveal": {"type": "boolean", "default": False, "description": "Whether to decrypt and return plaintext values"}
            }
        }
    },
    {
        "name": "infisical_get_secret",
        "description": "Retrieve and decrypt a specific secret using AES-256-GCM.",
        "inputSchema": {
            "type": "object",
            "required": ["key"],
            "properties": {
                "key": {"type": "string", "description": "Secret key name"},
                "project_id": {"type": "string", "description": "Project ID"},
                "environment": {"type": "string", "description": "Target environment"},
                "path": {"type": "string", "default": "/", "description": "Secret folder path"}
            }
        }
    },
    {
        "name": "infisical_set_secret",
        "description": "Encrypt and store a secret using Zero-Knowledge AES-256-GCM with automatic point-in-time versioning.",
        "inputSchema": {
            "type": "object",
            "required": ["key", "value"],
            "properties": {
                "key": {"type": "string", "description": "Secret key name"},
                "value": {"type": "string", "description": "Plaintext secret value"},
                "project_id": {"type": "string", "description": "Project ID"},
                "environment": {"type": "string", "default": "production", "description": "Environment"},
                "path": {"type": "string", "default": "/", "description": "Folder path"},
                "comment": {"type": "string", "default": "", "description": "Documentation note"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Labels/tags"}
            }
        }
    },
    {
        "name": "infisical_rollback_secret",
        "description": "Roll back an existing secret to any historical version.",
        "inputSchema": {
            "type": "object",
            "required": ["key", "version"],
            "properties": {
                "key": {"type": "string", "description": "Secret key name"},
                "version": {"type": "integer", "description": "Target version number to restore"},
                "project_id": {"type": "string", "description": "Project ID"},
                "environment": {"type": "string", "default": "production"}
            }
        }
    },
    {
        "name": "infisical_scan_workspace",
        "description": "Scan codebase files for leaked credentials, private keys, and high-entropy tokens.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "default": ".", "description": "Directory path to scan"}
            }
        }
    },
    {
        "name": "infisical_scan_snippet",
        "description": "Scan a code snippet, config file, or PR diff for secret leaks.",
        "inputSchema": {
            "type": "object",
            "required": ["text"],
            "properties": {
                "text": {"type": "string", "description": "Text content to scan"},
                "label": {"type": "string", "default": "<agent_input>", "description": "File label or source"}
            }
        }
    },
    {
        "name": "infisical_create_dynamic_lease",
        "description": "Generate on-demand ephemeral credentials with automatic TTL expiration (PostgreSQL, MySQL, AWS IAM, Redis, MongoDB).",
        "inputSchema": {
            "type": "object",
            "required": ["secret_name"],
            "properties": {
                "secret_name": {"type": "string", "description": "Name of dynamic secret config"},
                "engine_type": {"type": "string", "enum": ["postgres", "mysql", "aws-iam", "redis", "mongodb"], "default": "postgres"},
                "ttl_seconds": {"type": "integer", "default": 3600, "description": "TTL in seconds"}
            }
        }
    },
    {
        "name": "infisical_revoke_dynamic_lease",
        "description": "Immediately revoke an active dynamic credential lease.",
        "inputSchema": {
            "type": "object",
            "required": ["lease_id"],
            "properties": {
                "lease_id": {"type": "string", "description": "Lease ID to revoke"}
            }
        }
    },
    {
        "name": "infisical_list_dynamic_leases",
        "description": "List all active, expired, and revoked dynamic credential leases.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "infisical_issue_certificate",
        "description": "Issue an internal X.509 TLS certificate signed by the Sovereign Certificate Authority.",
        "inputSchema": {
            "type": "object",
            "required": ["common_name"],
            "properties": {
                "common_name": {"type": "string", "description": "Subject Common Name (e.g. service.internal)"},
                "sans": {"type": "array", "items": {"type": "string"}, "description": "Subject Alternative Names"},
                "validity_days": {"type": "integer", "default": 90, "description": "Validity period in days"}
            }
        }
    },
    {
        "name": "infisical_revoke_certificate",
        "description": "Revoke an X.509 certificate and register it on the Certificate Revocation List (CRL).",
        "inputSchema": {
            "type": "object",
            "required": ["serial_number"],
            "properties": {
                "serial_number": {"type": "string", "description": "Certificate serial number"},
                "reason": {"type": "string", "default": "KeyCompromise", "description": "Revocation reason"}
            }
        }
    },
    {
        "name": "infisical_sync_cloud_integration",
        "description": "Trigger two-way secret synchronization to Kubernetes, AWS Secrets Manager, GitHub Actions, or Vercel.",
        "inputSchema": {
            "type": "object",
            "required": ["integration_id"],
            "properties": {
                "integration_id": {"type": "string", "description": "Integration ID (e.g. int-k8s-prod-01)"}
            }
        }
    },
    {
        "name": "infisical_create_access_request",
        "description": "Submit a break-glass temporary privilege elevation request.",
        "inputSchema": {
            "type": "object",
            "required": ["role", "reason"],
            "properties": {
                "role": {"type": "string", "description": "Requested elevated role"},
                "reason": {"type": "string", "description": "Operational justification"},
                "duration_minutes": {"type": "integer", "default": 60, "description": "Duration in minutes"},
                "environment": {"type": "string", "default": "production"}
            }
        }
    },
    {
        "name": "infisical_approve_access_request",
        "description": "Approve a break-glass access request.",
        "inputSchema": {
            "type": "object",
            "required": ["request_id"],
            "properties": {
                "request_id": {"type": "string", "description": "Request ID"},
                "approver": {"type": "string", "default": "secops-director", "description": "Approver identity"}
            }
        }
    },
    {
        "name": "infisical_verify_audit_chain",
        "description": "Verify the mathematical integrity of the SHA-256 tamper-evident audit blockchain.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "infisical_run_sovereign_lifecycle",
        "description": "Execute the full 12-Phase Sovereign SecretOps Lifecycle and return certified manifest.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]


def dispatch_tool(name: str, args: Dict[str, Any]) -> Any:
    """Dispatches tool call to Infisical client/orchestrator."""
    if name == "infisical_get_telemetry":
        return client.get_telemetry()
    elif name == "infisical_list_projects":
        return client.list_projects()
    elif name == "infisical_list_secrets":
        return client.list_secrets(
            project_id=args.get("project_id"),
            environment=args.get("environment"),
            secret_path=args.get("path", "/"),
            reveal_values=args.get("reveal", False),
        )
    elif name == "infisical_get_secret":
        res = client.get_secret(
            key=args["key"],
            project_id=args.get("project_id"),
            environment=args.get("environment"),
            secret_path=args.get("path", "/"),
        )
        return res or {"error": f"Secret '{args['key']}' not found"}
    elif name == "infisical_set_secret":
        return client.set_secret(
            key=args["key"],
            value=args["value"],
            project_id=args.get("project_id"),
            environment=args.get("environment", "production"),
            secret_path=args.get("path", "/"),
            comment=args.get("comment", ""),
            tags=args.get("tags", []),
        )
    elif name == "infisical_rollback_secret":
        res = client.rollback_secret(
            key=args["key"],
            target_version=args["version"],
            project_id=args.get("project_id"),
            environment=args.get("environment", "production"),
        )
        return res or {"error": f"Failed to rollback secret '{args['key']}' to v{args['version']}"}
    elif name == "infisical_scan_workspace":
        return client.scan_workspace_for_leaks(args.get("path", "."))
    elif name == "infisical_scan_snippet":
        return client.scan_content_for_leaks(args["text"], label=args.get("label", "<agent_input>"))
    elif name == "infisical_create_dynamic_lease":
        return client.create_dynamic_secret_lease(
            secret_name=args["secret_name"],
            engine_type=args.get("engine_type", "postgres"),
            ttl_seconds=args.get("ttl_seconds", 3600),
        )
    elif name == "infisical_revoke_dynamic_lease":
        return {"revoked": client.revoke_dynamic_lease(args["lease_id"])}
    elif name == "infisical_list_dynamic_leases":
        return client.list_dynamic_leases()
    elif name == "infisical_issue_certificate":
        return client.issue_tls_certificate(
            common_name=args["common_name"],
            sans=args.get("sans"),
            validity_days=args.get("validity_days", 90),
        )
    elif name == "infisical_revoke_certificate":
        return {"revoked": client.revoke_certificate(args["serial_number"], reason=args.get("reason", "KeyCompromise"))}
    elif name == "infisical_sync_cloud_integration":
        return client.sync_integration(args["integration_id"])
    elif name == "infisical_create_access_request":
        return client.create_access_request(
            requester="agent",
            role=args["role"],
            reason=args["reason"],
            duration_minutes=args.get("duration_minutes", 60),
            environment=args.get("environment", "production"),
        )
    elif name == "infisical_approve_access_request":
        return client.approve_access_request(args["request_id"], approver=args.get("approver", "secops-director"))
    elif name == "infisical_verify_audit_chain":
        return client.verify_audit_ledger()
    elif name == "infisical_run_sovereign_lifecycle":
        return orchestrator.do_everything()
    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    """Runs standard JSON-RPC stdio loop for MCP."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            try:
                result = dispatch_tool(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                    }
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32603, "message": str(e)}
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

        elif method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "infisical-mcp-server", "version": "2.0.0"}
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
