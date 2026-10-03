"""Unit tests for SQLFluff automation runner."""

import subprocess
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.sqlfluff_runner import resolve_sqlfluff_cmd


def test_resolve_sqlfluff_cmd():
    cmd = resolve_sqlfluff_cmd()
    assert isinstance(cmd, list)
    assert len(cmd) >= 1
    # Verify that the command can execute and return version
    res = subprocess.run(cmd + ["--version"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "sqlfluff" in res.stdout.lower()


def test_sqlfluff_lint_clean_schema():
    cmd = resolve_sqlfluff_cmd()
    res = subprocess.run(
        cmd + ["lint", "aios/databases/init_schema.sql", "--dialect", "sqlite"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"Lint failed with: {res.stdout}\n{res.stderr}"
