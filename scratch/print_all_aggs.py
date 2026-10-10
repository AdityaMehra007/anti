import json

with open("scratch/lowes_ddo_clean.json", "r", encoding="utf-8") as f:
    ddo = json.load(f)

eager = ddo.get("eagerLoadRefineSearch", {}).get("data", {})
for a in eager.get("aggregations", []):
    print(a.get('field'), ":", [v.get('value') for v in a.get('values', []) or []])
