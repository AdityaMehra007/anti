"""
Live Remote Job Scraper & Multi-Feed Aggregator
Pulls active job listings in real-time from Remotive, RemoteOK, and WeWorkRemotely.
"""

import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Dict, List, Optional

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def fetch_remotive(search: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    jobs = []
    base_url = "https://remotive.com/api/remote-jobs"
    params = {}
    if search:
        params["search"] = search
    if limit:
        params["limit"] = str(limit)
    url = f"{base_url}?{urllib.parse.urlencode(params)}" if params else base_url

    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data.get("jobs", []):
                jobs.append({
                    "id": f"remotive-{item.get('id')}",
                    "title": item.get("title", "").strip(),
                    "company": item.get("company_name", "").strip(),
                    "url": item.get("url", "").strip(),
                    "location": item.get("candidate_required_location", "Anywhere").strip() or "Anywhere",
                    "salary": item.get("salary", "").strip(),
                    "tags": item.get("tags", []) or [item.get("category", "")],
                    "published": item.get("publication_date", "")[:10],
                    "source": "Remotive"
                })
    except Exception as err:
        print(f"[Warning] Remotive fetch error: {err}", file=sys.stderr)
    return jobs


def fetch_remoteok(search: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    jobs = []
    base_url = "https://remoteok.com/api"
    url = f"{base_url}?tag={urllib.parse.quote(search)}" if search else base_url

    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
            # The first item in remoteok api is often a disclaimer / metadata object
            entries = raw[1:] if len(raw) > 1 and "position" in raw[1] else raw
            count = 0
            for item in entries:
                if not isinstance(item, dict) or not item.get("position"):
                    continue
                pos = item.get("position", "").strip()
                company = item.get("company", "").strip()
                salary_min = item.get("salary_min")
                salary_max = item.get("salary_max")
                salary = ""
                if salary_min or salary_max:
                    salary = f"${salary_min or 0:,.0f} - ${salary_max or 0:,.0f}"

                jobs.append({
                    "id": f"remoteok-{item.get('id')}",
                    "title": pos,
                    "company": company,
                    "url": item.get("url", f"https://remoteok.com/remote-jobs/{item.get('id')}"),
                    "location": item.get("location", "Worldwide").strip() or "Worldwide",
                    "salary": salary,
                    "tags": item.get("tags", []) or [],
                    "published": item.get("date", "")[:10],
                    "source": "RemoteOK"
                })
                count += 1
                if count >= limit:
                    break
    except Exception as err:
        print(f"[Warning] RemoteOK fetch error: {err}", file=sys.stderr)
    return jobs


def fetch_weworkremotely(search: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    jobs = []
    feed_url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    try:
        req = urllib.request.Request(feed_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=12) as resp:
            xml_text = resp.read().decode("utf-8", errors="ignore")
            root = ET.fromstring(xml_text)
            count = 0
            for item in root.findall("./channel/item"):
                title_raw = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date = item.findtext("pubDate", "")
                # Format is typically "Company Name: Job Title"
                company = "Various"
                title = title_raw
                if ":" in title_raw:
                    parts = title_raw.split(":", 1)
                    company = parts[0].strip()
                    title = parts[1].strip()

                if search:
                    s_lower = search.lower()
                    if s_lower not in title.lower() and s_lower not in company.lower():
                        continue

                jobs.append({
                    "id": f"wwr-{hash(link)}",
                    "title": title,
                    "company": company,
                    "url": link,
                    "location": "Worldwide / Unspecified",
                    "salary": "",
                    "tags": ["programming", "dev"],
                    "published": pub_date[:16] if pub_date else "",
                    "source": "WeWorkRemotely"
                })
                count += 1
                if count >= limit:
                    break
    except Exception as err:
        print(f"[Warning] WeWorkRemotely fetch error: {err}", file=sys.stderr)
    return jobs


def search_all_jobs(keyword: Optional[str] = None, limit_per_source: int = 30) -> List[Dict[str, Any]]:
    results = []
    results.extend(fetch_remotive(keyword, limit=limit_per_source))
    results.extend(fetch_remoteok(keyword, limit=limit_per_source))
    results.extend(fetch_weworkremotely(keyword, limit=limit_per_source))

    # Deduplicate by normalized title + company
    seen = set()
    deduped = []
    for j in results:
        sig = (re.sub(r'[^a-zA-Z0-9]', '', j['title'].lower()), re.sub(r'[^a-zA-Z0-9]', '', j['company'].lower()))
        if sig not in seen:
            seen.add(sig)
            deduped.append(j)

    return deduped


def format_markdown(jobs: List[Dict[str, Any]], keyword: Optional[str]) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Live Remote Job Opportunities",
        f"*Generated: {now} | Search Query: `{keyword or 'ALL'}` | Total Listings: {len(jobs)}*",
        "",
        "| Role / Title | Company | Location | Source | Salary / Tags | Apply Link |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for j in jobs:
        tags_str = ", ".join(j["tags"][:3]) if j["tags"] else "General"
        info = j["salary"] if j["salary"] else tags_str
        lines.append(
            f"| **{j['title']}** | {j['company']} | {j['location']} | `{j['source']}` | {info} | [Apply]({j['url']}) |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Live Remote Job Scraper & Multi-Feed Aggregator")
    parser.add_argument("-k", "--keyword", help="Search keyword (e.g. python, react, ai, devops, ruby)")
    parser.add_argument("-l", "--limit", type=int, default=20, help="Max results per source (default: 20)")
    parser.add_argument("-o", "--output", help="Output file path (JSON or Markdown based on extension)")
    parser.add_argument("--markdown", action="store_true", help="Print or save as Markdown table")

    args = parser.parse_args()

    print(f"Aggregating live jobs across Remotive, RemoteOK, and WeWorkRemotely (Query: '{args.keyword or 'ALL'}')...")
    jobs = search_all_jobs(keyword=args.keyword, limit_per_source=args.limit)
    print(f"Fetched {len(jobs)} active opportunities.\n")

    if not jobs:
        print("No matching listings found. Try a broader search term.")
        return

    if args.markdown or (args.output and args.output.endswith(".md")):
        md_text = format_markdown(jobs, args.keyword)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(md_text)
            print(f"Saved Markdown report to: {args.output}")
        else:
            print(md_text)
        return

    if args.output and args.output.endswith(".json"):
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2)
        print(f"Saved JSON data to: {args.output}")
        return

    # Print clean terminal table
    print(f"{'TITLE':<42} | {'COMPANY':<20} | {'LOCATION':<18} | {'SOURCE':<10}")
    print("-" * 98)
    for j in jobs[:25]:
        title = j['title'][:40]
        company = j['company'][:18]
        loc = j['location'][:16]
        print(f"{title:<42} | {company:<20} | {loc:<18} | {j['source']:<10}")
    if len(jobs) > 25:
        print(f"\n... and {len(jobs) - 25} more listings.")


if __name__ == "__main__":
    main()
