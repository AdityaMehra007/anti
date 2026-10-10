from bs4 import BeautifulSoup
import re

with open('scratch/az_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
print("Page Title:", soup.title.string if soup.title else '')

# Look for total jobs
headings = soup.find_all(re.compile(r'h[1-4]'))
for h in headings[:10]:
    print("Heading:", h.get_text(strip=True))

# Look for job links
job_links = soup.find_all('a', href=re.compile(r'/job/'))
print(f"Total job links on page: {len(job_links)}")
for a in job_links[:15]:
    parent = a.find_parent('li') or a.find_parent('div')
    loc = ''
    if parent:
        loc_el = parent.find(class_=re.compile(r'location', re.I))
        if loc_el:
            loc = loc_el.get_text(strip=True)
    clean_title = re.sub(r'[^\x00-\x7F]+', ' ', a.get_text(strip=True))
    print(f"  {clean_title} | {loc} -> {a.get('href')}")

# Check filters/facets
filter_section = soup.find('section', id=re.compile(r'filter|search', re.I))
if filter_section:
    for btn in filter_section.find_all(['h3', 'h4', 'button']):
        print("Filter section:", btn.get_text(strip=True))
