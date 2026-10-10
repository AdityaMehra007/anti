import json

with open("scratch/lowes_ddo_clean.json", "r", encoding="utf-8") as f:
    ddo = json.load(f)

eager = ddo.get("eagerLoadRefineSearch", {}).get("data", {})
print("SEARCH_CONFIG:", json.dumps(eager.get("SEARCH_CONFIG"), indent=2))
print("ui_selections:", json.dumps(eager.get("ui_selections"), indent=2))
print("ui_skills_selection:", json.dumps(eager.get("ui_skills_selection"), indent=2))
