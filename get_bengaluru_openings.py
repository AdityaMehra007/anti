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

def get_bengaluru_roles():
    search_queries = [
        "Bengaluru New Associate",
        "Bengaluru Procurement New Associate",
        "Bengaluru Sales Operations",
        "Bengaluru Trust & Safety",
        "Bengaluru Customer Service",
        "Bengaluru Operations",
        "Bengaluru Program Project Management"
    ]
    seen_ids = set()
    bengaluru_jobs = []

    for sq in search_queries:
        payload = {
            "appliedFacets": {"locationCountry": ["c4f78be1a8f14da0ab49ce1162348a5e"]},
            "limit": 10,
            "offset": 0,
            "searchText": sq
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for j in data.get("jobPostings", []):
                    path = j.get("externalPath", "")
                    if "Bengaluru" in path and path not in seen_ids:
                        seen_ids.add(path)
                        bengaluru_jobs.append({
                            "title": j.get("title"),
                            "posted": j.get("postedOn"),
                            "path": path,
                            "link": f"https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers{path}"
                        })
        except Exception as e:
            print(f"Error {sq}: {e}")

    with open("e:/anti/bengaluru_fresher_openings.json", "w", encoding="utf-8") as f:
        json.dump(bengaluru_jobs, f, indent=2, ensure_ascii=False)

    print(f"Found {len(bengaluru_jobs)} distinct Bengaluru openings.")

if __name__ == "__main__":
    get_bengaluru_roles()
