"""
Automated Verification Suite for CS Video Courses Engine & Intelligence Ecosystem
Validates parser fidelity, SQLite FTS5 search, career roadmaps, and REST endpoints.
"""

import os
import json
import sqlite3
import unittest
from pathlib import Path

from cs_courses_engine import CSCoursesEngine, DB_PATH, JSON_PATH
from cs_courses_roadmaps import CSRoadmapsEngine, ROADMAPS_JSON_PATH


class TestCSCoursesEngine(unittest.TestCase):
    """Test suite validating end-to-end data pipelines and indexing."""

    @classmethod
    def setUpClass(cls):
        cls.engine = CSCoursesEngine()
        if not DB_PATH.exists():
            cls.engine.build_database()
        cls.roadmaps_engine = CSRoadmapsEngine()
        if not ROADMAPS_JSON_PATH.exists():
            cls.roadmaps_engine.build_all_roadmaps()

    def test_database_record_count(self):
        """Verify that at least 1,400 courses are indexed."""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM courses;")
        count = cur.fetchone()[0]
        conn.close()
        self.assertGreaterEqual(count, 1400, f"Expected >= 1400 courses, got {count}")

    def test_courses_with_videos(self):
        """Verify video playlist detection captured at least 900 video courses."""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM courses WHERE has_video = 1;")
        count = cur.fetchone()[0]
        conn.close()
        self.assertGreaterEqual(count, 900, f"Expected >= 900 video courses, got {count}")

    def test_fts5_full_text_search(self):
        """Verify FTS5 search performs fast matching across multiple topics."""
        queries = ["distributed systems", "database systems", "deep learning", "compiler", "algorithms"]
        for q in queries:
            results = self.engine.search_courses(query=q, limit=5)
            self.assertGreater(len(results), 0, f"Search for '{q}' returned no results")
            self.assertIn("id", results[0])
            self.assertIn("title", results[0])

    def test_key_institutions_present(self):
        """Verify world-class academic institutions are recognized."""
        stats = self.engine.get_summary_stats()
        inst_names = {i["institution"] for i in stats["institutions"]}
        expected_institutions = ["MIT", "Stanford", "Carnegie Mellon (CMU)", "UC Berkeley", "Harvard"]
        for expected in expected_institutions:
            self.assertIn(expected, inst_names, f"Expected institution '{expected}' not found in catalog")

    def test_signature_courses_indexed(self):
        """Verify known flagship courses exist in catalog."""
        flagship_codes = ["6.824", "15-445", "CS 162", "CS 229"]
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        for code in flagship_codes:
            cur.execute("SELECT COUNT(*) FROM courses WHERE code LIKE ?;", (f"%{code}%",))
            count = cur.fetchone()[0]
            self.assertGreater(count, 0, f"Flagship course code '{code}' not found")
        conn.close()

    def test_career_roadmaps_integrity(self):
        """Verify that 9 career roadmaps exist and each has 4 tiers."""
        with open(ROADMAPS_JSON_PATH, "r", encoding="utf-8") as f:
            roadmaps = json.load(f)
        self.assertEqual(len(roadmaps), 9, "Expected 9 role roadmaps")
        for r in roadmaps:
            self.assertEqual(len(r["tiers"]), 4, f"Role {r['role_id']} does not have 4 tiers")
            self.assertGreater(r["course_count"], 0, f"Role {r['role_id']} has 0 courses")

    def test_json_catalog_exists(self):
        """Verify JSON export is valid and populated."""
        self.assertTrue(JSON_PATH.exists())
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertGreaterEqual(len(data), 1400)

    def test_curricula_markdown_files_exist(self):
        """Verify that markdown curriculum guides are generated for all 9 roles."""
        curricula_dir = Path(__file__).resolve().parent.parent / "docs" / "curricula"
        self.assertTrue(curricula_dir.exists())
        expected_files = [
            "genai-llm-engineer.md",
            "systems-distributed-engineer.md",
            "database-storage-architect.md",
            "algorithms-competitive-quant.md",
            "applied-ml-data-scientist.md",
            "security-cryptography-engineer.md",
            "embedded-robotics-autonomy.md",
            "computer-vision-multimodal.md",
            "software-architect-fullstack.md"
        ]
        for f in expected_files:
            file_path = curricula_dir / f
            self.assertTrue(file_path.exists(), f"Curriculum file {f} missing")
            self.assertGreater(file_path.stat().st_size, 500, f"Curriculum file {f} too small")


if __name__ == "__main__":
    unittest.main()
