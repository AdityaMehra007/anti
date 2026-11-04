import json

with open('data/bangalorestartupmap_startups.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

compact_items = []
for item in items:
    # clean $undefined
    cleaned = {}
    for k, v in item.items():
        if v != "$undefined":
            cleaned[k] = v
            
    c_item = {
        "n": cleaned.get("name", ""),
        "k": cleaned.get("kind", "startup"),
        "sec": cleaned.get("sector") or ("VC / Investor" if cleaned.get("kind") == "vc" else "Tech"),
        "stg": cleaned.get("stage") or ("Fund" if cleaned.get("kind") == "vc" else "Early Stage"),
        "area": cleaned.get("area") or "Bengaluru",
        "addr": cleaned.get("hsr_location") or "",
        "lat": cleaned.get("lat"),
        "lng": cleaned.get("lng"),
        "web": cleaned.get("website") or "",
        "tag": cleaned.get("tagline") or "",
        "desc": cleaned.get("description") or "",
        "fnd": cleaned.get("founders") or "",
        "fl": cleaned.get("founder_links") or [],
        "t": cleaned.get("tags") or [],
        "yr": cleaned.get("founded_year")
    }
    compact_items.append(c_item)

json_str = json.dumps(compact_items, ensure_ascii=False)
print("Compact items count:", len(compact_items))
print("Compact JSON length in KB:", len(json_str.encode('utf-8')) / 1024)
