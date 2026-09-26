import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'manifest.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

tools = data['tools']
domains = {}
for t in tools:
    domains.setdefault(t['category'], []).append(t)

md = ['# 🚀 Antigravity 300 Executable Enterprise Automation Tools Catalog\n\n']
md.append('Complete master catalog of **300 standalone executable automation tools** across **10 Enterprise Domains**.\n\n')
md.append('## 📊 Master Domain Summary\n\n')
md.append('| # | Domain | Tool Count | ID Range | Directory |\n')
md.append('|---|---|---|---|---|\n')

idx = 1
for cat, tlist in domains.items():
    dom_id = tlist[0]['domain_id']
    min_id = min(t['tool_id'] for t in tlist)
    max_id = max(t['tool_id'] for t in tlist)
    md.append(f'| {idx} | **{cat}** | {len(tlist)} | `TOOL-{min_id:03d}` - `TOOL-{max_id:03d}` | [`tools/{dom_id}/`](file:///e:/anti/tools_300/tools/{dom_id}/) |\n')
    idx += 1

md.append('\n---\n\n')

for cat, tlist in domains.items():
    dom_id = tlist[0]['domain_id']
    md.append(f'## 📁 {cat} (30 Tools)\n\n')
    md.append('| ID | Slug | Tool Name | Description | Executable File |\n')
    md.append('|---|---|---|---|---|\n')
    for t in tlist:
        md.append(f'| `TOOL-{t["tool_id"]:03d}` | `{t["slug"]}` | **{t["name"]}** | {t["description"]} | [`{t["filename"]}`](file:///e:/anti/tools_300/{t["relative_path"]}) |\n')
    md.append('\n---\n\n')

with open(os.path.join(BASE_DIR, 'TOOLS_DIRECTORY.md'), 'w', encoding='utf-8') as f:
    f.write(''.join(md))

print('TOOLS_DIRECTORY.md successfully generated!')
