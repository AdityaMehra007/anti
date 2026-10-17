import urllib.request
import json
import sys

# Ensure utf-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers/jobs"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def search_jobs(search_text="", facets=None, limit=15):
    if facets is None:
        facets = {}
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

def format_job(j):
    path = j.get('externalPath', '')
    locations = j.get('locationsText', 'Multiple Locations')
    posted = j.get('postedOn', '')
    title = j.get('title', '')
    link = f"https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers{path}"
    return {
        "title": title,
        "location": locations,
        "posted": posted,
        "link": link
    }

def main():
    results = {}

    print("Fetching Latest Global Openings...")
    latest = search_jobs("", limit=15)
    results["latest_global"] = [format_job(j) for j in latest.get('jobPostings', [])]

    print("Fetching Latest India Openings...")
    india = search_jobs("", facets={"locationCountry": ["c4f78be1a8f14da0ab49ce1162348a5e"]}, limit=15)
    results["latest_india"] = [format_job(j) for j in india.get('jobPostings', [])]

    print("Fetching Latest AI & Data Openings...")
    ai = search_jobs("AI", limit=15)
    results["latest_ai_data"] = [format_job(j) for j in ai.get('jobPostings', [])]

    print("Fetching Latest Software & Cloud Openings...")
    tech = search_jobs("Software Engineer", limit=15)
    results["latest_software"] = [format_job(j) for j in tech.get('jobPostings', [])]

    with open("e:/anti/accenture_openings.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("Done saving to accenture_openings.json")

if __name__ == "__main__":
    main()
