from bs4 import BeautifulSoup
import re
import csv
import json

def parse_dice():
    with open('scratch/dice_resp.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Try finding job cards
    # On Dice, cards are often <dhi-search-card> or <div class="card ...">
    cards = soup.find_all(['dhi-search-card', 'div', 'article'], class_=re.compile(r'card|search-card', re.I))
    print(f"Total potential card containers: {len(cards)}")
    
    # Let's inspect links with /job-detail/
    seen = set()
    jobs = []
    
    # Collect all job-detail links
    for a in soup.find_all('a', href=re.compile(r'/job-detail/([a-f0-9\-]+)')):
        m = re.search(r'/job-detail/([a-f0-9\-]+)', a['href'])
        if not m:
            continue
        job_id = m.group(1)
        if job_id in seen:
            continue
        
        # Get card context
        parent = a.find_parent(['dhi-search-card', 'div', 'li', 'article'])
        title = a.get_text(strip=True)
        if not title and parent:
            title_el = parent.find(['h5', 'h4', 'h3', 'a', 'span'], class_=re.compile(r'title', re.I))
            if title_el:
                title = title_el.get_text(strip=True)
                
        company = ""
        location = ""
        snippet = ""
        
        if parent:
            comp_el = parent.find(['a', 'span', 'div'], class_=re.compile(r'company|employer', re.I))
            if comp_el:
                company = comp_el.get_text(strip=True)
                
            loc_el = parent.find(['span', 'div'], class_=re.compile(r'location', re.I))
            if loc_el:
                location = loc_el.get_text(strip=True)
                
            desc_el = parent.find(['div', 'p', 'span'], class_=re.compile(r'desc|snippet|summary', re.I))
            if desc_el:
                snippet = desc_el.get_text(strip=True)
                
            if not snippet:
                # get all text
                snippet = parent.get_text(separator=' | ', strip=True)[:250]
                
        if title:
            seen.add(job_id)
            jobs.append({
                'Job Title': title,
                'Company': company if company else "Tech Enterprise / Staffing Partner",
                'Job ID': job_id,
                'Location': location if location else "Bengaluru, Karnataka, India",
                'Summary': snippet[:200],
                'Apply URL': f"https://www.dice.com/job-detail/{job_id}"
            })
            
    print(f"Extracted {len(jobs)} unique jobs from Dice Bengaluru page:")
    for j in jobs[:8]:
        print(f"- {j['Job Title']} | {j['Company']} | ID: {j['Job ID']}")
        print(f"  URL: {j['Apply URL']}")
        
    with open('dice_bengaluru_jobs.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Job Title', 'Company', 'Job ID', 'Location', 'Summary', 'Apply URL'])
        writer.writeheader()
        writer.writerows(jobs)
        
    print(f"Exported {len(jobs)} jobs to dice_bengaluru_jobs.csv successfully.")

if __name__ == '__main__':
    parse_dice()
