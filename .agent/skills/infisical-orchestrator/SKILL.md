---
name: infisical-orchestrator
description: Autonomous SDK, CLI, and operational standard for Infisical SecretOps platform. Enables end-to-end encrypted secret management, dynamic credential leases, secret leak scanning, internal PKI/CA issuance, multi-cloud synchronization, break-glass RBAC workflows, and cryptographic audit blockchain verification.
---

# Infisical Autonomous SecretOps Orchestrator Skill

Autonomous standard operating procedure and deep SDK for the Infisical SecretOps platform (https://github.com/Infisical/infisical).

## Architecture & Cryptographic Primitives

1. **Dual-Mode Sovereign Architecture**:
   - **Live Platform Mode**: Directly targets real self-hosted or cloud Infisical servers via REST API (`/api/v1`, `/api/v2`, `/api/v3`) using Universal Auth Machine Identities or Bearer tokens.
   - **Autonomous Sovereign Mode**: Ultra-high-fidelity offline cryptographic simulation engine implementing true AES-256-GCM encryption with 96-bit random nonces, PBKDF2-HMAC-SHA256 (100,000 rounds) key derivation, genuine X.509 Certificate Authority & TLS certificate issuance, and tamper-evident SHA-256 chained audit logs.

2. **Core SecretOps Capabilities**:
   - **Zero-Knowledge Secrets Repository**: Hierarchical folders, multi-environment scoping (`dev`, `staging`, `production`, `sovereign-vault`), point-in-time versioning, and instant rollback.
   - **High-Entropy Secret Scanner**: Detects 35+ credential patterns (AWS, GitHub PATs, Stripe keys, OpenAI/Anthropic keys, Slack tokens, JWTs, private keys) and calculates Shannon entropy in bits per character.
   - **Dynamic Ephemeral Secrets**: Just-in-time credentials for PostgreSQL, MySQL, AWS IAM, Redis, and MongoDB with strict TTL leases and automated revocation.
   - **Internal PKI / Certificate Authority**: Root CA generation, intermediate CA signing, X.509 TLS certificate issuance with Subject Alternative Names (SANs), and Certificate Revocation Lists (CRL).
   - **Multi-Cloud Integrations Sync**: Two-way synchronization formatting and exporting to Kubernetes Secrets (`v1/Secret` Opaque YAML), AWS Secrets Manager, GitHub Actions, and Vercel.
   - **Break-Glass RBAC Workflows**: Dual-custody emergency privilege elevation with required justification and expiration tracking.
   - **Cryptographic Audit Blockchain**: Every secret mutation, read, or escalation is hashed into a SHA-256 Merkle-like chain with tamper verification.
   - **Process Memory Injection**: `infisical run` injects decrypted secrets directly into process memory without touching disk.

## CLI Usage

```bash
# Query cluster telemetry & cryptographic health
python infisical_cli.py status

# List secrets in production (masked)
python infisical_cli.py secrets list --env production

# Reveal decrypted secrets
python infisical_cli.py secrets list --env production --reveal

# Set or update secret with AES-256-GCM encryption and versioning
python infisical_cli.py secrets set OPENAI_API_KEY "sk-live-..." --tags ai,prod --comment "Production model gateway"

# Rollback secret to historical version
python infisical_cli.py secrets rollback OPENAI_API_KEY 1

# Deep scan workspace for leaked credentials
python infisical_cli.py scan --path .

# Generate dynamic ephemeral database credentials with 30m TTL
python infisical_cli.py dynamic create-lease pg-db --engine postgres --ttl 1800

# Issue internal X.509 TLS certificate with SANs
python infisical_cli.py pki issue-cert api.omega.internal --sans api.omega.internal,localhost --days 90

# Trigger two-way sync to Kubernetes cluster
python infisical_cli.py integrations sync int-k8s-prod-01

# Submit and approve break-glass access request
python infisical_cli.py access-requests create "Break-Glass Operator" "Database latency spike triage" --duration 45
python infisical_cli.py access-requests approve req-1234567890

# Cryptographically verify the SHA-256 audit blockchain
python infisical_cli.py audit verify

# Inject secrets directly into application environment in memory (zero disk trace)
python infisical_cli.py run --env production -- python app.py

# Execute the 12-Phase Sovereign SecretOps Lifecycle
python infisical_cli.py do-everything
```

## Local REST API & Mission Control Cockpit

```bash
# Launch API server on port 8772
python infisical_api_server.py --port 8772

# Endpoints:
#   GET  /api/status          - Cluster telemetry & crypto health
#   GET  /api/secrets         - List secrets (?env=production&reveal=false)
#   POST /api/secrets/set     - Provision or update secret
#   POST /api/scan            - Scan snippet for leaks
#   POST /api/dynamic/create  - Generate leased dynamic credentials
#   POST /api/pki/issue       - Issue X.509 TLS certificate
#   POST /api/do-everything   - Run complete 12-phase sovereign lifecycle
```

## Model Context Protocol (MCP) Tools

Run `python infisical_mcp_server.py` over stdio to enable autonomous AI agent SecretOps:
- `infisical_get_telemetry`
- `infisical_list_secrets`
- `infisical_get_secret`
- `infisical_set_secret`
- `infisical_rollback_secret`
- `infisical_scan_workspace`
- `infisical_create_dynamic_lease`
- `infisical_issue_certificate`
- `infisical_sync_cloud_integration`
- `infisical_verify_audit_chain`
- `infisical_run_sovereign_lifecycle`
