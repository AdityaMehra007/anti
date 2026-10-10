import unittest
import sqlite3
import os

class TestOmniverseEngine(unittest.TestCase):
    def setUp(self):
        self.db_path = r"e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
        import omniverse_engine
        omniverse_engine.populate_omniverse_data(self.db_path)

    def test_database_exists(self):
        self.assertTrue(os.path.exists(self.db_path), "Database file should exist")

    def test_tables_created(self):
        import omniverse_engine
        omniverse_engine.init_omniverse_tables(self.db_path)
        
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cur.fetchall()]
        conn.close()

        required_tables = [
            "omniverse_companies",
            "omniverse_corporate_relationships",
            "omniverse_live_vacancies",
            "omniverse_recruiters",
            "omniverse_audit_log"
        ]
        for tbl in required_tables:
            self.assertIn(tbl, tables, f"Table {tbl} must be present in database")

    def test_live_vacancies_populated(self):
        import omniverse_engine
        omniverse_engine.populate_omniverse_data(self.db_path)

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM omniverse_live_vacancies WHERE non_sales_verified = 1;")
        count = cur.fetchone()[0]
        conn.close()

        self.assertGreaterEqual(count, 8, "Should have at least 8 verified non-sales live vacancies")

    def test_cockpit_html_generated(self):
        import omniverse_engine
        html_path = r"e:\anti\OMNIVERSE_INFINITY_COCKPIT.html"
        omniverse_engine.generate_cockpit_html(self.db_path, html_path)
        self.assertTrue(os.path.exists(html_path), "Cockpit HTML must be generated")
        self.assertGreater(os.path.getsize(html_path), 5000, "Cockpit HTML must be substantial")

if __name__ == "__main__":
    unittest.main()
