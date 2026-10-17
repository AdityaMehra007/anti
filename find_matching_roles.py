import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers/jobs"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def query_jobs(search_text, facets=None, limit=8):
    if facets is None:
        facets = {"locationCountry": ["c4f78be1a8f14da0ab49ce1162348a5e"]}
    payload = {
        "appliedFacets": facets,
        "limit": limit,
        "offset": 0,
        "searchText": search_text
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error querying {search_text}: {e}")
        return {}

def format_item(j):
    return {
        "title": j.get("title", ""),
        "posted": j.get("postedOn", ""),
        "location": j.get("locationsText", "Bengaluru/India"),
        "link": f"https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers{j.get('externalPath', '')}"
    }

def main():
    categories = [
        "New Associate",
        "Operations Support",
        "Service Delivery",
        "Business Operations",
        "Inside Sales",
        "Program Project Management",
        "Data"
    ]
    results = {}
    for cat in categories:
        res = query_jobs(cat, limit=6)
        results[cat] = {
            "total": res.get("total", 0),
            "jobs": [format_item(j) for j in res.get("jobPostings", [])]
        }
        print(f"{cat}: {res.get('total', 0)} openings found")

    with open("e:/anti/matching_accenture_jobs.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
