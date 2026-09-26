"""
CREATE ALL 26 SPECIALIZED AGENTS AND SKILLS ENGINE
Creates agent JSON configurations and skill markdown instructions in e:\anti\.agents
implementing Section 46 of Bangalore Employment Market Intelligence System.
"""

import os
import json
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
AGENTS_DIR = WORKSPACE / ".agents" / "agents"
SKILLS_DIR = WORKSPACE / ".agents" / "skills"

AGENTS_LIST = [
    ("market_scout", "Maps Bangalore companies, commercial sectors, and hiring clusters."),
    ("company_intelligence", "Maintains canonical company records, funding data, and office locations."),
    ("job_scout", "Discovers active job postings across Bangalore MNCs, GCCs, and startups."),
    ("historical_hiring_analyst", "Builds hiring timelines, seasonal hiring patterns, and graduate intake windows."),
    ("fresher_scout", "Finds entry-level, graduate trainee, and 0-2 year experience opportunities."),
    ("ai_job_scout", "Tracks AI-native, AI-adopting, and AI-enabled business operations roles."),
    ("startup_scout", "Monitors funded startups, scale-ups, and high-growth Bangalore ventures."),
    ("mnc_gcc_scout", "Tracks multinational corporations and Global Capability Centers in Bangalore."),
    ("geo_intelligence", "Maps employment clusters in Koramangala, ORR, Whitefield, Manyata, and CBD."),
    ("salary_analyst", "Tracks market compensation ranges, median pay, and variable bonuses."),
    ("skill_analyst", "Tracks fast-rising, stable, and declining skill demand in Bangalore."),
    ("recruiter_intelligence", "Identifies talent acquisition managers, recruiters, and hiring leads."),
    ("job_quality_control", "Filters duplicate listings, stale job postings, and suspicious vacancies."),
    ("candidate_fit_engine", "Scores jobs against Aditya Mehra's 100-point candidate fit model."),
    ("application_strategist", "Prioritizes Queue A applications and selects optimal ATS CV variants."),
    ("outreach_strategist", "Synthesizes personalized 298-character LinkedIn notes and email drafts."),
    ("application_tracker", "Monitors application stages from Discovered to Submitted and Confirmed."),
    ("interview_intelligence", "Prepares STAR defense stories, likely questions, and mock interview scores."),
    ("outcome_analyst", "Calculates funnel conversion rates and Expected Career Value (ECV)."),
    ("career_strategist", "Optimizes long-term career trajectory, international mobility, and compounding."),
    ("data_quality_agent", "Verifies completeness, freshness, and evidence links across all JSON databases."),
    ("research_agent", "Investigates new company expansions, funding announcements, and market signals."),
    ("contradiction_agent", "Detects conflicting salary, location, or requirement data."),
    ("forecast_agent", "Estimates future hiring windows and interview probabilities."),
    ("system_improvement_agent", "Audits system performance, error logs, and subagent response quality."),
    ("executive_orchestrator", "Coordinates all 25 subagents and produces the daily executive action queue.")
]

SKILLS_LIST = [
    ("bangalore-market-scouting", "Instructions for mapping Bangalore companies, tech parks, and commercial sectors."),
    ("fresher-job-matching", "Instructions for identifying entry-level and BBA International Business opportunities."),
    ("salary-benchmarking", "Instructions for calculating evidence-backed compensation ranges in Bangalore."),
    ("interview-defense-drills", "Instructions for conducting mock interview Q&A drills using verified STAR stories."),
    ("recruiter-outreach-synthesis", "Instructions for writing 298-character LinkedIn connection notes and .eml drafts.")
]

def create_all_agents():
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    created_count = 0
    for agent_id, desc in AGENTS_LIST:
        agent_folder = AGENTS_DIR / agent_id
        agent_folder.mkdir(parents=True, exist_ok=True)
        agent_file = agent_folder / "agent.json"
        
        agent_data = {
            "name": agent_id,
            "description": desc,
            "system_prompt": f"You are the specialized {agent_id} subagent in ADI CAREER OS v9. Mission: {desc}",
            "model": "inherit",
            "status": "ACTIVE"
        }
        with open(agent_file, "w", encoding="utf-8") as f:
            json.dump(agent_data, f, indent=2)
        created_count += 1
    print(f"✅ Created {created_count} specialized subagents in {AGENTS_DIR}")

def create_all_skills():
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    created_count = 0
    for skill_id, desc in SKILLS_LIST:
        skill_folder = SKILLS_DIR / skill_id
        skill_folder.mkdir(parents=True, exist_ok=True)
        skill_file = skill_folder / "SKILL.md"
        
        content = f"""---
name: {skill_id}
description: {desc}
---

# {skill_id.replace('-', ' ').title()} Skill Instructions

## Overview
{desc}

## Execution Steps
1. Read canonical data from `career-hub/candidate/`.
2. Apply strict zero-fiction evidence rules.
3. Output structured results into `E:\\anti`.
"""
        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(content)
        created_count += 1
    print(f"✅ Created {created_count} skill modules in {SKILLS_DIR}")

def update_skills_json():
    skills_json = WORKSPACE / ".agents" / "skills.json"
    data = {
        "entries": [
            { "path": "skills/bangalore-market-scouting" },
            { "path": "skills/fresher-job-matching" },
            { "path": "skills/salary-benchmarking" },
            { "path": "skills/interview-defense-drills" },
            { "path": "skills/recruiter-outreach-synthesis" },
            { "path": "../external_skills/mattpocock-skills/skills/productivity" },
            { "path": "../external_skills/mattpocock-skills/skills/engineering" },
            { "path": "../external_skills/apache-maka/skills" },
            { "path": "../external_skills/openhuman" }
        ]
    }
    with open(skills_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Updated {skills_json}")

if __name__ == "__main__":
    create_all_agents()
    create_all_skills()
    update_skills_json()
