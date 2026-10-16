#!/usr/bin/env python3
"""
React.js Interview Autonomous CLI Engine
Search 444+ questions via SQLite FTS5, inspect 13 coding projects, drill 8 custom hooks & 4 labs, and launch the Web Command Center.
"""

import sys
import json
import sqlite3
import random
import webbrowser
from pathlib import Path

DB_PATH = Path(r"e:\anti\data\react_interview.db")
JSON_PATH = Path(r"e:\anti\data\react_interview_questions.json")
CODING_JSON_PATH = Path(r"e:\anti\data\react_full_coding_suite.json")
HTML_PATH = Path(r"e:\anti\react_interview_command_center.html")

def search_questions(query: str, limit: int = 5):
    if not DB_PATH.exists():
        print("[-] Database not found. Run process_react_questions.py first.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    try:
        results = c.execute("""
            SELECT id, title, category, difficulty, answer_markdown
            FROM react_questions_fts
            WHERE react_questions_fts MATCH ?
            LIMIT ?
        """, (query, limit)).fetchall()
    except Exception:
        results = c.execute("""
            SELECT id, title, category, difficulty, answer_markdown
            FROM react_questions
            WHERE title LIKE ? OR answer_markdown LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", limit)).fetchall()
    conn.close()

    print(f"\nFound {len(results)} matches for '{query}':")
    print("=" * 80)
    for q_id, title, cat, diff, ans in results:
        print(f"#{q_id} | {title} [{cat}] ({diff})")
        clean_ans = ans[:280].replace("\n", " ").strip()
        print(f"    Preview: {clean_ans}...")
        print("-" * 80)

def random_question():
    if not JSON_PATH.exists():
        print("[-] Questions JSON not found.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    q = random.choice(questions)
    print("\n" + "=" * 80)
    print(f"QUESTION #{q.get('number', q.get('id'))}: {q.get('question', q.get('title'))}")
    print(f"Category: {q.get('category')} | Level: {q.get('difficulty', 'Senior')}")
    print("=" * 80)
    input("\n[Press Enter to reveal answer]...")
    print("\nANSWER:")
    print(q.get('answer', q.get('answer_markdown')))
    print("=" * 80)

def list_projects():
    if not CODING_JSON_PATH.exists():
        print("[-] Coding catalog JSON not found.")
        return

    with open(CODING_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n13 MACHINE CODING PROJECTS:")
    print("=" * 70)
    for idx, p in enumerate(data.get("projects", []), 1):
        num_files = len(p.get("files", {}))
        print(f"[{idx:2d}] {p['name']:22s} ({num_files} source files)")
    print("=" * 70)

def list_hooks():
    if not CODING_JSON_PATH.exists():
        print("[-] Coding catalog JSON not found.")
        return

    with open(CODING_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n8 CUSTOM PRODUCTION HOOKS:")
    print("=" * 70)
    for idx, h in enumerate(data.get("hooks", []), 1):
        h_len = len(h.get("hook_code", ""))
        print(f"[{idx:2d}] {h['name']:25s} (Implementation: {h_len} bytes)")
    print("=" * 70)

def list_labs():
    if not CODING_JSON_PATH.exists():
        print("[-] Coding catalog JSON not found.")
        return

    with open(CODING_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n4 DIAGNOSTIC LABS (Problem vs Solution):")
    print("=" * 70)
    for idx, l in enumerate(data.get("exercises", []), 1):
        print(f"[{idx:2d}] {l['name']}")
    print("=" * 70)

def open_dashboard():
    if HTML_PATH.exists():
        print(f"[+] Opening {HTML_PATH} in browser...")
        webbrowser.open(HTML_PATH.as_uri())
    else:
        print("[-] Dashboard HTML not found.")

def show_stats():
    if not JSON_PATH.exists():
        print("[-] Questions JSON not found.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    from collections import Counter
    print("\nREACT.JS MASTERY ECOSYSTEM METRICS:")
    print("=" * 60)
    print(f"Total Interview Questions: {len(questions)}")
    print("Categories:")
    for cat, count in Counter(q["category"] for q in questions).most_common():
        print(f"  • {cat:35s}: {count:3d}")
    
    if CODING_JSON_PATH.exists():
        with open(CODING_JSON_PATH, "r", encoding="utf-8") as f:
            cdata = json.load(f)
        print("\nMachine Coding Arsenal:")
        print(f"  • Mini-App Projects: {len(cdata.get('projects', []))}")
        print(f"  • Production Custom Hooks: {len(cdata.get('hooks', []))}")
        print(f"  • Diagnostic Problem/Solution Labs: {len(cdata.get('exercises', []))}")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("""React.js Interview & Coding CLI Engine
Usage:
  python react_interview_engine.py --dashboard      # Launch Interactive Unified Web Command Center
  python react_interview_engine.py --search <query>  # Fast FTS5 search across all 444+ questions
  python react_interview_engine.py --random          # Drill a random question in terminal
  python react_interview_engine.py --projects        # List all 13 machine coding projects
  python react_interview_engine.py --hooks           # List all 8 production custom hooks
  python react_interview_engine.py --labs            # List all 4 diagnostic problem/solution labs
  python react_interview_engine.py --stats           # Show full ecosystem metrics
        """)
        return

    cmd = sys.argv[1].lower()
    if cmd in ["--dashboard", "-d", "dashboard", "--web"]:
        open_dashboard()
    elif cmd in ["--search", "-s", "search"]:
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not q:
            print("Please specify a search query.")
            return
        search_questions(q)
    elif cmd in ["--random", "-r", "random"]:
        random_question()
    elif cmd in ["--projects", "-p", "projects"]:
        list_projects()
    elif cmd in ["--hooks", "-h", "hooks"]:
        list_hooks()
    elif cmd in ["--labs", "-l", "labs"]:
        list_labs()
    elif cmd in ["--stats", "stats"]:
        show_stats()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
