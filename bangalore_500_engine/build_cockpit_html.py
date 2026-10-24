"""
Bangalore Top 500 Startups Interactive Cockpit Builder
Compiles cockpit_template.html with the embedded 500 startups database.
"""

import json
import os

TEMPLATE_PATH = "E:/anti/bangalore_500_engine/cockpit_template.html"
DATA_PATH = "E:/anti/data/BANGALORE_TOP_500_STARTUPS_PROJECTS_PROMPTS_MASTER.json"
HTML_OUTPUT_PATH = "E:/anti/bangalore_top_500_cockpit.html"

def generate_cockpit():
    print(f"Loading template from {TEMPLATE_PATH}...")
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    print(f"Loading master database from {DATA_PATH}...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    json_str = json.dumps(data, ensure_ascii=False)
    print(f"Inlining {len(data)} startup records ({len(json_str) / 1024 / 1024:.2f} MB JSON)...")

    html_content = template.replace("__DATA_PLACEHOLDER__", json_str)

    print(f"Writing compiled Cockpit to {HTML_OUTPUT_PATH}...")
    with open(HTML_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    file_size_mb = os.path.getsize(HTML_OUTPUT_PATH) / 1024 / 1024
    print(f"SUCCESS: Interactive Cockpit written ({file_size_mb:.2f} MB).")

if __name__ == "__main__":
    generate_cockpit()
