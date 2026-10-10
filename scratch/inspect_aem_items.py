import json

with open("scratch/walmart_script_props.json", "r", encoding="utf-8") as f:
    data = json.load(f)

pageProps = data.get("props", {}).get("pageProps", {})
model = pageProps.get("model", {})
cqItems = model.get("cqItems", {})
print("cqItems keys:", cqItems.keys())
root = cqItems.get("root", {})
print("root keys:", root.keys())
items = root.get(":items", {})
print("root :items keys:", items.keys())
for k, v in items.items():
    print(f"\nItem: {k} (type: {v.get(':type')})")
    print("  keys:", list(v.keys())[:10])
    if ":items" in v:
        subitems = v.get(":items", {})
        print("  subitems keys:", list(subitems.keys()))
        for sk, sv in subitems.items():
            print(f"    Subitem {sk} (type: {sv.get(':type')}): keys {list(sv.keys())[:10]}")
            if "search" in sk.lower() or "job" in sk.lower() or "result" in sk.lower():
                print(f"      DETAILS: {str(sv)[:300]}")
