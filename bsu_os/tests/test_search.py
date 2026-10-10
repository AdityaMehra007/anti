"""Unit tests for BSU OS Super Search Engine."""

import pytest
from bsu_os.seed_data import seed_database
from bsu_os.search_engine import super_search
from bsu_os.config import DATABASE_PATH


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_database()


def test_search_startup_by_name():
    """Verifies that searching for 'Sarvam' retrieves the AI startup."""
    res = super_search("Sarvam")
    assert len(res["startups"]) > 0
    assert any("Sarvam" in s["name"] for s in res["startups"])


def test_search_by_sector():
    """Verifies search by sector keyword like 'FinTech'."""
    res = super_search("FinTech")
    assert len(res["startups"]) > 0


def test_search_founder():
    """Verifies founder lookup returns associated startup."""
    res = super_search("Nithin Kamath")
    assert len(res["founders"]) > 0
    assert any("Nithin Kamath" in f["name"] for f in res["founders"])


def test_search_cluster():
    """Verifies searching for 'HSR' returns cluster info."""
    res = super_search("HSR")
    assert len(res["clusters"]) > 0
