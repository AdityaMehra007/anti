import json

with open("scratch/walmart_script_props.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Props keys:", data.keys())
pageProps = data.get("props", {}).get("pageProps", {})
model = pageProps.get("model", {})
print("Model keys:", model.keys())
for k, v in model.items():
    if isinstance(v, (str, int, float, bool)):
        print(f"  {k}: {v}")
    elif isinstance(v, dict):
        print(f"  {k} (dict): {list(v.keys())}")
    elif isinstance(v, list):
        print(f"  {k} (list): len {len(v)}")
