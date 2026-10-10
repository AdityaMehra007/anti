import json

with open("scratch/walmart_india_jobs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for facet in data.get('facets', []):
    fid = facet.get('facetParameter')
    if "location" in fid.lower():
        print(f"\nFacet: {fid}")
        for v in facet.get('values', []):
            desc = v.get('descriptor', '')
            val_id = v.get('id', '')
            count = v.get('count', 0)
            if any(k in desc.lower() for k in ["india", "bangalore", "bengaluru", "chennai", "gurgaon", "ind"]):
                print(f"  -> {desc} (id: {val_id}) : {count}")
