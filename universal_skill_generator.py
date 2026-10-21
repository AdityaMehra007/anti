#!/usr/bin/env python3
"""
universal_skill_generator.py - OMEGA Universal Skill Generator & Job-to-Skill Matrix Builder
============================================================================================
Catalogs and maps the 3,800+ existing skills in .agents/skills to the Universal Job Taxonomy.
Generates comprehensive Master Skill Packages for every major job archetype, containing:
  - Standard YAML Frontmatter
  - Detailed Specification & Core Directives
  - Deterministic Step-by-Step SOP (Standard Operating Procedure)
  - Tool Guidelines, MCP Integrations & Constraints
  - Evaluation Rubric & Quality Gateways

Outputs:
  - .agents/skills/skill-master-<archetype>/SKILL.md
  - data/job_to_skills_master_matrix.json
  - data/job_to_skills_master_matrix.csv
"""

import os
import re
import csv
import json
from pathlib import Path
from typing import Dict, List, Any

from universal_job_taxonomy_master import get_all_archetypes, UNIVERSAL_JOB_TAXONOMY

ROOT_DIR = Path(r"e:\anti")
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
DATA_DIR = ROOT_DIR / "data"
MATRIX_JSON_PATH = DATA_DIR / "job_to_skills_master_matrix.json"
MATRIX_CSV_PATH = DATA_DIR / "job_to_skills_master_matrix.csv"


