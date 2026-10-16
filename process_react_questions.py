#!/usr/bin/env python3
"""
Master Parser & Structuring Pipeline for sudheerj/reactjs-interview-questions
Parses 444+ questions, categorizes by topic, tags difficulty, and exports JSON, CSV & SQLite.
"""

import re
import json
import csv
import sqlite3
import os
from pathlib import Path

README_PATH = Path(r"e:\anti\reactjs-interview-questions\README.md")
OUT_JSON = Path(r"e:\anti\data\react_interview_questions.json")
OUT_CSV = Path(r"e:\anti\data\react_interview_questions.csv")
OUT_TOP50 = Path(r"e:\anti\data\react_interview_top_50.json")
OUT_DB = Path(r"e:\anti\data\react_interview.db")

CATEGORIES = [
    ("React 18 / 19 & Server Components", ["concurrent", "suspense", "server component", "rsc", "starttransition", "useid", "usetransition", "usedeferredvalue", "react 18", "react 19", "hydrate"]),
    ("Virtual DOM, Fiber & Reconciliation", ["fiber", "virtual dom", "reconciliation", "diffing", "tree", "re-render", "shadow dom", "synthetic event"]),
    ("React Hooks", ["hook", "usestate", "useeffect", "usememo", "usecallback", "useref", "usecontext", "usereducer", "uselayouteffect", "custom hook"]),
    ("Performance Optimization", ["performance", "memo", "purecomponent", "profiler", "lazy", "code splitting", "optimization", "immutable", "shallow"]),
    ("Redux & State Management", ["redux", "flux", "store", "reducer", "action", "middleware", "thunk", "saga", "context api", "mobx", "zustand"]),
    ("State & Lifecycle", ["lifecycle", "componentdidmount", "componentdidupdate", "shouldcomponentupdate", "state", "setstate", "getderivedstatefromprops"]),
    ("Components & Props", ["props", "proptypes", "children", "higher order", "hoc", "render props", "controlled", "uncontrolled", "fragment", "portal", "error boundary"]),
    ("Routing & Navigation", ["router", "route", "link", "history", "navigation", "switch", "routes"]),
    ("Forms & Events", ["event", "form", "synthetic", "preventdefault", "target", "input", "change"]),
    ("Testing & Debugging", ["test", "jest", "rtl", "enzyme", "debug", "profiling", "dev tools", "mock"]),
    ("Core React & JSX", ["jsx", "babel", "element", "component", "react.createelement", "cra", "vite", "webpack", "transpile"])
]

def determine_category(title: str, body: str) -> str:
    text = (title + " " + body[:300]).lower()
    for cat, keywords in CATEGORIES:
        if any(kw in text for kw in keywords):
            return cat
    return "Core React & General"

def determine_difficulty(num: int, title: str, body: str) -> str:
    t_lower = title.lower()
    b_lower = body.lower()
    
    # Senior / Staff
    if any(k in t_lower for k in ["fiber", "reconciliation", "concurrent", "server component", "memory leak", "internals", "architecture", "under the hood", "custom hook", "middleware"]):
        return "Senior / Staff"
    if any(k in b_lower[:400] for k in ["work loop", "linked list", "reconciliation phase", "commit phase", "time slicing"]):
        return "Senior / Staff"
        
    # Mid-Level
    if any(k in t_lower for k in ["usecallback", "usememo", "useref", "usereducer", "hoc", "render prop", "context", "error boundary", "portal", "redux", "profiler", "lazy"]):
        return "Mid-Level"
    if "hook" in t_lower or "lifecycle" in t_lower or "performance" in t_lower:
        return "Mid-Level"
        
    # Foundational / Junior
    return "Foundational"

