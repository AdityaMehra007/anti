#!/usr/bin/env python3
"""
Infisical Universal CLI & Autonomous SecretOps Control Interface
================================================================
Universal command-line tool for Infisical SecretOps platform.
Manages secrets, projects, high-entropy leak scanning, dynamic leased credentials,
internal PKI TLS certificates, cloud integrations, and cryptographic audit logs.

Usage examples:
  python infisical_cli.py status
  python infisical_cli.py secrets list --env production --reveal
  python infisical_cli.py secrets set API_KEY "super-secret" --tags ai,prod
  python infisical_cli.py secrets rollback API_KEY 1
  python infisical_cli.py scan --path .
  python infisical_cli.py dynamic create-lease pg-db --engine postgres --ttl 1800
  python infisical_cli.py pki issue-cert api.omega.internal --sans api.omega.internal,gateway.omega.internal
  python infisical_cli.py integrations sync int-k8s-prod-01
  python infisical_cli.py audit verify
  python infisical_cli.py run --env production -- python -c "import os; print(os.environ.get('DATABASE_URL'))"
  python infisical_cli.py do-everything
"""

from __future__ import annotations

import os
import sys
import json
import argparse
from typing import Any, List

from infisical_orchestrator import InfisicalClient, InfisicalOrchestrator, InfisicalConfig


def print_table(headers: List[str], rows: List[List[Any]]):
    """Utility to print clean ASCII formatted tables."""
    if not rows:
        print("  (No records found)")
        return
    
    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(val)))
            
    header_str = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    print("  " + header_str)
    print("  " + separator)
    for row in rows:
        row_str = " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
        print("  " + row_str)


