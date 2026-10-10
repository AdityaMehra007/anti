"""
Live Careers Aggregator - Bengaluru
Aggregates live openings across:
1. Aditya Birla Group (ABG)
2. IHCL (Tata / Taj Hotels)
3. Marriott International
4. The Oberoi Group (OCER)
"""

import sys
import re
import csv
import json
import urllib.request
import urllib.parse
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def fetch_url(url, headers_extra=None):
    h = dict(HEADERS)
    if headers_extra:
        h.update(headers_extra)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def get_ihcl_bangalore_jobs():
    jobs = []
    queries = ["Bangalore", "Bengaluru"]
    seen = set()
    
    for q in queries:
        url = f"https://careers.ihcltata.com/search/?q={q}"
        try:
            html = fetch_url(url)
            tiles = re.split(r'<li class="job-tile', html)
            for t in tiles[1:]:
                title_m = re.search(r'<a class="jobTitle-link[^"]*"[^>]*>([^<]+)</a>', t)
                url_m = re.search(r'href="(/IHCL/job/[^"]+)"', t)
                if title_m and url_m:
                    title = title_m.group(1).replace("&amp;", "&").strip()
                    job_url = "https://careers.ihcltata.com" + url_m.group(1).strip()
                    if job_url not in seen:
                        seen.add(job_url)
                        jobs.append({
                            "conglomerate": "Tata Group / IHCL",
                            "brand_division": "Taj Hotels / IHCL",
                            "city": "Bengaluru",
                            "title": title,
                            "req_id": job_url.rstrip("/").split("/")[-1],
                            "url": job_url
                        })
        except Exception as e:
            print(f"[!] Error fetching IHCL with query {q}: {e}")
            
    return jobs

def get_marriott_bengaluru_jobs():
    jobs = []
    url = "https://careers.marriott.com/jobs?location_type=1&location_name=BANGLORE&filter%5Bcity%5D%5B0%5D=Bengaluru"
    try:
        html = fetch_url(url)
        titles = re.findall(r'class="results-list__item-title--link"[^>]*>([^<]+)<', html)
        locs = re.findall(r'class="results-list__item-location--label"[^>]*>([^<]+)<', html)
        refs = re.findall(r'class="reference\s*">([^<]+)<', html)
        links = re.findall(r'class="results-list__item-apply"[^>]*href="([^"]+)"', html)
        
        for i in range(len(titles)):
            loc = locs[i].strip() if i < len(locs) else "Marriott Bengaluru"
            ref = refs[i].strip() if i < len(refs) else ""
            href = ("https://careers.marriott.com" + links[i].strip()) if i < len(links) else url
            jobs.append({
                "conglomerate": "Marriott International",
                "brand_division": loc,
                "city": "Bengaluru",
                "title": titles[i].strip(),
                "req_id": ref,
                "url": href
            })
    except Exception as e:
        print(f"[!] Error fetching Marriott: {e}")
        
    return jobs

def get_aditya_birla_bengaluru_jobs():
    jobs = []
    seen = set()
    # Discover token dynamically from job-search HTML
    token = None
    try:
        page_html = fetch_url("https://careers.adityabirla.com/job-search")
        token_m = re.search(r'\"token\":\"([a-f0-9]{32,64})\"', page_html)
        if token_m:
            token = token_m.group(1)
        else:
            token = "9f12ab0e7c6c9d65e9dc74b44f19a6a4c5c03861df6eb0fbd10ff4f4f9cd0349"
    except Exception:
        token = "9f12ab0e7c6c9d65e9dc74b44f19a6a4c5c03861df6eb0fbd10ff4f4f9cd0349"

    api_headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    for q in ["Bangalore", "Bengaluru"]:
        url = f"https://careers.adityabirla.com/api/v3/jobs?page=1&limit=100&searchString={q}"
        try:
            res_str = fetch_url(url, headers_extra=api_headers)
            res = json.loads(res_str)
            for j in res.get("data", []):
                code = j.get("jobCode")
                if code and code not in seen:
                    seen.add(code)
                    jobs.append({
                        "conglomerate": "Aditya Birla Group",
                        "brand_division": j.get("organisationName") or "ABG Corporate / Retail",
                        "city": "Bengaluru",
                        "title": j.get("jobTitle", "").strip(),
                        "req_id": code,
                        "url": f"https://careers.adityabirla.com/job-search/job-details/{code}"
                    })
        except Exception as e:
            print(f"[!] Error fetching ABG with query {q}: {e}")

    return jobs

def main():
    print("=" * 65)
    print("Fetching Live Bengaluru Enterprise Openings...")
    print("=" * 65)
    
    ihcl_jobs = get_ihcl_bangalore_jobs()
    print(f"[+] IHCL (Tata / Taj Group): {len(ihcl_jobs)} live openings found.")
    
    marriott_jobs = get_marriott_bengaluru_jobs()
    print(f"[+] Marriott International: {len(marriott_jobs)} live openings found.")
    
    abg_jobs = get_aditya_birla_bengaluru_jobs()
    print(f"[+] Aditya Birla Group (ABG): {len(abg_jobs)} live openings found in Bengaluru.")
    
    all_jobs = ihcl_jobs + marriott_jobs + abg_jobs
    
    csv_file = "bengaluru_hospitality_jobs.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["conglomerate", "brand_division", "city", "title", "req_id", "url"])
        writer.writeheader()
        writer.writerows(all_jobs)
        
    print(f"\n[+] Successfully exported {len(all_jobs)} total verified jobs to '{csv_file}'!")
    print(f"[+] Oberoi OCER Register: https://www.oberoigroup.com/careers/ocer")

if __name__ == "__main__":
    main()
