import urllib.request
import ssl

ctx = ssl.create_default_context()
url = 'https://careers.cognizant.com/global-en/jobs/?keyword=&location=Bangalore%2C+Karnataka%2C+India&radius=100&lat=12.9628957&lng=77.57754&cname=India&ccode=IN&pagesize=10'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        print('Status:', resp.status)
        content = resp.read()
        print('Bytes:', len(content))
        with open('scratch/cognizant_success.html', 'wb') as f:
            f.write(content)
except Exception as e:
    print('Error:', e)