def build_job_to_skill_matrix() -> Dict[str, Any]:
    """Scans existing skills and maps them 1:1 to all job families and archetypes."""
    existing_skills = []
    if SKILLS_DIR.exists():
        existing_skills = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]

    archetypes = get_all_archetypes()
    matrix = {
        "metadata": {
            "title": "OMEGA Universal Job-to-Skill Master Matrix",
            "total_existing_skills": len(existing_skills),
            "total_archetypes": len(archetypes),
            "version": "2.0.0"
        },
        "mappings": []
    }

    family_skill_prefixes = {
        "software_engineering": ["software-skill", "devops-skill", "react", "frontend", "git", "coding"],
        "ai_ml_data": ["ai-infra", "genai-skill", "data-intel", "analytics-skill", "pytorch", "mle"],
        "product_design": ["product-ux", "figma", "design", "canvas"],
        "cybersecurity_governance": ["security-gov", "security", "hipaa", "audit"],
        "corporate_finance_treasury": ["finance-treasury", "finance-skill", "sovereign-banking"],
        "b2b_sales_revenue": ["b2b-sales", "ai-sdr", "lead-enrichment", "prospecting"],
        "growth_marketing_seo": ["growth-seo", "growth-skill", "seo", "content-engine"],
        "operations_supply_chain_exim": ["exim-trade", "exim-skill", "operations", "logistics"],
        "people_hr_recruiting": ["talent-people", "talent-skill", "recruiter", "interview"],
        "executive_founders_office": ["exec-strategy", "chief-of-staff", "empire-capital", "sovereign"],
        "customer_success_support": ["customer-success", "revops", "churn"],
        "healthcare_biotech": ["biomanufacturing", "healthcare", "phi"],
        "consulting_advisory": ["council", "strategic-compact", "plan-canvas"]
    }

    csv_rows = []

    for arch in archetypes:
        fam_key = arch["family_key"]
        role_key = arch["role_key"]
        role_title = arch["title"]
        prefixes = family_skill_prefixes.get(fam_key, ["software-skill"])

        # Find matching existing skills
        matched_existing = [
            s for s in existing_skills
            if any(s.startswith(p) for p in prefixes)
        ]

        master_skill_name = f"skill-master-{role_key.replace('_', '-')}"

        record = {
            "role_key": role_key,
            "role_title": role_title,
            "family_key": fam_key,
            "family_name": arch["family_name"],
            "master_skill_name": master_skill_name,
            "required_hard_skills": arch.get("hard_skills", []),
            "required_soft_skills": arch.get("soft_skills", []),
            "top_ats_keywords": arch.get("ats_keywords", [])[:10],
            "sample_kpis": arch.get("sample_kpis", []),
            "total_matched_agent_skills": len(matched_existing),
            "sample_matched_agent_skills": matched_existing[:8]
        }
        matrix["mappings"].append(record)

        csv_rows.append([
            role_key,
            role_title,
            arch["family_name"],
            master_skill_name,
            "; ".join(arch.get("hard_skills", [])[:5]),
            "; ".join(arch.get("ats_keywords", [])[:5]),
            len(matched_existing)
        ])

    # Save JSON
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(MATRIX_JSON_PATH, "w", encoding="utf-8") as fp:
        json.dump(matrix, fp, indent=2, ensure_ascii=False)

    # Save CSV
    with open(MATRIX_CSV_PATH, "w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["Role Key", "Role Title", "Job Family", "Master Skill ID", "Primary Hard Skills", "Top ATS Keywords", "Matched Subagents Count"])
        writer.writerows(csv_rows)

    return matrix


def generate_master_archetype_skills(matrix: Dict[str, Any], limit: int = 35) -> List[Path]:
    """Generates standardized flagship SKILL.md packages for all job archetypes."""
    created_paths = []
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    for item in matrix["mappings"][:limit]:
        skill_name = item["master_skill_name"]
        role_title = item["role_title"]
        family_name = item["family_name"]
        hard_skills_str = ", ".join(item["required_hard_skills"][:6])
        ats_str = ", ".join(item["top_ats_keywords"][:8])
        kpis_str = "\n".join([f"- {kpi}" for kpi in item["sample_kpis"]])

        skill_folder = SKILLS_DIR / skill_name
        skill_folder.mkdir(parents=True, exist_ok=True)
        skill_file = skill_folder / "SKILL.md"

        content = f"""---
name: {skill_name}
description: Autonomous master capability and execution standard operating procedure for {role_title} ({family_name}).
---

# Master Capability Module: {role_title}

**Skill ID:** {skill_name}  
**Job Family:** {family_name}  
**Specialization:** {role_title} Execution & Delivery  
**Verification Level:** Deterministic / Zero Vibe Coding / Full Telemetry Traceability  

## 1. Scope & Architectural Mandate
This skill governs the autonomous execution, technical delivery, and operational excellence for the **{role_title}** role. Agents invoking this skill adhere to strict standard operating procedures, verified toolchains, and zero-hallucination protocols.

## 2. Core Hard Skills & Technical Stack
The agent must demonstrate verifiable competency in:
- {hard_skills_str}

## 3. Top High-Signal ATS Keywords
Resume artifacts, documentation, and technical deliverables generated by this skill must incorporate:
`{ats_str}`

## 4. Key Performance Indicators (KPIs)
Deliverables must verifiably satisfy:
{kpis_str}

## 5. Standard Operating Procedure (SOP)
1. **Ingest & Scoping**: Parse problem statements, specifications, PRDs, or JDs into atomic requirements.
2. **Deterministic Execution**: Apply domain-specific design patterns, testing harnesses, and validated toolchains.
3. **Verification & Audit**: Run automated test suites (TDD) and verify zero regressions before committing.
4. **Artifact Generation**: Emit structured telemetry, actionable documentation, and clean commit logs.

## 6. Constraints & Safety Gates
- Never hallucinate credentials, metrics, or technical APIs.
- Adhere to the OMEGA Constitution and repository engineering guidelines.
"""
        with open(skill_file, "w", encoding="utf-8") as fp:
            fp.write(content.strip() + "\n")

        created_paths.append(skill_file)

    return created_paths


if __name__ == "__main__":
    m = build_job_to_skill_matrix()
    print(f"Matrix built with {len(m['mappings'])} role mappings.")
    created = generate_master_archetype_skills(m)
    print(f"Generated {len(created)} Master Archetype Skill packages in {SKILLS_DIR}.")
