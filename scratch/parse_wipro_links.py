import re
from bs4 import BeautifulSoup

with open('scratch/wipro_page.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find job links
job_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if '/job/' in href:
        job_links.append((a.get_text().strip(), href))

print('Total job links found on page:', len(job_links))
for title, link in job_links[:15]:
    print(f"- {title} -> {link}")

# Find total job count indicator
spans = soup.find_all(class_=re.compile(r'paginationLabel|resultCount|total', re.I))
for sp in spans:
    print('Pagination/Result span:', sp.get_text().strip())
