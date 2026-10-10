import urllib.request
import json

url = "https://api.lever.co/v0/postings/meesho"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as resp:
        jobs = json.loads(resp.read().decode('utf-8'))
        print(f"Total live Meesho jobs fetched: {len(jobs)}")
        
        with open("scratch/meesho_all_jobs.json", "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2)
            
        # Analyze locations, categories, departments
        locations = {}
        departments = {}
        teams = {}
        workplace_types = {}
        
        for j in jobs:
            loc = j.get('categories', {}).get('location', 'Unknown')
            locations[loc] = locations.get(loc, 0) + 1
            
            dept = j.get('categories', {}).get('department', 'Unknown')
            departments[dept] = departments.get(dept, 0) + 1
            
            team = j.get('categories', {}).get('team', 'Unknown')
            teams[team] = teams.get(team, 0) + 1
            
            wpt = j.get('workplaceType', 'Unknown')
            workplace_types[wpt] = workplace_types.get(wpt, 0) + 1

        print("\nLocations breakdown:")
        for l, count in sorted(locations.items(), key=lambda x: -x[1])[:10]:
            print(f"  {l}: {count}")

        print("\nDepartments breakdown:")
        for d, count in sorted(departments.items(), key=lambda x: -x[1])[:15]:
            print(f"  {d}: {count}")

        print("\nTeams breakdown:")
        for t, count in sorted(teams.items(), key=lambda x: -x[1])[:15]:
            print(f"  {t}: {count}")

        print("\nWorkplace Types:")
        for w, count in workplace_types.items():
            print(f"  {w}: {count}")

except Exception as e:
    print("Error:", e)
