"""
Test suite for Sovereign Continuum FastAPI Gateway.
"""

import pytest
from fastapi.testclient import TestClient
from sovereign_continuum.api.gateway import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_api_root_and_health(client):
    res_root = client.get("/")
    assert res_root.status_code == 200
    data = res_root.json()
    assert data["status"] == "OPERATIONAL"
    assert "capabilities" in data

    res_health = client.get("/health")
    assert res_health.status_code == 200
    health_data = res_health.json()
    assert health_data["status"] == "HEALTHY"
    assert health_data["subsystems"]["banking_engine"] == "ONLINE"


def test_banking_overview_endpoint(client):
    res = client.get("/api/v1/banking/overview")
    assert res.status_code == 200
    data = res.json()
    assert "central_bank_balance_sheet_assets_b" in data
    assert "assets_under_custody_b" in data
    assert data["total_fiat_deposits_usd"] > 0


def test_iso20022_transfer_endpoint(client):
    payload = {
        "debtor_name": "Siemens Mobility AG",
        "debtor_iban": "DE89370400440532013000",
        "debtor_bic": "DEUTDEDD",
        "creditor_name": "Terra Kinetics Corp",
        "creditor_iban": "GB82WEST12345698765432",
        "creditor_bic": "BARCGB22",
        "amount": 12_500_000.0,
        "currency": "USD",
        "priority": "HIGH",
    }
    res = client.post("/api/v1/banking/iso20022/transfer", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ACCP"
    assert data["cleared_amount"] == 12_500_000.0
    assert "uetr" in data
    assert "<Document" in data["xml_payload"]


def test_cash_sweep_endpoint(client):
    payload = {
        "subsidiary_balances": {
            "SUB_AMER": 45_000_000.0,
            "SUB_EMEA": 15_000_000.0,
            "SUB_APAC": 25_000_000.0,
        },
        "operating_cushion_usd": 5_000_000.0,
    }
    res = client.post("/api/v1/banking/cash-sweep", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_liquidity_concentrated_usd"] == 70_000_000.0
    assert data["master_treasury_target"] == "OMEGA_GLOBAL_TREASURY_ACCOUNT"


def test_robotics_telemetry_endpoint(client):
    res = client.get("/api/v1/robotics/telemetry")
    assert res.status_code == 200
    data = res.json()
    assert data["is_safe"] is True
    assert data["safety_state"] == "nominal"
    assert len(data["joints_snapshot"]) == 6


def test_smr_offtake_endpoint(client):
    payload = {
        "num_reactors": 4,
        "base_power_price_per_mwh": 62.0,
        "ai_token_monetization_multiplier": 3.8,
    }
    res = client.post("/api/v1/energy/smr-offtake", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["num_reactors"] == 4
    assert data["cluster_capacity"]["continuous_clean_power_mwe"] > 0
    assert len(data["10_year_trajectory"]) > 0


def test_dna_compile_endpoint(client):
    payload = {
        "molecule_name": "Taxadiene_Synthase",
        "target_cas_number": "12345-67-8",
        "target_pathway": "terpenoid_synthase",
        "host_organism": "Pichia_pastoris",
    }
    res = client.post("/api/v1/bio/compile", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "plasmid_id" in data
    assert data["target_molecule"] == "Taxadiene_Synthase"
    assert data["codon_adaptation_index"] > 0.90
