import json
import os
import re
import urllib.request
from typing import Any, Dict, List

README_URL = "https://raw.githubusercontent.com/lukasz-madon/awesome-remote-job/master/README.md"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def fetch_readme() -> str:
    req = urllib.request.Request(
        README_URL,
        headers={"User-Agent": "Awesome-Remote-Job-Extractor/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")

def parse_item(line: str) -> Dict[str, str]:
    pattern = r"^\s*(?:\d+\.|\*|\-)\s+\[([^\]]+)\]\(([^)]+)\)(?:\s*[-–—:]\s*(.*))?$"
    m = re.match(pattern, line.strip())
    if m:
        name = m.group(1).strip()
        url = m.group(2).strip()
        desc = (m.group(3) or "").strip()
        return {"name": name, "url": url, "description": desc}
    fallback = r"\[([^\]]+)\]\(([^)]+)\)\s*(?:[-–—:]\s*(.*))?"
    m2 = re.search(fallback, line)
    if m2:
        name = m2.group(1).strip()
        url = m2.group(2).strip()
        desc = (m2.group(3) or "").strip()
        return {"name": name, "url": url, "description": desc}
    return {}

def categorize_company(name: str, desc: str) -> List[str]:
    tags = []
    text = f"{name} {desc}".lower()
    mapping = {
        "ai": ["ai", "machine learning", "ml", "nlp", "llm", "data science"],
        "devtools": ["developer", "devtools", "api", "git", "ci/cd", "deployment", "ide"],
        "security": ["security", "auth", "vpn", "cyber", "privacy"],
        "design": ["design", "ui", "ux", "creative", "figma"],
        "cloud-infra": ["cloud", "hosting", "kubernetes", "database", "infrastructure", "server"],
        "fintech-web3": ["crypto", "blockchain", "finance", "payment", "bank", "token", "web3"],
        "saas": ["saas", "software", "platform", "b2b", "crm", "collaboration"],
        "media": ["content", "media", "publishing", "writing", "video", "marketing"]
    }
    for tag, keywords in mapping.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    if not tags:
        tags.append("general-tech")
    return tags

def categorize_board(name: str, desc: str) -> List[str]:
    tags = []
    text = f"{name} {desc}".lower()
    mapping = {
        "ai-ml": ["ai", "machine learning"],
        "python": ["python"],
        "ruby": ["ruby"],
        "golang": ["golang", "go "],
        "javascript": ["javascript", "js", "typescript", "vue", "react", "frontend"],
        "backend": ["backend", "clojure", "devops", "sre", "cloud", "embedded"],
        "web3-crypto": ["crypto", "web3", "blockchain"],
        "design": ["design", "ui", "ux", "art"],
        "regional-latam": ["latam", "chile", "spanish"],
        "regional-europe": ["german", "swiss", "poland", "portuguese", "spanish contracts", "europe", "canada"],
        "flexible-4day": ["4 day", "4day", "freelance"],
        "general": ["remote-first", "curated", "all roles"]
    }
    for tag, keywords in mapping.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    if not tags:
        tags.append("general")
    return tags

def extract_all(content: str) -> Dict[str, Any]:
    sections = re.split(r"\n(?=## )", content)
    data = {
        "companies": [],
        "job_boards": [],
        "job_aggregators": [],
        "housing": [],
        "relocation_incentives": [],
        "interviewing": [],
        "tools": [],
        "podcasts": [],
        "books": [],
        "communities": []
    }

    for section in sections:
        lines = section.strip().splitlines()
        if not lines:
            continue
        header = lines[0].strip().replace("#", "").strip()
        header_lower = header.lower()

        target_key = None
        if 'companies with "remote dna"' in header_lower:
            target_key = "companies"
        elif header_lower == "job boards":
            target_key = "job_boards"
        elif "aggregators" in header_lower:
            target_key = "job_aggregators"
        elif "housing" in header_lower:
            target_key = "housing"
        elif "relocation" in header_lower:
            target_key = "relocation_incentives"
        elif "interviewing" in header_lower:
            target_key = "interviewing"
        elif "tools" in header_lower:
            target_key = "tools"
        elif "podcasts" in header_lower:
            target_key = "podcasts"
        elif "books" in header_lower:
            target_key = "books"
        elif "communities" in header_lower:
            target_key = "communities"

        if not target_key:
            continue

        for line in lines[1:]:
            parsed = parse_item(line)
            if parsed and parsed.get("name") and parsed.get("url"):
                if target_key == "companies":
                    parsed["tags"] = categorize_company(parsed["name"], parsed["description"])
                elif target_key in ("job_boards", "job_aggregators"):
                    parsed["tags"] = categorize_board(parsed["name"], parsed["description"])
                data[target_key].append(parsed)

    return data

def run():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Fetching upstream awesome-remote-job repository...")
    raw = fetch_readme()
    parsed = extract_all(raw)

    total = 0
    for key, items in parsed.items():
        out_file = os.path.join(DATA_DIR, f"{key}.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"  - Saved {len(items):3d} items to data/{key}.json")
        total += len(items)

    print(f"\nSuccessfully extracted and indexed {total} total resources!")

if __name__ == "__main__":
    run()
