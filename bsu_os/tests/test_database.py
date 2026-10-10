"""Unit tests for BSU OS Database Engine."""

import pytest
import sqlite3
from pathlib import Path
from bsu_os.database import init_db, get_connection, get_all_startups, get_startup_by_id
from bsu_os.seed_data import seed_database


@pytest.fixture
def temp_db(tmp_path):
    """Provides a fresh isolated SQLite database."""
    db_file = tmp_path / "test_bsu.db"
    seed_database(db_file)
    return db_file


def test_database_initialization(temp_db):
    """Verifies that all required tables and indices are created."""
    conn = get_connection(temp_db)
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    conn.close()

    expected_tables = [
        "clusters", "startups", "founders", "investors",
        "funding_rounds", "jobs", "events", "watchlists", "alerts"
    ]
    for tbl in expected_tables:
        assert tbl in tables, f"Expected table '{tbl}' to exist in SQLite schema."


def test_startups_retrieval(temp_db):
    """Verifies retrieval of seeded startups with filters."""
    startups = get_all_startups(conn=get_connection(temp_db))
    assert len(startups) >= 5, "Expected at least 5 seeded startups."

    # Test sector filter
    ai_startups = get_all_startups(sector="AI / ML", conn=get_connection(temp_db))
    assert len(ai_startups) >= 1
    assert all(s["sector"] == "AI / ML" for s in ai_startups)


def test_startup_hydration(temp_db):
    """Verifies startup relations (founders, funding, jobs) are hydrated."""
    conn = get_connection(temp_db)
    first_startup = conn.execute("SELECT id FROM startups LIMIT 1").fetchone()
    startup_id = first_startup["id"]
    conn.close()

    detailed = get_startup_by_id(startup_id, hydrate=True, conn=get_connection(temp_db))
    assert detailed is not None
    assert "founders" in detailed
    assert "funding_rounds" in detailed
    assert "open_jobs" in detailed
    assert len(detailed["founders"]) >= 1
