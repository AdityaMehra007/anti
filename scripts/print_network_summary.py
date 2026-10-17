import json

with open('aditya_accenture_linkedin_network.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== 1. PROCUREMENT, SUPPLY CHAIN & ORDER OPS (THE EXACT TARGET ROLES) ===")
for c in data['procurement_and_supply_chain']:
    print(f"• Name: {c['name']}")
    print(f"  Title: {c['position']}")
    print(f"  Connected: {c['connected_on']}")
    print(f"  LinkedIn: {c['url']}\n")

print("\n=== 2. ACCENTURE RECRUITERS & TALENT ACQUISITION (CAN SCREEN & INTERVIEW DIRECTLY) ===")
for c in data['recruiters']:
    print(f"• Name: {c['name']}")
    print(f"  Title: {c['position']}")
    print(f"  Connected: {c['connected_on']}")
    print(f"  LinkedIn: {c['url']}\n")

print("\n=== 3. OPERATIONS MANAGERS & DECISION MAKERS ===")
for c in data['leadership_and_managers']:
    print(f"• Name: {c['name']}")
    print(f"  Title: {c['position']}")
    print(f"  Connected: {c['connected_on']}")
    print(f"  LinkedIn: {c['url']}\n")
