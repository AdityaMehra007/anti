import os
import json
import re

nodes_base = r"e:\anti\n8n-core\packages\nodes-base\nodes"
nodes_list = []

for root, dirs, files in os.walk(nodes_base):
    for f in files:
        if f.endswith(".node.json") or (f.endswith(".node.ts") and not any(x in f for x in [".test.", ".spec."])):
            node_name = f.replace(".node.json", "").replace(".node.ts", "")
            fpath = os.path.join(root, f)
            rel_path = os.path.relpath(fpath, r"e:\anti\n8n-core").replace("\\", "/")
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fl:
                    content = fl.read(4096)
                    display_name_m = re.search(r"displayName:\s*['\"]([^'\"]+)['\"]", content)
                    desc_m = re.search(r"description:\s*['\"]([^'\"]+)['\"]", content)
                    group_m = re.search(r"group:\s*\[([^\]]+)\]", content)

                    display_name = display_name_m.group(1) if display_name_m else node_name
                    desc = desc_m.group(1) if desc_m else ""
                    group = group_m.group(1).replace("'", "").replace('"', "").strip() if group_m else "utility"

                    nodes_list.append({
                        "name": node_name,
                        "displayName": display_name,
                        "description": desc,
                        "group": group,
                        "file": rel_path
                    })
            except Exception:
                pass

unique_nodes = {}
for n in nodes_list:
    if n["name"] not in unique_nodes or (not unique_nodes[n["name"]]["description"] and n["description"]):
        unique_nodes[n["name"]] = n

final_nodes = list(unique_nodes.values())
print(f"Parsed {len(final_nodes)} distinct n8n nodes!")

out_path = r"e:\anti\data\n8n_node_catalog.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(final_nodes, f, indent=2)

print("Saved node catalog to data/n8n_node_catalog.json")
