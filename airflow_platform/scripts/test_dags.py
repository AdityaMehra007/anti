"""
Automated CI/CD Validation Suite for Apache Airflow DAGs and Plugins.
Runs via pytest: verifies syntax, AST structure, mandatory tags, and execution contracts.
"""

import ast
from pathlib import Path
import sys
import pytest

DAGS_FOLDER = Path(__file__).resolve().parent.parent / "dags"
PLUGINS_FOLDER = Path(__file__).resolve().parent.parent / "plugins"

DAG_FILES = list(DAGS_FOLDER.glob("*.py"))


def test_dags_folder_not_empty():
    """Assert that the DAGs folder contains active python DAG definition files."""
    assert len(DAG_FILES) > 0, "No Python DAG files found in dags directory."


@pytest.mark.parametrize("dag_path", DAG_FILES, ids=lambda p: p.name)
def test_dag_ast_syntax(dag_path: Path):
    """Parses each DAG file using Python's AST compiler to catch syntax bugs immediately."""
    source = dag_path.read_text(encoding="utf-8")
    try:
        parsed = ast.parse(source, filename=str(dag_path))
        assert parsed is not None
    except SyntaxError as e:
        pytest.fail(f"Syntax error in DAG file {dag_path.name}: {e}")


@pytest.mark.parametrize("dag_path", DAG_FILES, ids=lambda p: p.name)
def test_dag_standards_and_tags(dag_path: Path):
    """Enforces organizational best practices: catchup flag and tagging."""
    content = dag_path.read_text(encoding="utf-8")
    # Verify catchup is explicitly configured
    assert "catchup=" in content, f"{dag_path.name} must explicitly declare `catchup=False` or `catchup=True`."
    # Verify tags are declared for discovery in Airflow UI
    assert "tags=" in content, f"{dag_path.name} must declare `tags=[...]` for filtering."


def test_custom_plugin_structure():
    """Verifies that custom plugins define the requisite hooks and operators."""
    plugin_file = PLUGINS_FOLDER / "custom_orchestration_plugin.py"
    assert plugin_file.exists(), "Custom plugin file must exist."
    content = plugin_file.read_text(encoding="utf-8")
    assert "class SovereignWebhookHook" in content
    assert "class SovereignEventOperator" in content
    assert "class EnterpriseCustomPlugin" in content
