import os
import json
import sqlite3

db_path = r"e:\anti\data\omega_unified_master.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Ingest Summer 2027 Active Listings
summer_json = r"e:\anti\data\summer2027_active.json"
if os.path.exists(summer_json):
    listings = json.load(open(summer_json, encoding="utf-8"))
    print(f"Ingesting {len(listings)} Summer 2027 listings...")
    for idx, item in enumerate(listings):
        lid = f"S27-{idx:05d}"
        comp = item.get("company_name", item.get("company", ""))
        role = item.get("title", item.get("role", ""))
        locs = json.dumps(item.get("locations", [])) if isinstance(item.get("locations"), list) else str(item.get("locations", ""))
        url = item.get("url", item.get("application_url", ""))
        date_p = str(item.get("date_posted", item.get("date_updated", "")))
        cur.execute("""
            INSERT OR REPLACE INTO summer2027_listings (id, company, role, locations, application_url, date_posted, is_active, season)
            VALUES (?, ?, ?, ?, ?, ?, 1, 'Summer 2027')
        """, (lid, comp, role, locs, url, date_p))
        
        cur.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, ("Summer 2027", lid, f"{comp} - {role}", "Internship", f"{comp} {role} {locs} {url}"))

# 2. Ingest React Interview Questions
react_json = r"e:\anti\data\react_interview_questions.json"
if os.path.exists(react_json):
    questions = json.load(open(react_json, encoding="utf-8"))
    print(f"Ingesting {len(questions)} React questions...")
    for q in questions:
        qid = q.get("number", q.get("id"))
        qtitle = q.get("question", q.get("title", ""))
        cat = q.get("category", "")
        diff = q.get("difficulty", "Senior")
        ans = q.get("answer", q.get("answer_markdown", ""))
        has_code = 1 if q.get("has_code") else 0
        cur.execute("""
            INSERT OR REPLACE INTO react_questions (id, number, question, category, difficulty, answer, has_code)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (qid, qid, qtitle, cat, diff, ans, has_code))

        cur.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, ("React Interview", f"REACT-{qid}", qtitle, cat, f"{qtitle} {ans}"))

# 3. Ingest React Coding Projects
coding_json = r"e:\anti\data\react_full_coding_suite.json"
if os.path.exists(coding_json):
    csuite = json.load(open(coding_json, encoding="utf-8"))
    projs = csuite.get("projects", [])
    print(f"Ingesting {len(projs)} React machine coding projects...")
    for p in projs:
        pname = p.get("name")
        fdict = p.get("files", {})
        readme = p.get("readme", "")
        cur.execute("""
            INSERT OR REPLACE INTO react_coding_projects (name, files_count, files_json, readme)
            VALUES (?, ?, ?, ?)
        """, (pname, len(fdict), json.dumps(fdict), readme))

        cur.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, ("React Coding", f"CODE-{pname}", f"Project: {pname}", "Machine Coding", f"{pname} {readme}"))

# 4. Ingest n8n Nodes
n8n_nodes_json = r"e:\anti\data\n8n_node_catalog.json"
if os.path.exists(n8n_nodes_json):
    nodes = json.load(open(n8n_nodes_json, encoding="utf-8"))
    print(f"Ingesting {len(nodes)} n8n nodes...")
    for n in nodes:
        name = n.get("name")
        dname = n.get("displayName", name)
        desc = n.get("description", "")
        grp = n.get("group", "utility")
        fpath = n.get("file", "")
        cur.execute("""
            INSERT OR REPLACE INTO n8n_nodes (name, display_name, description, group_name, file_path)
            VALUES (?, ?, ?, ?, ?)
        """, (name, dname, desc, grp, fpath))

        cur.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, ("n8n Automation", f"N8N-{name}", dname, grp, f"{dname} {name} {desc}"))

# 5. Ingest n8n Workflows
n8n_wf_json = r"e:\anti\data\n8n_active_workflows.json"
if os.path.exists(n8n_wf_json):
    wfs = json.load(open(n8n_wf_json, encoding="utf-8"))
    print(f"Ingesting {len(wfs)} n8n workflows...")
    for w in wfs:
        fname = w.get("filename")
        wname = w.get("name")
        ncount = w.get("nodes_count", 0)
        njson = json.dumps(w.get("nodes", []))
        wjson = json.dumps(w.get("raw", {}))
        cur.execute("""
            INSERT OR REPLACE INTO n8n_workflows (filename, name, nodes_count, nodes_json, workflow_json)
            VALUES (?, ?, ?, ?, ?)
        """, (fname, wname, ncount, njson, wjson))

        cur.execute("""
            INSERT INTO unified_search_fts (domain, entity_id, title, category, content_text)
            VALUES (?, ?, ?, ?, ?)
        """, ("n8n Workflow", f"WF-{fname}", wname, "Production DAG", f"{wname} {fname} {njson}"))

conn.commit()
print("All domains indexed into unified database!")

# Verify counts
for tbl in ["summer2027_listings", "react_questions", "react_coding_projects", "n8n_nodes", "n8n_workflows", "unified_search_fts"]:
    cur.execute(f"SELECT COUNT(*) FROM {tbl}")
    print(f"  • {tbl:25s}: {cur.fetchone()[0]:,d} records")

conn.close()
