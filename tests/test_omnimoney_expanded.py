import pytest
from fastapi.testclient import TestClient
from omnimoney.server import app
from omnimoney.agent_workforce import AgentWorkforceSwarm
from omnimoney.morning_brief import MorningBriefEngine
from omnimoney.business_generator import BusinessGenerator
from omnimoney.omnimoney_engine import OmniMoneyEngine
from omnimoney.b2b_sales_engine import B2BSalesEngine

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["system"] == "OMNIMONEY OS"
    assert data["status"] == "ONLINE"

def test_api_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "swarm" in data

def test_api_today_action():
    response = client.get("/api/today")
    assert response.status_code == 200
    data = response.json()
    assert "opportunity" in data
    assert "exact_next_action" in data

def test_api_crm_workflow():
    # Test getting prospects
    res_get = client.get("/api/crm/prospects")
    assert res_get.status_code == 200
    data = res_get.json()
    initial_count = len(data["prospects"])

    # Test creating new prospect
    new_lead = {
        "business_name": "Test Bangalore Wellness Clinic",
        "category": "Healthcare",
        "location": "Indiranagar",
        "contact_person": "Dr. Test",
        "phone": "+91 99999 88888",
        "email": "drtest@example.com",
        "website": "https://testclinic.com",
        "notes": "Testing lead ingestion",
        "deal_value_inr": 20000.0
    }
    res_post = client.post("/api/crm/prospects", json=new_lead)
    assert res_post.status_code == 200
    created_id = res_post.json()["lead"]["id"]

    # Test updating status
    update_payload = {
        "lead_id": created_id,
        "new_status": "AUDIT_SENT",
        "notes": "Loom video sent"
    }
    res_update = client.post("/api/crm/update-status", json=update_payload)
    assert res_update.status_code == 200
    assert res_update.json()["new_status"] == "AUDIT_SENT"

def test_agent_workforce_swarm():
    swarm = AgentWorkforceSwarm()
    agents = swarm.get_all_agents()
    assert len(agents) == 18

    cycle = swarm.run_swarm_cycle()
    assert cycle["total_agents"] == 18
    assert cycle["active_agents"] >= 10
    assert len(cycle["top_directives"]) > 0

def test_morning_brief_engine():
    engine = OmniMoneyEngine()
    sales = B2BSalesEngine()
    brief_engine = MorningBriefEngine(engine, sales)
    brief = brief_engine.generate_brief()

    assert "date" in brief
    assert "markdown_brief" in brief
    assert "priority_action" in brief
    assert len(brief["non_negotiable_actions"]) == 3

def test_business_generator():
    gen = BusinessGenerator()
    # Test Clinic blueprint
    bp_clinic = gen.generate_blueprint("Aesthetic Clinic")
    assert "Clinic" in bp_clinic.vertical_name
    assert bp_clinic.monthly_pl_projection["net_profit_margin_pct"] > 80.0

    # Test Real Estate blueprint
    bp_re = gen.generate_blueprint("Real Estate Broker")
    assert "Real Estate" in bp_re.vertical_name
    assert len(bp_re.acute_pain_points) >= 3

    # Test Peenya EXIM blueprint
    bp_exim = gen.generate_blueprint("Peenya Exporter")
    assert "Peenya" in bp_exim.vertical_name
    assert "Tier 1 (Trade Audit)" in bp_exim.offer_stack
