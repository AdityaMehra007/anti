import json

with open('data/bangalorestartupmap_startups.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

startups = []
vcs = []

for item in items:
    # Clean up $undefined values
    cleaned = {}
    for k, v in item.items():
        if v == "$undefined":
            cleaned[k] = None
        else:
            cleaned[k] = v
            
    if cleaned.get('kind') == 'vc':
        vcs.append(cleaned)
    else:
        startups.append(cleaned)

print(f"Total: {len(items)}, Startups: {len(startups)}, VCs: {len(vcs)}")

# Inspect geocoded coverage
geocoded_startups = [s for s in startups if s.get('lat') is not None and s.get('lng') is not None]
geocoded_vcs = [v for v in vcs if v.get('lat') is not None and v.get('lng') is not None]
print(f"Geocoded startups: {len(geocoded_startups)}/{len(startups)}")
print(f"Geocoded VCs: {len(geocoded_vcs)}/{len(vcs)}")

# Check areas distribution
areas = {}
for s in startups:
    a = s.get('area') or 'Unspecified'
    areas[a] = areas.get(a, 0) + 1

sorted_areas = sorted(areas.items(), key=lambda x: x[1], reverse=True)
print("\nTop 15 Areas:")
for a, count in sorted_areas[:15]:
    print(f"  {a}: {count}")

# Check sectors distribution
sectors = {}
for s in startups:
    sec = s.get('sector') or 'Other'
    sectors[sec] = sectors.get(sec, 0) + 1

sorted_sectors = sorted(sectors.items(), key=lambda x: x[1], reverse=True)
print("\nTop Sectors:")
for sec, count in sorted_sectors:
    print(f"  {sec}: {count}")
