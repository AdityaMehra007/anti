"""
Automated Verification Suite for Trillion-Dollar Sovereign Empire Agent Skills.
"""

import os
import pytest


SKILLS_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", ".agent", "skills")

EMPIRE_SKILLS = [
    "empire-capital-allocator",
    "sovereign-chokehold-architect",
    "planetary-fleet-ops",
    "m2m-settlement-clearing",
    "energy-compute-coupling",
    "geopolitical-sovereign-shield",
    "biomanufacturing-scaling",
    "antifragile-red-team",
    "sovereign-wealth-syndication",
    "sovereign-banking-engine",
]


def test_empire_skills_exist_and_contain_valid_frontmatter():
    for skill_name in EMPIRE_SKILLS:
        skill_dir = os.path.join(SKILLS_ROOT, skill_name)
        skill_file = os.path.join(skill_dir, "SKILL.md")

        assert os.path.exists(skill_file), f"Skill file missing: {skill_file}"

        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        assert content.startswith("---"), f"Skill {skill_name} missing YAML frontmatter header"
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"Skill {skill_name} YAML frontmatter improperly closed"

        frontmatter = parts[1]
        assert f"name: {skill_name}" in frontmatter
        assert "description:" in frontmatter
        assert len(parts[2].strip()) > 100, f"Skill {skill_name} body content is too short"


def test_empire_skills_cross_referencing():
    """Verify that skills cross-reference the actual codebase modules."""
    for skill_name in EMPIRE_SKILLS:
        skill_file = os.path.join(SKILLS_ROOT, skill_name, "SKILL.md")
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        assert "file:///" in content, f"Skill {skill_name} lacks clickable code symbol links"
