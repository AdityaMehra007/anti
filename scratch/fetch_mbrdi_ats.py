import urllib.request
import re

url = 'https://jobs.mercedes-benz.com/en?en=&ParentOrganization=[140]&PositionLocation.Country=[390]'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Status: {resp.status}, length: {len(html)}")
        with open('scratch/mercedes_jobs_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Saved to scratch/mercedes_jobs_page.html")
except Exception as e:
    print(f"Error: {e}")