def parse_all():
    os.makedirs(r"e:\anti\data", exist_ok=True)
    print(f"[+] Reading {README_PATH}...")
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(r'(\d+)\.\s+###\s+([^\n]+)\n(.*?)(?=\n\d+\.\s+###|\Z)', re.DOTALL)
    matches = pattern.findall(content)
    print(f"[+] Found {len(matches)} raw question blocks.")

    questions = []
    for num_str, title_raw, body_raw in matches:
        q_num = int(num_str)
        title = title_raw.strip()
        
        # Clean answer body (strip Back to Top navigation links)
        clean_body = body_raw.split("**[⬆ Back to Top]")[0].strip()
        clean_body = re.sub(r'\[⬆ Back to Top\]\([^\)]+\)', '', clean_body).strip()
        
        category = determine_category(title, clean_body)
        difficulty = determine_difficulty(q_num, title, clean_body)

        # Check if code block exists
        has_code = "```" in clean_body

        q_item = {
            "id": q_num,
            "title": title,
            "category": category,
            "difficulty": difficulty,
            "has_code": has_code,
            "answer_markdown": clean_body,
            "answer_preview": clean_body[:220].replace("\n", " ").strip() + "..."
        }
        questions.append(q_item)

    # Sort by ID
    questions.sort(key=lambda x: x["id"])

    # Export JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2)
    print(f"[✓] Saved {len(questions)} questions to {OUT_JSON}")

    # Export CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "category", "difficulty", "has_code", "answer_preview"])
        writer.writeheader()
        for q in questions:
            row = {
                "id": q["id"],
                "title": q["title"],
                "category": q["category"],
                "difficulty": q["difficulty"],
                "has_code": q["has_code"],
                "answer_preview": q["answer_preview"]
            }
            writer.writerow(row)
    print(f"[✓] Saved CSV to {OUT_CSV}")

    # Curate Top 50 Senior Questions
    senior_questions = [q for q in questions if q["difficulty"] in ["Senior / Staff", "Mid-Level"]]
    # Rank by relevance and core concepts
    priority_topics = ["React Hooks", "Virtual DOM, Fiber & Reconciliation", "Performance Optimization", "React 18 / 19 & Server Components", "Redux & State Management"]
    top_50 = sorted(senior_questions, key=lambda x: (
        0 if x["category"] in priority_topics else 1,
        0 if x["difficulty"] == "Senior / Staff" else 1,
        x["id"]
    ))[:50]

    with open(OUT_TOP50, "w", encoding="utf-8") as f:
        json.dump(top_50, f, indent=2)
    print(f"[✓] Curated and saved Top 50 Senior Questions to {OUT_TOP50}")

    # Load into SQLite Database with FTS5
    if OUT_DB.exists():
        try: OUT_DB.unlink()
        except Exception: pass

    conn = sqlite3.connect(str(OUT_DB))
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS react_questions (
        id INTEGER PRIMARY KEY,
        title TEXT,
        category TEXT,
        difficulty TEXT,
        has_code INTEGER,
        answer_markdown TEXT
    )
    """)
    c.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS react_questions_fts USING fts5(
        id UNINDEXED,
        title,
        category,
        difficulty,
        answer_markdown,
        content=react_questions,
        content_rowid=rowid
    )
    """)

    rows = [(q["id"], q["title"], q["category"], q["difficulty"], 1 if q["has_code"] else 0, q["answer_markdown"]) for q in questions]
    c.executemany("INSERT OR REPLACE INTO react_questions VALUES (?,?,?,?,?,?)", rows)
    c.execute("INSERT INTO react_questions_fts(react_questions_fts) VALUES('rebuild')")
    conn.commit()
    conn.close()
    print(f"[✓] Indexed {len(questions)} questions in SQLite FTS5 database at {OUT_DB}!")

    from collections import Counter
    print("\n--- DATASET METRICS ---")
    print("Categories:", Counter(q["category"] for q in questions).most_common(12))
    print("Difficulties:", Counter(q["difficulty"] for q in questions).most_common(5))
    print(f"Questions containing Code Snippets: {sum(1 for q in questions if q['has_code'])}")

if __name__ == "__main__":
    parse_all()
