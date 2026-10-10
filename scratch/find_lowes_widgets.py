import re

with open("scratch/lowes_page.html", "r", encoding="utf-8") as f:
    html = f.read()

pos = html.find("https://talent.lowes.com/widgets")
while pos != -1:
    print("\n--- Match for widgets ---")
    print(html[max(0, pos-200):min(len(html), pos+400)])
    pos = html.find("https://talent.lowes.com/widgets", pos+1)

# search for refNum or reqId in html to extract jobs rendered on page
req_blocks = re.findall(r'<li[^>]*class="[^"]*jobs-list-item[^"]*"[^>]*>(.*?)</li>', html, re.S)
print(f"\njobs-list-item blocks: {len(req_blocks)}")

if not req_blocks:
    # search for data-ph-at-job-title or similar
    job_titles = re.findall(r'data-ph-at-job-title-text="([^"]+)"', html)
    print("job_titles via data-ph-at-job-title-text:", len(job_titles), job_titles[:5])
    
    # search for all links to /job/
    job_links = re.findall(r'href="([^"]*/job/[^"]+)"', html)
    print("job_links:", len(job_links), job_links[:5])