def main():
    parser = argparse.ArgumentParser(
        description="Infisical Universal Autonomous SecretOps CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of tables")
    parser.add_argument("--project", default=None, help="Infisical Project ID")
    parser.add_argument("--env", default="production", help="Target environment (dev, staging, production)")

    subparsers = parser.add_subparsers(dest="command", help="Operational Subcommand")

    # 1. status / info
    subparsers.add_parser("status", help="Display cluster telemetry and cryptographic health")
    subparsers.add_parser("info", help="Display cluster telemetry and cryptographic health")

    # 2. projects
    proj_parser = subparsers.add_parser("projects", help="Project and workspace management")
    proj_sub = proj_parser.add_subparsers(dest="proj_cmd")
    proj_sub.add_parser("list", help="List all registered projects")
    p_create = proj_sub.add_parser("create", help="Create a new project")
    p_create.add_argument("name", help="Human-readable project name")
    p_create.add_argument("slug", help="URL and folder safe slug")
    p_create.add_argument("--desc", default="", help="Description")

    # 3. secrets
    sec_parser = subparsers.add_parser("secrets", help="Secret store operations (Zero-Knowledge AES-256-GCM)")
    sec_sub = sec_parser.add_subparsers(dest="sec_cmd")
    
    s_list = sec_sub.add_parser("list", help="List secrets in environment")
    s_list.add_argument("--path", default="/", help="Secret folder path")
    s_list.add_argument("--reveal", action="store_true", help="Decrypt and reveal plain values")
    
    s_get = sec_sub.add_parser("get", help="Get and decrypt a secret")
    s_get.add_argument("key", help="Secret name/key")
    s_get.add_argument("--path", default="/", help="Secret folder path")
    
    s_set = sec_sub.add_parser("set", help="Set or update a secret")
    s_set.add_argument("key", help="Secret name/key")
    s_set.add_argument("value", help="Plain text secret value")
    s_set.add_argument("--path", default="/", help="Secret folder path")
    s_set.add_argument("--comment", default="", help="Comment / note")
    s_set.add_argument("--tags", default="", help="Comma-separated tags")
    
    s_del = sec_sub.add_parser("delete", help="Delete a secret from vault")
    s_del.add_argument("key", help="Secret name/key")
    s_del.add_argument("--path", default="/", help="Secret folder path")
    
    s_roll = sec_sub.add_parser("rollback", help="Roll back a secret to a previous version")
    s_roll.add_argument("key", help="Secret name/key")
    s_roll.add_argument("version", type=int, help="Target historical version number")
    s_roll.add_argument("--path", default="/", help="Secret folder path")

    # 4. scan
    scan_parser = subparsers.add_parser("scan", help="Deep high-entropy secret leak scanning")
    scan_parser.add_argument("--path", default=".", help="Directory to scan")
    scan_parser.add_argument("--text", default=None, help="Inline string or snippet to scan")

    # 5. dynamic
    dyn_parser = subparsers.add_parser("dynamic", help="Dynamic ephemeral secrets & leases")
    dyn_sub = dyn_parser.add_subparsers(dest="dyn_cmd")
    d_create = dyn_sub.add_parser("create-lease", help="Generate ephemeral credentials with TTL")
    d_create.add_argument("name", help="Dynamic secret config name")
    d_create.add_argument("--engine", choices=["postgres", "mysql", "aws-iam", "redis", "mongodb"], default="postgres")
    d_create.add_argument("--ttl", type=int, default=3600, help="Lease time-to-live in seconds")
    dyn_sub.add_parser("list-leases", help="List all generated credential leases")
    d_rev = dyn_sub.add_parser("revoke-lease", help="Revoke active lease immediately")
    d_rev.add_argument("lease_id", help="Lease ID to revoke")

    # 6. pki
    pki_parser = subparsers.add_parser("pki", help="Internal Certificate Authority & X.509 issuance")
    pki_sub = pki_parser.add_subparsers(dest="pki_cmd")
    pki_sub.add_parser("list-cas", help="List registered Certificate Authorities")
    p_issue = pki_sub.add_parser("issue-cert", help="Issue an X.509 TLS certificate")
    p_issue.add_argument("common_name", help="Subject Common Name (e.g. api.domain.internal)")
    p_issue.add_argument("--sans", default="", help="Comma-separated Subject Alternative Names")
    p_issue.add_argument("--ca", default=None, help="Issuer CA ID")
    p_issue.add_argument("--days", type=int, default=90, help="Validity period in days")
    pki_sub.add_parser("list-certs", help="List issued certificates")
    p_rev = pki_sub.add_parser("revoke-cert", help="Revoke certificate and add to CRL")
    p_rev.add_argument("serial", help="Certificate serial number in HEX")
    p_rev.add_argument("--reason", default="KeyCompromise", help="Revocation reason")

    # 7. integrations
    int_parser = subparsers.add_parser("integrations", help="Multi-cloud and CI/CD secret syncing")
    int_sub = int_parser.add_subparsers(dest="int_cmd")
    int_sub.add_parser("list", help="List active cloud integrations")
    i_sync = int_sub.add_parser("sync", help="Trigger immediate sync to external cloud")
    i_sync.add_argument("id", help="Integration ID (e.g. int-k8s-prod-01)")

    # 8. access-requests
    acc_parser = subparsers.add_parser("access-requests", help="Break-glass elevation & approval workflows")
    acc_sub = acc_parser.add_subparsers(dest="acc_cmd")
    a_create = acc_sub.add_parser("create", help="Request break-glass temporary privilege")
    a_create.add_argument("role", help="Requested role")
    a_create.add_argument("reason", help="Operational justification")
    a_create.add_argument("--duration", type=int, default=60, help="Duration in minutes")
    a_app = acc_sub.add_parser("approve", help="Approve an access request")
    a_app.add_argument("request_id", help="Access request ID")
    a_app.add_argument("--approver", default="security-lead", help="Approver identity")
    acc_sub.add_parser("list", help="List all access requests")

    # 9. audit
    aud_parser = subparsers.add_parser("audit", help="Cryptographic SHA-256 audit log ledger")
    aud_sub = aud_parser.add_subparsers(dest="aud_cmd")
    a_list = aud_sub.add_parser("list", help="List recent audit entries")
    a_list.add_argument("--limit", type=int, default=20, help="Max records")
    aud_sub.add_parser("verify", help="Verify mathematical integrity of SHA-256 hash chain")

    # 10. run
    run_parser = subparsers.add_parser("run", help="Inject decrypted secrets into command environment in-memory")
    run_parser.add_argument("--env", default="production", help="Environment to inject")
    run_parser.add_argument("command_args", nargs=argparse.REMAINDER, help="Command and arguments to execute")

    # 11. do-everything
    subparsers.add_parser("do-everything", help="Execute complete 12-Phase Sovereign Lifecycle")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    config = InfisicalConfig(
        project_id=args.project or "proj-omega-core-001",
        environment=args.env,
    )
    client = InfisicalClient(config)

    # -----------------------------------------------------------------
    # Command Dispatch
    # -----------------------------------------------------------------

    if args.command in ("status", "info"):
        data = client.get_telemetry()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print("\n  === INFISICAL SOVEREIGN SECRETOPS TELEMETRY ===")
            print(f"  Mode           : {data['mode']}")
            print(f"  Version        : {data['version']}")
            print(f"  Cipher         : {data['crypto']['cipher']}")
            print(f"  Key Derivation : {data['crypto']['kdf']}")
            print(f"  Audit Chain    : {'VALID [OK]' if data['crypto']['audit_chain_valid'] else 'CORRUPTED [!]'} ({data['crypto']['audit_records_count']} blocks)")
            print(f"  Projects       : {data['metrics']['projects_count']}")
            print(f"  Stored Secrets : {data['metrics']['secrets_count']}")
            print(f"  Active Leases  : {data['metrics']['active_leases']}")
            print(f"  PKI CAs / Certs: {data['metrics']['pki_cas_count']} / {data['metrics']['pki_certs_count']}")
            print(f"  Integrations   : {data['metrics']['integrations_count']}")
            print(f"  Pending Elevs  : {data['metrics']['pending_access_requests']}\n")

    elif args.command == "projects":
        if args.proj_cmd == "create":
            p = client.create_project(args.name, args.slug, args.desc)
            if args.json:
                print(json.dumps(p, indent=2))
            else:
                print(f"[OK] Project created: {p['name']} ({p['id']})")
        else:
            projects = client.list_projects()
            if args.json:
                print(json.dumps(projects, indent=2))
            else:
                print(f"\n  === REGISTERED PROJECTS ({len(projects)}) ===")
                rows = [[p["id"], p["name"], p["slug"], ",".join(p["environments"][:3]), p["secrets_count"]] for p in projects]
                print_table(["ID", "Name", "Slug", "Environments", "Secrets"], rows)
                print()

    elif args.command == "secrets":
        if args.sec_cmd == "get":
            sec = client.get_secret(args.key, secret_path=args.path)
            if not sec:
                print(f"[ERROR] Secret '{args.key}' not found in {args.env}:{args.path}")
                sys.exit(1)
            if args.json:
                print(json.dumps(sec, indent=2))
            else:
                print(f"\n  Key        : {sec['key']}")
                print(f"  Value      : {sec['value']}")
                print(f"  Version    : v{sec['version']}")
                print(f"  Environment: {sec['environment']}")
                print(f"  Path       : {sec['secret_path']}")
                print(f"  Comment    : {sec['comment']}")
                print(f"  Tags       : {', '.join(sec['tags'])}\n")

        elif args.sec_cmd == "set":
            tags_list = [t.strip() for t in args.tags.split(",") if t.strip()]
            sec = client.set_secret(
                key=args.key,
                value=args.value,
                secret_path=args.path,
                comment=args.comment,
                tags=tags_list,
            )
            if args.json:
                print(json.dumps(sec, indent=2))
            else:
                print(f"[OK] Secret set: {sec['key']} (v{sec['version']}, AES-256-GCM Encrypted)")

        elif args.sec_cmd == "delete":
            ok = client.delete_secret(args.key, secret_path=args.path)
            if ok:
                print(f"[OK] Secret '{args.key}' deleted from vault.")
            else:
                print(f"[ERROR] Secret '{args.key}' not found.")
                sys.exit(1)

        elif args.sec_cmd == "rollback":
            sec = client.rollback_secret(args.key, args.version, secret_path=args.path)
            if not sec:
                print(f"[ERROR] Could not rollback secret '{args.key}' to v{args.version}.")
                sys.exit(1)
            if args.json:
                print(json.dumps(sec, indent=2))
            else:
                print(f"[OK] Rolled back secret '{args.key}' to version {args.version} (now at v{sec['version']})")

        else:
            # list
            secrets = client.list_secrets(secret_path=args.path, reveal_values=args.reveal)
            if args.json:
                print(json.dumps(secrets, indent=2))
            else:
                print(f"\n  === SECRETS IN [{args.env}:{args.path}] ({len(secrets)}) ===")
                rows = [[s["key"], s["value"], f"v{s['version']}", ",".join(s["tags"]), s["comment"]] for s in secrets]
                print_table(["Key", "Value (AES-256-GCM)", "Version", "Tags", "Comment"], rows)
                print()

    elif args.command == "scan":
        if args.text:
            matches = client.scan_content_for_leaks(args.text, label="<cli_input>")
        else:
            matches = client.scan_workspace_for_leaks(args.path)

        if args.json:
            print(json.dumps(matches, indent=2))
        else:
            print(f"\n  === INFISICAL DEEP SECRET SCANNER FINDINGS ({len(matches)}) ===")
            if not matches:
                print("  [OK] Zero leaked credentials detected. Workspace is SECURE.")
            else:
                rows = [[m["severity"], m["rule_name"], f"{m['file_path']}:{m['line_number']}", m["entropy"], m["snippet"]] for m in matches]
                print_table(["Severity", "Rule Name", "Location", "Entropy", "Snippet"], rows)
            print()

    elif args.command == "dynamic":
        if args.dyn_cmd == "create-lease":
            lease = client.create_dynamic_secret_lease(args.name, engine_type=args.engine, ttl_seconds=args.ttl)
            if args.json:
                print(json.dumps(lease, indent=2))
            else:
                print(f"\n  === EPHEMERAL DYNAMIC CREDENTIAL GENERATED ===")
                print(f"  Lease ID   : {lease['lease_id']}")
                print(f"  Engine     : {lease['engine_type']}")
                print(f"  Username   : {lease['username']}")
                print(f"  Password   : {lease['password']}")
                print(f"  TTL        : {lease['ttl_seconds']}s (Expires: {lease['expires_at']})\n")

        elif args.dyn_cmd == "revoke-lease":
            ok = client.revoke_dynamic_lease(args.lease_id)
            if ok:
                print(f"[OK] Leased credential {args.lease_id} REVOKED.")
            else:
                print(f"[ERROR] Lease {args.lease_id} not found.")

        else:
            leases = client.list_dynamic_leases()
            if args.json:
                print(json.dumps(leases, indent=2))
            else:
                print(f"\n  === DYNAMIC SECRET LEASES ({len(leases)}) ===")
                rows = [[l["lease_id"], l["secret_name"], l["engine_type"], l["username"], l["status"], f"{l['ttl_seconds']}s"] for l in leases]
                print_table(["Lease ID", "Secret", "Engine", "Username", "Status", "TTL"], rows)
                print()

    elif args.command == "pki":
        if args.pki_cmd == "issue-cert":
            sans = [s.strip() for s in args.sans.split(",") if s.strip()] or [args.common_name]
            cert = client.issue_tls_certificate(args.common_name, sans=sans, ca_id=args.ca, validity_days=args.days)
            if args.json:
                print(json.dumps(cert, indent=2))
            else:
                print(f"\n  === X.509 TLS CERTIFICATE ISSUED ===")
                print(f"  Serial Number : {cert['serial_number']}")
                print(f"  Common Name   : {cert['subject_cn']}")
                print(f"  SANs          : {', '.join(cert['sans'])}")
                print(f"  Valid Until   : {cert['not_after']}")
                print(f"  Status        : {cert['status']}\n")

        elif args.pki_cmd == "revoke-cert":
            ok = client.revoke_certificate(args.serial, reason=args.reason)
            if ok:
                print(f"[OK] Certificate {args.serial} REVOKED and posted to CRL.")
            else:
                print(f"[ERROR] Certificate {args.serial} not found.")

        elif args.pki_cmd == "list-cas":
            cas = client.list_certificate_authorities()
            if args.json:
                print(json.dumps(cas, indent=2))
            else:
                print(f"\n  === CERTIFICATE AUTHORITIES ({len(cas)}) ===")
                rows = [[ca["id"], ca["common_name"], "Root CA" if ca["is_root"] else "Intermediate", ca["status"]] for ca in cas]
                print_table(["ID", "Common Name", "Type", "Status"], rows)
                print()

        else:
            certs = client.list_certificates()
            if args.json:
                print(json.dumps(certs, indent=2))
            else:
                print(f"\n  === ISSUED TLS CERTIFICATES ({len(certs)}) ===")
                rows = [[c["serial_number"][:16] + "...", c["subject_cn"], ",".join(c["sans"][:2]), c["status"], c["not_after"][:10]] for c in certs]
                print_table(["Serial", "Common Name", "SANs", "Status", "Expires"], rows)
                print()

    elif args.command == "integrations":
        if args.int_cmd == "sync":
            res = client.sync_integration(args.id)
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print(f"[OK] Integration '{res['name']}' ({res['target']}) synced {res['synced_keys_count']} secrets to {res['target_env']}.")
        else:
            integrations = client.list_integrations()
            if args.json:
                print(json.dumps(integrations, indent=2))
            else:
                print(f"\n  === CLOUD INTEGRATIONS ({len(integrations)}) ===")
                rows = [[i["id"], i["name"], i["target"], f"{i['source_env']} -> {i['target_env']}", i["sync_status"], i["synced_keys_count"]] for i in integrations]
                print_table(["ID", "Name", "Target", "Mapping", "Status", "Keys Synced"], rows)
                print()

    elif args.command == "access-requests":
        if args.acc_cmd == "create":
            req = client.create_access_request(
                requester="cli-user",
                role=args.role,
                reason=args.reason,
                duration_minutes=args.duration,
                environment=args.env,
            )
            if args.json:
                print(json.dumps(req, indent=2))
            else:
                print(f"[OK] Access request submitted: {req['request_id']} for role '{req['role_requested']}'")

        elif args.acc_cmd == "approve":
            req = client.approve_access_request(args.request_id, approver=args.approver)
            if args.json:
                print(json.dumps(req, indent=2))
            else:
                print(f"[OK] Access request {req['request_id']} APPROVED by {req['approver']}.")

        else:
            requests = client.list_access_requests()
            if args.json:
                print(json.dumps(requests, indent=2))
            else:
                print(f"\n  === ACCESS APPROVAL REQUESTS ({len(requests)}) ===")
                rows = [[r["request_id"], r["requester"], r["role_requested"], r["environment"], r["status"], r["reason"]] for r in requests]
                print_table(["Request ID", "Requester", "Role", "Env", "Status", "Reason"], rows)
                print()

    elif args.command == "audit":
        if args.aud_cmd == "verify":
            res = client.verify_audit_ledger()
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                if res["valid"]:
                    print(f"\n  [OK] SHA-256 Cryptographic Audit Blockchain VERIFIED.")
                    print(f"       Records Verified : {res['records_verified']}")
                    print(f"       Latest Root Hash : {res['latest_block_hash']}\n")
                else:
                    print(f"\n  [!] AUDIT INTEGRITY FAILURE: {res['error']}\n")
                    sys.exit(1)
        else:
            logs = client.list_audit_logs(limit=args.limit)
            if args.json:
                print(json.dumps(logs, indent=2))
            else:
                print(f"\n  === RECENT CRYPTOGRAPHIC AUDIT LOGS ({len(logs)}) ===")
                rows = [[l["timestamp"][:19], l["actor"], l["action"], l["resource_type"], l["hash"][:12] + "..."] for l in logs]
                print_table(["Timestamp", "Actor", "Action", "Resource", "Hash Block"], rows)
                print()

    elif args.command == "run":
        cmd_args = args.command_args
        if cmd_args and cmd_args[0] == "--":
            cmd_args = cmd_args[1:]
        if not cmd_args:
            print("[ERROR] No command specified for execution. Example: python infisical_cli.py run -- node server.js")
            sys.exit(1)

        code, stdout, stderr = client.run_with_secrets(cmd_args, environment=args.env)
        if stdout:
            sys.stdout.write(stdout)
        if stderr:
            sys.stderr.write(stderr)
        sys.exit(code)

    elif args.command == "do-everything":
        orchestrator = InfisicalOrchestrator(client)
        manifest = orchestrator.do_everything()
        if args.json:
            print(json.dumps(manifest, indent=2))
        else:
            print("\n" + "=" * 70)
            print("  OMEGA INFISICAL SOVEREIGN SECRETOPS LIFECYCLE: 100% CERTIFIED")
            print("=" * 70)
            for p in manifest["phases"]:
                print(f"  [OK] Phase {p['phase']:2d}: {p['name']} ({p['duration_ms']} ms)")
            print("=" * 70)
            print(f"  Manifest written to: omega/data/infisical_do_everything_manifest.json")
            print(f"  Audit Blockchain Hash: {manifest['cryptographic_ledger_signature']}")
            print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
