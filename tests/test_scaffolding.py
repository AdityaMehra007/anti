import unittest
from byox.cli import main

class TestScaffolding(unittest.TestCase):
    def test_cli_help(self):
        code = main(["--help"])
        self.assertEqual(code, 0)
        
    def test_cli_version(self):
        code = main(["--version"])
        self.assertEqual(code, 0)

if __name__ == "__main__":
    unittest.main()
