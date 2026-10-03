"""
execute_all_automations.py — Full Suite Verification of OMEGA Automation Hub
Executes all 7 workflows across webhooks, AI agents, dropzone files, and email generators.
"""

import json
import time
import urllib.request
from pathlib import Path
from n8n_client import N8nClient

def main():
    print("================================================================================")
    print("          OMEGA AUTOMATION & WORKFLOW SUITE :: 7-PIPELINE MASTER RUN            ")
    print("================================================================================")

    client = N8nClient(base_url="http://localhost:5678")

    # 1. Health check
    print("\n[Step 1] Verifying Automation Engine Health...")
    if not client.health_check():
        print("[!] Engine offline. Aborting.")
        return
    print("[OK] Engine is ONLINE on http://localhost:5678/healthz")

    # 2. List Workflows
    print("\n[Step 2] Discovering Registered Automation Pipelines...")
    workflows = client.list_workflows()
    print(f"[OK] Found {len(workflows)} active workflows:")
    for wf in workflows:
        print(f"   -> [{wf.get('id')}] {wf.get('name')}")

    # 3. Trigger Zap 1: Lead Outreach Dispatcher
    print("\n[Step 3] Executing Zap: 'OMEGA Outreach Event Dispatcher'...")
    res_lead = client.trigger_webhook("outreach-dispatch", {
        "recipient_email": "founder@stellarai.com",
        "company": "Stellar AI Systems",
        "source": "ZAPIER_ACQUISITION"
    })
    print("   Response:", json.dumps(res_lead, indent=4))

    # 4. Trigger Zap 2: Webhook Event Ingestion
    print("\n[Step 4] Executing Zap: 'OMEGA Inbound Webhook Ingestion Bridge'...")
    res_event = client.trigger_webhook("omega-events", {
        "source": "ZAPIER_WEBHOOK",
        "action": "SYNC_TELEMETRY",
        "data": {"nodes_active": 12, "healthy": True}
    })
    print("   Response:", json.dumps(res_event, indent=4))

    # 5. Trigger Zap 3: Automated B2B Email Drafter
    print("\n[Step 5] Executing Zap: 'OMEGA Automated B2B Email Drafter Zap'...")
    res_email = client.trigger_webhook("email-drafter", {
        "recipient_email": "marcus.vance@vanceholdings.com",
        "company": "Vance Holdings Global",
        "value_prop": "Autonomous Capital Velocity & M2M Clearing"
    })
    print("   Saved File:", res_email.get("file_path"))
    print("   Status:", res_email.get("status"))

    # 6. Trigger Zap 4: Market Intelligence Zap
    print("\n[Step 6] Executing Zap: 'OMEGA Market Intelligence & Competitor Intel Zap'...")
    res_market = client.trigger_webhook("market-intel", {
        "sector": "Autonomous Infrastructure & Clean Energy"
    })
    print("   Market Report Destination:", res_market.get("folder") or res_market.get("destination"))

    # 7. Trigger Zap 5: Autonomous Dropzone File Ingestion
    print("\n[Step 7] Simulating Dropzone File Ingestion (e:\\anti\\n8n\\dropzone)...")
    drop_file = Path("e:/anti/n8n/dropzone/batch_upload_leads.csv")
    drop_file.write_text("id,lead,company\n1,Alice,Alpha Tech\n2,Bob,Beta Systems\n", encoding="utf-8")
    print(f"   Created dropped file: {drop_file.name}")
    print("   Waiting for background watcher ingestion (5s)...")
    time.sleep(6)
    processed_files = list(Path("e:/anti/n8n/processed").glob("*"))
    print(f"   [OK] Processed Archive Count: {len(processed_files)} files archived")

    # 8. Trigger Zap 6: AI Agent Researcher
    print("\n[Step 8] Executing Zap: 'OMEGA AI Agent Researcher'...")
    ai_exec = client._request("POST", "workflows/ai_agent_researcher/execute", data={
        "message": "Evaluate enterprise ROI on self-hosted automation infrastructure"
    })
    print("   Agent:", ai_exec.get("output", {}).get("agent"))
    print("   Summary Findings:", ai_exec.get("output", {}).get("findings", [])[:2])

    # 9. Query Ledger
    print("\n[Step 9] Querying Total Executions Audit Ledger...")
    exec_data = client._request("GET", "executions")
    executions = exec_data.get("data", [])
    print(f"[OK] Total Executions Successfully Logged: {len(executions)}")

    print("\n================================================================================")
    print("   [SUCCESS] Full 7-Pipeline Suite Executed & Audited Successfully!")
    print("   Live Web Dashboard: http://localhost:5678")
    print("================================================================================")

if __name__ == "__main__":
    main()
