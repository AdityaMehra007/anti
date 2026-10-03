"""
Unit tests for Live Enterprise Outreach Dispatcher (scripts/live_enterprise_outreach.py)
"""
import os
import pytest
from scripts.live_enterprise_outreach import EnterpriseOutreachDispatcher

def test_enterprise_outreach_dispatcher_init(tmp_path):
    drafts_dir = str(tmp_path / "Email_Drafts")
    dispatcher = EnterpriseOutreachDispatcher(drafts_dir=drafts_dir)
    assert os.path.exists(drafts_dir)

def test_generate_personalized_draft(tmp_path):
    drafts_dir = str(tmp_path / "Email_Drafts")
    dispatcher = EnterpriseOutreachDispatcher(drafts_dir=drafts_dir)
    
    lead = {
        "contact_id": "999",
        "name": "Rajesh Sharma",
        "company": "Tata Motors",
        "position": "Head of Talent Acquisition",
        "linkedin_url": "https://linkedin.com/in/test",
        "email": "rajesh@tatamotors.com"
    }

    draft_path = dispatcher.generate_lead_draft(lead)
    assert os.path.exists(draft_path)
    with open(draft_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Rajesh Sharma" in content
    assert "Tata Motors" in content
    assert "Subject" in content

def test_batch_generate_and_track(tmp_path):
    drafts_dir = str(tmp_path / "Email_Drafts")
    db_path = str(tmp_path / "test_outreach.db")
    dispatcher = EnterpriseOutreachDispatcher(drafts_dir=drafts_dir, db_path=db_path)

    leads = [
        {"contact_id": "1001", "name": "Anita Roy", "company": "Infosys", "position": "HR Director", "email": "a@test.com", "linkedin_url": ""},
        {"contact_id": "1002", "name": "Vikram Seth", "company": "Wipro", "position": "VP Talent", "email": "v@test.com", "linkedin_url": ""}
    ]

    generated = dispatcher.generate_batch_drafts(leads)
    assert len(generated) == 2
    for p in generated:
        assert os.path.exists(p)
