import re
import json
import csv
from bs4 import BeautifulSoup
import urllib.request

def analyze_randstad():
    with open('scratch/randstad_bangalore.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check all job links matching UUID pattern
    # e.g., /jobs/l2-support-engineer-product-specialist_bangalore_d9d72450-5ff7-4134-af89-200f97d10222/
    pattern = re.compile(r'/jobs/([a-zA-Z0-9\-]+)_bangalore_([a-f0-9\-]+)/')
    
    jobs = []
    seen = set()
    
    for a in soup.find_all('a', href=True):
        m = pattern.search(a['href'])
        if m:
            slug = m.group(1)
            job_id = m.group(2)
            url = f"https://www.randstad.in{a['href']}"
            if job_id not in seen:
                seen.add(job_id)
                # Find title and text
                card = a.find_parent('li') or a.find_parent('article') or a.find_parent('div', class_=re.compile(r'card|search-result', re.I))
                title = ""
                card_type = ""
                snippet = ""
                if card:
                    h3 = card.find('h3') or card.find('h2')
                    title = h3.get_text(strip=True) if h3 else slug.replace('-', ' ').title()
                    # extract metadata tags
                    meta_spans = [span.get_text(strip=True) for span in card.find_all(['span', 'p']) if span.get_text(strip=True)]
                    snippet = " | ".join(meta_spans[:5])
                else:
                    title = slug.replace('-', ' ').title()
                
                jobs.append({
                    'title': title,
                    'job_id': job_id,
                    'slug': slug,
                    'url': url,
                    'snippet': snippet
                })
                
    print(f"Total unique job postings extracted from page 1: {len(jobs)}")
    for j in jobs[:10]:
        print(f"- {j['title']} | ID: {j['job_id']}")
        print(f"  URL: {j['url']}")
        
    # Check pagination links
    pager_links = []
    for a in soup.find_all('a', href=True):
        if 'page' in a['href'].lower() or 'p=' in a['href']:
            pager_links.append(a['href'])
    print(f"Pager links found: {set(pager_links)}")
    
    # Save page 1 jobs to CSV
    with open('randstad_bengaluru_jobs.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Job Title', 'Job ID', 'Job Function / Type', 'Location', 'Apply URL'])
        writer.writeheader()
        for j in jobs:
            # Parse contract type or details from snippet
            writer.writerow({
                'Job Title': j['title'].title(),
                'Job ID': j['job_id'],
                'Job Function / Type': j['snippet'][:150],
                'Location': 'Bengaluru, Karnataka',
                'Apply URL': j['url']
            })
    print("Exported to randstad_bengaluru_jobs.csv successfully.")

if __name__ == '__main__':
    analyze_randstad()
