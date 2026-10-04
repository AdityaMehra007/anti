import pytest
from pathlib import Path
from scripts.activate_email_dispatcher import verify_eml_batch

def test_email_dispatcher_dry_run_batch():
    result = verify_eml_batch(limit=5)
    assert result["total_selected"] == 5
    assert result["verified_valid"] == 5
    for item in result["results"]:
        assert item["valid"] is True
        assert "@" in item["to"]
        assert len(item["subject"]) > 5
