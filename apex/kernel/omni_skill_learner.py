"""
APEX Omni-Skill Learner & Cognitive Knowledge Graph Synthesizer
Learns, parses, catalogs, and indexes all 300 Domain Skills into a unified semantic execution graph.
"""
import os
import re
import json
import time
from pathlib import Path
from typing import Dict, Any, List

WORKSPACE = Path(r"e:\anti")
SKILLS_DIR = WORKSPACE / ".agents" / "skills"
DATA_DIR = WORKSPACE / "apex" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

class OmniSkillLearner:
    def __init__(self):
        self.skills_graph: Dict[str, Any] = {}
        self.category_index: Dict[str, List[str]] = {}
        self.tools_index: Dict[str, List[str]] = {}
        self.total_learned = 0

    def learn_all_skills(self) -> Dict[str, Any]:
        start_time = time.time()
        skill_folders = [d for d in SKILLS_DIR.iterdir() if d.is_dir()]
        
        for folder in skill_folders:
            skill_md = folder / "SKILL.md"
            if not skill_md.exists():
                continue
            
            with open(skill_md, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Parse YAML frontmatter & sections
            name_match = re.search(r"name:\s*(.+)", content)
            desc_match = re.search(r"description:\s*(.+)", content)
            
            name = name_match.group(1).strip() if name_match else folder.name
            desc = desc_match.group(1).strip() if desc_match else "Autonomous Skill Capability"
            
            # Determine portfolio category
            cat = "General"
            if "analytics" in folder.name: cat = "Data Analytics & Financial Modeling"
            elif "b2b-sales" in folder.name: cat = "Business Development & B2B Sales"
            elif "devops" in folder.name: cat = "Software Engineering, Cloud & DevOps"
            elif "events" in folder.name: cat = "Event Operations & Brand Activation"
            elif "exim" in folder.name: cat = "International Trade, EXIM & Global Logistics"
            elif "finance" in folder.name: cat = "Corporate Finance, Cost Optimization & Governance"
            elif "genai" in folder.name: cat = "Generative AI, Agentic Workflows & SDK"
            elif "growth" in folder.name: cat = "Digital Marketing, SEO & Growth Marketing"
            elif "market-intel" in folder.name: cat = "Market Intelligence & Competitive Strategy"
            elif "talent" in folder.name: cat = "Talent Acquisition & People Operations"

            skill_entry = {
                "slug": folder.name,
                "name": name,
                "category": cat,
                "description": desc,
                "path": str(skill_md),
                "learned_at": time.time(),
                "status": "LEARNED_AND_INDEXED"
            }

            self.skills_graph[folder.name] = skill_entry
            
            if cat not in self.category_index:
                self.category_index[cat] = []
            self.category_index[cat].append(folder.name)
            
            self.total_learned += 1

        elapsed = round(time.time() - start_time, 3)

        output_payload = {
            "total_skills_learned": self.total_learned,
            "portfolios_covered": len(self.category_index),
            "indexing_latency_sec": elapsed,
            "category_distribution": {k: len(v) for k, v in self.category_index.items()},
            "skills": self.skills_graph
        }

        # Persist learned knowledge graph
        out_file = DATA_DIR / "apex_learned_skills_graph.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(output_payload, f, indent=2)

        return output_payload

if __name__ == "__main__":
    learner = OmniSkillLearner()
    res = learner.learn_all_skills()
    print(f"[OMNI_LEARNER] Successfully learned and indexed {res['total_skills_learned']} skills across {res['portfolios_covered']} portfolios in {res['indexing_latency_sec']}s!")
