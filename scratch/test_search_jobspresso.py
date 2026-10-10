import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://jobspresso.co/remote-work/'
}

url = 'https://jobspresso.co/jm-ajax/get_listings/'

def test_query(params):
    data = urllib.parse.urlencode(params).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        j = json.loads(resp.read().decode('utf-8'))
        soup = BeautifulSoup(j.get('html', ''), 'html.parser')
        listings = soup.find_all('li', class_='job_listing')
        return len(listings), j.get('max_num_pages', 0)

# Test search_keywords="Worldwide"
c1, m1 = test_query({'search_keywords': 'Worldwide', 'page': 1, 'per_page': 50})
print(f"Keywords 'Worldwide': {c1} items, {m1} pages")

# Test search_keywords="India"
c2, m2 = test_query({'search_keywords': 'India', 'page': 1, 'per_page': 50})
print(f"Keywords 'India': {c2} items, {m2} pages")

# Test search_keywords="Support"
c3, m3 = test_query({'search_keywords': 'Support', 'page': 1, 'per_page': 50})
print(f"Keywords 'Support': {c3} items, {m3} pages")

# Test search_keywords="Operations"
c4, m4 = test_query({'search_keywords': 'Operations', 'page': 1, 'per_page': 50})
print(f"Keywords 'Operations': {c4} items, {m4} pages")

# Test search_keywords="AI"
c5, m5 = test_query({'search_keywords': 'AI', 'page': 1, 'per_page': 50})
print(f"Keywords 'AI': {c5} items, {m5} pages")
