import pytest
import os
import json
from pathlib import Path
from omega.integrations.gauzy_connector import GauzyAPIClient, GauzySyncManager

def test_gauzy_client_initialization():
    client = GauzyAPIClient(base_url="http://localhost:3000/api")
    assert client.base_url == "http://localhost:3000/api"
    assert client.token is None

def test_gauzy_candidate_payload_structure():
    client = GauzyAPIClient()
    sync_mgr = GauzySyncManager(client=client, dry_run=True)
    payload = sync_mgr.build_candidate_payload()

    assert payload["firstName"] == "Aditya"
    assert payload["lastName"] == "Mehra"
    assert "adityamehra799@gmail.com" in payload["email"]
    assert "Bengaluru" in payload["city"]
    assert "Tier-1 Vendor SLA Governance" in payload["tags"]
    assert "AERO INDIA 2025 Lead" in payload["tags"]

def test_gauzy_dry_run_sync_candidate():
    client = GauzyAPIClient()
    sync_mgr = GauzySyncManager(client=client, dry_run=True)
    res = sync_mgr.sync_candidate()
    assert res["status"] == "DRY_RUN"
    assert res["payload"]["firstName"] == "Aditya"

def test_gauzy_dry_run_sync_jobs():
    client = GauzyAPIClient()
    sync_mgr = GauzySyncManager(client=client, dry_run=True)
    res = sync_mgr.sync_jobs(limit=5)
    assert len(res) > 0
    assert res[0]["status"] == "DRY_RUN"
    assert res[0]["count"] <= 5
    assert len(res[0]["jobs"]) <= 5
    assert "title" in res[0]["jobs"][0]
    assert "location" in res[0]["jobs"][0]

def test_gauzy_dry_run_sync_recruiters():
    client = GauzyAPIClient()
    sync_mgr = GauzySyncManager(client=client, dry_run=True)
    res = sync_mgr.sync_recruiters(limit=5)
    assert len(res) > 0
    assert res[0]["status"] == "DRY_RUN"
    assert res[0]["count"] <= 5
    assert "firstName" in res[0]["contacts"][0]
    assert "company" in res[0]["contacts"][0]
