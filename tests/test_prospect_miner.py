import pytest
import sqlite3
import os
from omnimoney.prospect_miner import ProspectMiner

@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test_db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE company_founder_gaps (
            id INTEGER PRIMARY KEY,
            company TEXT,
            sector TEXT,
            corridor TEXT,
            founder_ceo_name TEXT,
            founder_ceo_title TEXT,
            hr_name TEXT,
            hr_designation TEXT,
            hr_email TEXT,
            careers_email TEXT,
            hr_phone TEXT,
            linkedin_search_url TEXT,
            identified_company_gap TEXT,
            candidate_solution TEXT,
            pitch_angle TEXT,
            fit_score INTEGER,
            status TEXT
        )
    """)
    cursor.executemany(
        "INSERT INTO company_founder_gaps (company, sector, corridor, fit_score, status) VALUES (?, ?, ?, ?, ?)",
        [
            ("Tech A", "AI", "Whitefield", 90, "READY_FOR_OUTREACH"),
            ("Tech B", "Cloud", "ORR", 80, "READY_FOR_OUTREACH"),
            ("Tech C", "AI", "ORR", 70, "NOT_READY"),
            ("Tech D", "Fintech", "HSR", 95, "READY_FOR_OUTREACH"),
            ("Tech E", "AI", "Whitefield", 85, "READY_FOR_OUTREACH")
        ]
    )
    conn.commit()
    conn.close()
    return str(db_path)

def test_mine_high_value_prospects(test_db):
    miner = ProspectMiner(db_path=test_db)
    prospects = miner.mine_high_value_prospects(limit=2)
    assert len(prospects) == 2
    assert prospects[0]['company'] == "Tech D"  # fit_score 95
    assert prospects[1]['company'] == "Tech A"  # fit_score 90

def test_mine_by_sector(test_db):
    miner = ProspectMiner(db_path=test_db)
    prospects = miner.mine_by_sector("AI", limit=10)
    assert len(prospects) == 2
    assert prospects[0]['company'] == "Tech A"
    assert prospects[1]['company'] == "Tech E"

def test_mine_by_corridor(test_db):
    miner = ProspectMiner(db_path=test_db)
    prospects = miner.mine_by_corridor("Whitefield", limit=10)
    assert len(prospects) == 2
    assert set(p['company'] for p in prospects) == {"Tech A", "Tech E"}

def test_get_available_sectors(test_db):
    miner = ProspectMiner(db_path=test_db)
    sectors = miner.get_available_sectors()
    assert set(sectors) == {"AI", "Cloud", "Fintech"}

def test_get_outreach_ready_count(test_db):
    miner = ProspectMiner(db_path=test_db)
    counts = miner.get_outreach_ready_count()
    assert counts == {"AI": 2, "Cloud": 1, "Fintech": 1}

def test_generate_prospect_report(test_db):
    miner = ProspectMiner(db_path=test_db)
    report = miner.generate_prospect_report(limit=2)
    assert "Tech D (Fintech)" in report
    assert "Total High-Value Prospects Found:" in report
    assert "2" in report

def test_export_prospect_csv(test_db, tmp_path):
    miner = ProspectMiner(db_path=test_db)
    csv_path = str(tmp_path / "out.csv")
    miner.export_prospect_csv(csv_path, limit=2)
    assert os.path.exists(csv_path)
    with open(csv_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Tech D" in content
    assert "Tech A" in content
