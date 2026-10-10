import urllib.request
import urllib.parse
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://jobspresso.co/remote-work/'
}

# Test 1: jm-ajax/get_listings/
url1 = 'https://jobspresso.co/jm-ajax/get_listings/'
data = urllib.parse.urlencode({
    'page': 1,
    'per_page': 50,
    'orderby': 'featured',
    'order': 'DESC'
}).encode('utf-8')

req = urllib.request.Request(url1, data=data, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = resp.read().decode('utf-8')
        print(f"jm-ajax success! Length: {len(res)}")
        try:
            j = json.loads(res)
            print(f"Keys: {j.keys()}, found_jobs: {j.get('found_jobs')}, max_num_pages: {j.get('max_num_pages')}")
            with open('e:/anti/scratch/jobspresso_page1.json', 'w', encoding='utf-8') as out:
                json.dump(j, out, indent=2)
        except Exception as e:
            print("Not JSON:", res[:500])
except Exception as e:
    print("jm-ajax error:", e)

# Test 2: wp-admin/admin-ajax.php?action=get_listings
url2 = 'https://jobspresso.co/wp-admin/admin-ajax.php'
data2 = urllib.parse.urlencode({
    'action': 'get_listings',
    'page': 1,
    'per_page': 50,
    'orderby': 'featured',
    'order': 'DESC'
}).encode('utf-8')

req2 = urllib.request.Request(url2, data=data2, headers=headers)
try:
    with urllib.request.urlopen(req2, timeout=15) as resp:
        res2 = resp.read().decode('utf-8')
        print(f"admin-ajax success! Length: {len(res2)}")
        try:
            j2 = json.loads(res2)
            print(f"Keys: {j2.keys()}, found_jobs: {j2.get('found_jobs')}")
        except:
            pass
except Exception as e:
    print("admin-ajax error:", e)
