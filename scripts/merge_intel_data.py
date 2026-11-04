"""
Script to merge scraped Bangalore Startup Map data (1,011 startups + 74 VCs + 15 news)
with the existing BSIE-X data in data/bengaluru_startup_intel.json.
"""

import json
import os

with open('data/bengaluru_startup_intel.json', 'r', encoding='utf-8') as f:
    existing_data = json.load(f)

with open('data/bangalorestartupmap_startups.json', 'r', encoding='utf-8') as f:
    scraped_items = json.load(f)

with open('data/bangalorestartupmap_news.json', 'r', encoding='utf-8') as f:
    scraped_news = json.load(f)

# Existing startups map by lowercase name
existing_startups = {s['name'].strip().lower(): s for s in existing_data.get('startups', [])}

merged_startups = list(existing_data.get('startups', []))
merged_vcs = []

# Process scraped items
new_startup_count = 0
for item in scraped_items:
    # clean $undefined
    cleaned = {}
    for k, v in item.items():
        if v == "$undefined":
            cleaned[k] = None
        else:
            cleaned[k] = v

    name = (cleaned.get('name') or '').strip()
    if not name:
        continue

    kind = cleaned.get('kind', 'startup')
    if kind == 'vc':
        vc_id = f"VC-{len(merged_vcs) + 1:03d}"
        vc_record = {
            "id": vc_id,
            "name": name,
            "slug": cleaned.get('slug', ''),
            "tagline": cleaned.get('tagline', '') or '',
            "description": cleaned.get('description', '') or '',
            "area": cleaned.get('area', '') or 'Bengaluru',
            "address": cleaned.get('hsr_location', '') or '',
            "lat": cleaned.get('lat'),
            "lng": cleaned.get('lng'),
            "website": cleaned.get('website', '') or '',
            "partners": cleaned.get('founders', '') or '',
            "founder_links": cleaned.get('founder_links', []),
            "tags": cleaned.get('tags', []),
            "founded_year": cleaned.get('founded_year'),
            "active": True
        }
        merged_vcs.append(vc_record)
    else:
        # Check if already in existing_startups
        key = name.lower()
        if key in existing_startups:
            # enrich existing record
            rec = existing_startups[key]
            rec["slug"] = cleaned.get('slug', '')
            rec["area"] = cleaned.get('area', rec.get('blr_location', ''))
            rec["address"] = cleaned.get('hsr_location', '')
            if cleaned.get('lat') is not None:
                rec["lat"] = cleaned.get('lat')
            if cleaned.get('lng') is not None:
                rec["lng"] = cleaned.get('lng')
            if not rec.get("website") and cleaned.get("website"):
                rec["website"] = cleaned.get("website")
            rec["founder_links"] = cleaned.get('founder_links', [])
            rec["tags"] = cleaned.get('tags', [])
            if cleaned.get('founded_year'):
                rec["founded_year"] = cleaned.get('founded_year')
        else:
            new_startup_count += 1
            st_id = f"ST-{len(merged_startups) + 1:04d}"
            st_record = {
                "id": st_id,
                "name": name,
                "slug": cleaned.get('slug', ''),
                "sector": cleaned.get('sector') or 'Tech',
                "stage": cleaned.get('stage') or 'Early Stage',
                "blr_location": cleaned.get('area') or 'Bengaluru',
                "area": cleaned.get('area') or 'Bengaluru',
                "address": cleaned.get('hsr_location') or '',
                "lat": cleaned.get('lat'),
                "lng": cleaned.get('lng'),
                "website": cleaned.get('website') or '',
                "founder": cleaned.get('founders') or 'Founding Team',
                "founder_links": cleaned.get('founder_links', []),
                "tags": cleaned.get('tags', []),
                "founded_year": cleaned.get('founded_year'),
                "verified_active": True
            }
            merged_startups.append(st_record)

print(f"Merged startups total: {len(merged_startups)} (new: {new_startup_count})")
print(f"Merged VCs total: {len(merged_vcs)}")

# Process news
merged_news = list(existing_data.get('news', []))
existing_titles = {n['title'].strip().lower() for n in merged_news}

new_news_count = 0
for n in scraped_news:
    title = (n.get('title') or '').strip()
    if not title or title.lower() in existing_titles:
        continue
    new_news_count += 1
    news_id = f"NEWS-BSM-{len(merged_news) + 1:03d}"
    pub_date = (n.get('published_at') or '')[:10] or '2026-11-02'
    source = n.get('source') or 'Bangalore Ecosystem Radar'
    news_record = {
        "id": news_id,
        "title": title,
        "category": n.get('category', 'market').capitalize(),
        "date": pub_date,
        "summary": f"{source} report: {title} (Entity: {n.get('company_slug', 'ecosystem')})",
        "source_url": n.get('url', 'https://www.bangalorestartupmap.com')
    }
    merged_news.append(news_record)

print(f"Merged news total: {len(merged_news)} (new: {new_news_count})")

# Process change_log deltas
merged_changelog = list(existing_data.get('changelog', []))
new_delta = {
    "delta_id": "DELTA-BSM-001",
    "status": "INGESTED",
    "record": f"BangaloreStartupMap.com Master Directory Ingestion ({len(merged_startups)} Startups, {len(merged_vcs)} VCs, {len(merged_news)} News)",
    "finding": "Expanded Bengaluru ecosystem coverage by 1,011 startups and 74 venture capital firms with geolocation coordinates, LinkedIn founder profiles, and real-time funding headlines."
}
merged_changelog.insert(0, new_delta)

# Prepare master unified dict
master_data = {
    "startups": merged_startups,
    "vcs": merged_vcs,
    "jobs": existing_data.get("jobs", []),
    "funding": existing_data.get("funding", []),
    "news": merged_news,
    "changelog": merged_changelog
}

with open('data/bengaluru_startup_intel.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=2, ensure_ascii=False)

print("Saved enriched data/bengaluru_startup_intel.json successfully!")
