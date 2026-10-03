"""
Unit tests for Skill Distillation Engine (aios/ai/skill_distiller.py)
"""
import os
import pytest
from aios.ai.skill_distiller import SkillDistiller

def test_skill_distiller_initialization(tmp_path):
    skills_dir = str(tmp_path / "skills")
    distiller = SkillDistiller(skills_dir=skills_dir)
    assert os.path.exists(skills_dir)

def test_skill_distiller_analyze_log_entries(tmp_path):
    skills_dir = str(tmp_path / "skills")
    distiller = SkillDistiller(skills_dir=skills_dir)
    
    sample_logs = [
        "ModuleNotFoundError: No module named 'fastapi'",
        "ModuleNotFoundError: No module named 'uvicorn'",
        "ModuleNotFoundError: No module named 'pydantic'"
    ]
    patterns = distiller.detect_error_patterns(sample_logs)
    assert len(patterns) >= 1
    assert "ModuleNotFoundError" in patterns[0]["error_type"]

def test_skill_distiller_synthesize_skill_manifest(tmp_path):
    skills_dir = str(tmp_path / "skills")
    distiller = SkillDistiller(skills_dir=skills_dir)

    skill_path = distiller.synthesize_skill(
        topic="python-dependency-resolution",
        description="Autonomous resolution of missing Python dependencies using stdlib alternatives",
        instructions="Always check standard library alternatives before installing external packages."
    )
    assert os.path.exists(skill_path)
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "name: distilled-python-dependency-resolution" in content
    assert "Autonomous resolution" in content
