import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en',
    'Ora-Irc-Language': 'en',
    'Referer': 'https://fa-ewjt-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_2/jobs'
}

# Fetch with Fresher facet and location India
url = 'https://fa-ewjt-saasfaprod1.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList&finder=findReqs;siteNumber=CX_2,selectedFlexFieldsFacets=%22AttributeChar4%7CFresher%22,locationId=300000000467203'

print('Connecting to EXL Oracle HCM API...')
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    items = data.get('items', [])
    print(f'Items returned: {len(items)}')
    if items:
        item = items[0]
        total = item.get('TotalJobsCount')
        reqs = item.get('requisitionList', [])
        print(f'Total Fresher Jobs in India: {total}, fetched on page 1: {len(reqs)}')
        with open('scratch/exl_freshers_india.json', 'w', encoding='utf-8') as f:
            json.dump(item, f, indent=2)
        
        for r in reqs:
            req_id = r.get('Id')
            title = r.get('Title')
            loc = r.get('PrimaryLocation')
            posted = r.get('PostedDate')
            dept = r.get('Department')
            print(f"[{req_id}] {title} | {loc} | {dept} | {posted}")
