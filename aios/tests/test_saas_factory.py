import unittest
import tempfile
import sys
import json
from pathlib import Path

# Add project root to sys.path for database imports
AIOS_ROOT = Path("E:/anti/aios")
if str(AIOS_ROOT) not in sys.path:
    sys.path.append(str(AIOS_ROOT))

from projects.saas_factory import SaaSFactory
from projects.agent_harness import AgentHarness
from databases.db import SCHEMA_PATH, get_connection

class TestSaaSFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize schema just in case
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        with get_connection() as con:
            con.executescript(schema_sql)
            con.commit()

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.factory = SaaSFactory(root_dir=self.temp_dir.name)
        
        with get_connection() as con:
            # Clear out test data before each run using a specific prefix could be better,
            # but we'll clear everything or delete by name to avoid concurrency issues if this was real
            pass

    def tearDown(self):
        self.temp_dir.cleanup()
        with get_connection() as con:
            con.execute("DELETE FROM saas_projects WHERE name LIKE 'test_%' OR name IN ('p1', 'p2')")
            con.commit()

    def test_scaffold_creates_directory(self):
        p = self.factory.scaffold_project("test_nextjs", "nextjs-fastapi", [])
        self.assertTrue(Path(p).exists())
        self.assertTrue((Path(p) / "frontend").exists())
        self.assertTrue((Path(p) / "backend").exists())

    def test_scaffold_generates_readme(self):
        p = self.factory.scaffold_project("test_readme", "static-api", [])
        readme = Path(p) / "README.md"
        self.assertTrue(readme.exists())
        content = readme.read_text()
        self.assertIn("# test_readme", content)
        self.assertIn("static-api", content)

    def test_scaffold_records_in_db(self):
        self.factory.scaffold_project("test_db", "python-cli", ['auth'])
        with get_connection() as con:
            cur = con.execute("SELECT * FROM saas_projects WHERE name='test_db' ORDER BY id DESC")
            row = cur.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row['stack'], 'python-cli')
            self.assertEqual(json.loads(row['features']), ['auth'])

    def test_list_projects_returns_scaffolded(self):
        self.factory.scaffold_project("p1", "nextjs-fastapi", [])
        self.factory.scaffold_project("p2", "static-api", [])
        projects = self.factory.list_projects()
        names = [p['name'] for p in projects]
        self.assertIn("p1", names)
        self.assertIn("p2", names)

    def test_agent_harness_creates_script(self):
        harness = AgentHarness(root_dir=self.temp_dir.name)
        p = harness.create_agent("test", ["web_search_stub", "file_reader", "calculator"])
        self.assertTrue(Path(p).exists())
        content = Path(p).read_text()
        self.assertIn("web_search_stub", content)
        self.assertIn("calculator", content)
        self.assertIn("TOKEN_BUDGET", content)

if __name__ == '__main__':
    unittest.main()
