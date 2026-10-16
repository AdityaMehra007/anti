import os
import json
import sqlite3

# 1. Parse workflows
wf_dir = r"e:\anti\n8n\workflows"
workflows = []
if os.path.exists(wf_dir):
    for f in sorted(os.listdir(wf_dir)):
        if f.endswith(".json"):
            fp = os.path.join(wf_dir, f)
            with open(fp, "r", encoding="utf-8") as fl:
                try:
                    data = json.load(fl)
                    workflows.append({
                        "filename": f,
                        "name": data.get("name", f.replace(".json", "").replace("_", " ").title()),
                        "nodes_count": len(data.get("nodes", [])),
                        "nodes": [n.get("name") for n in data.get("nodes", [])],
                        "active": data.get("active", False),
                        "raw": data
                    })
                except Exception:
                    pass

print(f"Parsed {len(workflows)} active OMEGA n8n workflows!")

with open(r"e:\anti\data\n8n_active_workflows.json", "w", encoding="utf-8") as out:
    json.dump(workflows, out, indent=2)

# 2. Re-create clean SQLite DB
db_path = r"e:\anti\data\n8n_arsenal_clean.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
CREATE TABLE n8n_nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    display_name TEXT,
    description TEXT,
    group_name TEXT,
    file_path TEXT
)
""")

cur.execute("""
CREATE VIRTUAL TABLE n8n_nodes_fts USING fts5(
    name,
    display_name,
    description,
    group_name
)
""")

cur.execute("""
CREATE TABLE n8n_workflows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT UNIQUE,
    name TEXT,
    nodes_count INTEGER,
    nodes_json TEXT,
    workflow_json TEXT
)
""")

# Load node catalog
with open(r"e:\anti\data\n8n_node_catalog.json", "r", encoding="utf-8") as f:
    nodes = json.load(f)

for n in nodes:
    cur.execute("""
        INSERT INTO n8n_nodes (name, display_name, description, group_name, file_path)
        VALUES (?, ?, ?, ?, ?)
    """, (n["name"], n["displayName"], n["description"], n["group"], n["file"]))
    cur.execute("""
        INSERT INTO n8n_nodes_fts (name, display_name, description, group_name)
        VALUES (?, ?, ?, ?)
    """, (n["name"], n["displayName"], n["description"], n["group"]))

for w in workflows:
    cur.execute("""
        INSERT INTO n8n_workflows (filename, name, nodes_count, nodes_json, workflow_json)
        VALUES (?, ?, ?, ?, ?)
    """, (w["filename"], w["name"], w["nodes_count"], json.dumps(w["nodes"]), json.dumps(w["raw"])))

conn.commit()

cur.execute("SELECT COUNT(*) FROM n8n_nodes")
print("Total Nodes in DB:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM n8n_workflows")
print("Total Workflows in DB:", cur.fetchone()[0])

conn.close()

# Overwrite n8n_arsenal.db
if os.path.exists(r"e:\anti\data\n8n_arsenal.db"):
    os.remove(r"e:\anti\data\n8n_arsenal.db")
os.rename(db_path, r"e:\anti\data\n8n_arsenal.db")
print("n8n_arsenal.db created and verified cleanly!")
