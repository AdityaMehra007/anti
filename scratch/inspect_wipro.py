import re
from bs4 import BeautifulSoup

with open('scratch/wipro_page.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print('Title:', soup.title.string if soup.title else 'No Title')

# Look for total jobs count
results_text = soup.find(class_=re.compile(r'pagination|result|total', re.I))
if results_text:
    print('Results text snippet:', results_text.get_text().strip()[:200])

# Look for job listings in table or list
job_rows = soup.find_all(['tr', 'li', 'div'], class_=re.compile(r'job|data-row|result', re.I))
print('Potential job rows count:', len(job_rows))

# Look for table headers and rows
table = soup.find('table')
if table:
    print('Found table!')
    rows = table.find_all('tr')
    print('Table rows count:', len(rows))
    for r in rows[:6]:
        cols = [c.get_text().strip() for c in r.find_all(['td', 'th']) if c.get_text().strip()]
        links = [a.get('href') for a in r.find_all('a') if a.get('href')]
        print('Row:', cols, '| Links:', links)
