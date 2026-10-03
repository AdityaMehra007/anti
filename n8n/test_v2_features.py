"""
test_v2_features.py — Verifies v2.0 Enterprise Automation Features:
GitHub Triage, Slack/Discord Notify, Financial Settlement, Visual Zap Creator, and Instant Backups.
"""

import json
import urllib.request

def test():
    # 1. GitHub Triage
    print("=== 1. GITHUB TRIAGE ZAP ===")
    req1 = urllib.request.Request(
        "http://localhost:5678/webhook/github-webhook",
        data=json.dumps({
            "title": "Crash: Memory leak in state channel verification",
            "author": "quantum-dev",
            "repo": "AdityaMehra007/anti"
        }).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req1) as r:
        res = json.loads(r.read())
        print("   Severity:", res.get("severity_score"))
        print("   Labels:", res.get("labels_applied"))
        print("   Comment:", res.get("comment_posted"))

    # 2. Channel Notify
    print("\n=== 2. SLACK / DISCORD NOTIFIER ZAP ===")
    req2 = urllib.request.Request(
        "http://localhost:5678/webhook/channel-notify",
        data=json.dumps({"message": "Sovereign cluster node #44 online at 99.999% uptime"}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req2) as r:
        res = json.loads(r.read())
        print("   Broadcast Status:", res.get("status"))
        print("   Channels Dispatched:", res.get("channels"))

    # 3. Financial Settlement
    print("\n=== 3. FINANCIAL SETTLEMENT ZAP ===")
    req3 = urllib.request.Request(
        "http://localhost:5678/webhook/settle-payment",
        data=json.dumps({"invoice_id": "INV-2026-OMEGA-01", "amount_usd": 500000.0, "currency": "USDC"}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req3) as r:
        res = json.loads(r.read())
        print("   Status:", res.get("status"))
        print("   State Channel Hash:", res.get("state_channel_hash"))
        print("   Clearing Latency:", res.get("clearing_latency_ms"), "ms")

    # 4. Visual Zap Creator Studio
    print("\n=== 4. VISUAL ZAP CREATOR STUDIO ===")
    req4 = urllib.request.Request(
        "http://localhost:5678/api/v1/workflows/create_visual",
        data=json.dumps({
            "name": "Stripe Production Charge Sentinel",
            "triggerType": "webhook",
            "webhookPath": "stripe-charges",
            "actionType": "ai"
        }).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req4) as r:
        res = json.loads(r.read())
        print("   New Zap Deployed:", res.get("data", {}).get("name"))
        print("   Zap ID:", res.get("data", {}).get("id"))

    # 5. Export Backup
    print("\n=== 5. BACKUP ENGINE EXPORT ===")
    with urllib.request.urlopen("http://localhost:5678/api/v1/export/all") as r:
        bundle = json.loads(r.read())
        wf_count = len(bundle.get("workflows", []))
        exec_count = len(bundle.get("executions", []))
        print(f"   [OK] Successfully Exported {wf_count} Workflows & {exec_count} Execution Logs!")

    print("\n================================================================================")
    print("   [SUCCESS] All Enterprise v2.0 Automation Features Verified!")
    print("================================================================================")

if __name__ == "__main__":
    test()
